from supabase import create_client, Client
import os

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_table(table_name: str):
    response = supabase.table(table_name).select("*").execute()
    return response.data

if __name__ == "__main__":
    table = "test"
    rows = fetch_table(table)
    print(rows)
