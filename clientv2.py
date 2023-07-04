import socket
import threading

class ChatClient:
    def __init__(self, nickname, ip, port):
        self.nickname = nickname
        self.ip = ip
        self.port = port
        self.server_socket = None

def start(self):
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client_socket.connect((self.ip, self.port))
    self.client_socket.sendall(self.nickname.encode("utf-8"))
    
    receive_thread = threading.Thread(target = self.receive_messages)
    receive_thread.start()
    
    while True:
        message = input()
        self.client_socket.sendall(message.encode("utf-8"))
        
def receive_messages(self):
    while True:
        try:
            message = self.client_socket.recv(1024).decode("utf-8")
            print(message)
        
        except Exception as e:
            print(f"Error occurred: {e}")
            break
        
if __name__ == "__main__":
    nickname = input("Enter your nickname: ")
    ip = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    
    chat_client = ChatClient(nickname, ip, port)
    chat_client.start()
            
            
    