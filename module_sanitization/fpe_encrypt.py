import pyffx

def encrypt(text: str, config: dict):
    """
    Format-preserving encryption using FFX (pyffx).
    Encrypts alphanumeric text with a fixed key and optional alphabet.
    """
    key = config.get("key", "default-fpe-key")
    alphabet = config.get("alphabet", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-_+=|\\[]{}\"':;/?.>,<")
    
    if isinstance(key, str):
        try:
            key = bytes.fromhex(key)  # Convert hex string to bytes
        except ValueError:
            raise ValueError("Key must be a valid hex string or bytes object")
    
    # print("key, ", key)
    
    words = text.split()
    encrypted_words = []
    for word in words:
        encrypter = pyffx.String(key, alphabet=alphabet, length=len(word))
        encrypted_words.append(encrypter.encrypt(word))
        # print(encrypted_words)
        # if all(char in alphabet for char in word):
        #     try:
        #         encrypter = pyffx.String(key, alphabet=alphabet, length=len(word))
        #         encrypted_words.append(encrypter.encrypt(word))
        #         print(encrypted_words)
        #     except Exception:
        #         encrypted_words.append(word)
        # else:
        #     encrypted_words.append(word)
            
    
    return ' '.join(encrypted_words)

def decrypt(text: str, config: dict) -> str:
    key = config.get("key", "default-fpe-key")
    alphabet = config.get("alphabet", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-_+=|\\[]{}\"':;/?.>,<")

    if isinstance(key, str):
        try:
            key = bytes.fromhex(key)  # Convert hex string to bytes
        except ValueError:
            raise ValueError("Key must be a valid hex string or bytes object")
        
    words = text.split()
    decrypted_words = []
    for word in words:
        try:
            decrypter = pyffx.String(key, alphabet=alphabet, length=len(word))
            decrypted_words.append(decrypter.decrypt(word))
        except Exception:
            decrypted_words.append(word)

    return ' '.join(decrypted_words)