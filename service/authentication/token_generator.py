from typing import Callable, Tuple, Optional

from cryptography.fernet import Fernet, InvalidToken

from service.base_service_response import ServiceResponse as Response


class TokenGenerator:
    def __init__(self, key: str):
        f = Fernet(key.encode('ascii'))
        self.encryptor: Callable = f.encrypt
        self.decryptor: Callable = f.decrypt

    def encrypt(self, text: str) -> Response:
        try:
            return Response(success=True, data=self.encryptor(text.encode('ascii')))
        except Exception as e:
            return Response(success=False)

    def decrypt(self, cypher_text: str) -> Response:
        try:
            return Response(success=True, data=self.decryptor(cypher_text).decode('ascii'))
        except Exception as e:
            return Response(success=False)
