import bcrypt

def hash_password(password: str) -> bytes:
    """Generate a salt and hash the password."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verify the password against the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
