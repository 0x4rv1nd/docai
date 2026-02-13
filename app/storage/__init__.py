import os
from app.storage.local import LocalStorageProvider
from app.storage.supabase import SupabaseStorageProvider

def get_storage():
    provider_type = os.environ.get("STORAGE_PROVIDER", "local").lower()
    
    if provider_type == "supabase":
        return SupabaseStorageProvider()
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return LocalStorageProvider(base_dir)

storage = get_storage()
