"""ZFS operations over SSH."""
import subprocess


class ZFSOperationsMixin:
    """Mixin providing ZFS operations over SSH."""
    
    def ssh_exec(self, command: str, stdin_data: bytes = None, ssh_key_file: str = None) -> tuple[int, bytes, bytes]:
        """
        Execute command via SSH to remote zpool host.
        
        Args:
            command: Shell command to execute on remote host
            stdin_data: Optional data to pipe to stdin
            ssh_key_file: SSH private key file (defaults to self.ssh_privkey)
            
        Returns:
            tuple of (return_code, stdout, stderr)
            
        Raises:
            ValueError: If SSH configuration is missing
            subprocess.CalledProcessError: If SSH command fails
        """
        ssh_host = self.ssh_host
        ssh_key = ssh_key_file or self.ssh_privkey
        
        if not ssh_host:
            raise ValueError("SSH_HOST is required. Set via environment or config file.")
        if not ssh_key:
            raise ValueError("SSH_PRIVKEY_FILE is required. Set via environment or config file.")
        if not self._auth.username:
            raise ValueError("ZPOOL_USER is required for SSH. Set via environment or config file.")
        
        ssh_cmd = [
            "ssh",
            "-i", ssh_key,
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{self._auth.username}@{ssh_host}",
            command
        ]
        
        result = subprocess.run(
            ssh_cmd,
            input=stdin_data,
            capture_output=True
        )
        
        return result.returncode, result.stdout, result.stderr
    
    def zfs_send_to_remote(self, local_snapshot: str, remote_dataset: str, 
                           incremental_base: str = None, ssh_key_file: str = None) -> None:
        """
        Send local ZFS snapshot to remote zpool via SSH.
        
        Executes: sudo zfs send local_snapshot | ssh user@host zfs recv remote_dataset
        
        Args:
            local_snapshot: Local snapshot (e.g., "rpool/test@snap1")
            remote_dataset: Remote dataset path (e.g., "zpool_abc123/test")
            incremental_base: Optional base snapshot for incremental send (e.g., "@snap1")
            ssh_key_file: SSH private key file (defaults to self.ssh_privkey)
            
        Raises:
            ValueError: If SSH configuration is missing
            RuntimeError: If send/recv operation fails (includes stderr output)
        """
        ssh_key = ssh_key_file or self.ssh_privkey
        
        if not self.ssh_host or not ssh_key or not self._auth.username:
            raise ValueError("SSH_HOST, SSH_PRIVKEY_FILE, and ZPOOL_USER are required")
        
        # Build zfs send command
        if incremental_base:
            send_cmd = ["sudo", "zfs", "send", "-i", incremental_base, local_snapshot]
        else:
            send_cmd = ["sudo", "zfs", "send", local_snapshot]
        
        # Build SSH + zfs recv command
        ssh_cmd = [
            "ssh",
            "-i", ssh_key,
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{self._auth.username}@{self.ssh_host}",
            f"zfs recv {remote_dataset}"
        ]
        
        # Execute: zfs send | ssh zfs recv
        send_proc = subprocess.Popen(send_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        recv_proc = subprocess.Popen(ssh_cmd, stdin=send_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Close send_proc stdout to allow recv_proc to receive EOF
        send_proc.stdout.close()
        
        # Wait for both to complete
        recv_stdout, recv_stderr = recv_proc.communicate()
        send_proc.wait()
        
        # Check for errors
        if send_proc.returncode != 0:
            _, send_stderr = send_proc.communicate()
            raise RuntimeError(f"zfs send failed: {send_stderr.decode('utf-8', errors='replace')}")
        
        if recv_proc.returncode != 0:
            raise RuntimeError(f"zfs recv failed: {recv_stderr.decode('utf-8', errors='replace')}")
    
    def zfs_recv_from_remote(self, remote_snapshot: str, local_dataset: str, 
                             force: bool = False, ssh_key_file: str = None) -> None:
        """
        Receive ZFS snapshot from remote zpool via SSH.
        
        Executes: ssh user@host zfs send remote_snapshot | sudo zfs recv local_dataset
        
        Args:
            remote_snapshot: Remote snapshot (e.g., "zpool_abc123/test@snap1")
            local_dataset: Local dataset to receive into (e.g., "rpool/test-restore")
            force: Use -F flag to force rollback if dataset exists
            ssh_key_file: SSH private key file (defaults to self.ssh_privkey)
            
        Raises:
            ValueError: If SSH configuration is missing
            RuntimeError: If send/recv operation fails (includes stderr output)
        """
        ssh_key = ssh_key_file or self.ssh_privkey
        
        if not self.ssh_host or not ssh_key or not self._auth.username:
            raise ValueError("SSH_HOST, SSH_PRIVKEY_FILE, and ZPOOL_USER are required")
        
        # Build SSH + zfs send command
        ssh_cmd = [
            "ssh",
            "-i", ssh_key,
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{self._auth.username}@{self.ssh_host}",
            f"zfs send {remote_snapshot}"
        ]
        
        # Build zfs recv command
        recv_cmd = ["sudo", "zfs", "recv"]
        if force:
            recv_cmd.append("-F")
        recv_cmd.append(local_dataset)
        
        # Execute: ssh zfs send | zfs recv
        send_proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        recv_proc = subprocess.Popen(recv_cmd, stdin=send_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Close send_proc stdout to allow recv_proc to receive EOF
        send_proc.stdout.close()
        
        # Wait for both to complete
        recv_stdout, recv_stderr = recv_proc.communicate()
        send_proc.wait()
        
        # Check for errors
        if send_proc.returncode != 0:
            _, send_stderr = send_proc.communicate()
            raise RuntimeError(f"remote zfs send failed: {send_stderr.decode('utf-8', errors='replace')}")
        
        if recv_proc.returncode != 0:
            raise RuntimeError(f"zfs recv failed: {recv_stderr.decode('utf-8', errors='replace')}")
