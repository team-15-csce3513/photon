from typing import Dict, List
from tkinter import messagebox
import tkinter as tk
from tkinter import Button, Entry, Label, font, Frame
import tkinter.simpledialog as simpledialog

import pygubu

from network import Network
from user_info import User
from main import supabase_client

database_response = None

def on_tab(event: tk.Event, root: tk.Tk, entry_ids: Dict, users: Dict, builder: pygubu.Builder) -> None:
    #global response 
    global database_response

    # Retrieve the ID of the field where the event occurred.
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

    # Handle user ID input and database lookup.
    elif "user_id" in entry_field_id:
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "User ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        database_response = supabase_client.table("users").select("*").eq("id", event.widget.get()).execute()

        if database_response.data:
            equipment_id: int = int(builder.get_object(entry_field_id.replace("user_id", "equipment_id"), root).get())
            user_id: int = int(database_response.data[0]["id"])
            username: str = database_response.data[0]["username"]
            
            if user_id in [user.user_id for user in users["green"]] or user_id in [user.user_id for user in users["red"]]:
                messagebox.showerror("Error", "User ID has already been entered")
                event.widget.delete(0, tk.END)
                root.after_idle(lambda: event.widget.focus_set())
                return

            users["green" if "green" in entry_field_id else "red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, username))

            builder.get_object(entry_field_id.replace("user_id", "username"), root).insert(0, username)

            row: int = int(entry_field_id.split("_")[-1])
            if row != 15:
                next_entry_field = builder.get_object(entry_field_id.replace(f"user_id_{row}", f"equipment_id_{row + 1}"), root)
                root.after_idle(lambda: next_entry_field.focus_set())
        else:
            # User does not exist, prompt for new username entry
            messagebox.showinfo("Info", "Type new username")
            # Clear any previously typed username and set focus to the username field for user input
            username_entry_field = builder.get_object(entry_field_id.replace("user_id", "username"), root)
            username_entry_field.delete(0, tk.END)
            root.after_idle(lambda: username_entry_field.focus_set())

    # If the user tabs from the username entry field, insert the user into the database if they don't already exist
    elif "username" in entry_field_id and database_response.data == []:

        # TODO: If the user goes back and deletes the username or user ID, remove the user from the users dictionary

        # Get equipment ID and user ID, user ID entry box for refocusing
        equipment_id: int = int(builder.get_object(entry_field_id.replace("username", "equipment_id"), root).get())
        user_id_widget: tk.Entry = builder.get_object(entry_field_id.replace("username", "user_id"), root)
        user_id: int = int(user_id_widget.get())

        # Get username from entry field
        username = event.widget.get()

        # Throw error if username already exists in users dictionary or database
        if username in [user.username for user in users["green"]] or username in [user.username for user in users["red"]]:
            messagebox.showerror("Error", "Username has already been entered")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return
        
        if supabase_client.table("users").select("*").eq("username", username).execute().data:
            messagebox.showerror("Error", "Username already exists in database")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Add user to dictionary
        users["green" if "green" in entry_field_id else "red"].append(User(int(entry_field_id.split("_")[-1]), equipment_id, user_id, username))

        # Attempt to insert the user into the database, display an error message if the POST request fails
        try:
            supabase_client.table("users").insert({
                "id": user_id,
                "username": username
            }).execute()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            user_id_widget.delete(0, tk.END)
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: user_id_widget.focus_set())
            return



    #Clear
def on_f12(main_frame: tk.Tk, entry_ids: Dict, users: Dict, builder: pygubu.Builder) -> None:
    # Clear all inputs from user entry fields.
    for _, entry_field_id in entry_ids.items():
        entry_widget = builder.get_object(entry_field_id, main_frame)
        entry_widget.delete(0, tk.END)

    # Set the focus back to the first user input field.
    initial_focus_target = builder.get_object("green_equipment_id_1", main_frame)
    initial_focus_target.focus_set()

    # Reset user lists for both teams.
    for team_list in users.values():
        team_list.clear()
    #Start
def on_f5(main_frame: tk.Tk, window: tk.Tk, users: Dict, network: Network) -> None:
    # Check for minimum player requirement on each team.
    if all(len(team) >= 1 for team in users.values()):
        # Disable further input and action keys.
        for key in ["<Tab>", "<KeyPress-F12>", "<KeyPress-F5>"]:
            window.unbind(key)

        # Clear instructions before proceeding to action screen
        for instruction in ['instruction_0', 'instruction_1', 'instruction_2', 'instruction_3']:
            if hasattr(window, instruction):
                getattr(window, instruction).grid_forget()

        # Initiate game equipment setup.
        users_flat = [user for team in users.values() for user in team]
        for user in users_flat:
            network.transmit_equipment_code(user.equipment_id)

        # Transition to the game's play action screen.
        main_frame.destroy()
        import countdown
        countdown.build(window, users, network)
    else:
        # Alert if teams are not adequately populated.
        messagebox.showerror("Error", "There must be at least 1 user on each team")


def build(window: tk.Tk, users: Dict, network: Network) -> None:

    # Header
    # Create a frame to contain the label at the top of the window
    top_frame = tk.Frame(window, bg="black")
    top_frame.grid(row=0, column=8, sticky="ew")

    # Configure the window to expand the first column where the frame is placed
    window.grid_columnconfigure(0, weight=1)

    # Add "Team 15" label to the top frame using grid
    team_15_label = tk.Label(top_frame, text="Team-15 Laser Tag Game", font=("Arial", 24, "bold"), fg="white", bg="black")
    team_15_label.grid(row=0, column=0, sticky="nsew")

    # Configure the top frame to expand the label to fill the space
    top_frame.grid_columnconfigure(0, weight=1)

    #Footer
    # Create a frame to contain the label at the bottom of the window
    bottom_frame = tk.Frame(window, bg="black")
    bottom_frame.grid(row=2, column=0, sticky="ew")  # Assuming row=1 is used by the main content

    # Configure the bottom frame to expand the label to fill the space
    bottom_frame.grid_columnconfigure(0, weight=1)

    # Initialize the user interface from the predefined UI layout.
    builder = pygubu.Builder()
    builder.add_from_file("../assets/ui/player_entry.ui")

    # Position the main container centrally within the window.
    main_frame = builder.get_object("master", window)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Retrieve the designated areas for both teams.
    teams_frame = builder.get_object("teams", main_frame)
    team_frames = {
        "red": builder.get_object("red_team", teams_frame),
        "green": builder.get_object("green_team", teams_frame)
    }

    # Compile a list of widget IDs for quick access during event handling.
    entry_fields = ["equipment_id_", "user_id_", "username_"]
    entry_ids = {
        widget.winfo_id(): f"{team}_{field}{index}"
        for team, frame in team_frames.items()
        for field in entry_fields
        for index in range(1, 16)
        if (widget := builder.get_object(f"{team}_{field}{index}", frame))
    }

    # Set initial focus to the first input field for a smooth user experience.
    builder.get_object("green_equipment_id_1", team_frames["green"]).focus_set()

    # Define event bindings for efficient interaction.
    events = {
        "<Tab>": lambda event: on_tab(event, window, entry_ids, users, builder),
        "<KeyPress-F12>": lambda event: on_f12(main_frame, entry_ids, users, builder),
        "<KeyPress-F5>": lambda event: on_f5(main_frame, window, users, network)
    }
    for event, action in events.items():
        window.bind(event, action)

    # Configure the window to expand the column where the bottom frame is placed
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=1)
    window.grid_columnconfigure(4, weight=1)
    window.grid_columnconfigure(5, weight=1)
    window.grid_columnconfigure(6, weight=1)
    window.grid_columnconfigure(7, weight=1)
    window.grid_columnconfigure(8, weight=1)
    window.grid_columnconfigure(9, weight=1)
    window.grid_columnconfigure(10, weight=1)
    window.grid_columnconfigure(11, weight=1)
    window.grid_columnconfigure(12, weight=1)
    window.grid_columnconfigure(13, weight=1)
    window.grid_columnconfigure(14, weight=1)
    window.grid_columnconfigure(15, weight=1)
    window.grid_columnconfigure(16, weight=1)
    window.grid_columnconfigure(17, weight=1)
    window.grid_columnconfigure(18, weight=1)
    window.grid_columnconfigure(19, weight=1)
    window.grid_columnconfigure(20, weight=1)
    window.grid_columnconfigure(21, weight=1)
    window.grid_columnconfigure(22, weight=1)
    window.grid_rowconfigure(0, weight=1)  # Top area for "Team 15" label, minimal expansion
    window.grid_rowconfigure(1, weight=90)  # Main content area, maximum expansion
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(4, weight=1)
    window.grid_rowconfigure(5, weight=1)

    # Configure the submit and clear buttons with their respective actions.
    submit_button = builder.get_object("submit", main_frame)
    submit_button.configure(command=lambda: on_f5(main_frame, window, users, network))
    cont_button: tk.Button = builder.get_object("clear", main_frame)
    cont_button.configure(command=lambda: on_f12(main_frame, entry_ids, users, builder))

    # Add shutdown instruction label to the bottom frame using grid
    window.instruction_0 = tk.Label(bottom_frame, text="Click <esc> to shut down", font=("Arial", 12), fg="white", bg="black")
    window.instruction_0.grid(row=2, column=0, sticky="ew")

    # Create labels for each instruction within the instructions frame
    window.instruction_1 = tk.Label(bottom_frame, text="MUST <Tab> after input", font=("Arial", 12), fg="white", bg="black")
    window.instruction_1.grid(row=3, column=0, sticky="ew") # Pack to the west (left side) of the frame

    window.instruction_2 = tk.Label(bottom_frame, text="Equipment code MUST match players", font=("Arial", 12), fg="white", bg="black")
    window.instruction_2.grid(row=4, column=0, sticky="ew")  

    window.instruction_3 = tk.Label(bottom_frame, text="Will lookup after User ID", font=("Arial", 12), fg="white", bg="black")
    window.instruction_3.grid(row=5, column=0, sticky="ew")  

######################

