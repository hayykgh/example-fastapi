from passlib.context import CryptContext

# Initialize CryptContext with bcrypt hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashes the password using bcrypt
def hash_password(password: str):
    """
    Hashes the provided password using bcrypt.

    Args:
    - password (str): Plain text password to hash.
    
    Returns:
    - str: Hashed password.
    """
    return pwd_context.hash(password)

# Compares if the two given passwords match
def verify_password(plain_password, hashed_password):
    """
    Verifies if the provided plain password matches the hashed password.

    Args:
    - plain_password (str): Plain text password to verify.
    - hashed_password (str): Hashed password stored in the database.
    
    Returns:
    - bool: True if the provided plain password, after hashing, matches the hashed password in the database. False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)