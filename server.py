import socket, threading


class Server:
    def __init__(self):
        # default port is choosen as 5068
        self.port=5068
        # server ip address is of private ip of host
        # change it to public to work over internet
        self.host=socket.gethostbyname(socket.gethostname())
        # server socket object
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # message size
        self.header=1024
        # encoding format
        self.format="utf-8"
        # map to store the names of client
        self.client_names={}
        self.disconnect='exit'


    # function to send messages to all other host
    def broadcast(self,msg):
        for client in self.client_names:
            client.send(msg)
    

    # function to handle a client
    def handle_client(self,client,client_addr):

        # get the name of the client and store it in the map
        client.send('Send-Name'.encode(self.format))
        self.client_names[client]=client.recv(self.header).decode(self.format)
        client_name=self.client_names[client]


        print(f"[{client_addr[0]}]-{client_addr[1]} - [{client_name}] - Connected")
        # inform everyone that 'this client' has joined the server
        self.broadcast(f'{client_name} has joined the chat!\n'.encode(self.format))
        # receive message until there is an error at client side
        while True:
            try:
                msg = client.recv(self.header).decode(self.format)
                # if message states to disconnect then break from the loop
                if msg==self.disconnect:
                    break
                print(f"[{client_addr[0]}]-{client_addr[1]} - [{client_name}] - {msg}")
                # add client name to the message and broadcast to every clients
                msg=f'{client_name}: {msg}'
                self.broadcast(msg.encode(self.format))
            except:
                break
        # close the connection
        client.close()
        print(f"[{client_addr[0]}]-{client_addr[1]} - [{client_name}] - Disconnected")
        del self.client_names[client]
        # inform everyone 'this client' has left the server
        self.broadcast(f'{client_name} has left the chat\n'.encode(self.format))
        print(f"Active Connections - {threading.active_count()-2}")


    # function to start the server
    def start_server(self):
        self.server.bind((self.host,self.port))
        # set the server to listening mode
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