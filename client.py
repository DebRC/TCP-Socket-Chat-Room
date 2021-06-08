import socket, threading, sys
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import messagebox

class Client:
    def __init__(self):
        self.port=5068
        self.server=socket.gethostbyname(socket.gethostname())
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.header=1024
        self.format="utf-8"
        self.client_name=None
        self.disconnect='exit'
        self.win=tk.Tk()
        self.gui_done=False
        
    
    def start_client(self):
        self.client.connect((self.server,self.port))
        self.win.withdraw()
        self.name=simpledialog.askstring("Name", "Please enter your name",parent=self.win)
        gui_thread=threading.Thread(target=self.gui)
        receive_thread=threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

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
        self.send_button.bind('<Return>',self.send)

        self.gui_done=True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def stop(self):
        self.client.send(self.disconnect.encode(self.format))
        self.win.quit()
        self.win.destroy()
        exit()

    def receive(self):
        while True:
            message=self.client.recv(self.header).decode(self.format)
            if message=='Send-Name':
                self.client.send(self.name.encode(self.format))
            else:
                if self.gui_done:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert('end', message)
                    self.chat_area.yview('end')
                    self.chat_area.config(state='disabled')
    def send(self):
        msg=f"{self.input_area.get('1.0', 'end').strip()}\n"
        self.client.send(msg.encode(self.format))
        self.input_area.delete('1.0', 'end')


c=Client()
c.start_client()