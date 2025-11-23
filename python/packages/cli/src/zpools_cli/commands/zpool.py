import typer
import json
from rich.console import Console
from rich.table import Table
from zpools import ZPoolsClient
from zpools._generated.api.zpools import (
    get_zpools,
    post_zpool,
    delete_zpool_zpool_id,
    post_zpool_zpool_id_modify,
    post_zpool_zpool_id_scrub
)
from zpools._generated.models.post_zpool_body import PostZpoolBody
from zpools._generated.models.post_zpool_body_new_size_in_gib import PostZpoolBodyNewSizeInGib
from zpools._generated.models.post_zpool_body_volume_type import PostZpoolBodyVolumeType
from zpools._generated.models.post_zpool_zpool_id_modify_body import PostZpoolZpoolIdModifyBody
from zpools._generated.models.post_zpool_zpool_id_modify_body_volume_type import PostZpoolZpoolIdModifyBodyVolumeType
from zpools._generated.types import UNSET

app = typer.Typer(help="Manage ZFS pools")
console = Console()

@app.command("list")
def list_zpools(
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """List all ZPools."""
    try:
        client = ZPoolsClient()
        auth_client = client.get_authenticated_client()
        
        response = get_zpools.sync_detailed(client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return

            zpools = response.parsed.detail.zpools
            if not zpools:
                console.print("No ZPools found.")
                return

            table = Table(title="Your ZPools")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Size (GiB)", style="green")
            table.add_column("Volume Type", style="yellow")
            table.add_column("Status", style="blue")

            for pool in zpools:
                table.add_row(
                    pool.zpool_id,
                    pool.name,
                    str(pool.size_gb),
                    pool.additional_properties.get("volume_type", "N/A"),
                    pool.status
                )
            console.print(table)
        else:
            if json_output:
                console.print(response.content.decode("utf-8"))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("create")
def create_zpool(
    size: int = typer.Option(125, help="Size in GiB (must be 125 during beta)"),
    volume_type: str = typer.Option("gp3", help="EBS volume type (gp3, sc1)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Create a new ZPool."""
    try:
        client = ZPoolsClient()
        auth_client = client.get_authenticated_client()
        
        # Validate and convert enums
        try:
            v_type = PostZpoolBodyVolumeType(volume_type)
        except ValueError:
            console.print(f"[red]Invalid volume type:[/red] {volume_type}. Must be one of: {[e.value for e in PostZpoolBodyVolumeType]}")
            return

        try:
            size_obj = PostZpoolBodyNewSizeInGib(size)
        except ValueError:
             console.print(f"[red]Invalid size:[/red] {size}. Must be one of: {[e.value for e in PostZpoolBodyNewSizeInGib]}")
             return

        body = PostZpoolBody(
            new_size_in_gib=size_obj,
            volume_type=v_type
        )
        
        response = post_zpool.sync_detailed(client=auth_client, body=body)
        
        if response.status_code == 202:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            console.print(f"[green]ZPool created successfully![/green]")
            console.print(f"ID: {response.parsed.detail.id}")
            console.print(f"Status: {response.parsed.detail.status}")
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("delete")
def delete_zpool(
    zpool_id: str = typer.Argument(..., help="ZPool ID to delete"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Delete a ZPool."""
    if not json_output:
        confirm = typer.confirm(f"Are you sure you want to delete ZPool {zpool_id}?")
        if not confirm:
            return

    try:
        client = ZPoolsClient()
        auth_client = client.get_authenticated_client()
        
        response = delete_zpool_zpool_id.sync_detailed(zpool_id=zpool_id, client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            else:
                console.print(f"[green]ZPool {zpool_id} deleted successfully.[/green]")
        elif response.status_code == 404:
            if json_output:
                print(json.dumps({"error": "Not found"}, indent=2))
            else:
                console.print(f"[red]ZPool {zpool_id} not found.[/red]")
        else:
            if json_output:
                print(json.dumps({"error": response.content}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("modify")
def modify_zpool(
    zpool_id: str = typer.Argument(..., help="ZPool ID to modify"),
    size: int = typer.Option(None, help="New size in GiB"),
    volume_type: str = typer.Option(None, help="New volume type"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Modify a ZPool."""
    try:
        client = ZPoolsClient()
        auth_client = client.get_authenticated_client()
        
        body_kwargs = {}
        if size is not None:
            body_kwargs["size_gb"] = size
        
        if volume_type is not None:
            try:
                body_kwargs["volume_type"] = PostZpoolZpoolIdModifyBodyVolumeType(volume_type)
            except ValueError:
                console.print(f"[red]Invalid volume type:[/red] {volume_type}")
                return

        if not body_kwargs:
            console.print("[yellow]No changes specified.[/yellow]")
            return

        body = PostZpoolZpoolIdModifyBody(**body_kwargs)
        
        response = post_zpool_zpool_id_modify.sync_detailed(zpool_id=zpool_id, client=auth_client, body=body)
        
        if response.status_code == 202:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            else:
                console.print(f"[green]ZPool {zpool_id} modified successfully.[/green]")
        else:
            if json_output:
                print(json.dumps({"error": response.content}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("scrub")
def scrub_zpool(
    zpool_id: str = typer.Argument(..., help="ZPool ID to scrub"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Start a scrub on a ZPool."""
    try:
        client = ZPoolsClient()
        auth_client = client.get_authenticated_client()
        
        response = post_zpool_zpool_id_scrub.sync_detailed(zpool_id=zpool_id, client=auth_client)
        
        if response.status_code == 202:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            else:
                console.print(f"[green]Scrub started for ZPool {zpool_id}.[/green]")
        else:
            if json_output:
                print(json.dumps({"error": response.content}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")
