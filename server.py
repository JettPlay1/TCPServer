import socket
import threading
import json
import os
import sys
import signal
from concurrent.futures import ThreadPoolExecutor
from config import settings


BUFFER_SIZE = 4096  # Размер буфера для принятия сообщения от клиента
HOST = "0.0.0.0"    # Адрес сервера
PORT = 9999         # Порт сервера

# Каталог для карантина
QUARANTINE_DIR = settings.QUARANTINE_DIR
if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)


def check_local_file(params):

    # Парсим параметры
    file_path = params.get("file_path")
    signature = params.get("signature").encode()

    # Проверяем, существует ли файл, переданный клиентом
    if not os.path.isfile(file_path):
        return {"status": "error", "message": "File not found"}

    # Ищем сигнатуру пользователя в файле, записываем смещения найденных сигнатур
    offsets = []
    with open(file_path, "rb") as f:
        data = f.read()
        index = data.find(signature)
        while index != -1:
            offsets.append(index)
            index = data.find(signature, index + 1)
    
    return {"status": "success", "offsets": offsets}


def quarantine_local_file(params):

    # Парсим путь до файла
    file_path = params.get("file_path")

    # Проверяем, существет ли файл
    if not os.path.isfile(file_path):
        return {"status": "error", "message": "File not found"}

    # Перемещаем файл в карантин
    quarantine_path = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
    os.rename(file_path, quarantine_path)

    return {"status": "success", "message": f"File moved to {quarantine_path}"}


def client_handler(client):
    try:

        # Получаем команду с параметрами от клиента
        data = b''
        while True:
            part = client.recv(BUFFER_SIZE)
            data += part
            if len(part) < BUFFER_SIZE:
                break
        
        # Парсим JSON
        request_data = json.loads(data.decode())

        command = request_data.get("command1")
        params = request_data.get("params")

        # Обрабатываем команду
        if command == "CheckLocalFile":
            response = check_local_file(params)
        elif command == "QuarantineLocalFile":
            response = quarantine_local_file(params)
        else:
            response = {"status": "error", "message": "Unknown command"}
        
        # Отправляем ответ пользователю
        client.send(json.dumps(response).encode())

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client.close()


def main(num_threads):

    # Создаём сокет для общения с клиентами
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    # Устанавливаем таймаут, чтобы сокет не блокировался и мы могли передать SIGINT
    server.settimeout(1)  
    
    # Создаём пул
    pool = ThreadPoolExecutor(max_workers=num_threads)
    shutdown_flag = threading.Event()
    
    # Хэндлер для SIGINT
    def signal_handler(signal, frame):
        print('Shutting down server...')

        # Закрываем сокет и пул и завершаем работу приложения
        shutdown_flag.set()
        server.close()
        pool.shutdown(wait=True)
        sys.exit(0)
    
    # Регистрируем хэндлер
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Server started on {HOST}:{PORT}")
    
    # Ждём подключений
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

    if len(sys.argv) < 2:
        print("Usage: python server.py <number of threads>")
        sys.exit(1)
    
    num_threads = int(sys.argv[1])  # Число потоков
    main(num_threads)

