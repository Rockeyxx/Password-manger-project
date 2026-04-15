
#omar haddad 2236620
import os,secrets
from cryptography.fernet import Fernet # cyptorgraphy مكتبه
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
"""
encryption class 
first choose the exact path where you want the key to exist .
if the key file exist then use it.
if not :
put a passphrase using secrets and create a key to put it in master key file using cryptography
then create a variable called cipher_sutie to use the key to encrypet 

create two method one to encrypet athoer to decrypet 
"""
class Encryption():
    def __init__(self) -> None:
        super().__init__()
        script_directory = os.path.dirname(os.path.abspath(__file__))#take the file path  
        master_key_file_path = os.path.join(script_directory, "master_key.key")#put the key in file path

        #if it exisit use it if its not create it 
        if os.path.exists(master_key_file_path):
            with open(master_key_file_path, "rb") as master_key_file:
                master_key = master_key_file.read()#read the data after opning it
        else:
            password = f"{secrets.token_bytes(32)}".encode('utf-8')#encode it using a random bytes taken from secrets 
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                iterations=100000,
                salt=salt,
                length=32,
                backend=default_backend()
             )
            master_key = kdf.derive(password)

            with open(master_key_file_path, "wb") as master_key_file:#open the file after creating it
                master_key_file.write(master_key)

        # Derive the encryption key using the master key
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(master_key))
    
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
    objectfrom = Encryption()
    alpha = objectfrom.encrypt("Omar")
    beta = objectfrom.decrypt(alpha)
    print(alpha)
    print(beta)
   
    

