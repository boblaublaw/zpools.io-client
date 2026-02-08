from datetime import datetime
from datetime import timezone as tz
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.console import Group
from zpools_cli.progress import ProgressMonitor


def wait_for_job_with_progress(client, job_id: str, operation_name: str, timeout: int = 1800, poll_interval: int = 60) -> dict:
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
    console = Console()
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
        
        # Build history table (show all events)
        history_table = Table(show_header=True, box=None, padding=(0, 1))
        history_table.add_column("Time", style="dim", width=8)
        history_table.add_column("Message", style="white")
        
        for event in history:
            timestamp = event.get('timestamp', '')
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
            
            history_table.add_row(time_str, event_msg)
        
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
