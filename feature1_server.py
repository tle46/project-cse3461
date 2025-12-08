import socket
import threading

IP_ADDRESS = ""
PORT = 5005

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
	with clients_lock:
		for client in clients:
			print(f"[BROADCAST] Broadcasting to {client.getpeername()}")
			client.send(message)

def handle_client(client_socket, addr):
	# 9: Client Handler (in each thread):
	print(f"[NEW CONNECTION] {addr} connected.")

	while True:
		try:
			# 10: Continuously receive messages from the assigned client
			message = client_socket.recv(1024)
			print(f"[RECEIVED] {addr}: {message.decode()}")

			# 12: If the client disconnects, close the connection and remove it from the list
			if not message:
				break

			# 11: For each received message, forward it to all other connected clients
			broadcast(message, client_socket)
		except:
			break

	# Remove the client after disconnect
	with clients_lock:
		clients.remove(client_socket)
	client_socket.close()
	print(f"[DISCONNECTED] {addr} left.")

def main():
	# 1: Create a TCP server socket and bind it to an IP address and port
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((IP_ADDRESS, PORT))

	# 2: Start listening for incoming client connections
	server.listen(1)
	print(f"[LISTENING] Server running on {IP_ADDRESS}:{PORT}")

	# 4: while server is running do
	while True:
		# 5: Accept a new client connection
		client_socket, addr = server.accept()

		# 6: Add the client to the list of active clients
		with clients_lock:
			clients.append(client_socket)

		# 7: Start a new thread to handle communication with that client
		background_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
		background_thread.daemon = True
		background_thread.start()
	print(f"Server Quitting")

if __name__ == "__main__":
	main()
