import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any

from ._generated import Client
from ._generated.api.authentication import post_login
from ._generated.models.post_login_body import PostLoginBody

class ZPoolsClient:
    """
    High-level client for zpools.io that handles authentication (PAT/JWT)
    and configuration loading automatically.
    """
    
    DEFAULT_API_URL = "https://api.zpools.io/v1"
    
    def __init__(
        self, 
        api_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        pat: Optional[str] = None,
        rc_file: Optional[Path] = None
    ):
        self._load_config(rc_file)
        
        # Priority: Explicit Arg > Env Var > RC File
        self.api_url = api_url or os.getenv("ZPOOL_API_URL") or self.config.get("ZPOOL_API_URL") or self.DEFAULT_API_URL
        self.username = username or os.getenv("ZPOOL_USER") or self.config.get("ZPOOL_USER")
        self.pat = pat or os.getenv("ZPOOLPAT") or self.config.get("ZPOOLPAT")
        
        # Password is never in RC file for security
        self.password = password or os.getenv("ZPOOL_PASSWORD")
        
        self._raw_client = Client(base_url=self.api_url)
        self._token_file = self._get_token_file_path()

    def set_password(self, password: str):
        """Set the password for login if not provided during init."""
        self.password = password

    def _load_config(self, rc_path: Optional[Path]):
        """Load configuration from ~/.config/zpools.io/zpoolrc or specified path."""
        self.config: Dict[str, str] = {}
        
        if rc_path:
            target = rc_path
        else:
            target = Path.home() / ".config" / "zpools.io" / "zpoolrc"
            
        if target.exists():
            # Simple shell-like parsing: KEY="VALUE" or KEY=VALUE
            with open(target, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, val = line.split("=", 1)
                        # Strip quotes if present
                        val = val.strip('"').strip("'")
                        self.config[key.strip()] = val

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
        print(f"DEBUG SDK: Creating AuthenticatedClient with token={token[:50]}...")
        # Create an AuthenticatedClient with the token
        client = AuthenticatedClient(
            base_url=self.api_url,
            token=token
        )
        print(f"DEBUG SDK: Created {type(client)}")
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
    
    def list_jobs(self):
        """
        List all jobs.
        
        Returns:
            Response with status_code and parsed list of jobs
        """
        from ._generated.api.jobs import get_jobs
        
        auth_client = self.get_authenticated_client()
        return get_jobs.sync_detailed(client=auth_client)
