import socket, threading
import tkinter as tk



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
        try:
            message=client.recv(HEADER).decode(FORMAT)
            if message=="Send-Name":
                client.send(NICKNAME.encode(FORMAT))
                continue
            print(message)
        except:
            exit()


# function for sending messages
def send():
    while True:
        # encode the message
        message=input("").encode(FORMAT)
        # send message length and message
        client.send(message)
        if message.decode(FORMAT)==DISCONNECT:
            client.close()
            exit()


def start_client():
    receive_thread=threading.Thread(target=receive)
    send_thread=threading.Thread(target=send)
    receive_thread.start()
    send_thread.start()
start_client()