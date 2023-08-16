import socket

class Client:
    def __init__(self, ui, server, port):
        self.ui = ui
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.initSocket()

    def initSocket(self):
        self.client.connect((str(self.server), int(self.port)))
        while True:
            message = self.client.recv(2048).decode('utf-8')
            if len(str(message)) != 0:
                self.ui.onMessageReceived(message)

    def sendMessage(self, msg):
        self.client.sendall(msg.encode('utf-8'))
