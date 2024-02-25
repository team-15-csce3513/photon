import tkinter as tk
from tkinter import Button, Entry, Label, font
import socket

red_entries = []
green_entries = []

def transmit_equipment_code(equipment_id, team_color):
    BROADCAST_ADDRESS = "127.0.0.1"
    TRANSMIT_PORT = 20001
    transmit_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"{equipment_id},{team_color}"  # Combine equipment ID and team color
    transmit_socket.sendto(message.encode(), (BROADCAST_ADDRESS, TRANSMIT_PORT))
    transmit_socket.close()

def create_player_entry_screen(supabase_client):
    # Create the main window
    window = tk.Tk()
    window.title("Player Entry Screen")
    window.geometry("1250x800")

    # Create and configure the header label
    header_font = font.Font(family='Helvetica', size=100, weight='bold')
    header_label = Label(window, text="Team-15 Laser Tag Game", font=header_font, fg='white')
    header_label.grid(row=0, column=0, columnspan=6, pady=(20, 10), sticky="ew")
    header_label.config(font=("Helvetica", 50, "bold"))

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
            # Populate default equipment IDs
            if j == 0 and i < 2:
                entry.insert(tk.END, f"Equipment ID {i+1}")  # Insert default equipment ID
            entry.grid(row=i+2, column=j+1, padx=5, pady=5)

    # Entry fields for green team
    for i in range(15):
        for j in range(3):
            entry = Entry(window, bg='green')
            # Populate default equipment IDs
            if j == 0 and i < 2:
                entry.insert(tk.END, f"Equipment ID {i+1}")  # Insert default equipment ID
            entry.grid(row=i+2, column=j+4, padx=5, pady=5)

    # Buttons that will be on the bottom of the screen
    def on_start_game():
        # transmit equipment codes when Start Game button is clicked
        for entry in red_entries:
            equipment_id = entry.get()
            transmit_equipment_code(equipment_id, 'red')
        print("Equipment codes transmitted for red team.")

        for entry in green_entries: 
            equipment_id = entry.get()
            transmit_equipment_code(equipment_id, 'green')
        print("Equipment codes transmitted for green team.")


    
    def onButtonPress():
        window.destroy()
 
    B1 = Button(window, text="Edit Game", fg='green', bg='white')
    B1.grid(row=17, column=1, padx=5, pady=5)  # Adjust row and column as needed

    B2 = Button(window, text="Game Parameters", fg='green', bg='white')
    B2.grid(row=17, column=2, padx=5, pady=5)  # Adjust row and column as needed

    B3 = Button(window, text="Click to Start Game", fg='green', bg='white', command=on_start_game)
    B3.grid(row=17, column=3, padx=5, pady=5)  # Adjust row and column as needed

    B4 = Button(window, text="PreEntered Games", fg='green', bg='white')
    B4.grid(row=17, column=4, padx=5, pady=5)  # Adjust row and column as needed

    B5 = Button(window, text="View Game", fg='green', bg='white')
    B5.grid(row=17, column=5, padx=5, pady=5)  # Adjust row and column as needed

    B6 = Button(window, text="Click to Clear Game", fg='green', bg='white', command= onButtonPress)
    B6.grid(row=17, column=6, padx=5, pady=5)  # Adjust row and column as needed
    window.mainloop()
        


# Main program
if __name__ == "__main__":
    create_player_entry_screen()
