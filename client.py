import socket
import threading
import time
import random
import sys

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

def create_malicious_connections(target_ip, target_port, num_idle=2, num_active=2):
    for _ in range(num_idle):
        thread = threading.Thread(target=idle_connection, args=(target_ip, target_port))
        thread.start()
    
    for _ in range(num_active):
        thread = threading.Thread(target=active_connection, args=(target_ip, target_port))
        thread.start()

def input_with_timeout(prompt, timeout, default):
    print(prompt, end=': ', flush=True)
    result = []
    def timeout_input():
        try:
            result.append(input())
        except:
            pass

    thread = threading.Thread(target=timeout_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if result:
        return result[0]
    else:
        print(f"\nTimeout reached. Using default value: {default}")
        return default

if __name__ == "__main__":
    target_ip = input_with_timeout("Enter target IP", 5, "127.0.0.1")
    
    try:
        target_port = int(input_with_timeout("Enter target port", 5, random.randint(10000, 10500)))
    except ValueError:
        target_port = random.randint(10000, 10500)
        print(f"Invalid input for port. Using random value: {target_port}")

    try:
        num_idle = int(input_with_timeout("Enter number of idle connections", 5, 1))
    except ValueError:
        num_idle = 1
        print("Invalid input for number of idle connections. Using default value: 1")

    try:
        num_active = int(input_with_timeout("Enter number of active connections", 5, 1))
    except ValueError:
        num_active = 1
        print("Invalid input for number of active connections. Using default value: 1")

    create_malicious_connections(target_ip, target_port, num_idle, num_active)
