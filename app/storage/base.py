from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageProvider(ABC):
    @abstractmethod
    def save(self, file_obj: BinaryIO, filename: str, bucket: str = "input") -> str:
        """Save a file and return the identifier."""
        pass

    @abstractmethod
    def get_path(self, file_id: str, extension: str, bucket: str = "input") -> str:
        """Get the local path or identifier for a file."""
        pass

    @abstractmethod
    def exists(self, file_id: str, bucket: str = "output") -> bool:
        """Check if a file exists."""
        pass

    @abstractmethod
    def get_download_url(self, file_id: str, bucket: str = "output") -> str:
        """Get a downloadable URL for the file."""
        pass

    @abstractmethod
    def delete(self, file_id: str, extension: str, bucket: str = "input"):
        """Delete a file."""
        pass
