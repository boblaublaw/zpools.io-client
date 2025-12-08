import sys
import json
import typer
from zpools import ZPoolsClient
from rich.console import Console

console = Console()


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
    # Create client with resolved config
    client = ZPoolsClient(
        api_url=config["api_url"],
        username=config["username"],
        password=config["password"],
        pat=config["pat"],
        ssh_host=config["ssh_host"],
        ssh_privkey=config["ssh_privkey"]
    )
    
    # Check if we need to login (if no PAT and no valid cached token)
    if not client.pat and not client._get_cached_token():
        if not client.password:
            # Prompt for credentials if missing
            if not client.username:
                client.username = typer.prompt("Username")
            client.set_password(typer.prompt("Password", hide_input=True))
    
    # This will trigger login if needed
    client.get_authenticated_client()
    
    return client
