# app/utils/token_generator.py

import secrets

def generate_token(length: int = 32) -> str:
    """Generate a secure URL-safe token."""
    return secrets.token_urlsafe(length)

