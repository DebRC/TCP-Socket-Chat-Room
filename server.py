import socket, threading


'''Global Variables'''
# port number
PORT = 5068
# getting server/host ip
SERVER = socket.gethostbyname(socket.gethostname())
# socket address ip+port
ADDR = (SERVER, PORT)
# specifies the max length of the message
HEADER = 1024
# format for encoding/decoding
FORMAT = "utf-8"
# message to disconnect
DISCONNECT = "exit"
# clients list
clients=[]
nicknames=[]


'''Socket Object'''
# creating a new server socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding the server socket object with server's socket
server.bind(ADDR)


'''Server Functions'''
def broadcast(msg):
    for c in clients:
        c.send(msg)



# function to handle the clients
def client(conn, addr):
    conn.send('Send-Nick'.encode(FORMAT))
    nickname=conn.recv(20).decode(FORMAT)
    clients.append(conn)
    nicknames.append(nickname)
    print(f"New Client - [{addr[0]}]-{addr[1]} connected with a Name - {nickname}")
    conn.send('Connected to the chat room. Type \'exit\' to disconnect.'.encode(FORMAT))
    broadcast(f'{nickname} has joined the chat!'.encode(FORMAT))
    connected = True
    while connected:

        # receiving message length and decoding it
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # if an empty message arrives ignore it
        if not msg_length:
            continue
        msg_length = int(msg_length)

        # receiving message and decoding it
        msg = conn.recv(msg_length).decode(FORMAT)

        # if disconnect nmessage arrives disconnect client
        if msg == f'{nickname}: exit':
            connected = False
        
        # otherwise print the message and send
        # "message received to client"
        else:
            print(f"[{addr[0]}]-{addr[1]} sent - {msg}")
            broadcast(msg.encode(FORMAT))
    # close client object
    conn.send(f"Disconnecting from Server...\nDone!".encode(FORMAT))
    print(f"[{addr[0]}]-{addr[1]} {nickname} Disconnected")
    conn.close()
    clients.remove(conn)
    nicknames.remove(nickname)
    broadcast(f'{nickname} has left the chat'.encode(FORMAT))
    print(f"Active Connections - {threading.active_count()-2}")
        
# function to start and run the server
def start_server():
    print("Server is starting...")
    # setting the server to listen mode
    server.listen()
    print(f"Server [{SERVER}] is ready to accept connections!")
    while True:
        # server accepting new socket object i.e. our client
        # and it's address
        conn, addr = server.accept()
        # Running multiple client/s concurrently using threading
        thread = threading.Thread(target=client, args=(conn, addr))
        thread.start()
        print(f"Active Connections - {threading.active_count()-1}")


# start server
start_server()