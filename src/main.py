import tkinter as tk
from splash import build as build_splash
from entry import create_player_entry_screen
import threading
import time
from supabase_config import initialize_supabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print loaded environment variables (for debugging)
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))

# Create Supabase client
supabase_client = initialize_supabase()

def main():
    window = tk.Tk()
    window.title("Splash Screen")
    window.geometry("800x600")

    # Build and display splash screen
    splash_screen = build_splash(window)
    window.update()
    time.sleep(2)

    splash_screen.destroy()


    # window.bind("Enter", splash_screen)
    
    window.destroy()
    # Simulate some processing time

    # Destroy the splash screen

    # Call the player entry screen


    # Call the player entry screen
    create_player_entry_screen(supabase_client)


    # Run UDP client and server in separate threads
    # client_thread = threading.Thread(target=udp_client)
    # server_thread = threading.Thread(target=udp_server)

    # client_thread.start()
    # server_thread.start()

    # Wait for both threads to finish
    # client_thread.join()
    # server_thread.join()

    window.mainloop()

if __name__ == "__main__":
    main()
