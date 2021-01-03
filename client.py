import socket
import threading

# Choosing username
username = input("Choose your username: ")

CONNECTION = input('Input IP address and port in the format (IP, PORT) without parentheses')

PORT = CONNECTION.split(',')[1].strip()
IP = CONNECTION.split(',')[0].strip()
ADDR = (IP, PORT)

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Listening to Server and Sending username
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'USER' Send username
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
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
            exit()
            break

# Sending Messages To Server
def write():
    while True:
        try:
            message = f"{username}: {input('')}"
            client.send(message.encode('ascii'))            

        except:
            print('YOU CANNOT SEND MESSAGES')
            exit()

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()        
