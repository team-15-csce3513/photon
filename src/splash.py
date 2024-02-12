from PIL import Image, ImageTk
import tkinter as tk

# Build the splash screen, destroy after 3 seconds
def build(root: tk.Tk) -> tk.Label:
    # Load the splash screen image
    splash_pil_image = Image.open("images/splash.jpg")
    splash_image = ImageTk.PhotoImage(splash_pil_image)

    # Build the splash screen
    splash_screen = tk.Label(root, image=splash_image)
    splash_screen.place(x=0, y=0, relwidth=1, relheight=1)
    splash_screen.image = splash_image

    # Make background black
    splash_screen.configure(background="black")
    
    # Build the splash screen
    splash: splash_screen = splash_screen.build(root)

    # After 3 seconds, destroy the splash screen and build the player entry screen
    # Play action screen will be built after F5 is pressed on player entry screen (see on_f5 function in src/player_entry.py)
    root.after(3000, splash.destroy)
    root.after(3000, player_entry.build, root, users, network)


if __name__ == "__main__":
    main()
    return splash_screen
