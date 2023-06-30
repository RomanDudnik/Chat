import socket
import threading

# Choosing Nickname
nickname = input("Enter your nickname: \n")

# client.connect(('91.200.148.112', 55555))
ip_addr = input ("Enter server IP: \n")
port = int(input("Enter server Port: \n"))

# Создаем сокет для подключения к серверу:
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключимся к серверу:
client.connect((ip_addr, port))

# Определим функцию для отправки сообщений.
# В цикле программа считывает сообщения от пользователя функцией input().
# Затем сообщение отправляется на сервер с помощью метода .send()
# Сообщение кодируется в байтовую кодировку методом encode().
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

# Определим функцию для приема сообщений от сервера.
# В цикле принимаются сообщения от сервера, декодируются из байтовой кодировки в строку
# И выводятся на экран. При ошибке соединение с сервером закрывается.
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Создадим два потока для отправки и приема сообщений:
write_thread = threading.Thread(target=write)
receive_thread = threading.Thread(target=receive)

# Запустим потоки:
write_thread.start()
receive_thread.start()
