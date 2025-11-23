import typer
import json
from rich.console import Console
from rich.table import Table
from zpools import ZPoolsClient
from zpools._generated.api.jobs import (
    get_jobs,
    get_job_job_id,
    get_job_job_id_history
)
from zpools._generated.types import UNSET

app = typer.Typer(help="Manage background jobs")
console = Console()

@app.command("list")
def list_jobs(
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """List all background jobs."""
    try:
        client = ZPoolsClient()
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
                status_val = job.status.value if job.status is not UNSET else "Unknown"
                message = job.message if job.message is not UNSET else ""
                # Truncate message if too long
                if len(message) > 50:
                    message = message[:47] + "..."
                
                table.add_row(
                    job.job_id,
                    job.operation,
                    status_val,
                    str(job.created_at),
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
        client = ZPoolsClient()
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
        client = ZPoolsClient()
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
