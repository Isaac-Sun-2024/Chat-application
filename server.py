# import modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users


def listen_for_messages(client, username):
    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':

            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"message sent from client {username} is empty")


def send_message_to_client(client, message):

    client.sendall(message.encode())


def send_messages_to_all(message):

    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client


def client_handler(client):
    # Server will listen for client message that will contain username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print('client username is empty')

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


# Main function
def main():
    # creating server socket class object
    # using IPv4 address

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()
