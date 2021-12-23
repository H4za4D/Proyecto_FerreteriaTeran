import os
import threading
import pyodbc
import random as rd

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Crypto.Hash import SHA256




class SimpleTools:
    def __init__(self):
        pass

    def hashPassword(self, passwd):
        hPass = SHA256.new(passwd.encode('utf-8'))
        return hPass.digest()

    def verifyEmties(self, data, list_lineEdit=False, list_comboBox=False):
        verif = False

        if list_lineEdit:  # Verifica LineEdit que estan en una lista
            count = 0
            for widget in data:
                if widget.text() == "":
                    count += 1

            if not count > 1:
                verif = True

        if list_comboBox:  # Verifica ComboBox que estan en una lista
            count = 0
            for widget in data:
                if widget.currentText() == "":
                    count += 1

            if not count > 1:
                verif = True

        return verif

    def verifyLnAlpha(self, lista):
        indicesA = []

        _isalpha = True
        count = 0

        for ind, wid in enumerate(lista):
            if not str(wid.text()).replace(" ","").isalpha():
                indicesA.append(ind)
                count += 1

        if count > 1:
            _isalpha = False

        return _isalpha, indicesA

    def verifyLnNumeric(self, lista):
        indicesN = []  # Lista que contendra los indices de los objetos erroneos

        _isnumeric = True
        count = 0

        for ind, wid in enumerate(lista):
            if not str(wid.text()).replace(" ","").isnumeric():
                indicesN.append(ind)
                count += 1

        if count > 1:
            _isnumeric = False

        return _isnumeric, indicesN  # Si la verificacion salio false este tambien devolvera la lista de indices


class Crud_DB():
    def __init__(self):
        super().__init__()

        self.__db = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-ABOMOKJ;DATABASE=FERRETERIA_TERAN;UID=sa;PWD=hazard50')
        self.__cursor = self.__db.cursor()

    def login(self, user, passw):
        access = False
        worker_type = ""
        username = ""


        #Se hashea la contraseña para luego mandarlo en la consulta
        has = SimpleTools().hashPassword(passwd=passw)
        # Se define la peticion hacia la base de datos
        query = "SELECT Usuario Usuario, Contrasena Constraseña, c.Nombre Cargo FROM DetallesUsuarios detalles INNER " \
                "JOIN Cargos c ON c.IdCargo = detalles.Cargo WHERE Usuario= ? AND Contrasena =? "

        # Ejecuta la consulta
        self.__cursor.execute(query, (user, has))

        # Obtenemos la fila de la consulta
        result = self.__cursor.fetchall()
        # Definimos la variable que contendra  el cargo del usuario
        worker_type = result[0][2]
        #Definimos el usuario que fue consultado en la base de datos
        username = result[0][0]
        # Se establece una condicion por si es que se encuentran los datos
        if result:
            access = True

        # Se guardar los cambios y  se cierra la base de datos
        self.__cursor.commit()
        self.__cursor.close()

        # Retorna el booleano confirmando el acceso y tambien se devuelve el tipo de trabajador y nombre de usuario
        return access, username, worker_type

    def runQuery(self, query, parameters, select=False):
        self.__result = None

        with self.__db as conn:
            if select:
                cursor = conn.cursor()
                # Guargamos los resultados
                self.__result = cursor.execute(query, parameters).fetchall()

            else:
                # Se crea un cursor sobre la base de datos
                cursor = conn.cursor()
                # Guargamos los resultados
                self.__result = cursor.execute(query, parameters)

                # Guardamos los cambios
                conn.commit()

        return self.__result

    def status_db(self):
        status = self.__cursor.execute("SELECT @@version")
        print(status.fetchone())


class MessageBX(QMessageBox):
    def __init__(self, ):
        super().__init__()

    def setTxt(self, title, msg):
        self.setWindowTitle(title)
        self.setText(msg)

    def insertIcon(self, ico, qIco):
        self.setIcon(qIco)
        self.setWindowIcon(QIcon(ico))

    def setButton(self):
        self.setStandardButtons(self.Yes | self.No)

    def connectFunction(self, target):
        self.buttonClicked.connect(target)



if __name__ == '__main__':
    l = Crud_DB()
    r = l.login("admin", "1234", "ADMINISTRADOR")
    print(r)
