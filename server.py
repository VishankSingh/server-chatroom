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
print(f"[LISTENING] Server is listening on {ADDR}")

# Lists For Clients and Their usernames
clients = []
usernames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

#server controller's commands
def server_command():
    while True:
        server_command_input = input("SERVER OWNER: ")
        
        if server_command_input.startswith('/kick'):
            name = server_command_input[6:]
            if name in usernames:
                name_index = usernames.index(name)
                client_to_kick = clients[name_index]
                clients.remove(client_to_kick)
                client_to_kick.send("KICKED".encode('ascii'))
                client_to_kick.close()
                usernames.remove(name)
                broadcast(f"{name} WAS KICKED BY THE SERVER!".encode('ascii'))

                


        elif server_command_input.startswith('/active'):
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}")

        elif server_command_input.startswith('/close'):
            broadcast('SERVER IS CLOSED')
            print("[SERVER CLOSED]")
            server.close()
            exit()

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
                    username = usernames[index]
                    broadcast(f'{username} left!'.encode('ascii'))
                    usernames.remove(username)
                    break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection

                
        client, address = server.accept()
            
        # Request And Store username
        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Print And Broadcast username
        print(f"\n[NEW CONNECTION] connected with {str(address)} with the username {username}")
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}")
        broadcast(f"{username} joined!".encode('ascii'))
        client.send('CONNECTION SUCCESSFUL!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        server_command_thread = threading.Thread(target=server_command)
        server_command_thread.start() 



          

receive()   

