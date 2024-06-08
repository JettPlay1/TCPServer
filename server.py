import socket
import threading
import json
import os
import sys
import signal
from concurrent.futures import ThreadPoolExecutor


BUFFER_SIZE = 4096

# Каталог для карантина
QUARANTINE_DIR = "quarantine"
if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)


def check_local_file(params):
    file_path = params.get("file_path")
    signature = params.get("signature").encode()
    if not os.path.isfile(file_path):
        return {"status": "error", "message": "File not found"}

    offsets = []
    with open(file_path, "rb") as f:
        data = f.read()
        index = data.find(signature)
        while index != -1:
            offsets.append(index)
            index = data.find(signature, index + 1)
    
    return {"status": "success", "offsets": offsets}


def quarantine_local_file(params):
    file_path = params.get("file_path")
    if not os.path.isfile(file_path):
        return {"status": "error", "message": "File not found"}

    quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
    os.rename(file_path, quarantine_path)
    return {"status": "success", "message": f"File moved to {quarantine_path}"}


def client_handler(client):
    try:
        data = b''
        while True:
            part = client.recv(BUFFER_SIZE)
            data += part
            if len(part) < BUFFER_SIZE:
                break
        
        request_data = json.loads(data.decode())
        
        command = request_data.get("command1")
        params = request_data.get("params")
        
        if command == "CheckLocalFile":
            response = check_local_file(params)
        elif command == "QuarantineLocalFile":
            response = quarantine_local_file(params)
        else:
            response = {"status": "error", "message": "Unknown command"}
        
        client.send(json.dumps(response).encode())

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client.close()


def main(host, port, num_threads):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    server.settimeout(1)
    
    pool = ThreadPoolExecutor(max_workers=num_threads)
    shutdown_flag = threading.Event()
    
    def signal_handler(sig, frame):
        print('Shutting down server...')
        shutdown_flag.set()
        server.close()
        pool.shutdown(wait=True)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Server started on {host}:{port}")
    
    while not shutdown_flag.is_set():
        try:
            client, addr = server.accept()
            print(f"Accepted connection from {addr}")
            pool.submit(client_handler, client)
        except socket.timeout:
            continue
        except socket.error:
            break


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 9999
    NUM_THREADS = 4
    main(HOST, PORT, NUM_THREADS)

