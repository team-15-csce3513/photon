import tkinter as tk
from tkinter import Button
from tkinter import font


def create_player_entry_screen():
    # Create a new Tkinter window
    #window = tk.Tk()

    # Define a function to close the window
    #def close_window(event):
     #   window.destroy()

    # Set the window title
    #window.title("Player Entry Screen")

    # Set the window size
    #window.geometry("800x600")

    # Bind the Esc key to the close_window function
    #window.bind('<Escape>', close_window)

    # Text widget
    textFont = font.Font(family='Helvetica', size=25, weight='bold')
    Text1 = tk.Text(height=1, width=16, font = textFont)
    Text1.tag_configure('blue_text', foreground='blue')
    Text1.insert("1.0", "Edit Current Game")
    Text1.tag_add('blue_text', "1.0", "end")
    Text1.pack()

    # Buttons that will be on bottom of screen 
    B1 = Button(text = "Edit Game", fg='green', bg='black')
    B1.place(x=0, y=500)
    B1.config(height=5)
    B2 = Button(text = "Game Parameters", fg='green', bg='black')
    B2.place(x=95, y=500)
    B2.config(height=5)
    B3 = Button(text = "Start Game", fg='green', bg='black')
    B3.place(x=235, y=500)
    B3.config(height=5)
    B4 = Button(text = "PreEntered Games", fg='green', bg='black')
    B4.place(x=340, y=500)
    B4.config(height=5)
    #B5 = Button(text = "")
    #B5.place(x=475, y=550)
    B6 = Button(text = "View Game", fg='green', bg='black')
    B6.place(x=490, y=500)
    B6.config(height=5)
    B7 = Button(text = "Flick Sync", fg='green', bg='black')
    B7.place(x=600, y=500)
    B7.config(height=5)
    B8 = Button(text = "Clear Game", fg='green', bg='black')
    B8.place(x=700, y=500)
    B8.config(height=5)

    # Start the window's event loop
    #window.mainloop()

# Main program
if __name__ == "__main__":
    create_player_entry_screen()


