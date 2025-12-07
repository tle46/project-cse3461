from socket import *
import threading

# Create a TCP server socket and bind it to an IP address and port
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("localhost", 12345))

# Flag to indicate if the server is running
server_running = True

# Start listening for incoming client connections
server_socket.listen()

# Initialize a dictionary to store each client's username and socket
clients = {}

# Thread function to handle client communication
def handle_client(client_socket, username):
            while True:
                try:
                    # Sets a flag to check if message was sent
                    message_sent = False

                    # Receive message from client
                    message = client_socket.recv(1024).decode()

                    # Check if the connection was closed
                    if not message:
                        print(f"Connection with {username} lost.")
                        break

                    # Check if the sender is using the correct format
                    elif message.startswith("@"):

                        # Search for the username in the message
                        for user, sock in clients.items():
                            if message.startswith("@" + user):

                                # Extract message
                                message = message[len(user) + 1:].strip()

                                # Send message to target user
                                sock.send(f"{username} (private): {message}".encode())
                                message_sent = True
                                break
                        
                        # If username not found, notify sender
                        if message_sent == False:
                            client_socket.send(f"Can't send message because User not found.".encode())
                    else:
                         # Notify sender of incorrect format
                         client_socket.send(f"Sender must use correct format, @username message, to send private messages.".encode())

                # Handle broken pipe or connection reset errors
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Connection with {username} lost.")
                    break

            # Remove client from dictionary and close socket
            del clients[username]
            client_socket.close()
            print(f"{username} has disconnected.")

# While server is running do
while server_running:
    try:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")

        # Request and receieve the username from the client
        client_socket.send("Please enter your username: ".encode())
        username = client_socket.recv(1024).decode()
        print(f"Username received: {username}")

        # Store the client's username and socket in the dictionary
        clients[username] = client_socket

        # Start a new thread to handle client communication
        client_thread = threading.Thread(target=handle_client, args=(client_socket, username))
        client_thread.start()

    except KeyboardInterrupt:
        # Shut down the server
        print("Shutting down server.")
        server_running = False

# Close the server socket
server_socket.close()