class ExpiredToken(Exception):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(detail)

class InvalidToken(Exception):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(detail)

class IncorrectPassword(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)