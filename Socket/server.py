import os
import socket
import threading

from portConfig import PORT


class Server:
    def __init__(self, port):
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = port
        self.ADDRESS = (self.HOST, int(self.PORT))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)

        self.color = 1

        # 1 = Blue \ 2 = Red
        self.turnColor = 1
        self.bluePlayer = None
        self.redPlayer = None

        self.players = []

        def send_action(action, playerId):
            for player in self.players:
                if playerId != player['player']:
                    print('Enviando ação para o player', player['player'], 'em', player['address'])
                    action_to_send = 'action=' + action
                    player['connection'].send(action_to_send.encode('utf-8'))

        def send_message(message):
            for player in self.players:
                message_to_send = message
                player['connection'].send(message_to_send.encode('utf-8'))

        def send_color_response(playerConnection):
            message_to_send = "color=%s" % str(self.color)
            playerConnection.send(message_to_send.encode('utf-8'))
            self.color = 2

        def end_game(colorWhoGaveUp):
            for player in self.players:
                msgToSend = "endGame=" + colorWhoGaveUp
                player['connection'].send(msgToSend.encode('utf-8'))

        def handle_players(connection, address, player):
            print('Jogador', player, 'conectado ao servidor pelo endereço:', address)

            print("\n\n" + str(player) + "\n\n")

            self.players.append({'player': player, 'connection': connection, 'address': address,
                                 'nickname': player})
            if player == 1:
                send_message("X")
            elif player == 2:
                send_message("O")

            while True:
                message = connection.recv(2048).decode('utf-8')
                if len(message) != 0:
                    send_message(message)

        def start():
            self.server.listen(2)
            for i in range(1, 3):  # Loop que estabelece a conexão dos jogadores com o server
                print('Servidor: aguardando a conexão do jogador ' + str(i) + "\n")

                connection, address = self.server.accept()

                player = i
                thread = threading.Thread(target=handle_players, args=(connection, address, player))
                thread.start()

        os.system('cls')
        start()

Server(PORT)
