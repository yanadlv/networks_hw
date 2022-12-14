Скрипт реализован на языке Python.

Сборка и запуск образа: 
```
docker build -t mtu_search -f Dockerfile .
docker run -it mtu_search 
```

Запуск скрипта:
```
python3 mtu_search.py host
```
 - Здесь `host` - обязательный параметр (хост)
