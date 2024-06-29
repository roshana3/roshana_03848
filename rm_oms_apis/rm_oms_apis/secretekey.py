import secrets

# Generate a secure random key with 32 bytes (256 bits)
SECRET_KEY = secrets.token_hex(32)
print("Generated Secret Key:", SECRET_KEY)