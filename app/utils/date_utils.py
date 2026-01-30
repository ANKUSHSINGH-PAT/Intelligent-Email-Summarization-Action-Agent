from datetime import datetime

def format_timestamp(ts: int) -> str:
    """
    Convert UNIX timestamp to readable date.
    """
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
