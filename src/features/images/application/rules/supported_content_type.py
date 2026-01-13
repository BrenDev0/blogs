from src.features.images.domain.exceptions import UnsuportedContentType

class SupportedContenType:
    def __init__(self):
        self.allowed_types = [
            "image/png",
            "image/jpeg",
            "image/jpg"
        ]

    def validate(
        self,
        content_type: str,
        filename: str
    ):
        if content_type not in self.allowed_types:
            raise UnsuportedContentType(f"Content type of: {content_type} in file: {filename} not supported. Supported content types {", ".join(self.allowed_types)}")
        
        return True