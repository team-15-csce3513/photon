import tkinter as tk
from tkinter import Button, Entry, Label, font
import socket
from splash import build
import time

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

def on_start_game():
    # window.iconify()
    equipment_window.iconify()  # Weird prerequisite to make countdown work...
    countdown_duration = 30  # Countdown duration in seconds

    for seconds_remaining in range(countdown_duration, 0, -1):
        countdown_label.config(text=f"Game starts in {seconds_remaining} seconds")
        window.update()
        time.sleep(1)

    countdown_label.config(text="Game started!")
    window.update()
    time.sleep(1)

    for entry in red_entries:
        equipment_id = entry.get()
        transmit_equipment_code(equipment_id, 'red')

    label_red = tk.Label(equipment_window, text="Equipment codes transmitted for red team.", font=("Helvetica", 12), bg='red', fg='white')
    label_red.grid(row=0, column=0)

    for entry in green_entries:
        equipment_id = entry.get()
        transmit_equipment_code(equipment_id, 'green')

    label_green = tk.Label(equipment_window, text="Equipment codes transmitted for green team.", font=("Helvetica", 12), bg='green', fg='white')
    label_green.grid(row=1, column=0)

def on_click_splash():
    splash_screen = build(window)
    window.update()
    time.sleep(1)
    splash_screen.destroy()
    if splash_screen.destroy():
        create_player_entry_screen()

def clear_screen():
    for entry in red_entries:
        entry.delete(0, tk.END)
    for entry in green_entries:
        entry.delete(0, tk.END)

def create_player_entry_screen(supabase_client=None):
    global window, equipment_window, countdown_label

    # Create the main window
    window = tk.Tk()
    window.title("Player Entry Screen")
    window.geometry("1250x800")
    window.configure(bg='#212121')  # Dark background color

    # Create and configure the header label
    header_font = font.Font(family='Helvetica', size=50, weight='bold')  # Adjusted font size
    header_label = Label(window, text="Team-15 Laser Tag Game", font=header_font, fg='#ffffff', bg='#212121')  # White text on dark background
    header_label.grid(row=0, column=0, columnspan=6, pady=(20, 10), sticky="ew")

    label_font = font.Font(family='Helvetica', size=14)  # Adjusted font size
    Notes_label = Label(window, text="Click Escape to end the game", font=label_font, fg='#ffffff', bg='#212121')  # White text on dark background
    Notes_label.grid(row=30, column=0, columnspan=3, pady=(20, 10), sticky="ew")

    # Labels for column headers
    labels = ['Equipment ID', 'User ID', 'Username']
    for i, label_text in enumerate(labels):
        # Red team column headers
        red_label = Label(window, text=label_text, font=("Helvetica", 16), bg='#b71c1c', fg='#ffffff')  # Dark red background with white text
        red_label.grid(row=1, column=i + 1, padx=5, pady=5)

        # Green team column headers
        green_label = Label(window, text=label_text, font=("Helvetica", 16), bg='#2e7d32', fg='#ffffff')  # Dark green background with white text
        green_label.grid(row=1, column=i + 4, padx=5, pady=5)

    # Entry fields for red team
    for i in range(15):
        for j in range(3):
            entry = Entry(window, bg='#ffccbc')  # Light orange background
            # Populate default equipment IDs
            if j == 0 and i < 2:
                entry.insert(tk.END, f"Equipment ID {1000}")  # Insert default equipment ID
            entry.grid(row=i + 2, column=j + 1, padx=5, pady=5)
            red_entries.append(entry)

    # Entry fields for green team
    for i in range(15):
        for j in range(3):
            entry = Entry(window, bg='#c8e6c9')  # Light green background
            # Populate default equipment IDs
            if j == 0 and i < 2:
                entry.insert(tk.END, f"Equipment ID {i + 1}")  # Insert default equipment ID
            entry.grid(row=i + 2, column=j + 4, padx=5, pady=5)
            green_entries.append(entry)

    # Countdown label
    countdown_label = Label(window, text="", font=("Helvetica", 16), bg='#212121', fg='#ffffff')  # Dark background with white text
    countdown_label.grid(row=18, column=1, columnspan=5, padx=5, pady=5)

    def end_program(event=None):
        window.destroy()

    window.bind("<Escape>", end_program)

    # Buttons at the end
    B3 = Button(window, text="Click to Start Game", fg='green', bg='white', command=on_start_game)
    B3.grid(row=20, column=1, padx=5, pady=5)

    B5 = Button(window, text="View Game", fg='green', bg='white', command=on_click_splash)
    B5.grid(row=20, column=3, padx=5, pady=5)

    B6 = Button(window, text="Clear Game", fg='green', bg='white', command=clear_screen)
    B6.grid(row=20, column=5, padx=5, pady=5)

    equipment_window = tk.Toplevel()
    equipment_window.configure(bg='black')
    equipment_window.geometry("800x600")

    window.mainloop()

# Main program
if __name__ == "__main__":
    create_player_entry_screen()
