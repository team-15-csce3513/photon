import tkinter as tk
from splash import build as build_splash
from udpclient import udp_client
from udpserver import udp_server
import threading
import time

def main():
    root = tk.Tk()
    root.title("Main Application")

    # Build and display splash screen
    splash_screen = build_splash(root)
    root.update()

    # Simulate some processing time
    time.sleep(2)

    # Destroy the splash screen
    splash_screen.destroy()

    # Run UDP client and server in separate threads
    client_thread = threading.Thread(target=udp_client)
    server_thread = threading.Thread(target=udp_server)

    client_thread.start()
    server_thread.start()

    # Wait for both threads to finish
    client_thread.join()
    server_thread.join()

    root.mainloop()

if __name__ == "__main__":
    main()
