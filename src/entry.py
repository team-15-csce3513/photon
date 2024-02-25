import tkinter as tk
from tkinter import Button, Entry, Label, font

def create_player_entry_screen():
    # Create the main window
    window = tk.Tk()
    window.title("Player Entry Screen")
    window.geometry("1250x800")

    # Create and configure the header label
    header_font = font.Font(family='Helvetica', size=100, weight='bold')
    header_label = Label(window, text="Laser Tag Game", font=header_font, fg='white')
    header_label.grid(row=0, column=0, columnspan=6, pady=(20, 10), sticky="ew")  # Adjust columnspan and pady as needed
    header_label.config(font=("Helvetica", 50, "bold"))  # Adjust the font size for bigger text

    # Labels for column headers
    labels = ['Equipment ID', 'User ID', 'Username']
    for i, label_text in enumerate(labels):
        # Red team column headers
        red_label = Label(window, text=label_text, font=("Helvetica", 12), bg='red', fg='white')
        red_label.grid(row=1, column=i+1, padx=5, pady=5)

        # Green team column headers
        green_label = Label(window, text=label_text, font=("Helvetica", 12), bg='green', fg='white')
        green_label.grid(row=1, column=i+4, padx=5, pady=5)

    # Entry fields for red team
    for i in range(15):
        for j in range(3):
            entry = Entry(window, bg='red')
            entry.grid(row=i+2, column=j+1, padx=5, pady=5)

    # Entry fields for green team
    for i in range(15):
        for j in range(3):
            entry = Entry(window, bg='green')
            entry.grid(row=i+2, column=j+4, padx=5, pady=5)

    # Buttons that will be on the bottom of the screen
    B1 = Button(window, text="Edit Game", fg='green', bg='yellow')
    B1.grid(row=17, column=1, padx=5, pady=5)  # Adjust row and column as needed

    B2 = Button(window, text="Game Parameters", fg='green', bg='yellow')
    B2.grid(row=17, column=2, padx=5, pady=5)  # Adjust row and column as needed

    B3 = Button(window, text="Start Game", fg='green', bg='yellow')
    B3.grid(row=17, column=3, padx=5, pady=5)  # Adjust row and column as needed

    B4 = Button(window, text="PreEntered Games", fg='green', bg='yellow')
    B4.grid(row=17, column=4, padx=5, pady=5)  # Adjust row and column as needed

    B5 = Button(window, text="View Game", fg='green', bg='yellow')
    B5.grid(row=17, column=5, padx=5, pady=5)  # Adjust row and column as needed

    B6 = Button(window, text="Clear Game", fg='green', bg='yellow')
    B6.grid(row=17, column=6, padx=5, pady=5)  # Adjust row and column as needed

    window.mainloop()

# Main program
if __name__ == "__main__":
    create_player_entry_screen()
