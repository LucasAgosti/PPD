import socket
import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk

import random

from threading import Thread
from tkinter import Text, Scrollbar, Button, Label

from portConfig import PORT



class JogoDaVelha3D_GUI(tk.Frame):
    def __init__(self, master):

        super().__init__(master)

        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()
        self.configure_grid()
        self.configure(bg="#242424")


        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)

        # Estado do jogo

        if random.randint(0,100) > 50:
            self.current_player = "X"
        else:
            self.current_player = "O"
        # self.current_player = "X"
        self.gameIsResetted = False

        # Definições de tamanho e espaçamento
        button_size = 60
        space_between_matrices = 20
        padding_x = 50
        padding_y = 50

        # Criando os botões do tabuleiro
        self.buttons = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    x_position = x * button_size + padding_x
                    y_position = y * button_size + z * (3 * button_size + space_between_matrices) + padding_y
                    self.buttons[z][y][x] = Button(
                        master, text='',
                        width=button_size // 10,  # Converter de pixels para unidades de texto
                        height=button_size // 20,
                        command=lambda z=z, y=y, x=x: self.on_button_click(z, y, x, False)
                    )
                    self.buttons[z][y][x].place(x=x_position, y=y_position)

        # self.create_widgets()
        self.simbolo = ""

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((str(socket.gethostbyname(socket.gethostname())), PORT))

        t1 = Thread(target=self.checkForMessages)
        t1.start()

    def configure_grid(self):
        # self.grid_columnconfigure(0, weight=2)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)  # coluna do tabuleiro
        self.grid_columnconfigure(1, weight=0)  # espaço entre tabuleiro e chat
        self.grid_columnconfigure(2, weight=1)  # coluna do chat
        # self.grid_columnconfigure(2, pad=80)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

    def create_game_board(self):

        self.game_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.matrices = []
        for z in range(3):
            matrix = Matrix3x3(self.game_frame, lambda y, x, z=z: self.on_button_click(z, y, x, False))
            matrix.grid(row=z, column=0, pady=30, padx=30, sticky='nsew')
            self.matrices.append(matrix)
    def create_widgets(self):


        # Criando um frame para o chat
        self.chat_frame = tk.Frame(self, bg="#242424")
        self.chat_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(80, 20), pady=20)

        self.chat_label = ctk.CTkLabel(self.chat_frame, text="Chat:", font=("Arial", 20, "bold"), text_color="#FFFFFF")
        self.chat_label.grid(row=0, column=0, sticky="nw", padx=5, pady=(0, 5))

        self.chat_text = ctk.CTkTextbox(self.chat_frame, height=500, width=350, fg_color="#2B2B2B", text_color="#FFFFFF")
        self.chat_text.grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.chat_text.bind("<FocusIn>", lambda e: self.master.focus_set())

        self.chat_entry = ctk.CTkEntry(self.chat_frame, width=200, placeholder_text="Insira o texto", fg_color="#343638", border_color="#565B5E", text_color="#FFFFFF")
        self.chat_entry.grid(row=2, column=0, sticky="nw", padx=5, pady=5)

        self.send_button = ctk.CTkButton(self.chat_frame, text="Enviar", command=self.on_chat_send)
        self.send_button.grid(row=2, column=0, sticky="ne", padx=5, pady=5)

        self.giveup_button = ctk.CTkButton(self, text="Desistir", command=self.on_giveup_click)
        self.giveup_button.grid(row=3, column=1, sticky="se", padx=(80, 20), pady=40)

        self.reset_button = ctk.CTkButton(self, text="Resetar", command=self.reset_game)
        self.reset_button.grid(row=3, column=2, sticky="se", padx=(80, 20), pady=40)

    # def showResetButton(self):
    #     self.reset_button = Button(self.master, text="Resetar", command=self.reset_game)
    #     self.reset_button.place(x=650, y=720)

    def collapseResetButton(self):
        self.reset_button.destroy()

    def checkForMessages(self):
        while True:
            try:
                message = self.client.recv(2048).decode('utf-8')
                if len(str(message)) != 0:
                    self.onMessageReceived(message)
            except:
                x = 0

    def onMessageReceived(self, message):
        if message == "X" and self.simbolo == "":
            self.simbolo = "X"
        elif message == "O" and self.simbolo == "":
            self.simbolo = "O"
        else:
            if message[1] == ":":
                self.chat_text.insert(tk.END, message + '\n')
            elif message.split("|")[0] == "action":
                print(message)
                if self.current_player != "?":
                    self.on_button_click(int(message.split("|")[1]), int(message.split("|")[2]), int(message.split("|")[3]), True)
            elif message.split("|")[0] == "endGame":
                self.endGame()
            elif message.split("|")[0] == "reset":
                self.reset_game()
            elif message.split("|")[0] == "giveUp":
                if message.split("|")[1] == "X":
                    winner = "[X]"
                else:
                    winner = "[O]"
                self.endGame()
                self.chat_text.insert(tk.END, f"SISTEMA: O JOGADOR {winner} VENCEU DEVIDO À DESISTÊNCIA!" + '\n')
                self.client.send(f"endGame|SISTEMA: O JOGADOR {winner} VENCEU DEVIDO À DESISTÊNCIA!".encode('utf-8'))
                # self.reset_game()


    def reset_game(self):

        if self.gameIsResetted == False:
            for z in range(3):
                for y in range(3):
                    for x in range(3):
                        self.buttons[z][y][x]['text'] = ""
                        self.buttons[z][y][x]['state'] = tk.NORMAL
            if random.randint(0, 100) > 50:
                self.current_player = "X"
            else:
                self.current_player = "O"
            # self.current_player = "O"
            # self.collapseResetButton()

            #self.gameIsResetted = True

            self.client.send("reset|".encode('utf-8'))
            self.gameIsResetted = True

    def check_winner(self):
        # Todas as linhas possíveis
        lines = [
                    # Horizontais/verticais dentro das matrizes
                    [[z, y, x] for x in range(3)] for z in range(3) for y in range(3)
                ] + [
                    [[z, x, y] for x in range(3)] for z in range(3) for y in range(3)
                ] + [
                    [[z, x, y] for y in range(3)] for z in range(3) for x in range(3)
                ] + [
                    # Diagonais dentro das matrizes
                    [[z, 0, 0], [z, 1, 1], [z, 2, 2]] for z in range(3)
                ] + [
                    [[z, 0, 2], [z, 1, 1], [z, 2, 0]] for z in range(3)
                ] + [
                    # Diagonais entre as matrizes
                    [[0, 0, x], [1, 1, x], [2, 2, x]] for x in range(3)
                ] + [
                    [[0, 2, x], [1, 1, x], [2, 0, x]] for x in range(3)
                ] + [
                    [[0, x, 0], [1, x, 1], [2, x, 2]] for x in range(3)
                ] + [
                    [[0, x, 2], [1, x, 1], [2, x, 0]] for x in range(3)
                ] + [
                    # Diagonais principais
                    [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
                    [[0, 0, 2], [1, 1, 1], [2, 2, 0]],
                    [[0, 2, 0], [1, 1, 1], [2, 0, 2]],
                    [[0, 2, 2], [1, 1, 1], [2, 0, 0]]
                ] + [
                    # Diagonais verticais entre as matrizes
                    [[z, x, y] for z in range(3)] for x in range(3) for y in range(3)
                ]

        for line in lines:
            if self.same_symbol(*line):
                z, y, x = line[0]
                return self.buttons[z][y][x]['text']

        return None

    def same_symbol(self, *coords):
        # Pega o símbolo da primeira coordenada
        symbol = self.buttons[coords[0][0]][coords[0][1]][coords[0][2]]['text']
        # Retorna False se o símbolo estiver vazio ou se algum dos outros símbolos for diferente
        return symbol and all(self.buttons[z][y][x]['text'] == symbol for z, y, x in coords)

    def on_button_click(self, z, y, x, serverAction):
        if self.gameIsResetted:
            self.gameIsResetted = False

        if self.current_player != "?":
            playersTurn = self.simbolo == self.current_player

            if not serverAction and playersTurn:
                actionMessage = "action" + "|" + str(z) + "|" + str(y) + "|" + str(x)
                self.client.send(actionMessage.encode('utf-8'))

            # Coloca o símbolo no botão se ele estiver vazio
            if not self.buttons[z][y][x]['text'] and (playersTurn or serverAction):
                self.buttons[z][y][x]['text'] = self.current_player
                self.toggle_player()

            # Após cada jogada, verifica se alguém ganhou
            winner = self.check_winner()
            if winner and self.current_player != "?":
                self.endGame()
                self.chat_text.insert(tk.END, f"SISTEMA: O JOGADOR {winner} VENCEU!" + '\n')
                self.client.send(f"endGame|SISTEMA: O JOGADOR {winner} VENCEU!".encode('utf-8'))  # Você pode substituir isso por qualquer ação desejada
                # ... (Adicionalmente, você pode adicionar lógica para resetar o jogo ou outras ações)

    def endGame(self):
        self.current_player = "?"
        # self.showResetButton()

    def toggle_player(self):
        """Alterna entre os jogadores."""
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def on_giveup_click(self):
        # Lógica de desistência
        if self.simbolo == "X":
            self.client.send("giveUp|O".encode('utf-8'))
            # self.chat_text.insert(tk.END, f"SISTEMA: O JOGADOR X VENCEU!" + '\n')

        else:
            self.client.send("giveUp|X".encode('utf-8'))
            # self.chat_text.insert(tk.END, f"SISTEMA: O JOGADOR O VENCEU!" + '\n')

        # self.giveup_button.grid(row=1, column=2, sticky="se", padx=20, pady=40)  # Modificado para grid



    def on_chat_send(self):
        # Lógica de envio de mensagem
        message = self.simbolo + ": " + self.chat_entry.get()
        if message:
            self.client.sendall(message.encode('utf-8'))
            self.chat_entry.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Jogo da Velha 3D')
    root.geometry('700x800')
    root.configure(bg="#242424")

    app = JogoDaVelha3D_GUI(root)
    root.mainloop()
