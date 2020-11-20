import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")


PORT = 55550
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'KICKED':
                print('YOU WERE KICKED OUT BY THE SERVER!')
                client.close()
                break
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        try:
            message = f"{nickname}: {input('')}"
            client.send(message.encode('ascii'))            

        except:
            print('YOU CANNOT SEND MESSAGES')

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()        
