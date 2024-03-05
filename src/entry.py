import tkinter as tk
from typing import Dict, List
from tkinter import Button, Entry, Label, font, messagebox
import socket
from splash import build
from supabase_config import initialize_supabase
import time

class User:
    def __init__(self, row: int, equipment_id: int, user_id:int, username: str) -> None:
        self.row = row
        self.equipment_id = equipment_id
        self.user_id = user_id
        self.username = username
    
    def __str__(self) -> str:
        return f"Username: {self.username}\nEquipment ID: {self.equipment_id}\nUser ID: {self.user_id}\n\n"

red_entries = []
green_entries = []
red_name_entries = []
green_name_entries = []

def on_tab(event: tk.Event, root: tk.Tk, entry_ids: Dict, users: Dict) -> None:
    global database_response
    
    entry_field_id: str = entry_ids.get(event.widget.winfo_id())
    if entry_field_id is None:
        return
    
    if "equipment_id" in entry_field_id:
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "Equipment ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return
        
        equipment_id: int = int(event.widget.get())

        if equipment_id < 0 or equipment_id > 100:
            messagebox.showerror("Error", "Equipment ID must be between 0 and 100")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        if equipment_id in [user.equipment_id for user in users["green"]] or equipment_id in [user.equipment_id for user in users["red"]]:
            messagebox.showerror("Error", "Equipment ID has already been entered")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

    elif "user_id" in entry_field_id:
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "User ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        database_response = initialize_supabase.table("users").select("*").eq("id", event.widget.get()).execute()

        if database_response.data:
            equipment_id: int = int(event.widget.get())  # Change this part if needed
            user_id: int = int(database_response.data[0]["id"])
            username: str = database_response.data[0]["username"]
            
            if user_id in [user.user_id for user in users["green"]] or user_id in [user.user_id for user in users["red"]]:
                messagebox.showerror("Error", "User ID has already been entered")
                event.widget.delete(0, tk.END)
                root.after_idle(lambda: event.widget.focus_set())
                return

            users["green" if "green" in entry_field_id else "red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, username))

            next_entry_field = root.nametowidget(entry_ids[event.widget.winfo_id() + 1])
            root.after_idle(lambda: next_entry_field.focus_set())

    elif "username" in entry_field_id and database_response.data == []:

        equipment_id: int = int(event.widget.get())  # Change this part if needed
        user_id_widget: tk.Entry = event.widget  # Change this part if needed
        user_id: int = int(user_id_widget.get())

        username = event.widget.get()

        if username in [user.username for user in users["green"]] or username in [user.username for user in users["red"]]:
            messagebox.showerror("Error", "Username has already been entered")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return
        
        if initialize_supabase.table("users").select("*").eq("username", username).execute().data:
            messagebox.showerror("Error", "Username already exists in database")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        users["green" if "green" in entry_field_id else "red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, username))

        try:
            initialize_supabase.table("users").insert({
                "id": user_id,
                "username": username
            }).execute()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            user_id_widget.delete(0, tk.END)
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: user_id_widget.focus_set())
            return

def transmit_equipment_code(equipment_id, team_color):
    BROADCAST_ADDRESS = "127.0.0.1"
    TRANSMIT_PORT = 20001
    transmit_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"{equipment_id},{team_color}"  # Combine equipment ID and team color
    transmit_socket.sendto(message.encode(), (BROADCAST_ADDRESS, TRANSMIT_PORT))
    transmit_socket.close()

def create_player_entry_screen():

    window = tk.Tk()
    window.title("Player Entry Screen")
    window.geometry("1250x800")

    player_data = []

    header_font = font.Font(family='Helvetica', size=100, weight='bold')
    header_label = Label(window, text="Team-15 Laser Tag Game", font=header_font, fg='white')
    header_label.grid(row=0, column=0, columnspan=6, pady=(20, 10), sticky="ew")
    header_label.config(font=("Helvetica", 50, "bold"))
    
    label_font = font.Font(family='Helvetica', size=10)
    Notes_label = Label(window, text="Click Escape to end the game", font=label_font, fg='white', bg='black')
    Notes_label.grid(row=30, column=0, columnspan=3, pady=(20, 10), sticky="ew")
    Notes_label.config(font=("Helvetica", 15, "bold"))

    labels = ['Equipment ID', 'User ID', 'Username']
    for i, label_text in enumerate(labels):
        red_label = Label(window, text=label_text, font=("Helvetica", 12), bg='red', fg='white')
        red_label.grid(row=1, column=i+1, padx=5, pady=5)

        green_label = Label(window, text=label_text, font=("Helvetica", 12), bg='green', fg='white')
        green_label.grid(row=1, column=i+4, padx=5, pady=5)

    equipment_window = tk.Toplevel()
    equipment_window.geometry("800x600")
    
    # Player Entry Fields for Red Team
    for row in range(2, 17):
        for col in range(3):
            entry = Entry(window)
            entry.grid(row=row, column=col+1, padx=5, pady=5)
            if col == 0:
                red_entries.append(entry)
            elif col == 2:
                red_name_entries.append(entry)

    # Player Entry Fields for Green Team
    for row in range(2, 17):
        for col in range(3):
            entry = Entry(window)
            entry.grid(row=row, column=col+4, padx=5, pady=5)
            if col == 0:
                green_entries.append(entry)
            elif col == 2:
                green_name_entries.append(entry)

    def on_start_game():
        # Iterate over red team entry fields
        for entry in red_entries:
            equipment_id = entry.get()
            user_id = entry.get()
            player_name = red_name_entries[red_entries.index(entry)].get()
            player_data.append((equipment_id, player_name, user_id))

            transmit_equipment_code(equipment_id, 'red')

        # Iterate over green team entry fields
        for entry in green_entries:
            equipment_id = entry.get()
            user_id = entry.get()
            player_name = green_name_entries[green_entries.index(entry)].get()
            player_data.append((equipment_id, player_name, user_id))

            transmit_equipment_code(equipment_id, 'green')

        # Label for green team transmission
        label_green = tk.Label(equipment_window, text="Equipment codes transmitted for green team.", font=("Helvetica", 12), bg='green', fg='white')
        label_green.grid(row=0, column=2, padx=5, pady=5)

        label_red = tk.Label(equipment_window, text="Equipment codes transmitted for red team.", font=("Helvetica", 12), bg='red', fg='white')
        label_red.grid(row=0, column=1, padx=5, pady=5)
        # Display collected player data
        if player_data:
            print("Player Data:")
            for data in player_data:
                if data[0] and data[1] and data[2]:
                    print(f"Equipment ID: {data[0]}, Player Name: {data[1]}, User ID:{data[2]}")


    def onButtonPress(event):
        window.destroy()
        
    window.bind("<Escape>", onButtonPress)
        
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
        for entry in red_name_entries:
            entry.delete(0, tk.END)
        for entry in green_name_entries:
            entry.delete(0, tk.END)
        
    B1 = Button(window, text="Edit Game", fg='green', bg='white')
    B1.grid(row=17, column=1, padx=5, pady=5)

    B2 = Button(window, text="Game Parameters", fg='green', bg='white')
    B2.grid(row=17, column=2, padx=5, pady=5)

    B3 = Button(window, text="Click to Start Game", fg='green', bg='white', command=on_start_game)
    B3.grid(row=17, column=3, padx=5, pady=5)

    B4 = Button(window, text="PreEntered Games", fg='green', bg='white')
    B4.grid(row=17, column=4, padx=5, pady=5)

    B5 = Button(window, text="View Game", fg='green', bg='white', command=on_click_splash)
    B5.grid(row=17, column=5, padx=5, pady=5)

    B6 = Button(window, text="Clear Game", fg='green', bg='white', command=clear_screen)
    B6.grid(row=17, column=6, padx=5, pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_player_entry_screen()
