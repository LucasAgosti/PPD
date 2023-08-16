import sys
from threading import Thread

from PySide2 import QtWidgets

from game import JogoDaVelha3D_GUI
from client import Client
from server import Server

class UserName(QtWidgets.QWidget):
    # ... (manter a estrutura original deste widget) ...

    def enterGame(self):
        self.ui = UI(self.userNameBox.text())
        self.client = Client(self.ui, self.serverIpBox.text(), self.serverPortBox.text())
        self.close()

    def hostGame(self):
        t1 = Thread(target=self.initServer)
        t1.start()
        t2 = Thread(target=self.initGame)
        t2.start()

    def initServer(self):
        self.server = Server(self.serverPortBox.text())

    def initGame(self):
        self.ui = UI(self.userNameBox.text())
        self.client = Client(self.ui, self.serverIpBox.text(), self.serverPortBox.text())
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UserName().show()
    sys.exit(app.exec_())
