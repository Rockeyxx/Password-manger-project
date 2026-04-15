
import subprocess

try:
    import sqlmodel , sqlalchemy
    import pyperclip
    from PyQt5 import QtWidgets, QtCore
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    print("you have it")
except ImportError:
    subprocess.run(['pip', 'install', 'pyperclip'])
    subprocess.run(['pip', 'install', 'PyQt5'])
    subprocess.run(['pip', 'install', 'cryptography'])
    subprocess.run(['pip', 'install', 'sqlmodel'])
    from PyQt5 import QtWidgets, QtCore
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    
