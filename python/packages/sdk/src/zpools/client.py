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
        self.api_url = api_url or os.getenv("API_DOMAIN") or self.config.get("API_DOMAIN") or self.DEFAULT_API_URL
        self.username = username or os.getenv("ZPOOLUSER") or self.config.get("ZPOOLUSER")
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

    def get_authenticated_client(self) -> Client:
        """Returns the raw client with the Authorization header set."""
        token = self.get_token()
        # Create a new client instance with the auth header
        # We can't just update headers on the existing one easily with this generator
        return Client(
            base_url=self.api_url, 
            headers={"Authorization": f"Bearer {token}"}
        )
