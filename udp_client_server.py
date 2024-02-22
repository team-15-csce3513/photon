import socket

class CombinedUDPClientServer:
    def __init__(self):
        self.transmit_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    #Transmits equipment codes to 
    def transmit_equipment_code(self, equipment_code: str) -> bool:
        BROADCAST_ADDRESS = "127.0.0.1"
        TRANSMIT_PORT = 20001          
        self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Attempt to send the equipment code
        bytes_sent = self.transmit_socket.sendto(str.encode(str(equipment_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
        
        # Check if the send operation was successful
        if bytes_sent > 0:
            return True
        else:
            print("Error: Failed to transmit equipment code.")
            return False
    
    def udp_client(self):
        msgFromClient = "Hello UDP Server"
        bytesToSend = str.encode(msgFromClient)
        serverAddressPort = ("127.0.0.1", 20001)
        bufferSize = 1024

        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)

    def udp_server(self):
        localIP = "127.0.0.1"
        localPort = 20001
        bufferSize = 1024
        msgFromServer = "Hello UDP Client"
        bytesToSend = str.encode(msgFromServer)

        # Create a datagram socket
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        UDPServerSocket.bind((localIP, localPort))

        print("UDP server up and listening")

        # Listen for incoming datagrams
        while True:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)

            print(clientMsg)
            print(clientIP)

            # Sending a reply to client
            UDPServerSocket.sendto(bytesToSend, address)
