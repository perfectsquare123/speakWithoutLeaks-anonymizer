import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def encrypt(text: str, config: dict):
    """
    AES encryption with CBC mode and PKCS7 padding.
    Returns base64-encoded ciphertext with IV prepended.
    """
    key = config.get("key", "default-fpe-key")
    
    if isinstance(key, str):
        try:
            key = bytes.fromhex(key)  # Convert hex string to bytes
        except ValueError:
            raise ValueError("Key must be a valid hex string or bytes object")
    
    aes_key = key[:32].ljust(32, b'0')  # Ensure 256-bit key

    try:
        encoded_text = text.encode("utf-8")
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(encoded_text) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_text) + encryptor.finalize()

        return base64.urlsafe_b64encode(iv + ciphertext).decode("utf-8")
    
    except Exception as e:
        print(f"[AES Error] {text} => {e}")
        return text

def decrypt(cipher_text: str, config: dict) -> str:

    key = config.get("key", "default-aes-key")
    
    if isinstance(key, str):
        try:
            key = bytes.fromhex(key)  # Convert hex string to bytes
        except ValueError:
            raise ValueError("Key must be a valid hex string or bytes object")
    
    aes_key = key[:32].ljust(32, b'0')

    try:
        data = base64.urlsafe_b64decode(cipher_text.encode("utf-8"))
        iv = data[:16]
        ciphertext = data[16:]

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_text = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plain_text = unpadder.update(padded_text) + unpadder.finalize()

        return plain_text.decode("utf-8")
    except Exception as e:
        print(f"[AES Decryption Error] {cipher_text} => {e}")
        return cipher_text