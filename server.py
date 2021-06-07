import socket, threading

class Server():
    def __init__(self):
        self.port=5068
        self.host=socket.gethostbyname(socket.gethostname())
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.header=1024
        self.format="utf-8"
        self.client_names={}
        self.disconnect='exit'

    def broadcast(self,msg):
        for client in self.client_names:
            client.send(msg)

    def handle_client(self,client,client_addr):
        client.send('Send-Name'.encode(self.format))
        self.client_names[client]=client.recv(self.header).decode(self.format)
        client_name=self.client_names[client]
        print(f"[{client_addr[0]}]-{client_addr[1]} connected with a Name - [{client_name}]")
        client.send('Connected to the chat room.'.encode(self.format))
        self.broadcast(f'{client_name} has joined the chat!'.encode(self.format))
        while True:
            try:
                msg = client.recv(self.header).decode(self.format)
                print(f"[{client_addr[0]}]-{client_addr[1]} - [{client_name}] - {msg}")
                if msg==self.disconnect:
                    break
                msg=f'{client_name}: {msg}'
                self.broadcast(msg.encode(self.format))
            except:
                break
        print(f"[{client_addr[0]}]-{client_addr[1]} with [{client_name}] Disconnected")
        del self.client_names[client]
        self.broadcast(f'{client_name} has left the chat'.encode(self.format))
        print(f"Active Connections - {threading.active_count()-2}")
        client.close()

    def start_server(self):
        self.server.bind((self.host,self.port))
        self.server.listen()
        print(f"Server is starting...\nServer [{self.host}] is ready to accept connections!")
        while True:
            # server accepting new socket object i.e. our client
            # and it's address
            client, client_addr = self.server.accept()
            # Running multiple client/s concurrently using threading
            thread = threading.Thread(target=self.handle_client, args=(client, client_addr))
            thread.start()
            print(f"Active Connections - {threading.active_count()-1}")
       
# start server
s=Server()
s.start_server()