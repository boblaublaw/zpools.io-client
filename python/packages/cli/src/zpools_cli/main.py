import typer
from rich.console import Console
from zpools import ZPoolsClient
from zpools._generated.api.authentication import get_hello

app = typer.Typer()
console = Console()

@app.command()
def hello():
    """
    Test connectivity to the API.
    """
    try:
        client = ZPoolsClient()
        
        # Check if we need to login (if no PAT and no valid cached token)
        # Note: hello endpoint is public, but let's simulate the auth flow check
        if not client.pat and not client._get_cached_token():
            if not client.password:
                # Prompt for password if missing
                if not client.username:
                    client.username = typer.prompt("Username")
                client.set_password(typer.prompt("Password", hide_input=True))
        
        # hello endpoint might not require auth, but let's use the raw client from the wrapper
        # The wrapper initializes _raw_client with the base URL
        # Use authenticated client to ensure we have a valid token (triggers login if needed)
        auth_client = client.get_authenticated_client()
        response = get_hello.sync_detailed(client=auth_client)
        
        if response.status_code == 200:
            console.print(f"[green]Success:[/green] {response.parsed.message}")
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command()
def version():
    """
    Show the CLI version.
    """
    console.print("zpools-cli v0.1.0")

if __name__ == "__main__":
    app()
