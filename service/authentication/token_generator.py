from typing import Callable, Tuple, Optional

from cryptography.fernet import Fernet, InvalidToken


class TokenGenerator:
    def __init__(self, key: str):
        f = Fernet(key.encode('ascii'))
        self.encryptor: Callable = f.encrypt
        self.decryptor: Callable = f.decrypt

    def encrypt(self, text: str) -> Tuple[bool, Optional[str]]:
        try:
            return True, self.encryptor(text.encode('ascii'))
        except Exception as e:
            return False, None

    def decrypt(self, cypher_text: str) -> Tuple[bool, Optional[str]]:
        try:
            return True, self.decryptor(cypher_text).decode('ascii')
        except Exception as e:
            return False, None
