import socket, threading
NICKNAME=""

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

NICKNAME=input("Enter your name: ")

'''Socket Object'''
# creating a new client socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting the client object with server's socket
client.connect(ADDR)

# function for receiving messages
def receive():
    while True:
        message=client.recv(HEADER).decode(FORMAT)
        if message=="Send-Nick":
            client.send(NICKNAME.encode(FORMAT))
            continue
        print(message)


# function for sending messages
def send():
    while True:
        # encode the message
        message=f'{NICKNAME}: {input("")}'
        message = message.encode(FORMAT)
        # pad extra bits to maintain HEADER size
        msg_length = str(len(message)).encode(FORMAT)
        msg_length += b' ' * (HEADER - len(msg_length))
        # send message length and message
        client.send(msg_length)
        client.send(message)


def start_client():
    receive_thread=threading.Thread(target=receive)
    send_thread=threading.Thread(target=send)
    receive_thread.start()
    send_thread.start()
start_client()