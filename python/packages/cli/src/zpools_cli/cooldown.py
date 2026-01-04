from datetime import datetime, timezone, timedelta


def calculate_cooldown_info(mod_last_time):
    """
    Calculate cooldown information for a volume based on its last modification time.
    
    Args:
        mod_last_time: datetime object or ISO format string of last modification
        
    Returns:
        dict with keys:
            - in_cooldown (bool): Whether volume is currently in cooldown
            - retry_time (datetime): When cooldown expires (or None if not in cooldown)
            - wait_seconds (int): Seconds until cooldown expires (or 0 if not in cooldown)
            - wait_str (str): Human-readable wait time like "5h 8m"
            - retry_str (str): Formatted retry time like "2026-01-04 08:54:50 UTC"
    """
    if not mod_last_time:
        return {
            'in_cooldown': False,
            'retry_time': None,
            'wait_seconds': 0,
            'wait_str': '',
            'retry_str': ''
        }
    
    if isinstance(mod_last_time, str):
        mod_last_time = datetime.fromisoformat(mod_last_time.replace('Z', '+00:00'))
    
    retry_time = mod_last_time + timedelta(hours=6)
    now = datetime.now(timezone.utc)
    
    if retry_time > now:
        wait_seconds = (retry_time - now).total_seconds()
        hours = int(wait_seconds // 3600)
        minutes = int((wait_seconds % 3600) // 60)
        return {
            'in_cooldown': True,
            'retry_time': retry_time,
            'wait_seconds': int(wait_seconds),
            'wait_str': f"{hours}h {minutes}m",
            'retry_str': retry_time.strftime('%Y-%m-%d %H:%M:%S UTC')
        }
    else:
        return {
            'in_cooldown': False,
            'retry_time': retry_time,
            'wait_seconds': 0,
            'wait_str': '',
            'retry_str': ''
        }
