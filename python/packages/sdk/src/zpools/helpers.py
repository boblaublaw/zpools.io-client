"""
Helper utilities for working with zpools.io API.

Includes job polling, resource waiting, and other convenience functions.
"""
import time
from typing import Optional, Callable


class JobPoller:
    """Helper for polling job status until completion."""
    
    def __init__(self, client, job_id: str, timeout: int = 600, poll_interval: int = 5):
        """
        Initialize job poller.
        
        Args:
            client: ZPoolsClient instance
            job_id: Job ID to poll
            timeout: Maximum time to wait in seconds (default: 10 minutes)
            poll_interval: Time between polls in seconds (default: 5 seconds)
        """
        self.client = client
        self.job_id = job_id
        self.timeout = timeout
        self.poll_interval = poll_interval
    
    def wait_for_completion(self) -> dict:
        """
        Poll job until it reaches a terminal state (succeeded/failed).
        
        Returns:
            Final job details dict (the 'job' object from additional_properties)
            
        Raises:
            TimeoutError: If job doesn't complete within timeout
            RuntimeError: If job fails
        """
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > self.timeout:
                raise TimeoutError(
                    f"Job {self.job_id} did not complete within {self.timeout}s"
                )
            
            response = self.client.get_job(self.job_id)
            
            if response.status_code != 200:
                raise RuntimeError(
                    f"Failed to get job status: {response.status_code}"
                )
            
            # The actual job data is in additional_properties['job']
            job_data = response.parsed.detail.additional_properties.get('job')
            if not job_data:
                raise RuntimeError(f"Job {self.job_id} response missing 'job' field")
            
            current_status = job_data.get('current_status', {})
            state = current_status.get('state')
            
            if state == "succeeded":
                return job_data
            elif state == "failed":
                error_msg = current_status.get('message', 'Unknown error')
                raise RuntimeError(f"Job {self.job_id} failed: {error_msg}")
            elif state in ("pending", "running", "queued", "in progress"):
                time.sleep(self.poll_interval)
            else:
                raise RuntimeError(f"Unknown job state: {state}")


def wait_for_zpool_ready(
    client,
    zpool_id: str,
    timeout: int = 600,
    poll_interval: int = 5
) -> dict:
    """
    Wait for zpool to appear in list (after creation job completes).
    
    Args:
        client: ZPoolsClient instance
        zpool_id: Zpool ID to wait for
        timeout: Maximum time to wait in seconds
        poll_interval: Time between polls in seconds
        
    Returns:
        Zpool details dict
        
    Raises:
        TimeoutError: If zpool doesn't appear within timeout
    """
    start_time = time.time()
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(
                f"Zpool {zpool_id} did not become ready within {timeout}s"
            )
        
        response = client.list_zpools()
        if response.status_code == 200:
            zpools = response.parsed.detail.zpools
            for zpool in zpools:
                if zpool.zpool_id == zpool_id:
                    return zpool
        
        time.sleep(poll_interval)


def poll_until(
    poll_fn: Callable,
    condition: Callable[[any], bool],
    timeout: int = 60,
    poll_interval: int = 2
) -> any:
    """
    Generic polling helper.
    
    Args:
        poll_fn: Function to call repeatedly (no args)
        condition: Function that returns True when done
        timeout: Maximum time to wait in seconds
        poll_interval: Time between polls in seconds
        
    Returns:
        Result from poll_fn when condition is met
        
    Raises:
        TimeoutError: If condition not met within timeout
    """
    start_time = time.time()
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(f"Condition not met within {timeout}s")
        
        result = poll_fn()
        if condition(result):
            return result
        
        time.sleep(poll_interval)
