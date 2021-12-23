# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from Main.TOOLS.Tools import Crud_DB, MessageBX
from Main.PRINCIPAL import Menu_Principal, Menu_Principal_Caja


class Ui_Login_Menu(object):
    def setupUi(self, Login_Menu):

        self.__window = Login_Menu
        Login_Menu.setObjectName("Login_Menu")
        Login_Menu.resize(316, 339)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/iconos/Principal.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login_Menu.setWindowIcon(icon)
        Login_Menu.setStyleSheet("QPushButton{\n"
                                 "    \n"
                                 "    font: bold 14pt \"Roboto\";\n"
                                 "    border-radius:15px;\n"
                                 "    border:2px solid black;\n"
                                 "    color:rgb(255, 255, 255)\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:pressed { \n"
                                 "    background-color: rgb(32, 90, 143);\n"
                                 "    border-style: inset;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit{\n"
                                 "border-radius:15px\n"
                                 "}\n"
                                 "\n"
                                 "\n"
                                 "\n"
                                 "")
        self.fondo_pantalla = QtWidgets.QLabel(Login_Menu)
        self.fondo_pantalla.setGeometry(QtCore.QRect(0, 0, 321, 341))
        self.fondo_pantalla.setText("")
        self.fondo_pantalla.setPixmap(QtGui.QPixmap(":/iconos/logo_login.PNG"))
        self.fondo_pantalla.setScaledContents(True)
        self.fondo_pantalla.setObjectName("fondo_pantalla")
        self.lbl_usuario = QtWidgets.QLabel(Login_Menu)
        self.lbl_usuario.setGeometry(QtCore.QRect(130, 60, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lbl_usuario.setFont(font)
        self.lbl_usuario.setStyleSheet("color:rgb(255, 255, 255);\n"
                                       "font: bold 12pt \"Roboto\";")
        self.lbl_usuario.setObjectName("lbl_usuario")
        self.lbl_passwo = QtWidgets.QLabel(Login_Menu)
        self.lbl_passwo.setGeometry(QtCore.QRect(110, 140, 101, 21))
        self.lbl_passwo.setStyleSheet("color:rgb(255, 255, 255);\n"
                                      "font: bold 12pt \"Roboto\";")
        self.lbl_passwo.setObjectName("lbl_passwo")
        self.btn_ingresar = QtWidgets.QPushButton(Login_Menu)
        self.btn_ingresar.setGeometry(QtCore.QRect(90, 270, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_ingresar.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/iconos/login.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_ingresar.setIcon(icon1)
        self.btn_ingresar.setIconSize(QtCore.QSize(50, 50))
        self.btn_ingresar.setObjectName("btn_ingresar")

        # Conectar el boton con la funcion
        self.btn_ingresar.clicked.connect(self.log)

        self.entry_user = QtWidgets.QLineEdit(Login_Menu)
        self.entry_user.setGeometry(QtCore.QRect(80, 90, 181, 20))
        self.entry_user.setText("")
        self.entry_user.setAlignment(QtCore.Qt.AlignCenter)
        self.entry_user.setObjectName("entry_user")
        self.entry_password = QtWidgets.QLineEdit(Login_Menu)
        self.entry_password.setGeometry(QtCore.QRect(80, 180, 181, 20))
        self.entry_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.entry_password.setAlignment(QtCore.Qt.AlignCenter)
        self.entry_password.setObjectName("entry_password")
        self.lbl_ico = QtWidgets.QLabel(Login_Menu)
        self.lbl_ico.setGeometry(QtCore.QRect(80, 40, 51, 41))
        self.lbl_ico.setText("")
        self.lbl_ico.setPixmap(QtGui.QPixmap(":/iconos/user.png"))
        self.lbl_ico.setScaledContents(True)
        self.lbl_ico.setObjectName("lbl_ico")
        self.lbl_pss = QtWidgets.QLabel(Login_Menu)
        self.lbl_pss.setGeometry(QtCore.QRect(60, 130, 51, 41))
        self.lbl_pss.setText("")
        self.lbl_pss.setPixmap(QtGui.QPixmap(":/iconos/password.png"))
        self.lbl_pss.setScaledContents(True)
        self.lbl_pss.setObjectName("lbl_pss")
        self.lbl_titulo = QtWidgets.QLabel(Login_Menu)
        self.lbl_titulo.setGeometry(QtCore.QRect(70, 0, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_titulo.setFont(font)
        self.lbl_titulo.setStyleSheet("color:rgb(255, 255, 255)")
        self.lbl_titulo.setObjectName("lbl_titulo")

        self.retranslateUi(Login_Menu)
        QtCore.QMetaObject.connectSlotsByName(Login_Menu)

    def retranslateUi(self, Login_Menu):
        _translate = QtCore.QCoreApplication.translate
        Login_Menu.setWindowTitle(_translate("Login_Menu", "Sistema Ventas Ferreteria Teran"))
        self.lbl_usuario.setText(_translate("Login_Menu", "Usuario"))
        self.lbl_passwo.setText(_translate("Login_Menu", "Contraseña"))
        self.btn_ingresar.setText(_translate("Login_Menu", "Ingresar"))
        self.lbl_titulo.setText(_translate("Login_Menu", "INICIO SESION"))

    def log(self):

        bd = Crud_DB()
        msbox = MessageBX()

        if self.entry_user.text() == "" or self.entry_password.text() == "":
            msbox.setTxt("Ingreso a FerSystem Teran", "Falta datos!")
            msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
            msbox.exec_()
        else:
            try:
                acceso, user, self.__workerType = bd.login(self.entry_user.text(), self.entry_password.text())

                if acceso:
                    msbox.setTxt("Bienvenido", f"Credenciales Correctas\n{self.__workerType}")
                    msbox.insertIcon("Imagenes/accept.ico", QMessageBox.Information)
                    msbox.exec_()

                    self.entry_user.clear()
                    self.entry_password.clear()

                    self.__window.close()

                    # Se crea las instancias para iniciar el menu principal
                    self.__mainWindow = PrincipalMenu(self.__window, self.__workerType, user)
                    self.__mainWindow.show()



                else:
                    msbox.setTxt("Aviso", "Credenciales Incorrectas")
                    msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                    msbox.exec_()

            except Exception as e:
                msbox.setTxt("Aviso", "Credenciales Incorrectas")
                msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                msbox.exec_()


"""Clase que podrá iniciar la interfaz principal según el rol del usuario"""


class PrincipalMenu(QtWidgets.QMainWindow):
    def __init__(self, login_window, type, usern):
        self.__type = type
        self.__usern = usern
        self.__window = None

        self.c = login_window

        super().__init__()
        self.startPrincipal()

    def startPrincipal(self):
        # En el caso que el usuario sea cajero
        if self.__type == 'CAJERO':
            self.__window = Menu_Principal_Caja.Ui_SistemaVentas_Caja()
            self.__window.setupUi(self,self.c, self.__usern)


        # En el caso que el usuario sea Administrador o  vendedor
        else:
            self.__window = Menu_Principal.Ui_SistemaVentas()
            self.__window.setupUi(self, self.c, self.__usern, self.__type)

        # Bloquear la maximizacion de la ventana
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)