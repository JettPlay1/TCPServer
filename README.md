# Многопоточный TCP-сервер и однопоточный консольный клиент для отправки запросов серверу.

## Описание

Запросы передаются в формате JSON и имеют следующий вид:

```json
{
 "command1":"name",
 "params": {
    "param1":"value1"
 }
}
```

## Установка
```sh
pip install -r requirements.txt
```

## Запуск сервера и отправка запросов
### Сервер:

```sh
python server.py <number of threads>
```
number of threads - число потоков в пуле.

### Клиент:

```sh
python client.py <command>
```

## Поддерживаемые команды

1. CheckLocalFile: Проверка указанного файла на наличие сигнатуры. Сервер возвращает список смещений найденных сигнатур.

Пример:
```sh
python client.py {\"command1\":\"CheckLocalFile\",\"params\":{\"file_path\":\"server.py\",\"signature\":\"BUFFER\"}}
```

2. QuarantineLocalFile: Перемещает указанный файл в карантин.

Пример:
```sh
python client.py {\"command1\":\"QuarantineLocalFile\",\"params\":{\"file_path\":\"testfile\"}}
```