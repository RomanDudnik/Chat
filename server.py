#!/bin/python3

# Серверная часть
# Импортируем необходимые модули: 
import socket
import threading

# Определяем константы для удобства:
HOST = 'ENTER YOUR IP'  # IP-адрес сервера
PORT = 55555            # Порт сервера

# Создадим сокет для приема входящих соединений.
# Зададим параметры сокета:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Создадим списки клиентов и их никнеймов:
clients = []
nicknames = []

# Sending Messages To All Connected Clients
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
            # Broadcasting Messages
            
            message = client.recv(1024).decode('utf-8')
            if message:
                broadcast(message)
        except:
            # Removing And Closing Clients
            
            # index = clients.index(client)
            # clients.remove(client)
            client.close()
            # nickname = nicknames[index]
            # broadcast('{} left!'.format(nickname).decode('utf-8'))
            # nicknames.remove(nickname)
            break

# Создадим функцию для прослушивания входящих соединений.
# В основном цикле программа принимает входящие соединения от клиентов чз метод .accept()
# Сервер выводит сообщение о подключении нового клиента.
# Затем для каждого клиента создается новый поток, в котором выполняется функция handle 
# И после запускается поток:
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()
