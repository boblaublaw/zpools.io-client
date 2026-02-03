"""
Pure API client for zpools.io that handles authentication (PAT/JWT).

This module provides the main ZPoolsClient class that coordinates all API operations
through a mixin-based architecture.
"""
from typing import Optional

from .auth import AuthManager
from .api.pats import PATMixin
from .api.sshkeys import SSHKeyMixin
from .api.zpools import ZPoolMixin
from .api.jobs import JobMixin
from .api.billing import BillingMixin
from .api.zfs_operations import ZFSOperationsMixin


class ZPoolsClient(PATMixin, SSHKeyMixin, ZPoolMixin, JobMixin, BillingMixin, ZFSOperationsMixin):
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
        ssh_privkey: Optional[str] = None,
        token_cache_dir: Optional[str] = None,
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
            token_cache_dir: Base directory for JWT token cache (unset = no cache; set explicitly to enable)
        """
        self._auth = AuthManager(
            api_url=api_url,
            username=username,
            password=password,
            pat=pat,
            token_cache_dir=token_cache_dir,
        )
        self.ssh_host = ssh_host if ssh_host is not None else "ssh.zpools.io"
        self.ssh_privkey = ssh_privkey

    def get_authenticated_client(self):
        """Returns the raw client with the Authorization header set."""
        return self._auth.get_authenticated_client()

