import typer
from zpools import ZPoolsClient


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
