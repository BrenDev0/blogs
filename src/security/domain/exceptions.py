class ExpiredToken(Exception):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(detail)

class InvalidToken(Exception):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(detail)

class IncorrectPassword(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)

class PermissionsException(Exception):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail)

class HMACException(Exception):
    def __init__(self, detail: str = "HMAC verification failed"):
        self.detail = detail
        super().__init__(detail)