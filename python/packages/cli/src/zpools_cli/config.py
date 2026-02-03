"""Configuration loading for zpools CLI."""
import os
from pathlib import Path
from typing import Dict, Optional

DEFAULT_SSH_KEY_PATH = "~/.ssh/id_zpool_ed25519"
DEFAULT_SSH_KEYGEN_CMD = f"ssh-keygen -t ed25519 -f {DEFAULT_SSH_KEY_PATH}"

# Commands that require a config file (and will trigger the wizard if none exists)
COMMANDS_NEEDING_CONFIG = ("hello", "zpool", "sshkey", "pat", "job", "billing", "zfs")


def run_config_wizard(rc_file_path: Path, console) -> bool:
    """
    Interactively create a new rc file. Returns True if the file was written, False if the user declined.
    """
    console.print("[yellow]It doesn't look like you've got a config file.[/yellow]")
    create = input("Would you like to make one now? [y/N]: ").strip().lower()
    if create not in ("y", "yes"):
        console.print("Run zpcli again when you have a config file at the default path or use --rcfile.")
        return False

    # ZPOOL_USER: required, no default
    while True:
        username = input("zpools.io username (required): ").strip()
        if username:
            break
        console.print("[red]Username is required.[/red]")

    # Token cache: 1=no cache, 2=/dev/shm/zpools.io, or custom path
    console.print(
        "\nToken cache directory: JWT tokens can be cached so you don't re-enter your password."
    )
    console.print(
        "  [dim]1 = No cache (most secure; you will be prompted for password when needed)[/dim]"
    )
    console.print(
        "  [dim]2 = /dev/shm/zpools.io (ephemeral RAM-backed cache; faster, still not on disk)[/dim]"
    )
    console.print("  [dim]Or type another path to use as the cache directory.[/dim]")
    choice = input("Choice [1]: ").strip() or "1"

    token_cache_dir: Optional[str] = None
    if choice == "1":
        token_cache_dir = None
    elif choice == "2":
        token_cache_dir = "/dev/shm/zpools.io"
    else:
        token_cache_dir = choice.strip()

    if token_cache_dir:
        cache_path = Path(token_cache_dir).expanduser()
        if not cache_path.exists():
            create_dir = input(f"Directory {cache_path} does not exist. Create it? [y/N]: ").strip().lower()
            if create_dir in ("y", "yes"):
                cache_path.mkdir(parents=True, mode=0o700)
                console.print(f"[green]Created[/green] {cache_path} with permissions 0700.")
            else:
                console.print("[yellow]Skipping cache directory creation; token cache will not be used until the path exists.[/yellow]")
                token_cache_dir = None
        elif not cache_path.is_dir():
            console.print(f"[red]{cache_path} is not a directory; skipping token cache.[/red]")
            token_cache_dir = None

    # SSH private key: create new (default) or use existing; we require a valid key pair before writing rc file
    ssh_privkey_file: Optional[str] = None
    console.print("\nSSH key for ZFS over SSH (required):")
    console.print("  [dim]1 = Create a new key (default)[/dim]")
    console.print("  [dim]2 = Use an existing key[/dim]")
    key_choice = input("Choice [1]: ").strip().lower() or "1"

    if key_choice == "1":
        # Create new: show command, user runs it; Enter = default path, re-ask until valid key pair exists
        console.print(f"\nRun this command in another terminal (tune to your preferences), then return here:")
        console.print(f"  [bold]{DEFAULT_SSH_KEYGEN_CMD}[/bold]")
        default_resolved = str(Path(DEFAULT_SSH_KEY_PATH).expanduser())
        while True:
            raw_path = input(f"Path to the key you created [{default_resolved}]: ").strip()
            key_path = Path(raw_path).expanduser() if raw_path else Path(default_resolved)
            pub_path = Path(str(key_path) + ".pub")
            if key_path.exists() and key_path.is_file() and pub_path.exists() and pub_path.is_file():
                ssh_privkey_file = str(key_path)
                console.print(f"[green]Found key pair[/green] {key_path} / {pub_path}")
                break
            console.print(f"[red]No key pair at {key_path} (expected {pub_path}). Enter the path again.[/red]")
    else:
        # Use existing: list ~/.ssh keys or accept path; require valid key pair
        ssh_dir = Path.home() / ".ssh"
        skip_names = {"config", "known_hosts", "authorized_keys", "known_hosts.old"}
        private_keys: list[Path] = []
        if ssh_dir.exists() and ssh_dir.is_dir():
            try:
                for p in sorted(ssh_dir.iterdir()):
                    if p.is_file() and not p.name.endswith(".pub") and p.name not in skip_names:
                        private_keys.append(p)
            except OSError:
                pass
        if private_keys:
            for i, p in enumerate(private_keys, 1):
                console.print(f"  [dim]{i}. {p}[/dim]")
            console.print("  [dim]Or type a path to a different key.[/dim]")
        while True:
            if private_keys:
                raw = input("Choice or path: ").strip()
            else:
                raw = input("Path to SSH private key: ").strip()
            if not raw:
                console.print("[red]A valid SSH key pair is required. Enter a choice or path.[/red]")
                continue
            if raw.isdigit() and private_keys:
                idx = int(raw)
                if 1 <= idx <= len(private_keys):
                    key_path = private_keys[idx - 1]
                else:
                    console.print(f"[red]Invalid choice. Enter 1–{len(private_keys)} or a path.[/red]")
                    continue
            else:
                key_path = Path(raw).expanduser()
            pub_path = Path(str(key_path) + ".pub")
            if key_path.exists() and key_path.is_file() and pub_path.exists() and pub_path.is_file():
                ssh_privkey_file = str(key_path)
                console.print(f"[green]Found key pair[/green] {key_path} / {pub_path}")
                break
            console.print(f"[red]No key pair at {key_path} (expected {pub_path}). Try again.[/red]")

    if not ssh_privkey_file:
        console.print("[red]A valid SSH key pair is required to create the config file. Run the wizard again when you have one.[/red]")
        return False

    # Write rc file
    rc_file_path = Path(rc_file_path)
    rc_file_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"ZPOOL_USER={username}"]
    if token_cache_dir:
        lines.append(f"ZPOOL_TOKEN_CACHE_DIR={token_cache_dir}")
    if ssh_privkey_file:
        lines.append(f"SSH_PRIVKEY_FILE={ssh_privkey_file}")
    optional_overrides = [
        "",
        "# Full reference: https://github.com/boblaublaw/zpools.io-client/blob/main/docs/configuration.md",
        "# Optional overrides (uncomment and set as needed):",
        "# 1. ZPOOL_API_URL=https://api.zpools.io/v1",
        "# 2. SSH_HOST=ssh.zpools.io",
    ]
    if not ssh_privkey_file:
        optional_overrides.append("# 3. SSH_PRIVKEY_FILE=path/to/private/key")
    optional_overrides.append("# 4. ZPOOLPAT=personal_access_token")
    if not token_cache_dir:
        optional_overrides.append(
            "# 5. ZPOOL_TOKEN_CACHE_DIR=path/to/cache/dir  (set to enable JWT caching; unset = no cache)"
        )
    optional_overrides.extend([
        "# 6. BZFS_BIN=path/to/bzfs",
        "# 7. LOCAL_POOL=your/local/zpool/dataset",
        "# 8. REMOTE_POOL=user@ssh.zpools.io:remote-zpool-id/remote-dataset",
        "",
        "",
    ])
    lines.extend(optional_overrides)

    rc_file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    console.print(f"[green]Wrote config to[/green] {rc_file_path}")
    return True


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
    token_cache_dir: Optional[str] = None,
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
        token_cache_dir: Explicit token cache base directory
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
        "ssh_host": get_config_value("SSH_HOST", ssh_host, rc_config, "ssh.zpools.io"),
        "ssh_privkey": get_config_value("SSH_PRIVKEY_FILE", ssh_privkey, rc_config),
        "token_cache_dir": get_config_value("ZPOOL_TOKEN_CACHE_DIR", token_cache_dir, rc_config),
    }
    
    # Password: ONLY from environment variable (never CLI arg or RC file)
    config["password"] = os.getenv("ZPOOL_PASSWORD")
    
    return config
