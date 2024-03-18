from PIL import Image, ImageTk
import tkinter as tk

# After 3 seconds, destroy the splash screen
def build(window: tk.Tk, duration_ms: int = 3000) -> tk.Label:
    splash_pil_image = Image.open("../assets/images/splash.jpg")
    splash_image = ImageTk.PhotoImage(splash_pil_image)

    # Build the splash screen
    splash_screen = tk.Label(window, image=splash_image, bg='black')
    splash_screen.place(x=0, y=0, relwidth=1, relheight=1)
    splash_screen.image = splash_image
