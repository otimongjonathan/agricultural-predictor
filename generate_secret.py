import secrets

# Generate a secure random secret key
secret_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")