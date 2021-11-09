import socket
import pickle


class Network:
    """
    Connect every player to the network
    """

    def __init__(self):
        # Initialize the connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        # Get the player number
        self.player = self.connect()

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            # Connect to the server
            self.client.connect(self.addr)
            # Receive the player number
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            # Send the data to the server
            self.client.send(str.encode(data))
            # Receive an instance of Game
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
