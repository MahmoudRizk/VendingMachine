from typing import Dict


class ServiceResponse:
    def __init__(self, success: bool = False, message: str = "", data=None):
        if data is None:
            data = {}
        self.success = success
        self.message = message
        self.data = data
