import socket
import json
import sys
from config import settings

def send_request(command, server_host, server_port):
    request = json.dumps(command)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        client_socket.send(request.encode())
        response = client_socket.recv(1024).decode()
        return json.loads(response)


if __name__ == "__main__":

    # Читаем аргумент коммандной строки
    if len(sys.argv) < 2:
        print("Usage: python client.py <command>")
        print("For example: {\"command1\":\"CheckLocalFile\",\"params\":{\"file_path\":\"my_file\",\"signature\":\"test\"}}")
        sys.exit(1)

    # Парсим JSON 
    command = json.loads(sys.argv[1])
    SERVER_HOST = settings.HOST
    SERVER_PORT = settings.SERVER_PORT
    
    # Отправляем запрос и получаем ответ от сервера
    response = send_request(command, SERVER_HOST, SERVER_PORT)
    print("Response from server:", response)
