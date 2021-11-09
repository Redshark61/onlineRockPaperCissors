import socket
import pickle
from _thread import start_new_thread
from game import Game

# Get the ip address of the server
server = socket.gethostbyname(socket.gethostname())
# Get the port number
port = 5555

# Initialize the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Try to bind the server to the port
    s.bind((server, port))
except socket.error as e:
    str(e)

# The server will listen to 2 clients at a time
s.listen(2)
print("Waiting for a connection, server started")

connected = set()
games = {}
idCount = 0


def threadedClient(connection, p, gameID):
    # Get the total number of players
    global idCount
    # As soon as the player connect, we send him it's number (player 1 or 0)
    # See the network.py file line 11 for more info
    connection.send(str.encode(str(p)))

    while True:
        # Try to connect to the client
        try:
            # Get the message from the client (get, reset, or the player move)
            data = connection.recv(4096).decode()
            # If the game is created
            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                # If there is data
                else:
                    # If the player want to reset the game
                    if data == "reset":
                        game.resetWent()
                    # If it's not a get, then he plays
                    elif data != "get":
                        game.play(p, data)
                    # Send the updated instance to the client
                    connection.sendall(pickle.dumps(game))
            else:
                break

        except:
            print("Error!")
            break

    print("Lost connection")

    try:
        del games[gameID]
        print(f"Closing game {gameID}")
    except:
        pass

    idCount -= 1
    connection.close()


# The server always waits for a connection
while True:
    # It will accept the connection and create a new thread for the client
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    idCount += 1
    player = 0
    # There is one game created every two players
    gameID = (idCount-1)//2

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print("Creating a new game")
    else:
        games[gameID].ready = True
        player = 1

    start_new_thread(threadedClient, (conn, player, gameID))
