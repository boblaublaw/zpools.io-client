"""Helper utilities for long-running wait operations with token refresh."""
import sys
import time
from typing import Optional


def wait_with_token_refresh(client, duration_seconds: float, show_progress: Optional[bool] = None):
    """
    Wait for specified duration, refreshing auth token every 50 minutes.
    
    JWT tokens expire after 1 hour. This helper refreshes tokens at 50 minutes
    (10 minutes before expiry) to handle ephemeral errors and ensure validity.
    
    Args:
        client: ZPoolsClient instance
        duration_seconds: How long to wait
        show_progress: Show refresh messages (defaults to True if interactive terminal)
    
    Example:
        # Wait for 5 hours with automatic token refresh
        wait_with_token_refresh(client, 5 * 3600)
    """
    if show_progress is None:
        show_progress = sys.stdout.isatty()
    
    refresh_interval = 50 * 60  # 50 minutes
    start = time.time()
    next_refresh = start + refresh_interval
    first_iteration = True
    
    while time.time() - start < duration_seconds:
        remaining = duration_seconds - (time.time() - start)
        if remaining <= 0:
            break
        
        # Show status on first iteration
        if first_iteration and show_progress:
            mins_remaining = int(remaining / 60)
            mins_to_next_refresh = int((next_refresh - time.time()) / 60)
            print(f"Wait remaining: {mins_remaining}m | Next token refresh: {mins_to_next_refresh}m")
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
                    mins_remaining = int(remaining / 60)
                    mins_to_next_refresh = int(refresh_interval / 60)
                    print(f"Token refreshed. Wait remaining: {mins_remaining}m | Next refresh: {mins_to_next_refresh}m")
                next_refresh = time.time() + refresh_interval
            except Exception:
                # Silent failure - will retry on next interval
                pass

