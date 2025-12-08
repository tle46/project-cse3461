from socket import *
import threading

# Create a TCP client socket
client_socket = socket(AF_INET, SOCK_STREAM)

# Connect to there server using the provided IP address and port
server_ip = "localhost"
server_port = 12345
client_socket.connect((server_ip, server_port))

# Event signals shutdown
shutdown_event = threading.Event()

# Function to receive messages from the server
def receive_messages():
    while not shutdown_event.is_set():
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print("\n" + message)
            else:
                # Server has closed the connection
                print("Connection closed by the server.")

                # Signal main thread to shutdown and close client socket
                shutdown_event.set()
                client_socket.close()
                break
        except:
            # Handle any exceptions that occur during receiving
            print("An error occurred while receiving messages.")

            # Signal main thread to shutdown and close client socket
            shutdown_event.set()
            client_socket.close()
            break

# Start a background thread to receive and display messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Set as a daemon so it exits when the main thread does
receive_thread.start()

# Main thread to send messages to the server
try:
    while not shutdown_event.is_set():
        message = input()
        client_socket.send(message.encode())
finally:
    # Close client socket
    client_socket.close()
    print("Client socket closed.")