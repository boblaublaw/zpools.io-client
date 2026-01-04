"""Billing and payment operations."""


class BillingMixin:
    """Mixin providing billing and payment operations."""
    
    def get_billing_balance(self):
        """
        Get account balance.
        
        Returns:
            Response with status_code and balance details
        """
        from .._generated.api.billing import get_billing_balance
        
        auth_client = self._auth.get_authenticated_client()
        return get_billing_balance.sync_detailed(client=auth_client)
    
    def get_billing_ledger(self, since: str = None, until: str = None, limit: int = None):
        """
        Get billing ledger entries with optional date filters.
        
        Filters by usage_date (the date charges are for), not transaction timestamp.
        Results include both usage_date and ts (transaction timestamp).
        
        Args:
            since: Start usage date in YYYY-MM-DD format (or date object)
            until: End usage date in YYYY-MM-DD format (or date object)
            limit: Maximum number of entries (1-5000, default 500)
            
        Returns:
            Response with status_code and ledger items
        """
        from .._generated.api.billing import get_billing_ledger
        from .._generated.types import UNSET
        from datetime import datetime
        
        auth_client = self._auth.get_authenticated_client()
        
        # Convert string dates to date objects
        since_param = UNSET
        if since is not None:
            if isinstance(since, str):
                since_param = datetime.strptime(since, "%Y-%m-%d").date()
            else:
                since_param = since
        
        until_param = UNSET
        if until is not None:
            if isinstance(until, str):
                until_param = datetime.strptime(until, "%Y-%m-%d").date()
            else:
                until_param = until
        
        limit_param = limit if limit is not None else UNSET
        
        return get_billing_ledger.sync_detailed(
            client=auth_client,
            since=since_param,
            until=until_param,
            limit=limit_param
        )
