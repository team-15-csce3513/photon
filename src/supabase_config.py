import os
from dotenv import load_dotenv
import supabase

# Load environment variables from .env file
load_dotenv()

# Print loaded environment variables (for debugging)
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))

# Function to initialize Supabase client
def initialize_supabase():
    supabase_client = supabase.create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )

    # Print Supabase client details (for debugging)
    print("Supabase Client:", supabase_client)

    return supabase_client
