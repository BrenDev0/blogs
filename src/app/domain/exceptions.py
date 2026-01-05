class GraphQlException(Exception):
    def __init__(self, detail: str = "Unable to process request at this time"):
        self.detail = detail
        super().__init__(detail)

   