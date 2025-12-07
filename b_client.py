import socket
import threading

SERVER_IP = ""
SERVER_PORT = 5005

# Stop event when server disconnects or error occurs
stop = threading.Event()

def receive_messages(sock):
	global running

	while True:
		try:
			# Receive incoming messages from the server
			msg = sock.recv(1024).decode()

			if not msg:
				break

			# Display received messages to the user
			print(f"Message received: " + msg)
		except:
			break
	stop.set()
	print(f"Message Receiver Thread Quitting")

def main():
	global running

	# 1: Create a TCP client socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 2: Connect to the server using the server’s IP address and port
	client_socket.connect((SERVER_IP, SERVER_PORT))

	# 3: Display the client’s local address and port information
	print(f"[CONNECTED] Your address: {client_socket.getsockname()}")

	# 4: Start a background thread
	background_thread = threading.Thread(target=receive_messages, args=(client_socket,))
	background_thread.daemon = True
	background_thread.start()

	while True:
		try:
			# Accept user input from the keyboard
			msg = input("")

			if stop.is_set():
				break

			# Send the typed message to the server
			client_socket.send(msg.encode())
		except:
			break

	stop.set()
	client_socket.close()
	print("Socket Closed")

if __name__ == "__main__":
	main()
