import socket
import json
import sys


def send_request(command, server_host, server_port):
    request = json.dumps(command)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        client_socket.send(request.encode())
        response = client_socket.recv(1024).decode()
        return json.loads(response)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <command> <params>")
        sys.exit(1)
    print(sys.argv[1])
    command = json.loads(sys.argv[1])
    SERVER_HOST = "localhost"
    SERVER_PORT = 9999
    
    response = send_request(command, SERVER_HOST, SERVER_PORT)
    print("Response from server:", response)
