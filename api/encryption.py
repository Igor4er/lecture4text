from Crypto.Cipher import AES
from config import CONFIG
from Crypto.Random import get_random_bytes
import base64


key = CONFIG.AES_KEY.get_secret_value().encode('utf-8')

def encrypt(text):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    encrypted_bytes = iv + cipher.encrypt(text.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt(encrypted_text):
    encrypted_data = base64.b64decode(encrypted_text.encode('utf-8'))
    iv = encrypted_data[:16]  # Extract the IV
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    return cipher.decrypt(encrypted_data[16:]).decode('utf-8')
