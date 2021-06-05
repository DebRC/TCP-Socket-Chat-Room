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


'''Socket Object'''
# creating a new socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding the host socket with socket object
server.bind(ADDR)


'''Server Functions'''
# function to handle the clients
def client(conn, addr):
    print(f"New Client - [{addr}] connected.")

    # running client until disconnect message sent
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
        if msg == DISCONNECT:
            print(f"Disconnecting from Server [{SERVER}]...\nDone!")
            connected = False
        
        # otherwise print the message and send
        # "message received to client"
        else:
            print(f"[{addr}] sent - {msg}")
            conn.send("Message received".encode(FORMAT))

    # close client object
    conn.close()
        
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
        # Running client/s concurrently using threading
        thread = threading.Thread(target=client, args=(conn, addr))
        thread.start()

        # -1 in active connection signifies this start() function
        print(f"Active Connections - {threading.activeCount() - 1}")


# start server
start_server()