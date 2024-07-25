from minio import Minio
from typing import List
from fastapi import File
from core import MINIO_ACCESS_KEY,MINIO_PORT,MINIO_SECRET_KEY,MINIO_HOST
from io import BytesIO
class MinIO:
    def __init__(self,access_key:str,secret_key:str,secure:bool=False,endpoint:str='127.0.0.1',port:int=9000,buckets:List[str]=[]):
        self.client = Minio(
            endpoint=f'{endpoint}:{port}',
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        try:
            for bucket in buckets:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
        except Exception as e:
            print(e)
    def make_bucket(self,bucketName:str):
        if not self.client.bucket_exists(bucketName):
            self.client.make_bucket(bucketName)
        return True
    def getImage(self,imageName):
        image = self.client.stat_object('image',imageName)
        if image:
            return self.client.get_object('image',imageName)
        return False


    def uploadImage(self,file:File,Event:int):
        data = file.file.read()
        file_name = " ".join(file.filename.strip().split())
        self.client.put_object(
            'image',
            object_name=file_name,
            data=BytesIO(data),
            content_type=file.content_type,
            length=-1,
            part_size=10*1024*1024,
        )
        return True;

MinIOClient = MinIO(
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    endpoint=MINIO_HOST,
    port=MINIO_PORT,
    buckets=['image']
)