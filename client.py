import socket
import threading


# Connection Data
PORT = 55550
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print("[STARTING] server is starting...")
print(f"[LISTENING] Server is listening on {SERVER}")

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

#server controller's commands
def server_command():
    while True:
        server_command_input = input("SERVER OWNER: ")
        
        if server_command_input.startswith('/')
            if server_command_input.startswith('/kick'):
                name = server_command_input[6:]
                if name in nicknames:
                    name_index = nicknames.index(name)
                    client_to_kick = clients[name_index]
                    clients.remove(client_to_kick)
                    client_to_kick.send("KICKED".encode('ascii'))
                    client_to_kick.close()
                    nicknames.remove(name)
                    broadcast(f"{name} WAS KICKED BY THE SERVER!".encode('ascii'))

            if server_command_input.startswith('/active'):
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}")


                
        else:
            broadcast(f"SERVER OWNER: {server_command_input}".encode('ascii'))



# Handling Messages From Clients
def handle(client):
    while True:
            
            try:
                    
                # Broadcasting Messages
                message = client.recv(1024)
                broadcast(message)
                    
            except:
                if client in clients:
                    # Removing And Closing Clients
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname = nicknames[index]
                    broadcast(f'{nickname} left!'.encode('ascii'))
                    nicknames.remove(nickname)
                    break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
            
        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(f"\n[NEW CONNECTION] connected with {str(address)} with the nickname {nickname}")
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}")
        broadcast(f"{nickname} joined!".encode('ascii'))
        client.send('CONNECTION SUCCESSFUL!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        server_command_thread = threading.Thread(target=server_command)
        server_command_thread.start() 



          

receive()   

