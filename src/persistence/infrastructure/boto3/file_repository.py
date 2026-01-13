import boto3
import io
from src.persistence.domain.file_repository import FileRepository

class Boto3FileRepository(FileRepository):
    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str
    ):
        self.__client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.__bucket_name = bucket_name


    def upload(self, key, file_bytes, content_type: str) -> str:
        file_obj = io.BytesIO(file_bytes)

        extra_args = {
            "ContentType": content_type
        }
        
        self.__client.upload_fileobj(file_obj, self.__bucket_name, key, ExtraArgs=extra_args)
        
        
        file_url = f"https://{self.__bucket_name}.s3.amazonaws.com/{key}"

        return file_url
    
    def delete(self, key): 
        self.__client.delete_object(Bucket=self.__bucket_name, Key=key)
        