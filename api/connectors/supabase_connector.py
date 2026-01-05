from supabase import create_client, Client


class SupabaseConnector:
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)

    def upsert_status(self, job: str, status: str):
        self.client.table("job_status").upsert(
            {"job": job, "status": status}
        ).execute()
import os
from typing import Optional

from supabase import Client, create_client


def get_supabase_client(url: Optional[str] = None, key: Optional[str] = None) -> Client:
    """Initialize a Supabase client from environment variables or overrides."""
    supabase_url = url or os.getenv("SUPABASE_URL")
    supabase_key = key or os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY is not configured")

    return create_client(supabase_url, supabase_key)
