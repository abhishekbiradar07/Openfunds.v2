from datetime import datetime


def format_btc(amount):
    """Format BTC amount"""
    if amount is None:
        return "0.00000000 BTC"
    return f"{float(amount):.8f} BTC"


def format_percentage(value):
    """Format percentage value"""
    if value is None:
        return "0%"
    return f"{float(value):.2f}%"


def format_date(date_string):
    """Format ISO date string"""
    if not date_string:
        return "N/A"
    
    try:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except Exception:
        return date_string
