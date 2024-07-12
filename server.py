import socket
import threading
import time

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

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Listening on {host}:{port}")
    
    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

def start_multiple_servers(start_port, end_port):
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=start_server, args=('0.0.0.0', port))
        thread.daemon = True
        thread.start()
        print(f"Started server on port {port}")

if __name__ == "__main__":
    start_multiple_servers(10000, 10500)
    
    # Keep the main thread running to keep the daemon threads alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down servers.")
