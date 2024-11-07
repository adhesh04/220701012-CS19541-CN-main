import socket

def start_server():
    # Set up TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)  # Server listens on port 12345
    server_socket.bind(server_address)
    server_socket.listen(1)  # Listen for incoming connections
    print(f"Server listening on {server_address}")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        
        try:
            while True:
                # Receive data from the client
                data = connection.recv(1024)
                if not data:
                    break  # If no data, connection is closed
                
                print(f"Received message: {data.decode()} from {client_address}")
                
                # Send the same message back to the client (echo)
                connection.sendall(data)
                print(f"Echoed message back to {client_address}")

        finally:
            # Clean up the connection
            connection.close()
            print(f"Connection closed with {client_address}")

if __name__ == "__main__":
    start_server()
