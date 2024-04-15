from typing import Dict, List
import tkinter as tk
from network import Network
from user_info import User
import splash
import entry
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import warnings
warnings.filterwarnings("ignore", message="Your system is avx2 capable but pygame was not built with support for it", category=RuntimeWarning)
import pygame # type: ignore
import logging
import random
from supabase_config import initialize_supabase

# Initialize the Supabase client
supabase_client = initialize_supabase()

# initialize pygame
pygame.init()

music_tracks = ["../assets/sounds/Photon 1.mp3", "../assets/sounds/Photon 2.mp3", "../assets/sounds/Photon 3.mp3", "../assets/sounds/Photon 4.mp3", "../assets/sounds/Photon 5.mp3", "../assets/sounds/Photon 6.mp3", "../assets/sounds/Photon 7.mp3", "../assets/sounds/Photon 8.mp3"]

selected_track = random.choice(music_tracks)

pygame.mixer.music.load(selected_track)

pygame.mixer.music.play(-1)


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
    # Displaying which track is being played
    print(f"Now Playing {selected_track}")
    
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

