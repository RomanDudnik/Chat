import socket
import threading

# Ввод данных для подключения к серверу
nickname = input("Введите ваш никнэйм: \n")
ip_addr = input ("Введите IP сервера: \n")
port = int(input("Введите Port сервера: \n"))

# Создаем сокет для подключения к серверу:
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключимся к серверу:
client.connect((ip_addr, port))

# Отправка ника на сервер
client.send(nickname.encode('utf-8'))

# Определим функцию для приема сообщений от сервера.
# В цикле принимаются сообщения от сервера, декодируются из байтовой кодировки в строку
# И выводятся на экран. При ошибке соединение с сервером закрывается.
def receive():
    while True:
        try:
            # Прием сообщения от сервера
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                # Если сервер запрашивает ник, отправляем его
                client.send(nickname.encode('utf-8'))
            else:
                # Выводим сообщеня в чат
                print(message)
        except:
            print("Ошибка подключения к серверу!!!")
            client.close()
            break
        
# Определим функцию для отправки сообщений.
# В цикле программа считывает сообщения от пользователя функцией input().
# Затем сообщение отправляется на сервер с помощью метода .send()
# Сообщение кодируется в байтовую кодировку методом encode().
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))


# Создадим два потока для отправки и приема сообщений:
write_thread = threading.Thread(target=write)
receive_thread = threading.Thread(target=receive)

# Запустим потоки:
write_thread.start()
receive_thread.start()
