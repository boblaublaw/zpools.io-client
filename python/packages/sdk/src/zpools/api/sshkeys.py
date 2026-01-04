"""SSH key management operations."""


class SSHKeyMixin:
    """Mixin providing SSH key management operations."""
    
    def list_sshkeys(self):
        """
        List all SSH keys.
        
        Returns:
            Response with status_code and parsed list of SSH keys
        """
        from .._generated.api.ssh_keys import get_sshkey
        
        auth_client = self._auth.get_authenticated_client()
        return get_sshkey.sync_detailed(client=auth_client)
    
    def add_sshkey(self, public_key: str):
        """
        Add an SSH public key.
        
        Args:
            public_key: SSH public key content
            
        Returns:
            Response with status_code and pubkey_id
        """
        from .._generated.api.ssh_keys import post_sshkey
        from .._generated.models.post_sshkey_body import PostSshkeyBody
        
        auth_client = self._auth.get_authenticated_client()
        
        return post_sshkey.sync_detailed(
            client=auth_client,
            body=PostSshkeyBody(pubkey=public_key)
        )
    
    def delete_sshkey(self, pubkey_id: str):
        """
        Delete an SSH key.
        
        Args:
            pubkey_id: The pubkey_id of the key to delete
            
        Returns:
            Response with status_code
        """
        from .._generated.api.ssh_keys import delete_sshkey_pubkey_id
        
        auth_client = self._auth.get_authenticated_client()
        return delete_sshkey_pubkey_id.sync_detailed(client=auth_client, pubkey_id=pubkey_id)
