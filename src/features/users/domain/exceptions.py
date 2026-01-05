class EmailInUseException(Exception):
    def __init__(self, detail: str = "Email in use"):
        super().__init__(detail)