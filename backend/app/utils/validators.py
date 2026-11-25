import re


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def validate_btc_address(address: str) -> bool:
    """Validate Bitcoin address format (simplified for testnet)"""
    # Testnet addresses start with m, n, or 2
    # Mainnet addresses start with 1 or 3
    pattern = r'^[123mn][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    return bool(re.match(pattern, address))
