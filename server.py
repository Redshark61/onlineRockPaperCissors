import socket
import pickle
from _thread import start_new_thread
from game import Game

server = "192.168.89.88"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, server started")

connected = set()
games = {}
idCount = 0


def threadedClient(connection, p, gameID):
    global idCount
    connection.send(str.encode(str(p)))
    reply = ""

    while True:
        try:
            data = connection.recv(4096).decode()

            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    connection.sendall(pickle.dumps(game))
            else:
                break

        except Exception as e:
            print("Error : ", e)
            break

    print("Lost connection")

    try:
        del games[gameID]
        print(f"Closing game {gameID}")
    except:
        pass

    idCount -= 1
    connection.close()


while True:
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    idCount += 1
    player = 0
    gameID = (idCount-1)//2

    if idCount % 2 == 1:
        games[gameID] = Game(gameID)
        print("Creating a new game")
    else:
        games[gameID].ready = True
        player = 1

    start_new_thread(threadedClient, (conn, player, gameID))
