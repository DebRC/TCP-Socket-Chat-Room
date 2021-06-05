import socket, threading


'''Global Variables'''
# port number
PORT = 5068
# change this to server ip addr if running
# on different host than server
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
# creating a new client socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting the client object with server's socket
client.connect(ADDR)

# function for sending one message
def send(msg):
    # encode the message
    message = msg.encode(FORMAT)
    # pad extra bits to maintain HEADER size
    msg_length = str(len(message)).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))
    # send message length and message
    client.send(msg_length)
    client.send(message)
    # printing "message" coming from
    # server side
    print(client.recv(HEADER).decode(FORMAT))


def start_client():
    print("Client-server connection is ready! Type 'exit' to disconnect")
    while True:
        msg=input("Type Your Message - ")
        send(msg)
        if msg==DISCONNECT:
            exit()

start_client()