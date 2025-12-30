from cryptography.fernet import Fernet
import os 

class FernetEncryptionService:
    def __init__(self):
        self.__secret_key = os.getenv("ENCRYPTION_KEY")

        if not self.__secret_key:
            raise ValueError("Encyption variables not set")
        
        self.__fernet = Fernet(self.__secret_key)
        

    def encrypt(self, plaintext: str) -> str:
        encrypted = self.__fernet.encrypt(plaintext.encode())
        return encrypted.decode()

    def decrypt(self, ciphertext: str) -> str:
        decrypted = self.__fernet.decrypt(ciphertext.encode())
        return decrypted.decode()