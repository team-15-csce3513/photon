from typing import Dict, List
import tkinter as tk
from network import Network
from user_info import User
import splash
import entry
from supabase_config import initialize_supabase

# Initialize the Supabase client
supabase_client = initialize_supabase()

def setup_main_window() -> tk.Tk:
    """Establishes the primary window for the application."""
    window = tk.Tk()
    window.title("Photon: A Laser Tag System")
    window.configure(bg="black")
    
    # Expand the window to fill the screen
    full_screen_width, full_screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry(f"{full_screen_width}x{full_screen_height}+0+0")
    
    return window

def destroy_window(window: tk.Tk, networking: Network) -> None:
    """Shuts down network connections and exits the main window."""
    networking.close_sockets()
    window.destroy()

def main():
    """Initializes and executes the main app workflow."""
    user_data = {"green": [], "red": []}  # Stores user team allocations

    networking = Network()
    networking.set_sockets()  # Initialize networking

    window = setup_main_window()  # Create the app's main window
    
    # Define how the app responds to closure events
    window.bind("<Escape>", lambda evt: destroy_window(window, networking))
    window.protocol("WM_DELETE_WINDOW", lambda: destroy_window(window, networking))

    splash.build(window)  # Show initial splash screen

    # Move to user setup screen after initial display
    window.after(3000, lambda: entry.build(window, user_data, networking))

    # Begin the main event loop
    window.mainloop()  

if __name__ == "__main__":
    main()
