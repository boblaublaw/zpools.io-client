import typer
import json
import datetime
from rich.console import Console
from rich.table import Table
from zpools_cli.utils import get_authenticated_client
from zpools._generated.api.personal_access_tokens import (
    get_pat,
    post_pat,
    delete_pat_key_id
)
from zpools._generated.models.post_pat_body import PostPatBody
from zpools._generated.types import UNSET

app = typer.Typer(help="Manage Personal Access Tokens", no_args_is_help=True)
console = Console()

@app.command("list")
def list_pats(
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """List all Personal Access Tokens."""
    try:
        client = get_authenticated_client()
        auth_client = client.get_authenticated_client()
        
        response = get_pat.sync_detailed(client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            items = response.parsed.detail.items if response.parsed.detail.items is not UNSET else []
            if not items:
                console.print("No PATs found.")
                return

            table = Table(title="Your Personal Access Tokens")
            table.add_column("ID", style="cyan")
            table.add_column("Label", style="magenta")
            table.add_column("Status", style="blue")
            table.add_column("Created At", style="green")
            table.add_column("Expiry", style="red")
            table.add_column("Last Used", style="yellow")
            table.add_column("Scopes", style="white")

            for token in items:
                last_used = str(token.last_used_at) if token.last_used_at is not UNSET else "Never"
                expiry = str(token.expiry_at) if token.expiry_at is not UNSET else "Never"
                status = token.status if token.status is not UNSET else "Unknown"
                scopes = ", ".join(token.scopes) if token.scopes is not UNSET else ""
                
                table.add_row(
                    token.key_id,
                    token.label,
                    status,
                    str(token.created_at),
                    expiry,
                    last_used,
                    scopes
                )
            console.print(table)
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("create")
def create_pat(
    label: str = typer.Argument(..., help="Label for the new token"),
    expiry: str = typer.Option(None, "--expiry", help="Optional expiry date (YYYY-MM-DD)"),
    tenant_id: str = typer.Option(None, "--tenant-id", help="Optional tenant ID"),
    scopes: list[str] = typer.Option(None, "--scope", help="Optional scopes (can be specified multiple times)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Create a new Personal Access Token."""
    try:
        client = get_authenticated_client()
        auth_client = client.get_authenticated_client()
        
        # Build the body with optional fields
        body_kwargs = {"label": label}
        
        if expiry:
            try:
                expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d").date()
                body_kwargs["expiry"] = expiry_date
            except ValueError:
                console.print("[red]Invalid expiry date format. Use YYYY-MM-DD[/red]")
                raise typer.Exit(1)
        
        if tenant_id:
            body_kwargs["tenant_id"] = tenant_id
        
        if scopes:
            body_kwargs["scopes"] = scopes
        
        body = PostPatBody(**body_kwargs)
        
        response = post_pat.sync_detailed(client=auth_client, body=body)
        
        if response.status_code == 201:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            console.print(f"[green]PAT created successfully![/green]")
            console.print(f"ID: {response.parsed.detail.key_id}")
            console.print(f"Token: [bold]{response.parsed.detail.token}[/bold]")
            console.print("[yellow]Make sure to copy your token now. You won't be able to see it again![/yellow]")
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("revoke")
def revoke_pat(
    key_id: str = typer.Argument(..., help="Key ID of the token to revoke"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Revoke a Personal Access Token."""
    if not json_output:
        confirm = typer.confirm(f"Are you sure you want to revoke PAT {key_id}?")
        if not confirm:
            return

    try:
        client = get_authenticated_client()
        auth_client = client.get_authenticated_client()
        
        response = delete_pat_key_id.sync_detailed(key_id=key_id, client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            else:
                console.print(f"[green]PAT {key_id} revoked successfully.[/green]")
        elif response.status_code == 404:
            if json_output:
                print(json.dumps({"error": "Not found"}, indent=2))
            else:
                console.print(f"[red]PAT {key_id} not found.[/red]")
        else:
            if json_output:
                print(json.dumps({"error": response.content}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")
