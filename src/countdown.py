import tkinter as tk
from tkinter import Button, Entry, Label, font
import socket
from splash import build
import time
from PIL import Image, ImageTk

def create_countdown_screen(CDwindow):
    CDwindow.title("Countdown Screen")
    CDwindow.geometry("1250x800")

     # Load the background image
    bg_image = Image.open("../images/bg2.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a Label to hold the background image
    bg_label = tk.Label(CDwindow, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make the label cover the entire window
    
    # Desired size for the alert image
    alert_width = 400  # Adjust width as needed
    alert_height = 170  # Adjust height as needed

    # Load and resize the alert image
    alert_image = Image.open("../images/alert2.jpg")
    alert_resized = alert_image.resize((alert_width, alert_height), Image.Resampling.LANCZOS)
    alert_photo = ImageTk.PhotoImage(alert_resized)

    # Create a Label to hold the alert image without a visible border
    alert_label = tk.Label(CDwindow, image=alert_photo, borderwidth=0, relief='flat')
    alert_label.image = alert_photo  # Keep a reference to avoid garbage collection
    alert_label.place(x=500, y=20)

    # Desired size for countdown images
    desired_width = 430 # Adjust width as needed
    desired_height = 250  # Adjust height as needed

    # Preload countdown images and resize them
    countdown_images = {}
    for i in range(31):  # From 0 to 30
        img = Image.open(f"../images/{i}.png")
        # Resize the image using Image.Resampling.LANCZOS for high-quality downsampling
        img_resized = img.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        countdown_images[i] = photo
    
    countdown_value = 30  # Start countdown at 30

    # Create a Label for countdown images
    countdown_label = tk.Label(CDwindow, image=countdown_images[countdown_value], borderwidth=0, relief='flat')
    countdown_label.place(x=415, y=265)  # Adjust position as needed

    def update_countdown():
        nonlocal countdown_value
        countdown_value -= 1
        if countdown_value < 0:
            return  # Stop the countdown
        countdown_label.config(image=countdown_images[countdown_value])
        if countdown_value == 0:
        # Schedule the window to be destroyed 1 second after the last countdown image appears
            CDwindow.after(1000, CDwindow.destroy)
        else:
            CDwindow.after(1000, update_countdown)  # Update countdown every second


    def toggle_alert_visibility():
        if alert_label.winfo_ismapped():
            alert_label.place_forget()  # Hide the alert image
        else:
            alert_label.place(x=430, y=40)  # Show the alert image, adjust position as needed
        CDwindow.after(500, toggle_alert_visibility)  # Toggle visibility every 1000ms (1 second)
    
    toggle_alert_visibility() 
    update_countdown() # start the countdown 

    CDwindow.mainloop()



if __name__ == "__main__":
    create_countdown_screen()
  
