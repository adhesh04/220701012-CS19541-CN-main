import socket

def start_tcp_server(host='127.0.0.1', port=65432):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"Server listening on {host}:{port}...")
    
    connection, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(f"Client: {data.decode()}")
            message = input("Server: ")
            connection.sendall(message.encode())
    finally:
        connection.close()

if __name__ == "__main__":
    start_tcp_server()
