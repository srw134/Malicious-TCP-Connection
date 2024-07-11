import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received data from {client_address}: {data}")
            client_socket.send(b"ACK\n")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print(f"Closing connection to {client_address}")
        client_socket.close()

def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Listening on {host}:{port}")
    
    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
