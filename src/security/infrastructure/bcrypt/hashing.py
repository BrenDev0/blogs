import bcrypt
import hashlib
from src.security.domain.services.hashing import HashingService
from src.security.domain.exceptions import IncorrectPassword

class BcryptHashingService(HashingService):
    def hash_for_search(self, data: str) -> str:
        email_bytes = data.lower().encode('utf-8')  
        hashed_data = hashlib.sha256(email_bytes).hexdigest()
        return hashed_data

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def compare_password(
        self,
        password: str, 
        hashed_password: str, 
        detail: str = "Incorrect password", 
        throw_error: bool = True
    ) -> bool:
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            if throw_error:
                raise IncorrectPassword(detail=detail)
            else:
                return False
        return True