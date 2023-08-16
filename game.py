import tkinter as tk
from tkinter import Text, Scrollbar, Button, Label, messagebox
from client import Client

class JogoDaVelha3D_GUI:
    def __init__(self, master, playerName, serverIp, serverPort):
        self.master = master
        master.title('Jogo da Velha 3D')
        master.geometry('800x800')
        self.client = Client(self, serverIp, serverPort)

        # Definições de tamanho e espaçamento
        button_size = 60
        space_between_matrices = 20
        
        # Estado do jogo
        self.current_player = "X"

        # Criando os botões do tabuleiro
        self.buttons = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    x_position = x * button_size
                    y_position = y * button_size + z * (3 * button_size + space_between_matrices)
                    self.buttons[z][y][x] = Button(
                        master, text='', 
                        width=button_size // 10,  # Converter de pixels para unidades de texto
                        height=button_size // 20, 
                        command=lambda z=z, y=y, x=x: self.on_button_click(z, y, x)
                    )
                    self.buttons[z][y][x].place(x=x_position, y=y_position)

        # Botão de desistência
        self.giveup_button = Button(master, text="Desistir", command=self.on_giveup_click)
        self.giveup_button.place(x=500, y=720)

        # Chat
        self.chat_label = Label(master, text="Chat:")
        self.chat_label.place(x=500, y=20)
        
        self.chat_text = Text(master, height=20, width=30)
        self.chat_text.place(x=500, y=50)
        
        # Prevenindo que o Text widget do chat seja clicável
        self.chat_text.bind("<FocusIn>", lambda e: self.master.focus_set())

        self.scrollbar = Scrollbar(master, command=self.chat_text.yview)
        self.scrollbar.place(x=760, y=50, height=400)
        
        self.chat_text.configure(yscrollcommand=self.scrollbar.set)
        
        self.chat_entry = tk.Entry(master, width=25)
        self.chat_entry.place(x=500, y=650)
        
        self.send_button = Button(master, text="Enviar", command=self.on_chat_send)
        self.send_button.place(x=680, y=645)

    def reset_game(self):
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    self.buttons[z][y][x]['text'] = ""
                    self.buttons[z][y][x]['state'] = tk.NORMAL
        self.turn = "X"

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

    def on_button_click(self, z, y, x):
        if not self.buttons[z][y][x]['text']:
            message = f"action={z},{y},{x}"
            self.client.sendMessage(message)

    def toggle_player(self):
        """Alterna entre os jogadores."""
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def on_giveup_click(self):
        # Lógica de desistência
        pass

    def on_chat_send(self):
        message = self.chat_entry.get()
        if message:
            server_message = f"message={message}"
            self.client.sendMessage(server_message)
            self.chat_text.insert(tk.END, f"Você: {message}" + '\n')
            self.chat_entry.delete(0, tk.END)

    def onMessageReceived(self, message):
        split_message = message.split('=')
        command = split_message[0]

        if command == 'action':
            z, y, x = map(int, split_message[1].split(','))
            self.buttons[z][y][x]['text'] = self.current_player
            self.toggle_player()
        elif command == 'message':
            self.chat_text.insert(tk.END, split_message[1] + '\n')

        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Jogo da Velha 3D", f"O jogador {winner} venceu!")
            self.reset_game()

if __name__ == '__main__':
    root = tk.Tk()
    app = JogoDaVelha3D_GUI(root, "Player1", "127.0.0.1", 8080)
    root.mainloop()
