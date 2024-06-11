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
python server.py <number_of_threads>
```
**number of threads** - число потоков в пуле.

### Клиент:

```sh
python client.py <command>
```

## Поддерживаемые команды

### **CheckLocalFile:** Проверка указанного файла на наличие сигнатуры. Сервер возвращает список смещений найденных сигнатур.

**Windows:**
```batch
python client.py {\"command1\":\"CheckLocalFile\",\"params\":{\"file_path\":\"server.py\",\"signature\":\"BUFFER\"}}
```

**Linux**
```sh
python client.py '{"command1":"CheckLocalFile","params":{"file_path":"server.py","signature":"BUFFER"}}'
```
### **QuarantineLocalFile:** Перемещает указанный файл в карантин.

**Windows:**
```batch
python client.py {\"command1\":\"QuarantineLocalFile\",\"params\":{\"file_path\":\"testfile\"}}
```

**Linux**
```sh
python client.py '{"command1":"QuarantineLocalFile","params":{"file_path":"testfile"}}'
```

## Параметры сервера

Для указания своей конфигурации сервера можете указать необходимые настройки в .env файле.

### Поддерживаемые параметры

* **QUARANTINE_DIR** - Путь до каталога карантина.
* **HOST** - Адрес сервера, по которому клиент будет подключаться.
* **SERVER_HOST** - Адрес, на котором будет запущен сервер.
* **SERVER_PORT** - Порт, на котором будет запущен сервер.