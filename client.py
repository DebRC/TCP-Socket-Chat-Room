import socket, threading, random
import tkinter as tk
import tkinter.scrolledtext
import easygui
from AES import AESCipher
from key_exchange import DiffieHellman

class Client:
    def __init__(self):
        # default port is choosen as 5068
        self.port=5068
        # server ip address is of private ip of host
        # change it to public ip to work over internet
        self.server=socket.gethostbyname(socket.gethostname())
        # client socket object
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # message size
        self.header=1024
        # encoding format
        self.format="utf-8"
        self.client_name=None
        self.disconnect='exit'

        # client key (by diffie hellman)
        self.client_key=DiffieHellman()
        # generating public key
        self.client_pub_key=str(self.client_key.gen_public_key())
        self.client_pvt_key=None
        # gui window
        self.win=tk.Tk()
        # flag to notify other functions that gui building is done
        self.gui_done=False
        
    # function to start client
    def start_client(self):
        # connecting the server to client
        self.client.connect((self.server,self.port))
        self.win.withdraw()
        # dialog box asking name
        self.name=easygui.enterbox("Please enter your name", "Name")
        # send the name
        self.sendName()
        # exchange keys
        self.exchangeKeys()
        # starting both gui and receive thread
        gui_thread=threading.Thread(target=self.gui)
        receive_thread=threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    # function for gui
    def gui(self):
        self.win=tk.Tk()
        self.win.geometry("550x490")
        self.win.maxsize(550,490)
        self.win.minsize(550,490)
        self.win.configure(bg="deep sky blue")

        self.chat_label=tk.Label(self.win, text="Chat Room", bg="deep sky blue")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20,pady=5)

        self.chat_area=tkinter.scrolledtext.ScrolledText(self.win, height=12, bg="powder blue")
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.insert('end', 'Connected to the chat room.\n')
        self.chat_area.config(state="disabled", font=("Arial",15))

        self.msg_label=tk.Label(self.win, text="Type Your Message", bg="deep sky blue")
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=20,pady=5)

        self.input_area=tk.Text(self.win, height=3, bg="powder blue")
        self.input_area.pack(padx=20,pady=5)

        self.send_button=tk.Button(self.win, text="Send", bg="PaleTurquoise1", command=self.send)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done=True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    # function to disconnect client
    def stop(self):
        # send server to disconnect
        self.client.send(self.aes.encrypt(self.disconnect))
        self.client.close()
        exit(0)

    def exchangeKeys(self):
        # exchanging keys
        # getting public key of server
        server_pub_key=int(self.client.recv(self.header).decode(self.format))
        # generating pvt key
        self.client_pvt_key=self.client_key.gen_shared_key(server_pub_key)
        # sending public key of client
        self.client.send(self.client_pub_key.encode(self.format))
        # creating aes object with the pvt key
        self.aes=AESCipher(self.client_pvt_key)

    def sendName(self):
        # sending name of the client
        if self.name is None:
            self.name="bot"+str(random.randint(1,99999))
        self.client.send(self.name.encode(self.format))

    # function to receive message
    def receive(self):
        # loop to receive msgs
        while True:
            try:
                # receiving msg from server
                message=self.client.recv(self.header)
                if self.gui_done:
                    # decrypting the msg
                    message=self.aes.decrypt(message)
                    # set the chat area to write mode
                    self.chat_area.config(state='normal')
                    # insert the new msg
                    self.chat_area.insert('end', message)
                    # auto scroll the chat area to recent
                    self.chat_area.yview('end')
                    # set the chat area to read mode
                    self.chat_area.config(state='disabled')
            except:
                print("Disconnected from server")
                break
    
    # function to send message
    def send(self):
        # get the message from input area
        msg=f"{self.input_area.get('1.0', 'end').strip()}\n"
        if len(msg)==1:
            return
        # encrypting the message
        msg=self.aes.encrypt(msg)
        # encode and send to server
        self.client.send(msg)
        # reset the input area to default
        self.input_area.delete('1.0', 'end')


c=Client()
c.start_client()