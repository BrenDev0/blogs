class EmailTransportException(Exception):
    def __init__(self, detail: str = "Unable to send email at this time"):
        super().__init__(detail)