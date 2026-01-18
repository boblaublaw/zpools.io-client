"""Helper utilities for long-running wait operations with token refresh."""
import sys
import time
from datetime import datetime, timezone
from typing import Optional
from rich.console import Console
from rich.table import Table


def wait_with_token_refresh(client, duration_seconds: float, console: Optional[Console] = None, show_progress: Optional[bool] = None):
    """
    Wait for specified duration, refreshing auth token every 50 minutes.
    
    JWT tokens expire after 1 hour. This helper refreshes tokens at 50 minutes
    (10 minutes before expiry) to handle ephemeral errors and ensure validity.
    
    Args:
        client: ZPoolsClient instance
        duration_seconds: How long to wait
        console: Rich Console instance for formatted output (optional)
        show_progress: Show refresh messages (defaults to True if interactive terminal)
    
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
    
    def format_time_table(refresh_time_utc, refresh_time_local):
        """Create a formatted table showing wait status."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="cyan", width=20)
        table.add_column(style="white")
        
        # Format refresh times
        refresh_utc_str = refresh_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
        refresh_local_str = refresh_time_local.strftime('%Y-%m-%d %H:%M:%S %Z')
        
        table.add_row("[cyan]Next token refresh:[/cyan]", f"[white]{refresh_utc_str} / {refresh_local_str}[/white]")
        
        return table
    
    while time.time() - start < duration_seconds:
        remaining = duration_seconds - (time.time() - start)
        if remaining <= 0:
            break
        
        # Show status on first iteration
        if first_iteration and show_progress:
            refresh_time_utc = datetime.fromtimestamp(next_refresh, tz=timezone.utc)
            refresh_time_local = refresh_time_utc.astimezone()
            table = format_time_table(refresh_time_utc, refresh_time_local)
            console.print(table)
            first_iteration = False
        
        # Sleep until next event (end of wait, refresh time, or max 60s)
        sleep_time = min(remaining, max(0, next_refresh - time.time()), 60)
        if sleep_time > 0:
            time.sleep(sleep_time)
        
        # Refresh if it's time
        if time.time() >= next_refresh:
            try:
                client.get_authenticated_client()
                if show_progress:
                    next_refresh = time.time() + refresh_interval
                    refresh_time_utc = datetime.fromtimestamp(next_refresh, tz=timezone.utc)
                    refresh_time_local = refresh_time_utc.astimezone()
                    console.print("[green]Token refreshed.[/green]")
                    table = format_time_table(refresh_time_utc, refresh_time_local)
                    console.print(table)
                else:
                    next_refresh = time.time() + refresh_interval
            except Exception:
                # Silent failure - will retry on next interval
                pass

