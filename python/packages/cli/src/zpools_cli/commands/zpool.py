import typer
import json
from rich.console import Console
from rich.table import Table
from zpools_cli.utils import get_authenticated_client
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

app = typer.Typer(help="Manage ZFS pools", no_args_is_help=True)
console = Console()

@app.command("list")
def list_zpools(
    ctx: typer.Context,
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """List all ZPools."""
    try:
        client = get_authenticated_client(ctx.obj)
        auth_client = client.get_authenticated_client()
        
        response = get_zpools.sync_detailed(client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                # Convert response to dict safely, handling nested objects
                try:
                    result = response.parsed.to_dict()
                    print(json.dumps(result, indent=2, default=str))
                except Exception as e:
                    # Fallback: manually build the dict structure
                    zpools_list = []
                    for pool in response.parsed.detail.zpools:
                        pool_dict = {
                            'zpool_id': pool.zpool_id if pool.zpool_id is not UNSET else None,
                            'name': pool.name if pool.name is not UNSET else None,
                            'size_gb': pool.size_gb if pool.size_gb is not UNSET else None,
                            'status': pool.status if pool.status is not UNSET else None,
                            'created_at': str(pool.created_at) if pool.created_at is not UNSET else None,
                        }
                        pool_dict.update(pool.additional_properties)
                        zpools_list.append(pool_dict)
                    print(json.dumps({'detail': {'zpools': zpools_list}, 'message': response.parsed.message}, indent=2, default=str))
                return

            zpools = response.parsed.detail.zpools
            if not zpools or not zpools.additional_properties:
                console.print("No ZPools found.")
                return

            # Display zpools - iterate and show each with its volumes
            for zpool_id, pool in zpools.additional_properties.items():
                # Get zpool-level info from SDK attributes
                username = pool.username if pool.username is not UNSET else 'N/A'
                volume_count = pool.volume_count if pool.volume_count is not UNSET else 0
                create_time = pool.create_time if pool.create_time is not UNSET else None
                last_scrub = pool.last_scrub_time if pool.last_scrub_time is not UNSET else None
                
                # Format dates
                create_time_str = create_time.strftime('%Y-%m-%d') if create_time else 'N/A'
                last_scrub_str = last_scrub.strftime('%Y-%m-%d') if last_scrub else 'Never'
                
                console.print(f"\n[bold cyan]ZPool:[/bold cyan] {zpool_id}")
                console.print(f"  User: {username}  |  Volumes: {volume_count}  |  Created: {create_time_str}  |  Last Scrub: {last_scrub_str}")
                
                # Get volumes from SDK attribute
                volumes = pool.volumes if pool.volumes is not UNSET else []
                
                if not volumes:
                    console.print("  [yellow]No volumes found[/yellow]")
                    continue
                
                # Create table for this zpool's volumes
                vol_table = Table(show_header=True, box=None, padding=(0, 2))
                vol_table.add_column("Volume ID", style="dim")
                vol_table.add_column("Size (GiB)", style="green")
                vol_table.add_column("Type", style="magenta")
                vol_table.add_column("State", style="yellow")
                vol_table.add_column("Mod State", style="blue")
                vol_table.add_column("Mod %", style="bright_blue")
                vol_table.add_column("Can Modify", style="white")
                
                for vol in volumes:
                    # Access SDK model attributes or additional_properties
                    vol_id = vol.volume_id if vol.volume_id is not UNSET else vol.additional_properties.get('VolumeId', 'N/A')
                    size = vol.size if vol.size is not UNSET else vol.additional_properties.get('Size', 'N/A')
                    vol_type = vol.volume_type if vol.volume_type is not UNSET else vol.additional_properties.get('VolumeType', 'N/A')
                    state = vol.state if vol.state is not UNSET else vol.additional_properties.get('State', 'N/A')
                    mod_state = vol.mod_state if vol.mod_state is not UNSET else vol.additional_properties.get('ModState', 'N/A')
                    mod_progress = vol.mod_progress if vol.mod_progress is not UNSET else vol.additional_properties.get('ModProgress', 'N/A')
                    can_modify = vol.can_modify_now if vol.can_modify_now is not UNSET else vol.additional_properties.get('CanModifyNow', False)
                    
                    vol_table.add_row(
                        vol_id,
                        str(size),
                        str(vol_type),
                        state,
                        mod_state,
                        f"{mod_progress}%" if mod_progress != 'N/A' else 'N/A',
                        "Yes" if can_modify else "No"
                    )
                
                console.print(vol_table)
        else:
            if json_output:
                console.print(response.content.decode("utf-8"))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("create")
def create_zpool(
    ctx: typer.Context,
    size: int = typer.Option(125, help="Size in GiB (must be 125 during beta)"),
    volume_type: str = typer.Option("gp3", help="EBS volume type (gp3, sc1)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Create a new ZPool."""
    try:
        client = get_authenticated_client(ctx.obj)
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
    ctx: typer.Context,
    zpool_id: str = typer.Argument(..., help="ZPool ID to delete"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Delete a ZPool."""
    if not json_output:
        confirm = typer.confirm(f"Are you sure you want to delete ZPool {zpool_id}?")
        if not confirm:
            return

    try:
        client = get_authenticated_client(ctx.obj)
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
    ctx: typer.Context,
    zpool_id: str = typer.Argument(..., help="ZPool ID to modify"),
    size: int = typer.Option(None, help="New size in GiB"),
    volume_type: str = typer.Option(None, help="New volume type"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Modify a ZPool."""
    try:
        client = get_authenticated_client(ctx.obj)
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
    ctx: typer.Context,
    zpool_id: str = typer.Argument(..., help="ZPool ID to scrub"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Start a scrub on a ZPool."""
    try:
        client = get_authenticated_client(ctx.obj)
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
