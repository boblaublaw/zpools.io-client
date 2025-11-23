import typer
import json
from rich.console import Console
from rich.table import Table
from zpools_cli.utils import get_authenticated_client
from zpools._generated.api.jobs import (
    get_jobs,
    get_job_job_id,
    get_job_job_id_history
)
from zpools._generated.types import UNSET

app = typer.Typer(help="Manage background jobs", no_args_is_help=True)
console = Console()

@app.command("list")
def list_jobs(
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """List all background jobs."""
    try:
        client = get_authenticated_client()
        auth_client = client.get_authenticated_client()
        
        response = get_jobs.sync_detailed(client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            jobs = response.parsed.detail.jobs
            if not jobs:
                console.print("No jobs found.")
                return

            table = Table(title="Your Jobs")
            table.add_column("ID", style="cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Status", style="blue")
            table.add_column("Created At", style="green")
            table.add_column("Message", style="white")

            for job in jobs:
                # API returns fields not in schema - they're in additional_properties
                job_id = job.job_id if job.job_id is not UNSET else ""
                
                # Try schema field first, then additional_properties
                operation = job.operation if job.operation is not UNSET else job.additional_properties.get('job_type', "")
                
                # Status is in current_status.state in additional_properties
                current_status = job.additional_properties.get('current_status', {})
                if isinstance(current_status, dict):
                    status_val = current_status.get('state', 'Unknown')
                    message = current_status.get('message', '')
                else:
                    # Fallback to schema status
                    status_val = job.status.value if job.status is not UNSET else "Unknown"
                    message = ""
                
                created_at = str(job.created_at) if job.created_at is not UNSET else ""
                
                # Truncate message if too long
                if len(message) > 50:
                    message = message[:47] + "..."
                
                table.add_row(
                    job_id,
                    operation,
                    status_val,
                    created_at,
                    message
                )
            console.print(table)
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("get")
def get_job(
    job_id: str = typer.Argument(..., help="Job ID to retrieve"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Get details of a specific job."""
    try:
        client = get_authenticated_client()
        auth_client = client.get_authenticated_client()
        
        response = get_job_job_id.sync_detailed(job_id=job_id, client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            job = response.parsed.detail
            console.print(f"[bold]Job ID:[/bold] {job.id}")
            console.print(f"[bold]Type:[/bold] {job.type}")
            console.print(f"[bold]Status:[/bold] {job.status}")
            console.print(f"[bold]Created At:[/bold] {job.created_at}")
            if job.updated_at:
                console.print(f"[bold]Updated At:[/bold] {job.updated_at}")
            if job.error:
                console.print(f"[red bold]Error:[/red bold] {job.error}")
            if job.result:
                console.print(f"[bold]Result:[/bold] {job.result}")
        elif response.status_code == 404:
            if json_output:
                print(json.dumps({"error": "Not found"}, indent=2))
            else:
                console.print(f"[red]Job {job_id} not found.[/red]")
        else:
            if json_output:
                print(json.dumps({"error": response.content}, indent=2))
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("history")
def job_history(
    job_id: str = typer.Argument(..., help="Job ID to get history for"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Get history of a specific job."""
    try:
        client = get_authenticated_client()
        auth_client = client.get_authenticated_client()
        
        response = get_job_job_id_history.sync_detailed(job_id=job_id, client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            events = response.parsed.detail.events
            if not events:
                console.print("No history found for this job.")
                return

            table = Table(title=f"History for Job {job_id}")
            table.add_column("Timestamp", style="green")
            table.add_column("Status", style="blue")
            table.add_column("Message", style="white")

            for event in events:
                table.add_row(
                    str(event.timestamp),
                    event.status,
                    event.message or ""
                )
            console.print(table)
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")
