import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SimpleEncryption:
    """A simple encryption utility using Fernet symmetric encryption."""
    
    def __init__(self, password: str = None):
        if password:
            self.key = self._derive_key(password)
            self.cipher_suite = Fernet(self.key)
        else:
            self.key = None
            self.cipher_suite = None
    
    def _derive_key(self, password: str, salt: bytes = b'salt_') -> bytes:
        """Derive a key from a password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def set_password(self, password: str):
        """Set the password and initialize the cipher suite."""
        self.key = self._derive_key(password)
        self.cipher_suite = Fernet(self.key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt a string."""
        if not self.cipher_suite:
            raise ValueError("Password not set. Call set_password() first.")
            
        encrypted_bytes = self.cipher_suite.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted_bytes).decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt a string."""
        if not self.cipher_suite:
            raise ValueError("Password not set. Call set_password() first.")
            
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode())
        decrypted_bytes = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()
    
    @staticmethod
    def hash_string(text: str) -> str:
        """Create a SHA-256 hash of a string."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def hash_file(file_path: str) -> str:
        """Create a SHA-256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()