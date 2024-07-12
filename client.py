import socket
import threading
import time
import random
import argparse

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
            # Increase the amount of data sent
            s.send(b"Malicious traffic\n" * 1000)
            data = s.recv(1024)
            # Reduce sleep time to send data more frequently
            time.sleep(0.1)
    except Exception as e:
        print(f"Active connection error: {e}")
    finally:
        s.close()

def create_malicious_connections(target_ip, target_port, num_idle=2, num_active=2):
    for _ in range(num_idle):
        thread = threading.Thread(target=idle_connection, args=(target_ip, target_port))
        thread.start()
    
    for _ in range(num_active):
        thread = threading.Thread(target=active_connection, args=(target_ip, target_port))
        thread.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create malicious connections to a target IP and port.')
    parser.add_argument('--ip', type=str, default="127.0.0.1", help='Target IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=random.randint(1024, 65535), help='Target port (default: random valid port)')
    parser.add_argument('--idle', type=int, default=1, help='Number of idle connections (default: 1)')
    parser.add_argument('--active', type=int, default=1, help='Number of active connections (default: 1)')

    args = parser.parse_args()

    target_ip = args.ip
    target_port = args.port
    num_idle = args.idle
    num_active = args.active

    create_malicious_connections(target_ip, target_port, num_idle, num_active)

