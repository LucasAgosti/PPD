import socket
import threading

class Server:
    def __init__(self, port):
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = port
        self.ADDRESS = (self.HOST, int(self.PORT))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)

        self.players = []

        def send_action(action, playerId):
            for player in self.players:
                if playerId != player['player']:
                    action_to_send = 'action=' + action
                    player['connection'].send(action_to_send.encode('utf-8'))

        def send_message(message):
            for player in self.players:
                message_to_send = message
                player['connection'].send(message_to_send.encode('utf-8'))

        def send_player_info(playerConnection, playerNum):
            message_to_send = "player=" + str(playerNum)
            playerConnection.send(message_to_send.encode('utf-8'))

        def handle_players(connection, address, player):
            while True:
                message = connection.recv(2048).decode('utf-8')
                split_message = message.split('=')
                if split_message[0] == 'action':
                    move = split_message[1]
                    send_action(move, player)

        def start():
            self.server.listen(2)
            for i in range(1, 3):
                connection, address = self.server.accept()
                player = i
                send_player_info(connection, player)
                self.players.append({'player': player, 'connection': connection, 'address': address})
                thread = threading.Thread(target=handle_players, args=(connection, address, player))
                thread.start()

        start()
