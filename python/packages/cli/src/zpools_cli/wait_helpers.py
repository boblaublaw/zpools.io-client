"""Helper utilities for long-running wait operations with token refresh."""
import sys
import time
from datetime import datetime, timezone
from typing import Optional
from rich.console import Console
from rich.table import Table
from zpools_cli.utils import format_timestamp


def wait_with_token_refresh(client, duration_seconds: float, console: Optional[Console] = None, show_progress: Optional[bool] = None, use_local_tz: bool = False):
    """
    Wait for specified duration, refreshing auth token every 50 minutes.
    
    JWT tokens expire after 1 hour. This helper refreshes tokens at 50 minutes
    (10 minutes before expiry) to handle ephemeral errors and ensure validity.
    
    Args:
        client: ZPoolsClient instance
        duration_seconds: How long to wait
        console: Rich Console instance for formatted output (optional)
        show_progress: Show refresh messages (defaults to True if interactive terminal)
        use_local_tz: Show timestamps in local timezone (default: UTC)
    
    Example:
        # Wait for 5 hours with automatic token refresh
        wait_with_token_refresh(client, 5 * 3600)
    """
    if console is None:
        console = Console()
    if show_progress is None:
        show_progress = sys.stdout.isatty()
    
    refresh_interval = 50 * 60  # 50 minutes
    start = time.time()
    next_refresh = start + refresh_interval
    first_iteration = True
    
    def format_time_table(refresh_time_utc):
        """Create a formatted table showing wait status."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="cyan", width=20)
        table.add_column(style="white")
        
        # Format refresh time using shared formatter
        refresh_str = format_timestamp(refresh_time_utc, use_local_tz)
        
        table.add_row("[cyan]Next token refresh:[/cyan]", f"[white]{refresh_str}[/white]")
        
        return table
    
    while time.time() - start < duration_seconds:
        remaining = duration_seconds - (time.time() - start)
        if remaining <= 0:
            break
        
        # Show status on first iteration
        if first_iteration and show_progress:
            refresh_time_utc = datetime.fromtimestamp(next_refresh, tz=timezone.utc)
            table = format_time_table(refresh_time_utc)
            console.print(table)
            first_iteration = False
        
        # Calculate time until next refresh
        current_time = time.time()
        time_until_refresh = next_refresh - current_time
        
        # Refresh if it's time (check with small tolerance for timing precision)
        if time_until_refresh <= 1:  # Within 1 second of refresh time
            try:
                client.get_authenticated_client()
                # Update next_refresh before showing output
                next_refresh = current_time + refresh_interval
                if show_progress:
                    refresh_time_utc = datetime.fromtimestamp(next_refresh, tz=timezone.utc)
                    console.print("[green]Token refreshed.[/green]")
                    table = format_time_table(refresh_time_utc)
                    console.print(table)
            except Exception as e:
                # Log error but continue - will retry on next iteration
                if show_progress:
                    console.print(f"[yellow]Token refresh failed, will retry: {e}[/yellow]")
                # Set next_refresh to retry in 1 minute instead of 50 minutes
                next_refresh = current_time + 60
        else:
            # Sleep until next event (end of wait, refresh time, or max 60s)
            sleep_time = min(remaining, max(0, time_until_refresh), 60)
            if sleep_time > 0:
                time.sleep(sleep_time)

