import os
import shutil
from typing import BinaryIO
from app.storage.base import StorageProvider

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_dir: str):
        self.storage_dir = os.path.join(base_dir, "storage")
        self.input_dir = os.path.join(self.storage_dir, "input")
        self.output_dir = os.path.join(self.storage_dir, "output")
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, file_obj: BinaryIO, filename: str, bucket: str = "input") -> str:
        target_dir = self.input_dir if bucket == "input" else self.output_dir
        path = os.path.join(target_dir, filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file_obj, buffer)
        return filename

    def get_path(self, file_id: str, extension: str, bucket: str = "input") -> str:
        target_dir = self.input_dir if bucket == "input" else self.output_dir
        return os.path.join(target_dir, f"{file_id}.{extension}")

    def exists(self, file_id: str, bucket: str = "output") -> bool:
        path = self.get_path(file_id, "pdf", bucket)
        return os.path.exists(path)

    def get_download_url(self, file_id: str, bucket: str = "output") -> str:
        # For local, we return a relative API path
        return f"/download/{file_id}"

    def delete(self, file_id: str, extension: str, bucket: str = "input"):
        path = self.get_path(file_id, extension, bucket)
        if os.path.exists(path):
            os.remove(path)
