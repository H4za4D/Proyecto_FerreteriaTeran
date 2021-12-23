import logging
import threading
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pyodbc import IntegrityError

from Main.TOOLS.Tools import MessageBX, Crud_DB, SimpleTools

logging.basicConfig(level=logging.DEBUG, format="%(threadName)-s %(message)s")


class HiloPutDetailDirc(threading.Thread):
    def __init__(self, cmbo_box):
        super().__init__()
        self.cmbo_box = cmbo_box
        self.types = ["Av", "Jr", "Calle", "Psje"]

    def run(self):
        logging.info("Insercion de calles")
        self.cmbo_box.addItems(self.types)
        logging.info("Insercion exitosa")




class Client:
    def __init__(self, mainWindow, cb_tipo, tb_view, btnnuevo,
                 btnmodificar, btneliminar, btnguardar, btnBuscar, btnCancelarBus , rd_poNombre, rd_porDni, ln_dni,
                 ln_nombre, ln_aPaterno, ln_aMaterno, ln_telefono, ln_mnombreDir, ln_numeroDir, ln_cProblado,
                 ln_buscarCli
                 ):
        self.mainWindowCli = mainWindow

        # ComboBox
        self.cb_tipo = cb_tipo
        self.tb_viewCli = tb_view

        self.tb_viewCli.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # Se estable la politica del men
        self.tb_viewCli.customContextMenuRequested.connect(
            self.menuAccionClientes)  # Al presionar anticlick este llamara al menu

        # Botones
        self.btnnuevo = btnnuevo
        self.btnmodificar = btnmodificar
        self.btneliminar = btneliminar
        self.btnguardar = btnguardar
        self.btnBuscar = btnBuscar
        self.btnCancela = btnCancelarBus

        """Radio buttons que escogen si la busqueda es por DNI o por Nombre y Apellido"""
        self.rd_poNombre = rd_poNombre
        self.rd_porDni = rd_porDni
        #Coneexion con la funcion de busqueda
        self.rd_poNombre.toggled.connect(self.changeValue)
        self.rd_porDni.toggled.connect(self.changeValue)

        self.ln_buscaCli = ln_buscarCli

        """Conexion con los funciones respectivas de cada boton"""
        self.btnnuevo.clicked.connect(self.newClient)
        self.btnguardar.clicked.connect(self.saveClient)
        self.btnmodificar.clicked.connect(self.modifyClient)
        self.btneliminar.clicked.connect(self.deleteClient)
        self.btnBuscar.clicked.connect(self.searchCliente)
        self.btnCancela.clicked.connect(self.actualizarTabla)

        self.ln_dni = ln_dni
        self.ln_nombre = ln_nombre
        self.ln_aPaterno = ln_aPaterno
        self.ln_aMaterno = ln_aMaterno
        self.ln_telefono = ln_telefono
        self.ln_nombreDir = ln_mnombreDir
        self.ln_numeroDir = ln_numeroDir
        self.ln_cProblado = ln_cProblado

        # Lista que contendra todos lineEDIT a revisar
        self.__list_LineEditWidgets = [self.ln_dni, self.ln_nombre, self.ln_aPaterno, self.ln_aMaterno,
                                       self.ln_telefono,
                                       self.ln_nombreDir, self.ln_numeroDir, self.ln_cProblado]

        # Lista que contendra todos ComboBox a revisar
        self.__list_ComboBoxWidgets = [self.cb_tipo]
        # Crea una instancia de la clase personalizada MSBOX(cuadros de dialogo)

        # Establecer los tipos de direcciones
        _hil = HiloPutDetailDirc(self.cb_tipo)
        _hil.start()
        _hil.join()
        # Bloquear las entradas
        self.enabled_Entries(True)

        # Mostrar todos los clientes
        self.mostrarClientes(self.tb_viewCli)

        self.mode = None #Necesario para los radio botons

    def enabled_Entries(self, bool):

        self.ln_dni.setReadOnly(bool)
        self.ln_nombre.setReadOnly(bool)
        self.ln_aPaterno.setReadOnly(bool)
        self.ln_aMaterno.setReadOnly(bool)
        self.ln_telefono.setReadOnly(bool)
        self.ln_nombreDir.setReadOnly(bool)
        self.ln_numeroDir.setReadOnly(bool)
        self.ln_cProblado.setReadOnly(bool)


    """Definir variables cuando los radiobuttones son marcados"""

    def changeValue(self):
        if self.rd_porDni.isChecked():
            self.mode = "dni"
        if self.rd_poNombre.isChecked():
            self.mode = "nombre"

        #logging.info(f"Valor {self.mode.upper()}")

    def searchCliente(self):
        ms_bx = MessageBX()
        cn = Crud_DB()

        next = None

        if self.mode == "" or self.mode == "":
            ms_bx.setTxt("Error",
                         f"No haz seleccionado el modo de busqueda")
            ms_bx.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
            ms_bx.exec_()
        else:
            q = ""
            prmt = ()

            if self.mode == "dni":
                if self.ln_buscaCli.text() == "":
                    ms_bx.setTxt("Error",
                                 f"Campo de busqueda vacio")
                    ms_bx.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                    ms_bx.exec_()
                    next = False

                else:
                    q = "SELECT * FROM Cliente WHERE Dni = ?"
                    prmt = (self.ln_buscaCli.text(), )
                    next = True

            elif self.mode == "nombre":
                try:
                    full_name = self.ln_buscaCli.text().split(" ")

                    AP = full_name[0]
                    AM = full_name[1]

                    q = "SELECT * FROM Cliente WHERE Apell_Paterno = ? and Apell_Materno = ?"
                    prmt = (AP, AM)

                    next = True


                except IndexError:
                    ms_bx.setTxt("Error", "Campo No valido")
                    ms_bx.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                    ms_bx.exec_()

                    next = False

            if next:

                try:
                    result = cn.runQuery(q, prmt, select = True)

                    if result:
                        fila = 0

                        for rowCliente in result:
                            self.tb_viewCli.setRowCount(fila + 1)
                            self.tb_viewCli.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(rowCliente[0])))
                            self.tb_viewCli.setItem(fila, 1, QtWidgets.QTableWidgetItem(rowCliente[1]))
                            self.tb_viewCli.setItem(fila, 2, QtWidgets.QTableWidgetItem(rowCliente[2]))
                            self.tb_viewCli.setItem(fila, 3, QtWidgets.QTableWidgetItem(rowCliente[3]))
                            self.tb_viewCli.setItem(fila, 4, QtWidgets.QTableWidgetItem(rowCliente[4]))
                            self.tb_viewCli.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(rowCliente[5])))
                            fila += 1
                    else:
                        ms_bx.setTxt("Error",
                                     f"No se encontraron resultados")
                        ms_bx.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                        ms_bx.exec_()

                except Exception as e:
                    ms_bx.setTxt("Error", f"Informar al desarrollador\n{type(e).__name__}\n{e.__str__()}")
                    ms_bx.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                    ms_bx.exec_()

        del ms_bx, cn



    def newClient(self):
        """Se bloquea los botones"""
        self.btnmodificar.setEnabled(False)
        self.btneliminar.setEnabled(False)

        self.enabled_Entries(False)

    def saveClient(self):
        msbox = MessageBX()
        # Crea uns instancia de la clase que controla la base de datos
        conx = Crud_DB()
        ST = SimpleTools()

        if not ST.verifyEmties(self.__list_LineEditWidgets, list_lineEdit=True) or not ST.verifyEmties(
                self.__list_ComboBoxWidgets, list_comboBox=True):

            QMessageBox().warning(None, "Aviso", "Datos Incompletos\nPor favor rellena todos los campos",
                                  QMessageBox.Ok)

            for widge in self.__list_LineEditWidgets:
                widge.clear()



        else:
            """Se crea 2 variables, la primera es una lista vacia, la segunda es una variable que contendra un booleano
                    si al verificar los campos el metodo retorna un false y una lista con los indices de los datos
                    erroneos los cuales se verificaran más adelante"""

            self.ln_verifiAlpha = [self.ln_nombre, self.ln_aPaterno, self.ln_aMaterno,
                                   self.ln_nombreDir, self.ln_cProblado]

            self.ln_verifiNum = [self.ln_dni, self.ln_telefono]

            self._areAlpha, self.indexsAlpha = ST.verifyLnAlpha(self.ln_verifiAlpha)

            #print(self.indexsAlpha)

            self._areNumer, self.indexsNume = ST.verifyLnNumeric(self.ln_verifiNum)

            #print(self.indexsNume)

            if not self._areAlpha:
                bad_data = ""

                for inx in self.indexsAlpha:
                    bad_data += (str(self.ln_verifiAlpha[inx].text()) + ", ")

                QMessageBox().warning(None, "Aviso", f"Los datos \'{bad_data}\' no son alfabeticos", QMessageBox.Ok)

            else:
                if not self._areNumer:
                    bad_numData = ""

                    for inx in self.indexsNume:
                        bad_numData += (str(self.ln_verifiNum[inx].text()) + ", ")

                    QMessageBox().warning(None, "Aviso", f"Los datos \'{bad_numData}\' no son Numéricos",
                                          QMessageBox.Ok)



                else:
                    if len(self.ln_telefono.text()) != 9:
                        QMessageBox().warning(None, "Aviso",
                                              f"El número telefonico no debe ser menor o mayor a los 9 digitos ",
                                              QMessageBox.Ok)

                    else:
                        if len(self.ln_dni.text()) != 8:
                            QMessageBox().warning(None, "Aviso",
                                                  f"El número Dni no debe ser menor o mayor a los 8 digitos ",
                                                  QMessageBox.Ok)
                        else:
                            try:
                                # Unir la todos los componentes de direccion en 1 solo
                                self.addres = str(self.cb_tipo.currentText()) + "_" + self.ln_nombreDir.text() + "_" + str(
                                    self.ln_numeroDir.text()) + "_" + self.ln_cProblado.text()
                                query = "INSERT INTO Cliente VALUES(?,?,?,?,?,?)"
                                prmt = (self.ln_dni.text(), self.ln_nombre.text(), self.ln_aPaterno.text(),
                                        self.ln_aMaterno.text(), self.addres, self.ln_telefono.text())

                                result = conx.runQuery(query, prmt)

                                if result:
                                    msbox.setTxt("Exito", f"El cliente {self.ln_nombre.text()} se añadio con exito.")
                                    msbox.insertIcon("Imagenes/accept.ico", QMessageBox.Information)
                                    msbox.exec_()

                                    for wid in self.__list_LineEditWidgets:
                                        wid.clear()

                                    self.btnmodificar.setEnabled(True)
                                    self.btneliminar.setEnabled(True)

                            except IntegrityError:
                                msbox.setTxt("Error",
                                             f"Error Critico\n El DNI {self.ln_dni.text()} ya se encuentra registrado")
                                msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                                msbox.exec_()

                            except Exception as e:
                                msbox.setTxt("Error",
                                             f"Error Critico\nInformar al desarrollador\nError:{type(e).__name__}\n{e.__str__()}")
                                msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                                msbox.exec_()
            self.actualizarTabla()

            del msbox, conx  # Para no ocupar la memoria se elimina las ainstancias """

    def modifyClient(self):
        msbox = MessageBX()
        # Crea uns instancia de la clase que controla la base de datos
        conx = Crud_DB()
        ST = SimpleTools()

        if not ST.verifyEmties(self.__list_LineEditWidgets, list_lineEdit=True) or not ST.verifyEmties(
                self.__list_ComboBoxWidgets, list_comboBox=True):

            QMessageBox().warning(None, "Aviso", "Datos Incompletos\nPor favor rellena todos los campos",
                                  QMessageBox.Ok)

            for widge in self.__list_LineEditWidgets:
                widge.clear()



        else:
            """Se crea 2 variables, la primera es una lista vacia, la segunda es una variable que contendra un booleano
                    si al verificar los campos el metodo retorna un false y una lista con los indices de los datos
                    erroneos los cuales se verificaran más adelante"""

            self.ln_verifiAlpha = [self.ln_nombre, self.ln_aPaterno, self.ln_aMaterno,
                                   self.ln_nombreDir, self.ln_cProblado]

            self.ln_verifiNum = [self.ln_dni, self.ln_telefono]

            self._areAlpha, self.indexsAlpha = ST.verifyLnAlpha(self.ln_verifiAlpha)

            #print(self.indexsAlpha)

            self._areNumer, self.indexsNume = ST.verifyLnNumeric(self.ln_verifiNum)

            #print(self.indexsNume)

            if not self._areAlpha:
                bad_data = ""

                for inx in self.indexsAlpha:
                    bad_data += (str(self.ln_verifiAlpha[inx].text()) + ", ")

                QMessageBox().warning(None, "Aviso", f"Los datos \'{bad_data}\' no son alfabeticos", QMessageBox.Ok)

            else:
                if not self._areNumer:
                    bad_numData = ""

                    for inx in self.indexsNume:
                        bad_numData += (str(self.ln_verifiNum[inx].text()) + ", ")

                    QMessageBox().warning(None, "Aviso", f"Los datos \'{bad_numData}\' no son Numéricos",
                                          QMessageBox.Ok)



                else:
                    if len(self.ln_telefono.text()) != 9:
                        QMessageBox().warning(None, "Aviso",
                                              f"El número telefonico no debe ser menor o mayor a los 9 digitos ",
                                              QMessageBox.Ok)

                    else:
                        if len(self.ln_dni.text()) != 8:
                            QMessageBox().warning(None, "Aviso",
                                                  f"El número Dni no debe ser menor o mayor a los 8 digitos ",
                                                  QMessageBox.Ok)
                        else:
                            time.sleep(0.5)

                            self.addres = str(self.cb_tipo.currentText()) + "_" + self.ln_nombreDir.text() + "_" + str(
                                self.ln_numeroDir.text()) + "_" + self.ln_cProblado.text()

                            self.params = (self.ln_nombre.text(), self.ln_aPaterno.text(), self.ln_aMaterno.text(),self.addres,
                                           self.ln_telefono.text(), self.ln_dni.text())

                            try:

                                query = """
                                UPDATE Cliente SET Nombre = ?, Apell_Paterno = ?, Apell_Materno=?,
                                Direccion = ?, Telefono =? WHERE Dni = ? """
                                param = self.params
                                result = conx.runQuery(query, parameters=param, select=False)

                                if result:
                                    msbox.setTxt("Exito",
                                                 f"¡La Cliente {self.ln_nombre.text()} ha sido actualizado con exito!")
                                    msbox.insertIcon("../Imagenes/accept.ico", QtWidgets.QMessageBox.Information)
                                    msbox.exec_()

                                    for widge in self.__list_LineEditWidgets:
                                        widge.clear()

                                    # Se Habilita  los botones
                                    self.btnmodificar.setEnabled(True)
                                    self.btneliminar.setEnabled(True)

                                    # Actualizar la tabla
                                    self.actualizarTabla()



                            except Exception as e:
                                msbox.setTxt("Error", f"Informar al desarrollador\n{e.__str__()}")
                                msbox.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                                msbox.exec_()
        del conx, msbox

    def deleteClient(self):
        dialogos = MessageBX()
        conexion = Crud_DB()
        ST = SimpleTools()

        cod = self.ln_dni.text()

        if cod != "":
            pregunta = QtWidgets.QMessageBox().warning(None, "Aviso",
                                                       f"¿Desea eliminar el Cliente {self.ln_nombre.text()}?",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.Yes)

            try:
                if pregunta == QtWidgets.QMessageBox.Yes:
                    query = "DELETE FROM Cliente WHERE Dni = ? "
                    paramt = (cod,)

                    result = conexion.runQuery(query, paramt, select=False)

                    if result:
                        try:
                            dialogos.setTxt("Exito", f"¡El Cliente {self.ln_nombre.text()} fue eliminada con exito!")
                            dialogos.insertIcon("../Imagenes/accept.ico", QtWidgets.QMessageBox.Information)
                            dialogos.exec_()

                            self.actualizarTabla()
                            self.btnguardar.setEnabled(True)
                            self.btnnuevo.setEnabled(True)

                        except Exception as e:
                            dialogos.setTxt("Error", f"Informar al desarrollador\n{e.__str__()}")
                            dialogos.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                            dialogos.exec_()
            except IntegrityError:
                dialogos.setTxt("Aviso", f"Cliente  no se pudo eliminar\nRazón: El cliente esta asociado a un pedido.")
                dialogos.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                dialogos.exec_()


        else:
            dialogos.setTxt("Error", "No haz seleccionado un item")
            dialogos.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
            dialogos.exec_()

        for widget in self.__list_LineEditWidgets:
            widget.clear()

    def actualizarTabla(self):
        self.tb_viewCli.clearContents()

        self.mostrarClientes(self.tb_viewCli)

    def mostrarClientes(self, table):
        conx = Crud_DB()
        query = "SELECT * FROM Cliente"
        # Obtenemos las categorias de la base de datos
        result = conx.runQuery(query, (), select=True)

        fila = 0

        for rowCliente in result:
            table.setRowCount(fila + 1)
            table.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(rowCliente[0])))
            table.setItem(fila, 1, QtWidgets.QTableWidgetItem(rowCliente[1]))
            table.setItem(fila, 2, QtWidgets.QTableWidgetItem(rowCliente[2]))
            table.setItem(fila, 3, QtWidgets.QTableWidgetItem(rowCliente[3]))
            table.setItem(fila, 4, QtWidgets.QTableWidgetItem(rowCliente[4]))
            table.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(rowCliente[5])))

            fila += 1

        del conx

    def menuAccionClientes(self, posicition):
        self.menu = QtWidgets.QMenu()

        itemsGroup = QtWidgets.QActionGroup(self.mainWindowCli)
        itemsGroup.setExclusive(True)

        self.menu.addAction(QtWidgets.QAction("Seleccionar Fila", itemsGroup))

        itemsGroup.triggered.connect(self.seleccionarFilaClientes)
        self.menu.exec_(self.tb_viewCli.viewport().mapToGlobal(posicition))

    def seleccionarFilaClientes(self):

        conx = Crud_DB()
        msbox = MessageBX()

        self.enabled_Entries(False)
        self.ln_dni.setReadOnly(True)

        self.btnnuevo.setEnabled(False)
        self.btnguardar.setEnabled(False)

        conx = Crud_DB()
        itm = []  # Lista que contendram los items seleccionados
        for item in self.tb_viewCli.selectedItems():  # Con for se recorre la fila seleccionada
            itm.append(item.text())  # Se agraga cada item pero convirtiendolo a un string

        #print(itm)

        self.ln_dni.setText(itm[0])
        self.ln_nombre.setText(itm[1])
        self.ln_aPaterno.setText(itm[2])
        self.ln_aMaterno.setText(itm[3])
        self.ln_telefono.setText(itm[5])

        try:

            totalDir = conx.runQuery(query="SELECT Direccion FROM Cliente WHERE Dni = ?", parameters=(str(itm[0]),),
                                     select=True)[0]

            parts_addres = str(totalDir[0]).split("_")

            self.ln_nombreDir.setText(parts_addres[1])
            self.ln_numeroDir.setText(str(parts_addres[2]))
            self.ln_cProblado.setText(parts_addres[3])
            # self.ln_mnombreDir.setText(parts_addres[])
            self.btnmodificar.setEnabled(True)
            self.btneliminar.setEnabled(True)



        except Exception as e:
            pass
            #msbox.setTxt("Error",
            #             f"Error Critico\nInformar al desarrollador\nError:{type(e).__name__}\n{e.__str__()}")
            #msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
            #msbox.exec_()

        del conx, msbox
