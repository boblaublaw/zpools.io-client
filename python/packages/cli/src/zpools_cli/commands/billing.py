import typer
import json
from rich.console import Console
from rich.table import Table
from zpools._generated.api.billing import (
    get_billing_balance,
    get_billing_ledger,
    post_codes_claim,
    post_dodo_start
)
from zpools._generated.models.post_codes_claim_body import PostCodesClaimBody
from zpools._generated.models.post_dodo_start_body import PostDodoStartBody
from zpools._generated.types import UNSET
import datetime

app = typer.Typer(help="Manage billing and payments", no_args_is_help=True)
console = Console()

@app.command("balance")
def get_balance(
    ctx: typer.Context,
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Get current account balance."""
    try:
        from zpools_cli.utils import get_authenticated_client
        client = get_authenticated_client(ctx.obj)
        auth_client = client.get_authenticated_client()
        
        response = get_billing_balance.sync_detailed(client=auth_client)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            balance_obj = response.parsed.detail.balance
            # Check if balance_obj is Unset or None
            if not balance_obj or isinstance(balance_obj, type(UNSET)):
                 console.print("[yellow]Balance information unavailable.[/yellow]")
                 return
            
            # Access balance_usd from the object
            balance_usd = balance_obj.balance_usd if balance_obj.balance_usd is not UNSET else 0
            console.print(f"[bold]Current Balance:[/bold] ${balance_usd:.2f}")
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("ledger")
def get_ledger(
    ctx: typer.Context,
    limit: int = typer.Option(None, help="Number of entries to display"),
    since: str = typer.Option(None, help="Start usage date (YYYY-MM-DD) - filters by when charges are for"),
    until: str = typer.Option(None, help="End usage date (YYYY-MM-DD) - filters by when charges are for"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """View billing transaction history. Shows both usage_date (when charges are for) and ts (when posted)."""
    try:
        from zpools_cli.utils import get_authenticated_client
        client = get_authenticated_client(ctx.obj)
        auth_client = client.get_authenticated_client()
        
        # Parse dates if provided
        since_date = None
        if since:
            try:
                since_date = datetime.datetime.strptime(since, "%Y-%m-%d").date()
            except ValueError:
                console.print("[red]Invalid date format for --since. Use YYYY-MM-DD[/red]")
                return

        until_date = None
        if until:
            try:
                until_date = datetime.datetime.strptime(until, "%Y-%m-%d").date()
            except ValueError:
                console.print("[red]Invalid date format for --until. Use YYYY-MM-DD[/red]")
                return

        # Build kwargs for API call (API returns newest-first)
        kwargs = {}
        if limit:
            kwargs["limit"] = limit
        if since_date:
            kwargs["since"] = since_date
        if until_date:
            kwargs["until"] = until_date

        response = get_billing_ledger.sync_detailed(client=auth_client, **kwargs)
        
        if response.status_code == 200:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            items = response.parsed.detail.items
            if not items or items is UNSET:
                console.print("No transactions found.")
                return

            table = Table(title="Billing Ledger")
            table.add_column("Date", style="green")
            table.add_column("Time", style="blue")
            table.add_column("Event Type", style="yellow")
            table.add_column("Source", style="cyan")
            table.add_column("Amount (USD)", style="magenta")
            table.add_column("Note", style="white")

            # API returns newest-first, display as-is
            for item in items:
                # Extract fields with UNSET checks
                usage_date = item.usage_date if item.usage_date is not UNSET else ""
                ts = item.ts if item.ts is not UNSET else ""
                event_type = item.event_type if item.event_type is not UNSET else ""
                source = item.source if item.source is not UNSET else ""
                amount_usd = item.amount_usd if item.amount_usd is not UNSET else 0
                note = item.note if item.note is not UNSET else ""
                
                # Format amount with color
                amount_str = f"${amount_usd:.2f}"
                if amount_usd > 0:
                    amount_str = f"[green]+{amount_str}[/green]"
                elif amount_usd < 0:
                    amount_str = f"[red]{amount_str}[/red]"
                
                table.add_row(
                    usage_date,
                    ts,
                    event_type,
                    source,
                    amount_str,
                    note
                )
            console.print(table)
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("claim")
def claim_code(
    ctx: typer.Context,
    code: str = typer.Argument(..., help="Credit code to redeem"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Redeem a credit code."""
    try:
        from zpools_cli.utils import get_authenticated_client
        client = get_authenticated_client(ctx.obj)
        auth_client = client.get_authenticated_client()
        
        body = PostCodesClaimBody(code=code)
        
        response = post_codes_claim.sync_detailed(client=auth_client, body=body)
        
        if response.status_code == 201:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            detail = response.parsed.detail
            amount = detail.amount_cents if detail.amount_cents is not UNSET else 0
            console.print(f"[green]Code redeemed successfully![/green]")
            console.print(f"Added: ${amount/100:.2f}")
            # New balance is not returned in this response model, user can check balance separately
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command("start")
def start_payment(
    ctx: typer.Context,
    amount: int = typer.Argument(..., help="Amount in dollars to add (1-100)"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON")
):
    """Start a payment session to add credits."""
    try:
        from zpools_cli.utils import get_authenticated_client
        client = get_authenticated_client(ctx.obj)
        auth_client = client.get_authenticated_client()
        
        # Validate amount (API accepts 1-100)
        if amount < 1 or amount > 100:
             console.print("[yellow]Amount must be between $1 and $100[/yellow]")
             return

        body = PostDodoStartBody(quantity=amount)
        
        response = post_dodo_start.sync_detailed(client=auth_client, body=body)
        
        if response.status_code == 201:
            if json_output:
                print(json.dumps(response.parsed.to_dict(), indent=2, default=str))
                return
            
            url = response.parsed.detail.payment_link
            console.print(f"[green]Payment session started![/green]")
            console.print(f"Please visit this URL to complete payment:")
            console.print(f"[link={url}]{url}[/link]")
        else:
            console.print(f"[red]Error {response.status_code}:[/red] {response.content}")

    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")
