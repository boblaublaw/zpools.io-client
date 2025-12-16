"""Live progress display utilities for CLI operations."""

import time
from typing import Callable, Any
from rich.console import Console
from rich.live import Live
from rich.panel import Panel


class ProgressMonitor:
    """
    Generic progress monitor with smooth animation decoupled from API polling.
    
    Provides a smooth spinner and live display that updates independently
    of API poll intervals.
    """
    
    def __init__(
        self,
        console: Console,
        poll_interval: int = 10,
        timeout: int = 1800,
        refresh_per_second: int = 4,
        spinner_update_interval: int = 2
    ):
        """
        Initialize progress monitor.
        
        Args:
            console: Rich console instance
            poll_interval: Seconds between API polls
            timeout: Maximum seconds to wait
            refresh_per_second: Display refresh rate
            spinner_update_interval: Update spinner every N display updates
        """
        self.console = console
        self.poll_interval = poll_interval
        self.timeout = timeout
        self.refresh_per_second = refresh_per_second
        self.spinner_update_interval = spinner_update_interval
        
        self.start_time = time.time()
        self.last_poll_time = 0
        self.frame_idx = 0
        self.update_counter = 0
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def get_spinner(self) -> str:
        """Get current spinner frame and advance on appropriate intervals."""
        if self.update_counter % self.spinner_update_interval == 0:
            self.frame_idx = (self.frame_idx + 1) % len(self.spinner_frames)
        self.update_counter += 1
        return self.spinner_frames[self.frame_idx]
    
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds since start."""
        return time.time() - self.start_time
    
    def elapsed_str(self) -> str:
        """Get formatted elapsed time string."""
        return f"{int(self.elapsed_time())}s"
    
    def should_poll(self) -> bool:
        """Check if it's time to poll the API again."""
        current_time = time.time()
        should = current_time - self.last_poll_time >= self.poll_interval
        if should:
            self.last_poll_time = current_time
        return should
    
    def check_timeout(self) -> None:
        """Raise TimeoutError if timeout exceeded."""
        if self.elapsed_time() > self.timeout:
            raise TimeoutError(f"Operation did not complete within {self.timeout}s")
    
    def monitor(
        self,
        poll_func: Callable[[], Any],
        render_func: Callable[[Any, str], Panel],
        check_complete_func: Callable[[Any], bool],
        operation_name: str
    ) -> Any:
        """
        Monitor progress with live display.
        
        Args:
            poll_func: Function that polls API and returns current state
            render_func: Function that renders display panel (state, spinner) -> Panel
            check_complete_func: Function that checks if operation is complete
            operation_name: Human-readable operation name
            
        Returns:
            Final state data
            
        Raises:
            TimeoutError: If operation doesn't complete in time
        """
        cached_state = None
        
        with Live(console=self.console, refresh_per_second=self.refresh_per_second) as live:
            while True:
                self.check_timeout()
                
                # Poll API at intervals
                if self.should_poll():
                    cached_state = poll_func()
                    
                    # Check if complete
                    if check_complete_func(cached_state):
                        live.stop()
                        return cached_state
                
                # Update display (continues regardless of API calls)
                if cached_state is not None:
                    panel = render_func(cached_state, self.get_spinner())
                    live.update(panel)
                
                # Sleep for display interval
                time.sleep(1.0 / self.refresh_per_second)
