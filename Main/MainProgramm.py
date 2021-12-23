import logging
import sys
import threading
from threading import Thread
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QWidget


from Main.Inicializador.Cargador import LoadSystem
from Main.LOGIN import Login_M

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-s) %(message)s')


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        # ========Inicializo el Qtime que este hara avanzar el progressBar
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(10)

        self.counter = 0
        self.total = 100

        self.load = LoadSystem()
        self.load.setupUi(self)

        # Cargando imagenes
        self.load.label.setPixmap(QtGui.QPixmap("Imagenes/fondo.png"))  # Fondo de pantalla
        self.load.label_3.setPixmap(QtGui.QPixmap("Imagenes/logo2_preview_rev_1.png"))  # Imagen de de fondo 2

    def loading(self):
        self.load.cargador.setValue(self.counter)

        if self.counter == (self.total - 80):
            self.load.label_4.setText("<strong>Iniciando....</strong>")
        elif self.counter == (self.total - 50):
            self.load.label_4.setText("Conectando al servidor..")
        elif self.counter == (self.total - 20):
            self.load.label_4.setText("Conectando a la base de datos...")
        elif self.counter == (self.total - 1):
            self.load.label_4.setText("Carga exitosa")

        elif self.counter == self.total:
            self.timer.stop()
            self.close()

            time.sleep(1)

            self.log = Log_Menu()
            self.log.show()


        self.counter += 1


"""Clase que inicializara el menú de Login"""


class Log_Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.startLogin()

    def startLogin(self):
        self.log = Login_M.Ui_Login_Menu()
        self.log.setupUi(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    sys.exit(app.exec_())
