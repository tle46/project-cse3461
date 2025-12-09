# TCP Client UI for Feature 1 and Feature 2

## Feature 1

### Dependencies

Firstly ensure python and tkinter are installed.

Tkinter can be installed on linux with

```
sudo apt-get install python3-tk
```

### Running the program

Start the server using:

```
python3 feature1_server.py
```

Stop server using [ctrl+c]

Start clients:

#### Console Client

Ensure that SERVER_IP and SERVER_PORT variables are properly set in the feature1_client.py file.

```
python3 feature1_client.py
```

Exit console client using [ctrl+c]

#### GUI Client

```
python3 feature1_client_gui.py
```
Set the server ip and port and click 'Connect' to establish connection.

Send messages using the lower text box at the bottom of the window.

Exit GUI program using close button at top right.

Note that each client may only open 1 single TCP connection. Please rerun the client programs to reconnect.
