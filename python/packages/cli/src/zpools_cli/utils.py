import sys
import json
import typer
from zpools import ZPoolsClient
from rich.console import Console

console = Console()


def format_usd(amount: float) -> str:
    """
    Format a USD amount with sufficient precision (no forced rounding).
    
    Shows only as many decimal places as needed to represent the value:
    - Formats with 6 decimal places (matches backend AMOUNT_PRECISION)
    - Strips trailing zeros
    - Returns numeric string only; callers add '$', signs, and Rich styling
    
    Examples:
        format_usd(0.01) -> "0.01"
        format_usd(0.010000) -> "0.01"
        format_usd(0.009996) -> "0.009996"
        format_usd(1.5) -> "1.5"
        format_usd(0) -> "0"
        format_usd(-0.01) -> "-0.01"
    """
    # Format with 6 decimal places (backend precision)
    formatted = f"{amount:.6f}"
    # Strip trailing zeros and unnecessary decimal point
    formatted = formatted.rstrip('0').rstrip('.')
    return formatted


def is_interactive() -> bool:
    """Check if running in an interactive terminal."""
    return sys.stdout.isatty()


def format_error_response(status_code: int, content: bytes, json_mode: bool = False) -> str:
    """
    Format an error response for display.
    
    Args:
        status_code: HTTP status code
        content: Raw response content (bytes)
        json_mode: If True (--json flag), returns raw JSON unchanged.
                   If False, extracts human-readable message for interactive terminals.
    
    Returns:
        Formatted error message string
    """
    # Decode bytes to string
    try:
        decoded = content.decode('utf-8')
    except:
        decoded = str(content)
    
    # If --json mode, return raw response as-is
    if json_mode:
        return decoded
    
    # If not interactive terminal (piped/redirected), return raw
    if not is_interactive():
        return decoded
    
    # Interactive terminal mode - try to extract human-readable message
    try:
        error_data = json.loads(decoded)
        
        # Extract message if available
        message = error_data.get('message', '')
        detail = error_data.get('detail', '')
        
        if message:
            return message
        elif detail:
            if isinstance(detail, str):
                return detail
            elif isinstance(detail, dict):
                # Try to extract a meaningful message from detail object
                detail_msg = detail.get('message', '')
                if detail_msg:
                    return detail_msg
        
        # If no clear message found, return formatted JSON
        return json.dumps(error_data, indent=2)
    except:
        # Not valid JSON, return as-is
        return decoded


def get_authenticated_client(config: dict) -> ZPoolsClient:
    """
    Get an authenticated ZPoolsClient, prompting for credentials if needed.
    
    Args:
        config: Client configuration dict from build_client_config()
    
    Returns:
        ZPoolsClient with valid authentication
    """
    # If PAT is provided, use it directly (no password needed)
    if config["pat"]:
        return ZPoolsClient(
            api_url=config["api_url"],
            pat=config["pat"],
            ssh_host=config["ssh_host"],
            ssh_privkey=config["ssh_privkey"]
        )
    
    # For JWT auth, we need username (password optional if cached token exists)
    username = config["username"]
    password = config["password"]
    api_url = config["api_url"]
    
    # Extract domain from API URL for password prompt
    # e.g., "https://api.zpools.io/v1" -> "zpools.io"
    # e.g., "https://api.dev.zpools.io/v1" -> "dev.zpools.io"
    domain = api_url.replace("https://", "").replace("http://", "").split("/")[0]
    if domain.startswith("api."):
        domain = domain[4:]  # Remove "api." prefix
    
    # Prompt for username if missing
    if not username:
        username = typer.prompt("Username")
    
    # Try to create client - it will use cached token if available
    # Only prompt for password if login fails
    client = ZPoolsClient(
        api_url=api_url,
        username=username,
        password=password,
        pat=None,
        ssh_host=config["ssh_host"],
        ssh_privkey=config["ssh_privkey"]
    )
    
    # Try to authenticate - will use cached token if valid
    try:
        client.get_authenticated_client()
        return client
    except Exception as e:
        # If authentication failed and we don't have a password, prompt for it
        if not password:
            password = typer.prompt(f"{domain} password", hide_input=True)
            # Recreate client with password
            client = ZPoolsClient(
                api_url=api_url,
                username=username,
                password=password,
                pat=None,
                ssh_host=config["ssh_host"],
                ssh_privkey=config["ssh_privkey"]
            )
            client.get_authenticated_client()
            return client
        else:
            # Had password but still failed - re-raise
            raise


def get_ssh_client(config: dict) -> ZPoolsClient:
    """
    Get a ZPoolsClient configured for SSH operations only (no HTTP auth).
    
    Used for ZFS commands that communicate via SSH, not the HTTP API.
    No authentication is performed - only SSH config is loaded.
    
    Args:
        config: Client configuration dict from build_client_config()
    
    Returns:
        ZPoolsClient with SSH configuration (no HTTP authentication)
    """
    # Create client with SSH config only - no HTTP authentication needed
    client = ZPoolsClient(
        api_url=config["api_url"],
        username=config["username"],
        ssh_host=config["ssh_host"],
        ssh_privkey=config["ssh_privkey"]
    )
    
    return client
