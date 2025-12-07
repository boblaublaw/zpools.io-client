"""Configuration loading for zpools CLI."""
import os
from pathlib import Path
from typing import Dict, Optional


def load_rc_file(rc_path: Optional[Path] = None) -> Dict[str, str]:
    """
    Load configuration from zpoolrc file.
    
    Args:
        rc_path: Path to RC file. If None, uses ~/.config/zpools.io/zpoolrc
        
    Returns:
        Dictionary of configuration values
    """
    config = {}
    
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
                    config[key.strip()] = val
    
    return config


def get_config_value(
    key: str,
    explicit: Optional[str] = None,
    rc_config: Optional[Dict[str, str]] = None,
    default: Optional[str] = None
) -> Optional[str]:
    """
    Get configuration value with priority: explicit > env var > RC file > default.
    
    Args:
        key: Configuration key (also used as env var name)
        explicit: Explicitly provided value (highest priority)
        rc_config: RC file config dictionary
        default: Default value if not found elsewhere
        
    Returns:
        Configuration value or None
    """
    if explicit is not None:
        return explicit
    
    env_value = os.getenv(key)
    if env_value is not None:
        return env_value
    
    if rc_config and key in rc_config:
        return rc_config[key]
    
    return default


def build_client_config(
    api_url: Optional[str] = None,
    username: Optional[str] = None,
    pat: Optional[str] = None,
    ssh_host: Optional[str] = None,
    ssh_privkey: Optional[str] = None,
    rc_file: Optional[Path] = None
) -> Dict[str, str]:
    """
    Build configuration for ZPoolsClient by merging explicit values, env vars, and RC file.
    
    Priority for most values: explicit args > environment variables > RC file > defaults
    Password priority: ONLY from ZPOOL_PASSWORD environment variable (never CLI arg or RC file)
    
    Args:
        api_url: Explicit API URL
        username: Explicit username
        pat: Explicit PAT token
        ssh_host: Explicit SSH host
        ssh_privkey: Explicit SSH private key path
        rc_file: Path to RC file (default: ~/.config/zpools.io/zpoolrc)
        
    Returns:
        Dictionary with resolved configuration values
    """
    # Load RC file if needed
    rc_config = load_rc_file(rc_file)
    
    # Build config with priority chain (explicit > env > RC > default)
    config = {
        "api_url": get_config_value("ZPOOL_API_URL", api_url, rc_config, "https://api.zpools.io/v1"),
        "username": get_config_value("ZPOOL_USER", username, rc_config),
        "pat": get_config_value("ZPOOLPAT", pat, rc_config),
        "ssh_host": get_config_value("SSH_HOST", ssh_host, rc_config),
        "ssh_privkey": get_config_value("SSH_PRIVKEY_FILE", ssh_privkey, rc_config),
    }
    
    # Password: ONLY from environment variable (never CLI arg or RC file)
    config["password"] = os.getenv("ZPOOL_PASSWORD")
    
    return config
