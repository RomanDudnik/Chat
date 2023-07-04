#!/bin/python3

# Серверная часть
# Импортируем необходимые модули: 
import socket
import threading

# Создадим списки клиентов и их никнеймов:
nicknames = []
clients = []

# Определяем константы для удобства:
HOST = '127.0.1.20'  # IP-адрес сервера
PORT = 55555            # Порт сервера

# Создадим серверный сокет для приема входящих соединений.
# Зададим параметры сокета:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Отправка сообщений всем клиентам.
def broadcast(message):
    for client in clients:
        client.send(message)

# Определяем функцию для обработки каждого клиента.
# В нее передается клиентский код. В цикле принимаемые сообщения от клиента 
# Декодируются из байтовой строки в строку методом decode(). 
# Затем сообщение выводиться на экран. При ошибке, соединение с клиентом закрывается: 
def handle(client):
    while True:
        try:
            # Прием сообщения от клиента
            message = client.recv(1024)
            # Отправка сообщения всем клиентам
            broadcast(message)
        except:
            # Удаление клиента при ошибке или отключении
            
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} покинул чат!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Создадим функцию для прослушивания входящих соединений.
# В основном цикле программа принимает входящие соединения от клиентов чз метод .accept()
# Сервер выводит сообщение о подключении нового клиента.
# Затем для каждого клиента создается новый поток, в котором выполняется функция handle 
# И после запускается поток:
def receive():
    while True:
        # Подключение клиента
        client, address = server.accept()
        print(f'Подключено: {str(address)}')

        # Запрос ника у клиента
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        
        # Отправка приветствия
        welcome = f'Добро пожаловать, {nickname}!'.encode('utf-8')
        client.send(welcome)
        broadcast(f'{nickname} присоединился к чату!'.encode('utf-8'))

        # Сохранение клиента и запуск обработчика в отдельном потоке
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
# Запуск сервера
print("Сервер запущен!...")
receive()
