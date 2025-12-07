import os
import json
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

from ._generated import Client
from ._generated.api.authentication import post_login
from ._generated.models.post_login_body import PostLoginBody

class ZPoolsClient:
    """
    Pure API client for zpools.io that handles authentication (PAT/JWT).
    
    Configuration (RC files, env vars) should be handled by the CLI layer.
    This class only accepts explicit values.
    """
    
    DEFAULT_API_URL = "https://api.zpools.io/v1"
    
    def __init__(
        self,
        api_url: str = DEFAULT_API_URL,
        username: Optional[str] = None,
        password: Optional[str] = None,
        pat: Optional[str] = None,
        ssh_host: Optional[str] = None,
        ssh_privkey: Optional[str] = None
    ):
        """
        Initialize the zpools.io API client.
        
        Args:
            api_url: API base URL (default: https://api.zpools.io/v1)
            username: Username for JWT authentication
            password: Password for JWT authentication
            pat: Personal Access Token (alternative to JWT)
            ssh_host: SSH hostname for ZFS operations
            ssh_privkey: Path to SSH private key file
        """
        self.api_url = api_url
        self.username = username
        self.password = password
        self.pat = pat
        self.ssh_host = ssh_host
        self.ssh_privkey = ssh_privkey
        
        self._raw_client = Client(base_url=self.api_url)
        self._token_file = self._get_token_file_path()

    def set_password(self, password: str):
        """Set the password for login if not provided during init."""
        self.password = password

    def _get_token_file_path(self) -> Path:
        """Determine path for caching JWT tokens (mimics bash script behavior)."""
        domain_clean = self.api_url.replace("https://", "").replace("http://", "").split("/")[0]
        user_safe = (self.username or "anon").replace(" ", "_")
        # Use /dev/shm if available (Linux), else temp dir
        if Path("/dev/shm").exists():
            return Path(f"/dev/shm/zpool_token_{domain_clean}_{user_safe}")
        else:
            import tempfile
            return Path(tempfile.gettempdir()) / f"zpool_token_{domain_clean}_{user_safe}"

    def _get_cached_token(self) -> Optional[str]:
        """Retrieve valid access token from cache if it exists and isn't expired."""
        if not self._token_file.exists():
            return None
            
        try:
            data = json.loads(self._token_file.read_text())
            expires_at = data.get("expires_at", 0)
            if time.time() < expires_at:
                return data.get("access_token")
        except Exception:
            return None
        return None

    def _login(self) -> str:
        """Perform login to get new JWT tokens."""
        if not self.username or not self.password:
            raise ValueError("Username and password are required for login.")

        response = post_login.sync_detailed(
            client=self._raw_client,
            body=PostLoginBody(username=self.username, password=self.password)
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Login failed: {response.status_code} - {response.content}")

        # Extract tokens
        # Note: Adjusting based on actual generated model structure
        detail = response.parsed.detail
        access_token = detail.access_token
        id_token = detail.id_token
        expires_in = detail.expires_in
        
        expires_at = int(time.time()) + expires_in
        
        # Cache tokens
        token_data = {
            "access_token": access_token,
            "id_token": id_token,
            "expires_at": expires_at
        }
        
        # Set permissions to 600 (user read/write only)
        self._token_file.touch(mode=0o600)
        self._token_file.write_text(json.dumps(token_data))
        
        return access_token

    def get_token(self) -> str:
        """
        Get a valid authentication token.
        Priority:
        1. PAT (if configured)
        2. Cached JWT (if valid)
        3. New JWT (via login)
        """
        if self.pat:
            return self.pat
            
        token = self._get_cached_token()
        if token:
            return token
            
        return self._login()

    def get_authenticated_client(self):
        """Returns the raw client with the Authorization header set."""
        from ._generated import AuthenticatedClient
        
        token = self.get_token()
        # Create an AuthenticatedClient with the token
        client = AuthenticatedClient(
            base_url=self.api_url,
            token=token
        )
        return client
    
    # PAT convenience methods
    def create_pat(self, label: str, scopes: list = None, expiry: str = None, tenant_id: str = None):
        """
        Create a Personal Access Token.
        
        Args:
            label: Human-readable label for the PAT
            scopes: Optional list of scopes (e.g., ['pat', 'sshkey', 'job', 'zpool'])
            expiry: Optional expiry date (YYYY-MM-DD)
            tenant_id: Optional tenant ID
            
        Returns:
            Response with status_code, detail.key_id, and detail.token
        """
        from ._generated.api.personal_access_tokens import post_pat
        from ._generated.models.post_pat_body import PostPatBody
        
        auth_client = self.get_authenticated_client()
        
        # Build kwargs, only including non-None values to avoid passing None to UNSET fields
        body_kwargs = {"label": label}
        if scopes is not None:
            body_kwargs["scopes"] = scopes
        if expiry is not None:
            body_kwargs["expiry"] = expiry
        if tenant_id is not None:
            body_kwargs["tenant_id"] = tenant_id
        
        return post_pat.sync_detailed(
            client=auth_client,
            body=PostPatBody(**body_kwargs)
        )
    
    def list_pats(self):
        """
        List all Personal Access Tokens.
        
        Returns:
            Response with status_code and parsed list of PATs
        """
        from ._generated.api.personal_access_tokens import get_pat
        
        auth_client = self.get_authenticated_client()
        return get_pat.sync_detailed(client=auth_client)
    
    def revoke_pat(self, key_id: str):
        """
        Revoke a Personal Access Token.
        
        Args:
            key_id: The key_id of the PAT to revoke
            
        Returns:
            Response with status_code
        """
        from ._generated.api.personal_access_tokens import delete_pat_key_id
        
        auth_client = self.get_authenticated_client()
        return delete_pat_key_id.sync_detailed(client=auth_client, key_id=key_id)
    
    # SSH Key convenience methods
    def list_sshkeys(self):
        """
        List all SSH keys.
        
        Returns:
            Response with status_code and parsed list of SSH keys
        """
        from ._generated.api.ssh_keys import get_sshkey
        
        auth_client = self.get_authenticated_client()
        return get_sshkey.sync_detailed(client=auth_client)
    
    def add_sshkey(self, public_key: str):
        """
        Add an SSH public key.
        
        Args:
            public_key: SSH public key content
            
        Returns:
            Response with status_code and pubkey_id
        """
        from ._generated.api.ssh_keys import post_sshkey
        from ._generated.models.post_sshkey_body import PostSshkeyBody
        
        auth_client = self.get_authenticated_client()
        
        return post_sshkey.sync_detailed(
            client=auth_client,
            body=PostSshkeyBody(pubkey=public_key)
        )
    
    def delete_sshkey(self, pubkey_id: str):
        """
        Delete an SSH key.
        
        Args:
            pubkey_id: The pubkey_id of the key to delete
            
        Returns:
            Response with status_code
        """
        from ._generated.api.ssh_keys import delete_sshkey_pubkey_id
        
        auth_client = self.get_authenticated_client()
        return delete_sshkey_pubkey_id.sync_detailed(client=auth_client, pubkey_id=pubkey_id)
    
    # Zpool convenience methods
    def create_zpool(self, size_gib: int = 125, volume_type: str = "gp3"):
        """
        Create a new zpool (async operation).
        
        Note: zpool_id is auto-generated by the API.
        
        Args:
            size_gib: Size in GiB (must be 125 during beta)
            volume_type: EBS volume type ('gp3' or 'sc1')
            
        Returns:
            Response with status_code 202, zpool_id, and job_id
        """
        from ._generated.api.zpools import post_zpool
        from ._generated.models.post_zpool_body import PostZpoolBody, PostZpoolBodyNewSizeInGib, PostZpoolBodyVolumeType
        
        auth_client = self.get_authenticated_client()
        
        # Convert to enum types
        size_enum = PostZpoolBodyNewSizeInGib(size_gib)
        vol_type_enum = PostZpoolBodyVolumeType(volume_type)
        
        return post_zpool.sync_detailed(
            client=auth_client,
            body=PostZpoolBody(new_size_in_gib=size_enum, volume_type=vol_type_enum)
        )
    
    def list_zpools(self):
        """
        List all zpools.
        
        Returns:
            Response with status_code and parsed list of zpools
        """
        from ._generated.api.zpools import get_zpools
        
        auth_client = self.get_authenticated_client()
        return get_zpools.sync_detailed(client=auth_client)
    
    def delete_zpool(self, zpool_id: str):
        """
        Delete a zpool (sync operation).
        
        Args:
            zpool_id: The zpool_id to delete
            
        Returns:
            Response with status_code 200
        """
        from ._generated.api.zpools import delete_zpool_zpool_id
        
        auth_client = self.get_authenticated_client()
        return delete_zpool_zpool_id.sync_detailed(client=auth_client, zpool_id=zpool_id)
    
    def scrub_zpool(self, zpool_id: str):
        """
        Start scrub on a zpool (async operation).
        
        Args:
            zpool_id: The zpool_id to scrub
            
        Returns:
            Response with status_code 202 and job_id
        """
        from ._generated.api.zpools import post_zpool_zpool_id_scrub
        
        auth_client = self.get_authenticated_client()
        return post_zpool_zpool_id_scrub.sync_detailed(client=auth_client, zpool_id=zpool_id)
    
    def modify_zpool(self, zpool_id: str, new_size_gib: int = None):
        """
        Modify a zpool (async operation).
        
        Args:
            zpool_id: The zpool_id to modify
            new_size_gib: New size in GiB
            
        Returns:
            Response with status_code 202 and job_id
        """
        from ._generated.api.zpools import post_zpool_zpool_id_modify
        from ._generated.models.post_zpool_zpool_id_modify_body import PostZpoolZpoolIdModifyBody
        
        auth_client = self.get_authenticated_client()
        
        body_kwargs = {}
        if new_size_gib is not None:
            body_kwargs["new_size_gib"] = new_size_gib
        
        return post_zpool_zpool_id_modify.sync_detailed(
            client=auth_client,
            zpool_id=zpool_id,
            body=PostZpoolZpoolIdModifyBody(**body_kwargs)
        )
    
    # Job convenience methods
    def get_job(self, job_id: str):
        """
        Get job details.
        
        Args:
            job_id: The job_id to query
            
        Returns:
            Response with status_code and job details
        """
        from ._generated.api.jobs import get_job_job_id
        
        auth_client = self.get_authenticated_client()
        return get_job_job_id.sync_detailed(client=auth_client, job_id=job_id)
    
    def list_jobs(self, limit=None, before=None, after=None, sort=None):
        """
        List all jobs with optional filtering and sorting.
        
        Args:
            limit: Maximum number of jobs to return (1-1000, default 100)
            before: Return jobs created before this datetime (ISO 8601 or datetime object)
            after: Return jobs created after this datetime (ISO 8601 or datetime object)
            sort: Sort order ("asc" or "desc", default "desc")
        
        Returns:
            Response with status_code and parsed list of jobs
        """
        from ._generated.api.jobs import get_jobs
        from ._generated.models.get_jobs_sort import GetJobsSort
        from ._generated.types import UNSET
        from datetime import datetime
        
        auth_client = self.get_authenticated_client()
        
        # Convert parameters to SDK types
        limit_param = limit if limit is not None else UNSET
        
        before_param = UNSET
        if before is not None:
            if isinstance(before, str):
                before_param = datetime.fromisoformat(before.replace('Z', '+00:00'))
            else:
                before_param = before
        
        after_param = UNSET
        if after is not None:
            if isinstance(after, str):
                after_param = datetime.fromisoformat(after.replace('Z', '+00:00'))
            else:
                after_param = after
        
        sort_param = UNSET
        if sort is not None:
            sort_param = GetJobsSort.ASC if sort.lower() == "asc" else GetJobsSort.DESC
        
        return get_jobs.sync_detailed(
            client=auth_client,
            limit=limit_param,
            before=before_param,
            after=after_param,
            sort=sort_param
        )
    
    def get_job_history(self, job_id: str):
        """
        Get job history/timeline.
        
        Args:
            job_id: The job_id to query
            
        Returns:
            Response with status_code and job history events
        """
        from ._generated.api.jobs import get_job_job_id_history
        
        auth_client = self.get_authenticated_client()
        return get_job_job_id_history.sync_detailed(client=auth_client, job_id=job_id)
    
    # Billing convenience methods
    def get_billing_balance(self):
        """
        Get account balance.
        
        Returns:
            Response with status_code and balance details
        """
        from ._generated.api.billing import get_billing_balance
        
        auth_client = self.get_authenticated_client()
        return get_billing_balance.sync_detailed(client=auth_client)
    
    def get_billing_ledger(self, since: str = None, until: str = None, limit: int = None):
        """
        Get billing ledger entries with optional date filters.
        
        Filters by usage_date (the date charges are for), not transaction timestamp.
        Results include both usage_date and ts (transaction timestamp).
        
        Args:
            since: Start usage date in YYYY-MM-DD format (or date object)
            until: End usage date in YYYY-MM-DD format (or date object)
            limit: Maximum number of entries (1-5000, default 500)
            
        Returns:
            Response with status_code and ledger items
        """
        from ._generated.api.billing import get_billing_ledger
        from ._generated.types import UNSET
        from datetime import datetime
        
        auth_client = self.get_authenticated_client()
        
        # Convert string dates to date objects
        since_param = UNSET
        if since is not None:
            if isinstance(since, str):
                since_param = datetime.strptime(since, "%Y-%m-%d").date()
            else:
                since_param = since
        
        until_param = UNSET
        if until is not None:
            if isinstance(until, str):
                until_param = datetime.strptime(until, "%Y-%m-%d").date()
            else:
                until_param = until
        
        limit_param = limit if limit is not None else UNSET
        
        return get_billing_ledger.sync_detailed(
            client=auth_client,
            since=since_param,
            until=until_param,
            limit=limit_param
        )
    
    # SSH/ZFS convenience methods
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
        if not self.username:
            raise ValueError("ZPOOL_USER is required for SSH. Set via environment or config file.")
        
        ssh_cmd = [
            "ssh",
            "-i", ssh_key,
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{self.username}@{ssh_host}",
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
        
        if not self.ssh_host or not ssh_key or not self.username:
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
            f"{self.username}@{self.ssh_host}",
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
        
        if not self.ssh_host or not ssh_key or not self.username:
            raise ValueError("SSH_HOST, SSH_PRIVKEY_FILE, and ZPOOL_USER are required")
        
        # Build SSH + zfs send command
        ssh_cmd = [
            "ssh",
            "-i", ssh_key,
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{self.username}@{self.ssh_host}",
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
