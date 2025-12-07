import typer
import json
import subprocess
import tempfile
from rich.console import Console
from rich.table import Table
from zpools_cli.utils import get_authenticated_client
from zpools._generated.types import UNSET

app = typer.Typer(help="Manage SSH keys", no_args_is_help=True)
console = Console()

def get_key_details(pubkey: str):
    """Calculate fingerprint and comment from public key using ssh-keygen."""
    try:
        with tempfile.NamedTemporaryFile(mode='w+') as f:
            f.write(pubkey)
            f.flush()
            # Output format: <bits> <fingerprint> <comment> (<type>)
            result = subprocess.check_output(['ssh-keygen', '-l', '-f', f.name], stderr=subprocess.STDOUT)
            parts = result.decode('utf-8').strip().split()
            if len(parts) >= 2:
                fingerprint = parts[1]
                comment = " ".join(parts[2:-1]) if len(parts) > 3 else (parts[2] if len(parts) > 2 else "")
                return fingerprint, comment
    except Exception:
        pass
    return "N/A", "N/A"

@app.command("list")
def list_sshkeys(
    ctx: typer.Context,
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """List all SSH keys."""
    try:
        client = get_authenticated_client(ctx.obj)
        
        response = client.list_sshkeys()
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            keys = response.parsed.detail.keys
            if not keys:
                console.print("No SSH keys found.")
                return

            table = Table(title="Your SSH Keys")
            table.add_column("ID", style="cyan")
            table.add_column("Fingerprint", style="magenta")
            table.add_column("Comment", style="green")

            for key in keys:
                fingerprint = key.additional_properties.get("fingerprint")
                comment = "N/A"
                
                # If fingerprint missing but we have pubkey, calculate it
                if not fingerprint and key.pubkey:
                    fingerprint, comment = get_key_details(key.pubkey)
                
                table.add_row(
                    key.pubkey_id,
                    fingerprint or "N/A",
                    comment
                )
            console.print(table)
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("add")
def add_sshkey(
    ctx: typer.Context,
    pubkey: str = typer.Argument(..., help="SSH public key string or path to file"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Add a new SSH key."""
    try:
        client = get_authenticated_client(ctx.obj)
        
        # Check if input is a file path
        import os
        if os.path.exists(pubkey):
            with open(pubkey, 'r') as f:
                pubkey_content = f.read().strip()
        else:
            pubkey_content = pubkey.strip()
        
        response = client.add_sshkey(public_key=pubkey_content)
        
        if response.status_code == 201:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            console.print(f"[green]SSH key added successfully![/green]")
            console.print(f"ID: {response.parsed.detail.id}")
            console.print(f"Fingerprint: {response.parsed.detail.fingerprint}")
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("delete")
def delete_sshkey(
    ctx: typer.Context,
    pubkey_id: str = typer.Argument(..., help="SSH key ID to delete"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Delete an SSH key."""
    if not json_output:
        confirm = typer.confirm(f"Are you sure you want to delete SSH key {pubkey_id}?")
        if not confirm:
            return

    try:
        client = get_authenticated_client(ctx.obj)
        
        response = client.delete_sshkey(fingerprint=pubkey_id)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            else:
                console.print(f"[green]SSH key {pubkey_id} deleted successfully.[/green]")
        elif response.status_code == 404:
            if json_output:
                print(json.dumps({"error": "Not found"}, indent=2))
            else:
                console.print(f"[red]SSH key {pubkey_id} not found.[/red]")
        else:
            if json_output:
                print(json.dumps({"error": response.content}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")
