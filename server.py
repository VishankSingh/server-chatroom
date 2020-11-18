import socket
import threading

def main():

    # Connection Data
    PORT = 55554
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
            if "kick" in server_command_input:
                server_command_input_word_list = server_command_input.split(' ')
                print(server_command_input_word_list)
                client = server_command_input_word_list[1]
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} kicked out!'.encode('ascii'))
                nicknames.remove(nickname)



    # Handling Messages From Clients
    def handle(client):
        while True:
            try:
                
                    # Broadcasting Messages
                    message = client.recv(1024)
                    broadcast(message)
                
            except:
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
            print(f"\n[NEW CONNECTION] connected with {str(address)}")
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}")

            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            print(f"Nickname is {nickname}")
            broadcast(f"{nickname} joined!".encode('ascii'))
            client.send('CONNECTION SUCCESSFUL!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

            server_command_thread = threading.Thread(target=server_command)
            server_command_thread.start()



            

    receive()   

main()                
