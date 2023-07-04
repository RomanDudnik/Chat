import socket
import threading

class ChatServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.clients = []
        
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
    
        print(f"Chat server started on {self.ip}:{self.port}")
    
        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target = self.handle_client, args = (client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_name = client_socket.recv(1024).decode("utf-8")
        self.broadcast_message(f"{client_name} joined the chat!")
        self.clients.append((client_name, client_socket))
    
        while True:
            try:
                messege = client_socket.recv(1024).decode("utf-8")
            
                if messege:
                    self.broadcast_message(f"{client_name}: {messege}")
                else:
                    self.remove_client(client_name, client_socket)
                    break
            except Exception as e:
                print(f"Error occurred: {e}")
                self.remove_client(client_name, client_socket)
                break

    def remove_client(self, client_name, client_socket):
        self.clients.remove((client_name, client_socket))
        self.broadcast_message(f"{client_name} left the chat.")
        client_socket.close()
    
    def broadcast_message(self, message):
        for _, client_socket in self.clients:
            try:
                client_socket.sendall(message.encode("utf-8"))
            except Exception as e:
                print(f"Error occurred: {e}")
            
if __name__ == "__main__":
    ip = input("Enter server IP:")
    port = int(input("Enter server port:"))
    
    chat_server = ChatServer(ip, port)
    chat_server.start()