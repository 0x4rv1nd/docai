import os
from typing import BinaryIO
from app.storage.base import StorageProvider
from supabase import create_client, Client

class SupabaseStorageProvider(StorageProvider):
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.client: Client = create_client(url, key)
        self.bucket_name = os.environ.get("SUPABASE_BUCKET", "pdfs")

    def save(self, file_obj: BinaryIO, filename: str, bucket: str = "input") -> str:
        path = f"{bucket}/{filename}"
        content = file_obj.read()
        self.client.storage.from_(self.bucket_name).upload(path, content)
        return filename

    def get_path(self, file_id: str, extension: str, bucket: str = "input") -> str:
        # For Supabase, path is just the key in the bucket
        return f"{bucket}/{file_id}.{extension}"

    def exists(self, file_id: str, bucket: str = "output") -> bool:
        path = f"{bucket}/{file_id}.pdf"
        try:
            res = self.client.storage.from_(self.bucket_name).list(bucket)
            return any(f['name'] == f"{file_id}.pdf" for f in res)
        except:
            return False

    def get_download_url(self, file_id: str, bucket: str = "output") -> str:
        path = f"{bucket}/{file_id}.pdf"
        res = self.client.storage.from_(self.bucket_name).create_signed_url(path, expires_in=3600)
        return res['signedURL']

    def delete(self, file_id: str, extension: str, bucket: str = "input"):
        path = f"{bucket}/{file_id}.{extension}"
        self.client.storage.from_(self.bucket_name).remove([path])
