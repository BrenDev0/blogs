class ImageUploadException(Exception):
    def __init__(self, detail: str = "Error uploading image"):
        super().__init__(detail)

class UnsuportedContentType(Exception):
    def __init__(self, detail: str = "Usupported content type"):
        super().__init__(detail)