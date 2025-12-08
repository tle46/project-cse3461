import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

DEFAULT_SERVER_IP = ""
DEFAULT_SERVER_PORT = 5000

client_socket = None

msg_box = None
entry_box = None
status_label = None
connect_button = None

# Stop event for when server disconnects or error occurs
stop = threading.Event()

# Print messages to the GUI message box
def gui_print(message):
  msg_box.config(state="normal")
  msg_box.insert(tk.END, message + "\n")
  msg_box.see(tk.END)
  msg_box.config(state="disabled")

# Terminate program and close socket
def close_app(window):
  try:
    if client_socket:
      client_socket.close()
  except:
    pass

  window.destroy()
  stop.set()

# Connect to server
def connect_to_server(ip_entry, port_entry):
  global client_socket

  server_ip = ip_entry.get()
  server_port = int(port_entry.get())

  try:
    stop.clear()

    # 1: Create a TCP client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2: Connect to the server using the server’s IP address and port
    client_socket.connect((server_ip, server_port))

    # 3: Display the client’s local address and port information
    gui_print(f"[CONNECTED] Your address: {client_socket.getsockname()}")
    status_label.config(text=f"Connected to {server_ip}:{server_port}", fg="green")


    # DISABLE CONNECT BUTTON TO PREVENT MORE THAN 1 CONNECTION
    connect_button.config(state="disabled")

    # 4: Start a background thread
    background_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    background_thread.daemon = True
    background_thread.start()
  except Exception as e:
    gui_print(f"[ERROR] Could not connect to {server_ip}:{server_port} -> {e}")

# Send message from entry box to server
def send_message():
  global client_socket

  if stop.is_set():
    return

  msg = entry_box.get()
  if msg.strip() == "":
    return

  try:
    client_socket.send(msg.encode())
  except:
    return

  entry_box.delete(0, tk.END)

# Continually receive messages from server
def receive_messages(sock):
  global status_label

  while True:
    try:
      # Receive incoming messages from the server
      msg = sock.recv(1024).decode()

      if not msg:
        break

      # Display received messages to the user
      gui_print(f"[MSG RECEIVED] " + msg)
    except:
      break
  gui_print(f"[DISCONNECTED]")
  status_label.config(text="Not connected", fg="red")
  stop.set()

def main():
  # GUI Setup
  global client_socket, msg_box, entry_box, status_label, connect_button

  # Window
  window = tk.Tk()
  window.title("TCP Client")

  # Connection Frame
  connect_frame = tk.Frame(window)
  connect_frame.pack(pady=5)

  # IP address entry box
  tk.Label(connect_frame, text="Server IP:").grid(row=0, column=0)
  ip_entry = tk.Entry(connect_frame, width=15)
  ip_entry.grid(row=0, column=1)
  ip_entry.insert(0, DEFAULT_SERVER_IP)

  # Port entry box
  tk.Label(connect_frame, text="Port:").grid(row=0, column=2)
  port_entry = tk.Entry(connect_frame, width=6)
  port_entry.grid(row=0, column=3)
  port_entry.insert(0, str(DEFAULT_SERVER_PORT))

  # Connected/Not connected status label
  status_label = tk.Label(window, text="Not connected", fg="red")
  status_label.pack()

  # Connect Button
  connect_button = tk.Button(connect_frame, text="Connect",
            command=lambda: connect_to_server(ip_entry, port_entry))
  connect_button.grid(row=0, column=4, padx=5)

  # Message Box to hold messages
  msg_box = scrolledtext.ScrolledText(window, state="disabled")
  msg_box.pack(padx=10, pady=10)

  # Entry box for user input
  entry_box = tk.Entry(window, width=50)
  entry_box.pack(side=tk.LEFT, padx=10, pady=10)
  entry_box.bind("<Return>", lambda event: send_message())

  # Send Button
  send_button = tk.Button(window, text="Send", command=send_message)
  send_button.pack(side=tk.LEFT, pady=10)

  # Handle window close
  window.protocol("WM_DELETE_WINDOW", lambda: close_app(window))

  window.mainloop()

  stop.set()
  client_socket.close()

if __name__ == "__main__":
  main()
