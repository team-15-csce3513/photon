from typing import Dict
from PIL import Image, ImageTk
import cv2
import os
import tkinter as tk
import pygubu
from network import Network




def update_video(video_label: tk.Label, cap: cv2.VideoCapture, frame_rate: int, video_width: int, video_height: int):
    """
    Updates the displayed video frame on a tkinter label.
    
    Args:
        video_label: The tkinter label to display the video on.
        cap: The OpenCV video capture object.
        frame_rate: The frame rate of the video.
        video_width: The width to resize video frames to.
        video_height: The height to resize video frames to.
    """
    # Attempt to read the next frame from the video capture
    success, frame = cap.read()
    
    # If successful, process and display the frame
    if success:
        # Resize and convert the frame for display
        processed_frame = cv2.resize(frame, (video_width, video_height))
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        
        # Convert the processed frame to a format tkinter can use and update the label
        tk_image = ImageTk.PhotoImage(image=Image.fromarray(processed_frame))
        video_label.config(image=tk_image)
        
        # Store a reference to the image to prevent it from being garbage collected
        video_label.image = tk_image
        
        # Schedule the next frame update
        video_label.after(round(1000 / frame_rate), lambda: update_video(video_label, cap, frame_rate, video_width, video_height))
    else:
        # If the video has ended, restart from the beginning
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        update_video(video_label, cap, frame_rate, video_width, video_height)

def update_timer(timer_label: tk.Label, seconds: int, main_frame: tk.Frame, network: Network, users: Dict, root: tk.Tk):
    """
    Handles the countdown timer logic.

    Parameters:
        timer_label (tk.Label): Label displaying the countdown.
        seconds (int): Number of seconds remaining.
        main_frame (tk.Frame): The main application frame.
        network (Network): Network object for communication.
        users (Dict): Dictionary of user data.
        root (tk.Tk): Root window.

    This function updates the countdown displayed on `timer_label` every second.
    When the countdown reaches zero, it initiates the transition to the game.
    """
    # Countdown still active, decrement and schedule next update
    if seconds > 0:
        timer_label.configure(text=f"Game Starts In: {seconds} Seconds", fg='black')
        root.after(1000, lambda: update_timer(timer_label, seconds - 1, main_frame, network, users, root))
    else:
        # Countdown complete, proceed to game
        start_game(main_frame, network, users, root)

def start_game(main_frame: tk.Frame, network: Network, users: Dict, root: tk.Tk):
    """
    Initiates the game after countdown ends.

    Parameters:
        main_frame (tk.Frame): The main application frame.
        network (Network): Network object for communication.
        users (Dict): Dictionary of user data.
        root (tk.Tk): Root window.

    Destroys the countdown frame and starts the game, signaling all necessary actions.
    """
    # Signal game start
    main_frame.destroy()  # Remove the countdown UI
    network.transmit_start_game_code()  # Signal to network

    # Transition to the game screen
    try:
        import play_action
        play_action.build(network, users, root)  # Build and display the game UI
    except ImportError as error:
        print(f"Error importing play_action module: {error}")


def build(root: tk.Tk, users: Dict, network: Network):
    """
    Initializes the countdown screen with user names and a countdown timer.

    Args:
        root: The root Tkinter window.
        users: A dictionary containing user data.
        network: The Network instance for communication.
    """
    # Initialize the GUI builder and load the design
    ui_builder = pygubu.Builder()
    ui_builder.add_from_file("../assets/ui/countdown.ui")

    # Centralize the main frame on the screen
    countdown_main_frame = ui_builder.get_object("master", root)
    countdown_main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Populate the UI with usernames for each team member
    populate_usernames(users, ui_builder, countdown_main_frame)

    # Setup and display the countdown timer and video
    setup_countdown_and_video(countdown_main_frame, ui_builder, root, users, network)

def populate_usernames(users: Dict, ui_builder: pygubu.Builder, frame: tk.Frame):
    """
    Fills in the user names on the countdown screen.

    Args:
        users: User data.
        ui_builder: The GUI builder instance.
        frame: The frame to populate usernames in.
    """
    for team, team_users in users.items():
        for index, user in enumerate(team_users, start=1):
            username_label_id = f"{team}_username_{index}"
            username_label = ui_builder.get_object(username_label_id, frame)
            username_label.config(text=user.username)

def setup_countdown_and_video(frame: tk.Frame, ui_builder: pygubu.Builder, root: tk.Tk, users: Dict, network: Network):
    """
    Configures and starts the countdown timer and video display.

    Args:
        frame: The main frame for the countdown UI.
        ui_builder: The GUI builder instance.
        root: The root Tkinter window.
        users: User data.
        network: The Network instance.
    """
    # Retrieve UI elements for the countdown and video
    timer_label = ui_builder.get_object("countdown_label", frame)
    video_frame = ui_builder.get_object("video_frame", ui_builder.get_object("countdown_frame", frame))

    # Initialize the video display
    video_label = tk.Label(video_frame)
    video_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    video_capture = cv2.VideoCapture("../assets/videos/countdown.mp4")

    # Set video and countdown parameters
    frame_rate = int(video_capture.get(cv2.CAP_PROP_FPS))
    video_dimensions = (500, 500)  # width, height
    countdown_duration = 30  # seconds

    # Begin the countdown and video playback
    update_timer(timer_label, countdown_duration, frame, network, users, root)
    update_video(video_label, video_capture, frame_rate, *video_dimensions)
