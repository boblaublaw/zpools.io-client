"""Personal Access Token (PAT) operations."""


class PATMixin:
    """Mixin providing PAT management operations."""
    
    def create_pat(self, label: str, scopes: list = None, expiry: str = None, tenant_id: str = None):
        """
        Create a Personal Access Token.
        
        Args:
            label: Human-readable label for the PAT
            scopes: Optional list of scopes (e.g., ['pat', 'sshkey', 'job', 'zpool'])
            expiry: Optional expiry date (YYYY-MM-DD)
            tenant_id: Optional tenant ID
            
        Returns:
            Response with status_code, detail.key_id, and detail.token
        """
        from .._generated.api.personal_access_tokens import post_pat
        from .._generated.models.post_pat_body import PostPatBody
        
        auth_client = self._auth.get_authenticated_client()
        
        # Build kwargs, only including non-None values to avoid passing None to UNSET fields
        body_kwargs = {"label": label}
        if scopes is not None:
            body_kwargs["scopes"] = scopes
        if expiry is not None:
            body_kwargs["expiry"] = expiry
        if tenant_id is not None:
            body_kwargs["tenant_id"] = tenant_id
        
        return post_pat.sync_detailed(
            client=auth_client,
            body=PostPatBody(**body_kwargs)
        )
    
    def list_pats(self):
        """
        List all Personal Access Tokens.
        
        Returns:
            Response with status_code and parsed list of PATs
        """
        from .._generated.api.personal_access_tokens import get_pat
        
        auth_client = self._auth.get_authenticated_client()
        return get_pat.sync_detailed(client=auth_client)
    
    def revoke_pat(self, key_id: str):
        """
        Revoke a Personal Access Token.
        
        Args:
            key_id: The key_id of the PAT to revoke
            
        Returns:
            Response with status_code
        """
        from .._generated.api.personal_access_tokens import delete_pat_key_id
        
        auth_client = self._auth.get_authenticated_client()
        return delete_pat_key_id.sync_detailed(client=auth_client, key_id=key_id)
