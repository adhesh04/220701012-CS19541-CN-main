import socket

def start_client():
    # Set up TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)  # Server address (same as server's address)
    
    # Connect to the server
    client_socket.connect(server_address)
    print(f"Connected to server at {server_address}")

    while True:
        # Get user input and send to server
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            print("Exiting...")
            break
        
        # Send message to server
        client_socket.sendall(message.encode())
        
        # Receive the echoed message from the server
        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode()}")

    # Close the socket after exiting the loop
    client_socket.close()

if __name__ == "__main__":
    start_client()
