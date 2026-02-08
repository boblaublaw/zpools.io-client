"""Job management operations."""


class JobMixin:
    """Mixin providing job management operations."""
    
    def get_job(self, job_id: str):
        """
        Get job details.
        
        Args:
            job_id: The job_id to query
            
        Returns:
            Response with status_code and job details
        """
        from .._generated.api.jobs import get_job_job_id
        
        auth_client = self._auth.get_authenticated_client()
        return get_job_job_id.sync_detailed(client=auth_client, job_id=job_id)
    
    def list_jobs(self, limit=None, before=None, after=None, sort=None):
        """
        List all jobs with optional filtering and sorting.
        
        Args:
            limit: Maximum number of jobs to return (1-1000, default 100)
            before: Return jobs created before this datetime (ISO 8601 or datetime object)
            after: Return jobs created after this datetime (ISO 8601 or datetime object)
            sort: Sort order ("asc" or "desc", default "desc")
        
        Returns:
            Response with status_code and parsed list of jobs
        """
        from .._generated.api.jobs import get_jobs
        from .._generated.models.get_jobs_sort import GetJobsSort
        from .._generated.types import UNSET
        from datetime import datetime
        
        auth_client = self._auth.get_authenticated_client()
        
        # Convert parameters to SDK types
        limit_param = limit if limit is not None else UNSET
        
        before_param = UNSET
        if before is not None:
            if isinstance(before, str):
                before_param = datetime.fromisoformat(before.replace('Z', '+00:00'))
            else:
                before_param = before
        
        after_param = UNSET
        if after is not None:
            if isinstance(after, str):
                after_param = datetime.fromisoformat(after.replace('Z', '+00:00'))
            else:
                after_param = after
        
        sort_param = UNSET
        if sort is not None:
            sort_param = GetJobsSort.ASC if sort.lower() == "asc" else GetJobsSort.DESC
        
        return get_jobs.sync_detailed(
            client=auth_client,
            limit=limit_param,
            before=before_param,
            after=after_param,
            sort=sort_param
        )
    
    def get_job_history(self, job_id: str):
        """
        Get job history/timeline.
        
        Args:
            job_id: The job_id to query
            
        Returns:
            Response with status_code and job history events
        """
        from .._generated.api.jobs import get_job_job_id_history
        
        auth_client = self._auth.get_authenticated_client()
        return get_job_job_id_history.sync_detailed(client=auth_client, job_id=job_id)
