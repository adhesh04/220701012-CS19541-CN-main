import socket

def start_tcp_client(host='127.0.0.1', port=65432):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    try:
        while True:
            message = input("Client: ")
            client_socket.sendall(message.encode())  # Send message to server
            
            data = client_socket.recv(1024)  # Receive response from server
            print(f"Server: {data.decode()}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_tcp_client()
