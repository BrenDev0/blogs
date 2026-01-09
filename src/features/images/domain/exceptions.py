class ImageUploadException(Exception):
    def __init__(self, detail: str = "Error uploading image"):
        super().__init__(detail)