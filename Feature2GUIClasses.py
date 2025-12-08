from socket import *
import threading
import tkinter as tk
from tkinter import scrolledtext

class Client:
    def __init__(self, server_ip='localhost', server_port=12345, username = "Guest", curr_message = None):

        # Initialize the client's attributes
        self.server_ip = server_ip
        self.server_port = server_port
        self.is_connected = False
        self.username = username
        self.curr_message = curr_message

        # Create a TCP client socket
        self.client_socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        # Alter connection status
        self.is_connected = True

        # Connect to the server using the provided IP address and port
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to server at {self.server_ip}:{self.server_port}")

        # Start background thread to receive messages
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_message(self, message):
        # Send a message to the server only if the client is connected
        if self.is_connected:
            self.client_socket.send(message.encode())

    def receive_message(self):
        # Receive a message from the server only if the client is connected
        while self.is_connected:
            try:
                data = self.client_socket.recv(1024)

                # Handle server disconnection
                if not data:
                    self.is_connected = False
                    break

                # Decode and set the received message
                message = data.decode()

                # Skip displaying server prompts in chat box
                if message.startswith("Server Prompt:"):
                    continue

                if self.curr_message:
                    self.curr_message(message)

            except Exception as e:
                # Handle any exceptions that occur during receiving
                self.is_connected = False
                if self.curr_message:
                    self.curr_message(f"Error: {str(e)}")
                break

    def close_connection(self):
        # Close the client socket
        self.is_connected = False
        self.client_socket.close()
        print("Client socket closed.")

class ClientGUI:
    def __init__(self, root):

        self.root = root
        self.root.title("Messaging Client")
        self.client = None

        # Login interface
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(padx=20, pady=20)

        tk.Label(self.login_frame, text="Enter Username:").pack(side=tk.LEFT)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(side=tk.LEFT)

        tk.Button(self.login_frame, text="Join Chat", command=self.join_chat).pack(side=tk.LEFT)

    def join_chat(self):
        username = self.username_entry.get().strip()
        if username:
            self.login_frame.destroy()  # remove login interface
            self.init_chat(username)
    
    def init_chat(self, username):
        self.root.title(f"Messaging Client - {username}")

        # Chat interface
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_display.pack(padx=10, pady=10)

        # Message interface
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=10, pady=10)

        send_button = tk.Button(self.root, text="Send", command=self.send_message)
        send_button.pack(side=tk.LEFT, padx=5)

        # Initialize client
        self.client = Client(username=username, curr_message=self.append_message)
        self.client.connect()

        # Send username to server
        self.client.client_socket.send(f"{username}".encode())

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def append_message(self, msg):
        # Schedule interface update in the main thread
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, msg + "\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def send_message(self):
        # Send message
        msg = self.message_entry.get()
        if msg:
            self.client.send_message(msg)
            self.message_entry.delete(0, tk.END)

    def close(self):
        # Close client connection and GUI
        if self.client:
            self.client.close_connection()
        self.root.destroy()
