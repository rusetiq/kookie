import os

from supabase import Client, create_client

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://kteucjvbatzazvzzkags.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
if not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_SERVICE_KEY) must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
