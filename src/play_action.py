from typing import Dict
import pygubu # type: ignore
import tkinter as tk
import os 
import time
import random
import threading
import pygame   # type: ignore
from network import Network
from game_logic import GameState
from main import destroy_window
import entry


def build_new_game(window: tk.Tk, users: Dict, network: Network) -> None:
    # Remove buttons from window
    for widget in window.winfo_children():
        widget.destroy()

    # Send back to player entry screen
    entry.build(window, users, network)

def destroy_current_game(window: tk.Tk, main_frame: tk.Frame, users: dict, network: Network, game: GameState) -> None:
    # Destroy the main frame
    main_frame.destroy()

    # Create label for displaying winning team
    winner: str
    if game.green_team_score > game.red_team_score:
        winner = "Green Team Wins!"
    elif game.red_team_score > game.green_team_score:
        winner = "Red Team Wins!"
    else:
        winner = "Tie Game!"
    winner_label: tk.Label = tk.Label(window, text=winner, font=("Fixedsys", 20), bg="#FFFFFF", fg="black")
    winner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Clear the user dictionary
    users["red"].clear()
    users["green"].clear()

    # Destroy game object
    del game

    # Place restart game and end game buttons
    restart_game_button: tk.Button = tk.Button(window, text="Restart Game", font=("Fixedsys", 16), bg="#FFFFFF", fg="black", command=lambda: build_new_game(window, users, network))
    restart_game_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    end_game_button: tk.Button = tk.Button(window, text="End Game", font=("Fixedsys", 16), bg="#FFFFFF", fg="black", command=lambda: destroy_window(window, network))
    end_game_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def update_stream(game: GameState, action_stream: tk.Frame) -> None:
    base_text = ("*B* ", ("Roboto", 16, "bold"), "#FFFFFF", "black")
    # Add scroll effect to action stream with game.game_event_list queue
    if len(game.game_event_list) > 0:
        # Get the last event from the queue along with player name
        event: str = game.game_event_list.pop()
        player_name: str = event.split("hit", 1)[0].strip()

        # Create label for event and add to action stream
        event_label: tk.Label = tk.Label(action_stream, text=event, font=("Fixedsys", 16), bg="#FFFFFF", fg="black")
        event_label.pack(side=tk.TOP, fill=tk.X)
        
        # Add B to player name if they hit a base
        if "hit green base" in event:
            for user in game.red_users:
                if user.username == player_name and "*B*" not in user.username:
                    user.username = f"{base_text[0]} {user.username}"
        elif "hit red base" in event:
            for user in game.green_users:
                if user.username == player_name and "*B*" not in user.username:
                    user.username = f"{base_text[0]} {user.username}"
        
        # Remove the last event from the bottom of the action stream
        if len(action_stream.winfo_children()) > 10:
            action_stream.winfo_children()[0].destroy()

    # Recursively call this function after 1 second to incrementally update action stream
    action_stream.after(1000, update_stream, game, action_stream)

def update_score(game: GameState, main_frame: tk.Frame, builder: pygubu.Builder) -> None:
    # Update scores for green team
    for user in game.green_users:
        builder.get_object(f"green_username_{user.row}", main_frame).config(text=user.username)
        builder.get_object(f"green_score_{user.row}", main_frame).config(text=user.game_score)
    builder.get_object("green_total_score", main_frame).config(text=game.green_team_score)

    # Update scores for red team
    for user in game.red_users:
        builder.get_object(f"red_username_{user.row}", main_frame).config(text=user.username)
        builder.get_object(f"red_score_{user.row}", main_frame).config(text=user.game_score)
    builder.get_object("red_total_score", main_frame).config(text=game.red_team_score)

    # Recursively call this function after 1 second to incrementally update scores
    main_frame.after(1000, update_score, game, main_frame, builder)

# Implementing play countdown timer for 6-minutes 
def update_timer(timer_label: tk.Label, seconds: int, window: tk.Tk, main_frame: tk.Frame, users: Dict, network: Network, game: GameState) -> None:
    # Update text being displayed in timer label
    mins, secs = divmod(seconds, 60)
    timer_label.config(text=f"Time Remaining: {mins:01d}:{secs:02d}", fg="black")
    timer_label.config(fg="green")

    if seconds <= 15:
            timer_label.config(fg="red")
            window.update()
            time.sleep(0.5)  # Adjust blinking speed as needed
            timer_label.config(fg="white")
            window.update()
            time.sleep(0.5)
            
    # Continue counting down, destroy main frame when timer reaches 0
    if seconds > 0:
        seconds -= 1
        timer_label.after(1000, update_timer, timer_label, seconds, window, main_frame, users, network, game)

    else:
        destroy_current_game(window, main_frame, users, network, game)
        pygame.mixer.music.stop()


def build(network: Network, users: Dict, window: tk.Tk) -> None:
    # Load the UI file and create the builder
    builder: pygubu.Builder = pygubu.Builder()
    builder.add_from_file("../assets/ui/play_action.ui")

     # Place the main frame in the center of the window window
    main_frame: tk.Frame = builder.get_object("master", window)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    timer_label: tk.Label = builder.get_object("countdown_label", main_frame)

    # Get action frame and prevent from resizing to fit label contents
    action_stream: tk.Frame = builder.get_object("action_stream_frame", main_frame)
    action_stream.pack_propagate(False)

    # Create game state model
    game: GameState = GameState(users)

    # Update score labels, timer, and action stream
    update_score(game, main_frame, builder)
    update_stream(game, action_stream)
    update_timer(timer_label, 360 , window, main_frame, users, network, game)

    # Start thread for UDP listening
    game_thread: threading.Thread = threading.Thread(target=network.run_game, args=(game,), daemon=True)
    game_thread.start()

    
