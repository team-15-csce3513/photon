import os
from dotenv import load_dotenv
import supabase


# Load environment variables from .env file
load_dotenv()

# Function to initialize Supabase client
def initialize_supabase():
    supabase_client: supabase.Client = supabase.create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY"))
    return supabase_client
