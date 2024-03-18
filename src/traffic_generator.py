import socket
import random
import time
from typing import Tuple

# Constants for network communication
BUFFER_SIZE = 1024
SERVER_ADDRESS_PORT = ("127.0.0.1", 7501)
CLIENT_ADDRESS_PORT = ("127.0.0.1", 7500)
START_CODE = "202"
END_CODE = "221"

# Retrieve player ID based on color and number
def get_player_id(color: str, player_number: int) -> str:
    prompt = f"Enter equipment id of {color} player {player_number} ==> "
    return input(prompt)

# Await the start signal from the game's software
def wait_for_start(sock: socket.socket):
    print("\nAwaiting game start signal")
    data_received = ""
    while data_received != START_CODE:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        data_received = data.decode("utf-8")
        print(f"Data received: {data_received}")

def main():
    # Initial setup and player ID collection
    print("Generate test traffic for a two-team game. Each team has 2 players.\n"
          "Wait for a start signal from the game software to begin.\n"
          "To send a hit message between two players, follow the prompts.\n"
          "To exit, type 'y' when asked.")

    green1 = get_player_id("green", 1)
    green2 = get_player_id("green", 2)
    red1 = get_player_id("red", 1)
    red2 = get_player_id("red", 2)

    # Setup sockets for communication
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(SERVER_ADDRESS_PORT)
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wait_for_start(receiver_socket)

    while True:
        # Select players for generating a message
        green_player = green1 if random.choice([True, False]) else green2
        red_player = red1 if random.choice([True, False]) else red2
        message = f"{green_player}:{red_player}" if random.choice([True, False]) else f"{red_player}:{green_player}"
        print(f"\n{message}")

        # Prompt for continuation or termination
        if input("Exit? (y/n): ").lower() == "y":
            break
        print(f"Sending: {message}")
        sender_socket.sendto(message.encode(), CLIENT_ADDRESS_PORT)

        # Handling incoming data
        data_received, _ = receiver_socket.recvfrom(BUFFER_SIZE)
        data_received = data_received.decode("utf-8")
        print(f"Data received: {data_received}")

        if data_received == END_CODE:
            break

        time.sleep(random.randint(1, 3))

    print("End of Program")

if __name__ == "__main__":
    main()
