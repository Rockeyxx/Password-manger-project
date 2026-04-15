
#omar haddad 2236620
import os
from cryptography.fernet import Fernet # cyptorgraphy مكتبه
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
"""
encryption class 
Uses a master password and a persisted salt to derive an encryption key at runtime.
The key is not stored on disk. Only the salt is persisted in 'salt.bin'.
"""
class Encryption():
    def __init__(self, master_password: str = None) -> None:
        super().__init__()
        if master_password is None:
            raise ValueError("Master password required")

        script_directory = os.path.dirname(os.path.abspath(__file__))
        salt_file_path = os.path.join(script_directory, "salt.bin")

        if os.path.exists(salt_file_path):
            with open(salt_file_path, "rb") as salt_file:
                salt = salt_file.read()
        else:
            salt = os.urandom(16)
            with open(salt_file_path, "wb") as salt_file:
                salt_file.write(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=salt,
            length=32,
            backend=default_backend()
        )
        
        key = kdf.derive(master_password.encode('utf-8'))
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(key))
    
    #encrypet the text( given)
    def encrypt(self, text:str)-> bytes:
        cipher_text = self.cipher_suite.encrypt(text.encode())
        return cipher_text
    
    #decrypet the cyper_text given
    def decrypt(self, cipher_text:bytes) -> str:
        if isinstance(cipher_text , str):
            cipher_text = cipher_text[1:].encode() 
        text = self.cipher_suite.decrypt(cipher_text).decode()
        return text

        
if "__main__"== __name__  :
    password = "MySecurePassword123"
    objectfrom = Encryption(master_password=password)
    alpha = objectfrom.encrypt("Omar")
    beta = objectfrom.decrypt(alpha)
    print(alpha)
    print(beta)
   
    

