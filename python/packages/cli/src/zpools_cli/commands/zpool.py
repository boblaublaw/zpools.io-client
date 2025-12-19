import typer
import json
import time
from datetime import datetime, timezone as tz
from rich.console import Console, Group
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from zpools_cli.utils import get_authenticated_client, format_error_response
from zpools_cli.progress import ProgressMonitor
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


def wait_for_job_with_progress(client, job_id: str, operation_name: str, timeout: int = 1800, poll_interval: int = 5) -> dict:
    """
    Wait for a job to complete with live progress animation and history display.
    
    Args:
        client: ZPoolsClient instance
        job_id: Job ID to monitor
        operation_name: Human-readable operation name (e.g., "ZPool creation")
        timeout: Maximum time to wait in seconds
        poll_interval: Time between polls in seconds
        
    Returns:
        Final job data dict
        
    Raises:
        TimeoutError: If job doesn't complete within timeout
        RuntimeError: If job fails
    """
    monitor = ProgressMonitor(console, poll_interval=poll_interval, timeout=timeout)
    
    def poll_api():
        """Poll job status and history."""
        response = client.get_job(job_id)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to get job status: {response.status_code}")
        
        job_data = response.parsed.detail.additional_properties.get('job')
        if not job_data:
            raise RuntimeError(f"Job {job_id} response missing 'job' field")
        
        # Get job history
        history_response = client.get_job_history(job_id)
        history = []
        if history_response.status_code == 200:
            history = history_response.parsed.detail.additional_properties.get('history', [])
        
        return {'job': job_data, 'history': history}
    
    def render_display(state, spinner):
        """Render the job status display."""
        job_data = state['job']
        history = state['history']
        
        current_status = job_data.get('current_status', {})
        job_state = current_status.get('state')
        
        # Status line
        status_text = Text()
        status_text.append(f"{spinner} ", style="cyan bold")
        status_text.append(f"{operation_name} ", style="white")
        status_text.append(f"[{job_state}]", style="yellow")
        status_text.append(f" ({monitor.elapsed_str()})", style="dim")
        
        # Build history table (show last 10 events)
        history_table = Table(show_header=True, box=None, padding=(0, 1))
        history_table.add_column("Time", style="dim", width=8)
        history_table.add_column("Event", style="cyan")
        history_table.add_column("Message", style="white")
        
        recent_history = history[-10:] if len(history) > 10 else history
        for event in recent_history:
            timestamp = event.get('timestamp', '')
            event_type = event.get('event_type', '')
            event_msg = event.get('message', '')
            
            # Calculate relative time
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                now = datetime.now(tz.utc)
                delta_sec = int((now - dt).total_seconds())
                if delta_sec < 60:
                    time_str = f"{delta_sec}s ago"
                elif delta_sec < 3600:
                    time_str = f"{delta_sec//60}m ago"
                else:
                    time_str = f"{delta_sec//3600}h ago"
            except:
                time_str = ""
            
            history_table.add_row(time_str, event_type, event_msg)
        
        # Combine into panel
        content = Group(
            status_text,
            Text(""),  # blank line
            history_table if history else Text("No events yet", style="dim")
        )
        return Panel(
            content,
            title=f"[bold]Job {job_id}[/bold]",
            border_style="blue"
        )
    
    def check_complete(state):
        """Check if job is complete and handle terminal states."""
        job_data = state['job']
        current_status = job_data.get('current_status', {})
        job_state = current_status.get('state')
        message = current_status.get('message', '')
        
        if job_state == "succeeded":
            console.print(f"\n[green]✓ {operation_name} completed successfully![/green]")
            return True
        elif job_state == "failed":
            error_msg = message or 'Unknown error'
            console.print(f"\n[red]✗ {operation_name} failed: {error_msg}[/red]")
            raise RuntimeError(f"Job {job_id} failed: {error_msg}")
        elif job_state not in ("pending", "running", "queued", "in progress"):
            raise RuntimeError(f"Unknown job state: {job_state}")
        
        return False
    
    result = monitor.monitor(poll_api, render_display, check_complete, operation_name)
    return result['job']


def wait_for_modify_with_progress(client, zpool_id: str, timeout: int = 1800, poll_interval: int = 10) -> dict:
    """
    Wait for zpool volume modifications to complete with live progress display.
    
    Polls the zpool list endpoint to check volume modification states.
    
    Args:
        client: ZPoolsClient instance
        zpool_id: ZPool ID to monitor
        timeout: Maximum time to wait in seconds
        poll_interval: Time between polls in seconds
        
    Returns:
        Final zpool data dict
        
    Raises:
        TimeoutError: If modifications don't complete within timeout
        RuntimeError: If zpool disappears or API errors
    """
    monitor = ProgressMonitor(console, poll_interval=poll_interval, timeout=timeout)
    
    def poll_api():
        """Poll zpool status."""
        response = client.list_zpools()
        if response.status_code != 200:
            raise RuntimeError(f"Failed to list zpools: {response.status_code}")
        
        zpools = response.parsed.detail.zpools.to_dict() if response.parsed.detail.zpools else {}
        zpool = zpools.get(zpool_id)
        
        if not zpool:
            raise RuntimeError(f"Zpool {zpool_id} not found in list")
        
        volumes = zpool.get('Volumes', zpool.get('volumes', []))
        return {'zpool': zpool, 'volumes': volumes}
    
    def render_display(state, spinner):
        """Render the modification progress display."""
        volumes = state['volumes']
        
        # Status line
        status_text = Text()
        status_text.append(f"{spinner} ", style="cyan bold")
        status_text.append(f"Modifying volumes for ZPool {zpool_id}", style="white")
        status_text.append(f" ({monitor.elapsed_str()})", style="dim")
        
        # Build volume status table
        vol_table = Table(show_header=True, box=None, padding=(0, 1))
        vol_table.add_column("Volume", style="dim", width=22)
        vol_table.add_column("State", style="cyan", width=12)
        vol_table.add_column("Mod State", style="yellow", width=12)
        vol_table.add_column("Progress", style="green", width=10)
        vol_table.add_column("Type", style="magenta", width=8)
        
        for vol in volumes:
            vol_id = vol.get('VolumeId', vol.get('volume_id', 'N/A'))
            vol_state = vol.get('State', vol.get('state', 'N/A'))
            mod_state = vol.get('ModState', vol.get('mod_state', 'none'))
            mod_progress = vol.get('ModProgress', vol.get('mod_progress', 0))
            vol_type = vol.get('VolumeType', vol.get('volume_type', 'N/A'))
            
            # Format progress
            if mod_state in ('modifying', 'optimizing'):
                progress_str = f"{mod_progress}%"
            elif mod_state == 'completed':
                progress_str = "✓ Done"
            else:
                progress_str = "-"
            
            vol_table.add_row(vol_id[-12:], vol_state, mod_state, progress_str, vol_type)
        
        # Combine into panel
        content = Group(
            status_text,
            vol_table if volumes else Text("No volume info available", style="dim")
        )
        return Panel(
            content,
            title=f"[bold]ZPool {zpool_id} - Volume Modifications[/bold]",
            border_style="blue"
        )
    
    def check_complete(state):
        """Check if all modifications are complete."""
        volumes = state['volumes']
        
        # Check if any volumes are actively modifying
        any_modifying = False
        all_complete = True
        
        for vol in volumes:
            mod_state = vol.get('ModState', vol.get('mod_state', 'none'))
            if mod_state in ('modifying', 'optimizing'):
                any_modifying = True
                all_complete = False
                break
            elif mod_state == 'completed':
                # At least one was modified
                pass
        
        if not any_modifying:
            # Check if there were any recent modifications (completed state)
            has_completed = any(
                vol.get('ModState', vol.get('mod_state', 'none')) == 'completed'
                for vol in volumes
            )
            
            if has_completed or all_complete:
                console.print(f"\n[green]✓ Volume modifications completed successfully![/green]")
            else:
                console.print(f"\n[yellow]No active modifications found for ZPool {zpool_id}[/yellow]")
            return True
        
        return False
    
    result = monitor.monitor(poll_api, render_display, check_complete, "Modify operation")
    return result['zpool']


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
            error_msg = format_error_response(response.status_code, response.content, json_output)
            if json_output:
                console.print(error_msg)
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {error_msg}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("create")
def create_zpool(
    ctx: typer.Context,
    size: int = typer.Option(125, help="Size in GiB (must be 125 during beta)"),
    volume_type: str = typer.Option("gp3", help="EBS volume type (gp3, sc1)"),
    wait: bool = typer.Option(False, "--wait", help="Wait for creation to complete"),
    timeout: int = typer.Option(1800, "--timeout", help="Timeout in seconds when using --wait (default: 1800)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Create a new ZPool."""
    try:
        client = get_authenticated_client(ctx.obj)
        
        response = client.create_zpool(size_gib=size, volume_type=volume_type)
        
        if response.status_code == 202:
            job_id = response.parsed.detail.job_id
            
            if json_output and not wait:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            elif not wait:
                console.print(f"[green]ZPool creation started![/green]")
                console.print(f"Job ID: {job_id}")
            
            # Wait for completion if requested
            if wait:
                if json_output:
                    from zpools.helpers import JobPoller
                    poller = JobPoller(client, job_id, timeout=timeout, poll_interval=10)
                    final_job = poller.wait_for_completion()
                    print(json.dumps(final_job, indent=2, default=str))
                else:
                    try:
                        final_job = wait_for_job_with_progress(
                            client, job_id, "ZPool creation", timeout=timeout, poll_interval=5
                        )
                        # Extract zpool_id from message if available
                        msg = final_job.get('current_status', {}).get('message', '')
                        if 'zpool_id:' in msg:
                            zpool_id = msg.split('zpool_id:')[1].strip()
                            console.print(f"ZPool ID: [cyan]{zpool_id}[/cyan]")
                    except TimeoutError:
                        console.print(f"[red]Timeout waiting for job to complete[/red]")
                        console.print(f"Job ID: {job_id}")
                    except RuntimeError:
                        console.print(f"Job ID: {job_id}")
        else:
            error_msg = format_error_response(response.status_code, response.content, json_output)
            console.print(f"[red]Error {response.status_code}:[/red] {error_msg}")

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
            error_msg = format_error_response(response.status_code, response.content, json_output)
            if json_output:
                print(json.dumps({"error": error_msg}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {error_msg}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("modify")
def modify_zpool(
    ctx: typer.Context,
    zpool_id: str = typer.Argument(..., help="ZPool ID to modify"),
    volume_type: str = typer.Option(None, "--type", help="Target volume type (gp3, sc1)"),
    wait: bool = typer.Option(False, "--wait", help="Wait for modification to complete"),
    resume: bool = typer.Option(False, "--resume", help="Resume monitoring an existing modification"),
    timeout: int = typer.Option(1800, "--timeout", help="Timeout in seconds when using --wait or --resume (default: 1800)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Change a ZPool's EBS volume type (gp3 <-> sc1)."""
    try:
        client = get_authenticated_client(ctx.obj)
        
        # If --resume, skip the API call and just monitor
        if resume:
            if json_output:
                from zpools.helpers import ModifyPoller
                poller = ModifyPoller(client, zpool_id, timeout=timeout, poll_interval=10)
                final_zpool = poller.wait_for_completion()
                print(json.dumps(final_zpool, indent=2, default=str))
            else:
                console.print(f"[cyan]Resuming monitoring of ZPool {zpool_id} modification...[/cyan]")
                try:
                    final_zpool = wait_for_modify_with_progress(
                        client, zpool_id, timeout=timeout, poll_interval=10
                    )
                except TimeoutError:
                    console.print(f"[red]Timeout waiting for modification to complete[/red]")
                except Exception as e:
                    console.print(f"[red]Error waiting for completion: {e}[/red]")
            return
        
        # Normal flow: submit modification
        if not volume_type:
            console.print("[red]Error:[/red] --type is required when not using --resume")
            raise typer.Exit(1)
        
        response = client.modify_zpool(zpool_id, target_volume_type=volume_type)
        
        if response.status_code == 202:
            if json_output and not wait:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            elif not wait:
                console.print(f"[green]ZPool {zpool_id} volume type modification submitted.[/green]")
                if response.parsed and response.parsed.detail:
                    summary = response.parsed.detail.summary
                    console.print(f"Submitted: {summary.submitted}/{summary.discovered} volumes")
            
            # Wait for completion if requested
            if wait:
                if json_output:
                    from zpools.helpers import ModifyPoller
                    poller = ModifyPoller(client, zpool_id, timeout=timeout, poll_interval=10)
                    final_zpool = poller.wait_for_completion()
                    print(json.dumps(final_zpool, indent=2, default=str))
                else:
                    try:
                        final_zpool = wait_for_modify_with_progress(
                            client, zpool_id, timeout=timeout, poll_interval=10
                        )
                    except TimeoutError:
                        console.print(f"[red]Timeout waiting for modification to complete[/red]")
                    except Exception as e:
                        console.print(f"[red]Error waiting for completion: {e}[/red]")
        elif response.status_code == 409:
            if response.parsed and response.parsed.message:
                console.print(f"[yellow]Conflict:[/yellow] {response.parsed.message}")
            else:
                error_msg = format_error_response(response.status_code, response.content, json_output)
                console.print(f"[yellow]Conflict:[/yellow] {error_msg}")
        else:
            error_msg = format_error_response(response.status_code, response.content, json_output)
            if json_output:
                print(json.dumps({"error": error_msg}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {error_msg}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("expand")
def expand_zpool(
    ctx: typer.Context,
    zpool_id: str = typer.Argument(..., help="ZPool ID to expand"),
    size: int = typer.Option(..., "--size", help="New size in GiB"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Expand a ZPool's size (Not Yet Implemented)."""
    console.print("[yellow]ZPool expansion is not yet implemented.[/yellow]")
    console.print("This feature is planned for a future release.")
    console.print("\nExpansion will:")
    console.print("  • Resize EBS volumes")
    console.print("  • Expand ZFS pool to use new space")
    console.print("  • Track progress via async job")
    raise typer.Exit(1)

@app.command("scrub")
def scrub_zpool(
    ctx: typer.Context,
    zpool_id: str = typer.Argument(..., help="ZPool ID to scrub"),
    wait: bool = typer.Option(False, "--wait", help="Wait for scrub to complete"),
    timeout: int = typer.Option(1800, "--timeout", help="Timeout in seconds when using --wait (default: 1800)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Start a scrub on a ZPool."""
    try:
        client = get_authenticated_client(ctx.obj)
        
        response = client.scrub_zpool(zpool_id)
        
        if response.status_code == 202:
            job_id = response.parsed.detail.job_id
            
            if json_output and not wait:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
            elif not wait:
                console.print(f"[green]Scrub started for ZPool {zpool_id}.[/green]")
                console.print(f"Job ID: {job_id}")
            
            # Wait for completion if requested
            if wait:
                if json_output:
                    from zpools.helpers import JobPoller
                    poller = JobPoller(client, job_id, timeout=timeout, poll_interval=5)
                    final_job = poller.wait_for_completion()
                    print(json.dumps(final_job, indent=2, default=str))
                else:
                    try:
                        final_job = wait_for_job_with_progress(
                            client, job_id, "ZPool scrub", timeout=timeout, poll_interval=5
                        )
                    except TimeoutError:
                        console.print(f"[red]Timeout waiting for scrub to complete[/red]")
                        console.print(f"Job ID: {job_id}")
                    except RuntimeError:
                        console.print(f"Job ID: {job_id}")
        else:
            error_msg = format_error_response(response.status_code, response.content, json_output)
            if json_output:
                print(error_msg)
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {error_msg}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")
