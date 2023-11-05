import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# List to store client connections
clients = []

# Function to broadcast messages to all connected clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # Remove the broken connection
                clients.remove(client)

# Function to handle each client separately
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                # Remove the broken connection
                clients.remove(client_socket)
                break
            else:
                # Broadcast the message to all clients
                broadcast(message, client_socket)
        except:
            # Remove the broken connection
            clients.remove(client_socket)
            break

# Accept and handle incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Add the new client to the list
    clients.append(client_socket)

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
