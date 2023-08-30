import socket
import game
import server
import client
import tkinter as tk
from tkinter import messagebox

def start():
    try:
        # Tentar iniciar como cliente
        client.start_client()
    except socket.error:
        # Se falhar, iniciar como servidor
        try:
            server.start_server()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar o servidor: {e}")

if __name__ == '__main__':
    start()
