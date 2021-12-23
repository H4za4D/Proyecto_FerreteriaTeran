import logging
import os
import threading
import time
import base64

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog
from pyodbc import IntegrityError

from Main.TOOLS.Tools import MessageBX, Crud_DB, SimpleTools
from Main.PRINCIPAL.Proveedor_registro import Ui_DetallesProveedor

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


class InizializeDtProv(QDialog):
    def __init__(self):
        super().__init__()

    def startWid(self):
        self.dtWind = Ui_DetallesProveedor()
        self.dtWind.setupUi(self)

        self.dtWind.btn_confirmar.clicked.connect(self.allOk)

        self.lineEdits = [self.dtWind.ln_ciudad, self.dtWind.ln_pais, self.dtWind.ln_nombreContacto,
                          self.dtWind.ln_cargoContacto,
                          self.dtWind.ln_correo]

        self.show()

        self.chargeData()

    def allOk(self):
        ST = SimpleTools()

        if not ST.verifyEmties(self.lineEdits, list_lineEdit=True):  # or not ST.verifyEmties(
            # self.__list_ComboBoxWidgets, list_comboBox=True):

            QMessageBox().warning(None, "Aviso", "Datos Incompletos\nPor favor rellena todos los campos",
                                  QMessageBox.Ok)

            for widge in self.lineEdits:
                widge.clear()

        else:
            line_edit =self.dtWind.ln_correo.text()

            if ".com" not in line_edit:
                QMessageBox().warning(None, "Error", "Correo invalido\nEjemplo:  spideverse@gmail.com", QMessageBox.Ok)
            else:
                if "@" not in line_edit:
                    QMessageBox().warning(None, "Error", "Correo invalido\nEjemplo:  spideverse@gmail.com",
                                          QMessageBox.Ok)

                else:
                    #print("paso la prueba")
                    all_word = self.dtWind.ln_ciudad.text() + "_" + self.dtWind.ln_pais.text() + "_" + self.dtWind.ln_nombreContacto.text() + "_" \
                               + self.dtWind.ln_cargoContacto.text() + "_" + self.dtWind.ln_correo.text()

                    ms_bx = MessageBX()
                    try:
                        with open("temporal.txt", "w+") as temporal:
                            temporal.write(str(all_word))

                        ms_bx.setTxt("Exito",
                                     f"Detalles establecidos")
                        ms_bx.insertIcon("Imagenes/accept.ico", QMessageBox.Information)
                        ms_bx.exec_()

                    except Exception as e:
                        ms_bx.setTxt("Error", f"Informar al desarrollador\n{e.__str__()}")
                        ms_bx.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                        ms_bx.exec_()

                    del ms_bx




    def chargeData(self):

        if os.path.exists("temporal.txt"):
            data = ""
            with open("temporal.txt", "r+") as t:
                data = t.read()

            if not data == "":
                data = data.split("_")

                self.dtWind.ln_ciudad.setText(data[0])
                self.dtWind.ln_pais.setText(data[1])
                self.dtWind.ln_nombreContacto.setText(data[2])
                self.dtWind.ln_cargoContacto.setText(data[3])
                self.dtWind.ln_correo.setText(data[4])


class Supplier:
    def __init__(self, mainWi, combo_box_A_productos ,cb_tipDir, tb_Provee, btnnuevo,
                 btnmodificar, btneliminar, btnguardar, btnBuscar, btnCancelarBus, btnmasDetalles, rd_porRuc, rd_porNombre, ln_ruc,
                 ln_nombre, ln_telefono, ln_nombreDir, ln_numeroDir, ln_departamento,
                 ln_buscarCli
                 ):
        self.mainWindowCli = mainWi

        # ComboBox
        self.cb_tipo = cb_tipDir
        self.tb_viewCli = tb_Provee

        #ComboBox del area de productos que sera de uso para actualizarlo despues de agregar un nuevo proveedor
        self.cb_proveed = combo_box_A_productos

        self.tb_viewCli.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # Se estable la politica del men
        self.tb_viewCli.customContextMenuRequested.connect(
            self.menuAccionClientes)  # Al presionar anticlick este llamara al menu

        # Botones
        self.btnnuevoP = btnnuevo
        self.btnmodificarP = btnmodificar
        self.btneliminarP= btneliminar
        self.btnguardarP = btnguardar
        self.btnBuscarP = btnBuscar
        self.btnCancelaP = btnCancelarBus
        self.btnmsDetalles = btnmasDetalles

        """Radio buttons que escogen si la busqueda es por DNI o por Nombre y Apellido"""
        self.rd_porRuc = rd_porRuc
        self.rd_porNombre = rd_porNombre
        #Coneexion con la funcion de busqueda
        self.rd_porRuc.toggled.connect(self.changeValue)
        self.rd_porNombre.toggled.connect(self.changeValue)

        self.ln_buscaCli = ln_buscarCli

        """Conexion con los funciones respectivas de cada boton"""

        self.btnnuevoP.clicked.connect(self.newSupplier)
        self.btnguardarP.clicked.connect(self.saveSupplier)
        self.btnmodificarP.clicked.connect(self.modifySupplier)
        self.btneliminarP.clicked.connect(self.deleteSupplier)
        self.btnBuscarP.clicked.connect(self.searchSupplier)
        self.btnCancelaP.clicked.connect(self.actualizarTabla)


        self.ln_rucP = ln_ruc
        self.ln_nombreP = ln_nombre
        self.ln_telefonoP = ln_telefono
        self.ln_nombreDirP = ln_nombreDir
        self.ln_numeroDirP = ln_numeroDir
        self.ln_departamentoP = ln_departamento

        # Lista que contendra todos lineEDIT a revisar
        self.__list_LineEditWidgets = [self.ln_rucP, self.ln_nombreP, self.ln_telefonoP, self.ln_nombreDirP,
                                       self.ln_numeroDirP,self.ln_departamentoP]

        # Lista que contendra todos ComboBox a revisar
        self.__list_ComboBoxWidgets = [self.cb_tipo]
        # Crea una instancia de la clase personalizada MSBOX(cuadros de dialogo)

        # Establecer los tipos de direcciones
        _hil = HiloPutDetailDirc(self.cb_tipo)
        _hil.start()
        _hil.join()

        del _hil

        detalleProve = InizializeDtProv()
        self.btnmsDetalles.clicked.connect(lambda: detalleProve.startWid())
        # Bloquear las entradas
        self.enabled_EntriesP(True)

        # Mostrar todos los clientes
        self.mostrarProveedores(self.tb_viewCli)

        self.modeP = None #Necesario para los radio botons

    def enabled_EntriesP(self, bool):

        self.ln_rucP.setReadOnly(bool)
        self.ln_nombreP.setReadOnly(bool)
        self.ln_telefonoP.setReadOnly(bool)
        self.ln_nombreDirP.setReadOnly(bool)
        self.ln_numeroDirP.setReadOnly(bool)
        self.ln_departamentoP.setReadOnly(bool)


    """Definir variables cuando los radiobuttones son marcados"""

    def changeValue(self):
        if self.rd_porRuc.isChecked():
            self.modeP = "ruc"
        if self.rd_porNombre.isChecked():
            self.modeP = "nombre"

        #logging.info(f"Valor {self.mode.upper()}")

    def searchSupplier(self):
        ms_bx = MessageBX()
        cn = Crud_DB()

        next = None

        if self.modeP == "" or self.modeP == "":
            ms_bx.setTxt("Error",
                         f"No haz seleccionado el modo de busqueda")
            ms_bx.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
            ms_bx.exec_()
        else:
            q = ""
            prmt = ()

            if self.modeP == "ruc":
                if self.ln_buscaCli.text() == "":
                    ms_bx.setTxt("Error",
                                 f"Campo de busqueda vacio")
                    ms_bx.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                    ms_bx.exec_()
                    next = False

                else:
                    q = "SELECT * FROM Proveedor WHERE RUC = ?"
                    prmt = (self.ln_buscaCli.text(), )
                    next = True

            elif self.modeP == "nombre":
                try:
                    full_name = self.ln_buscaCli.text()

                    q = "SELECT * FROM Proveedor WHERE Nombre= ?"
                    prmt = (full_name, )

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

    def newSupplier(self):
        """Se bloquea los botones"""
        self.btnmodificarP.setEnabled(False)
        self.btneliminarP.setEnabled(False)

        self.enabled_EntriesP(False)

    def saveSupplier(self):
        ms_box = MessageBX()
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
            """Primero se crea una lista que contiene los widgets necesarios para la verificacion, 
                Siguiendo se crea 2 variables que reciviran datos del método cerifyLnAlpha
                 la primera variable contiene un booleano y la segunda una lista de indices los cuales
                 son de aquellos datos erroneos los cuales se notificara mas adelante con una cuadro
                 de dialogo"""

            self.ln_verifiAlpha = [ self.ln_nombreP, self.ln_nombreDirP, self.ln_numeroDirP, self.ln_departamentoP]

            self.ln_verifiNum = [self.ln_rucP, self.ln_telefonoP]

            self._areAlpha, self.indexsAlpha = ST.verifyLnAlpha(self.ln_verifiAlpha)

            #print(self.indexsAlpha) #Solo para mostrar indices resultantes

            self._areNumer, self.indexsNume = ST.verifyLnNumeric(self.ln_verifiNum)

            #print(self.indexsNume)  #Solo para mostrar indices resultantes

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
                    if len(self.ln_telefonoP.text()) != 9:
                        QMessageBox().warning(None, "Aviso",
                                              f"El número telefonico no debe ser menor o mayor a los 9 digitos ",
                                              QMessageBox.Ok)

                    else:
                        if len(self.ln_rucP.text()) != 11:
                            QMessageBox().warning(None, "Aviso",
                                                  f"El número Ruc no debe ser menor o mayor a los 11 digitos ",
                                                  QMessageBox.Ok)
                        else:
                            if os.path.exists("temporal.txt"):
                                data = ""
                                with open("temporal.txt", "r+") as t:
                                    data = t.read()

                                if data == "":
                                    ms_box.setTxt("Error", f"Falta rellenar mas datos.")
                                    ms_box.insertIcon("../Imageneans/ccel.ico", QtWidgets.QMessageBox.Warning)
                                    ms_box.exec_()

                                else:
                                    data = data.split("_") #Con esto tendremos los demas campos para hacer el registro
                                    ciudad, pais, nContacto, cCargoConta, correo = data[0], data[1], data[2], data[3], data[4]

                                    try:
                                        """Se crea un Codigo poniendo primeramente los caracteres PT y 5 primeros digitos del RUC"""
                                        CdProvee = "TR" + str(self.ln_rucP.text())[:4]


                                        # Unir la todos los componentes de direccion en 1 solo
                                        self.addres = str(self.cb_tipo.currentText()) + "_" + self.ln_nombreDirP.text() + "_" + str(
                                            self.ln_numeroDirP.text()) + "_" + self.ln_departamentoP.text()


                                        query = "INSERT INTO Proveedor VALUES(?,?,?,?,?,?,?,?,?,?)"
                                        prmt = (self.ln_rucP.text(), self.ln_nombreP.text(),
                                                nContacto, cCargoConta, self.addres,ciudad,  self.ln_departamentoP.text(),
                                                pais, correo, self.ln_telefonoP.text())

                                        result = conx.runQuery(query, prmt)

                                        if result:
                                            ms_box.setTxt("Exito", f"El proveedor {self.ln_nombreP.text()} se añadio con exito.")
                                            ms_box.insertIcon("Imagenes/accept.ico", QMessageBox.Information)
                                            ms_box.exec_()

                                            for wid in self.__list_LineEditWidgets:
                                                wid.clear()

                                            with open("temporal.txt", "w") as t:
                                                pass

                                            # se actualiza el combo box
                                            self.updateComboBoxFromProducts()

                                    except IntegrityError:
                                        ms_box.setTxt("Error",
                                                     f"Error Critico\n El Proveedor {self.ln_nombreP.text()} ya se encuentra registrado")
                                        ms_box.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                                        ms_box.exec_()

                                    except Exception as e:
                                        ms_box.setTxt("Error",
                                                     f"Error Critico\nInformar al desarrollador\nError:{type(e).__name__}\n{e.__str__()}")
                                        ms_box.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                                        ms_box.exec_()


                            else:
                                ms_box.setTxt("Error",
                                              f"Falta rellenar Datos")
                                ms_box.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                                ms_box.exec_()

            self.actualizarTabla()
            self.btnmodificarP.setEnabled(True)
            self.btneliminarP.setEnabled(True)

            del ms_box, conx  # Para no ocupar la memoria se elimina las ainstancias """

    def modifySupplier(self):
        self.ln_rucP.setReadOnly(True)

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

            self.ln_verifiAlpha = [self.ln_nombreP, self.ln_nombreDirP, self.ln_numeroDirP,
                                   self.ln_departamentoP,]

            self.ln_verifiNum = [self.ln_telefonoP]

            self._areAlpha, self.indexsAlpha = ST.verifyLnAlpha(self.ln_verifiAlpha)

            print(self.indexsAlpha)

            self._areNumer, self.indexsNume = ST.verifyLnNumeric(self.ln_verifiNum)

            print(self.indexsNume)

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
                    if len(self.ln_telefonoP.text()) != 9:
                        QMessageBox().warning(None, "Aviso",
                                              f"El número telefonico no debe ser menor o mayor a los 9 digitos ",
                                              QMessageBox.Ok)

                    else:
                        if len(self.ln_rucP.text()) != 11:
                            QMessageBox().warning(None, "Aviso",
                                                  f"El número Dni no debe ser menor o mayor a los 8 digitos ",
                                                  QMessageBox.Ok)
                        else:
                            if os.path.exists("temporal.txt"):
                                data = ""
                                with open("temporal.txt", "r+") as t:
                                    data = t.read()

                                if data == "":
                                    msbox.setTxt("Error", f"Falta rellenar mas datos.")
                                    msbox.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                                    msbox.exec_()

                                else:
                                    #Cod_Necesario para la actualizacion
                                    #CdProveePrincipal = "TR" + str(self.ln_rucP.text())[:4]


                                    data = data.split("_")  # Con esto tendremos los demas campos para hacer el registro
                                    ciudad, pais, nContacto, cCargoConta, correo = data[0], data[1], data[2], data[3], \
                                                                                   data[4]
                                    time.sleep(0.5)

                                    self.addres = str(self.cb_tipo.currentText()) + "_" + self.ln_nombreDirP.text() + "_" + str(
                                        self.ln_numeroDirP.text()) + "_" + self.ln_departamentoP.text()

                                    self.params = (self.ln_nombreP.text(),nContacto, cCargoConta,
                                                   self.addres, ciudad, self.ln_departamentoP.text(),
                                                   pais, correo, self.ln_telefonoP.text(), self.ln_rucP.text())

                                    try:

                                        query = """
                                        UPDATE Proveedor SET Nombre = ?, 
                                        NombreContacto = ?, CargoContacto=?,
                                        Direccion = ?, Ciudad =?,Departamento = ?,  Pais =?, Correo =?, Telefono =? WHERE RUC = ? """

                                        param = self.params
                                        result = conx.runQuery(query, parameters=param, select=False)

                                        if result:
                                            msbox.setTxt("Exito",
                                                         f"¡La Proveedor {self.ln_nombreP.text()} ha sido actualizado con exito!")
                                            msbox.insertIcon("../Imagenes/accept.ico", QtWidgets.QMessageBox.Information)
                                            msbox.exec_()

                                            for widge in self.__list_LineEditWidgets:
                                                widge.clear()

                                            # Se Habilita  los botones
                                            self.btnnuevoP.setEnabled(True)
                                            self.btnguardarP.setEnabled(True)

                                            # Actualizar la tabla
                                            self.actualizarTabla()

                                            with open("temporal.txt", "w") as temporal:
                                                pass

                                            # Actualizar el combo box
                                            self.updateComboBoxFromProducts()



                                    except Exception as e:
                                        msbox.setTxt("Error", f"Informar al desarrollador\n{e.__str__()}")
                                        msbox.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                                        msbox.exec_()
        del conx, msbox

    def deleteSupplier(self):
        dialogos = MessageBX()
        conexion = Crud_DB()
        ST = SimpleTools()

        cod = self.ln_rucP.text()

        if cod != "":
            pregunta = QtWidgets.QMessageBox().warning(None, "Aviso",
                                                       f"¿Desea eliminar el proveedor {self.ln_nombreP.text()}?",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.Yes)

            if pregunta == QtWidgets.QMessageBox.Yes:
                try:
                    query = "DELETE FROM Proveedor WHERE RUC = ? "
                    paramt = (cod,)

                    result = conexion.runQuery(query, paramt, select=False)

                    if result:
                        dialogos.setTxt("Exito", f"¡El Proveedor {self.ln_nombreP.text()} fue eliminada con exito!")
                        dialogos.insertIcon("../Imagenes/accept.ico", QtWidgets.QMessageBox.Information)
                        dialogos.exec_()

                        self.actualizarTabla()

                        # Actualizar el combo box
                        self.updateComboBoxFromProducts()


                except IntegrityError:
                    """Esta exception controlara el FK_ osea sql server no permit eliminar proveedores que esten 
                                       associados a un producto"""


                    dialogos.setTxt("Error", f"No se puede elminar el proveedor porque esta asociado a un producto\n"
                                             f"Solucion:\n\t->Elimine el producto o cambiele el proveedor")
                    dialogos.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                    dialogos.exec_()

                except Exception as e :
                    dialogos.setTxt("Error", f"Informar al desarrollador\n{type(e).__name__}{e.__str__()}")
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

        self.mostrarProveedores(self.tb_viewCli)

    def mostrarProveedores(self, table):
        conx = Crud_DB()
        query = "SELECT RUC, Nombre,  NombreContacto, Direccion ,Correo, Telefono FROM Proveedor"
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
            table.setItem(fila, 5, QtWidgets.QTableWidgetItem(rowCliente[5]))

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

        self.enabled_EntriesP(False)
        self.ln_rucP.setReadOnly(True)

        self.btnnuevoP.setEnabled(False)
        self.btnguardarP.setEnabled(False)

        conx = Crud_DB()
        itm = []  # Lista que contendram los items seleccionados
        for item in self.tb_viewCli.selectedItems():  # Con for se recorre la fila seleccionada
            itm.append(item.text())  # Se agraga cada item pero convirtiendolo a un string
            print(item.text())

        addre = str(itm[3]).split("_")

        self.ln_rucP.setText(itm[0])
        self.ln_nombreP.setText(itm[1])
        self.ln_telefonoP.setText(itm[5])

        self.ln_nombreDirP.setText(addre[1])
        self.ln_numeroDirP.setText(addre[2])
        self.ln_departamentoP.setText(addre[3])


        try:


            total_detalles_Provee = conx.runQuery(query="SELECT Direccion, Ciudad, Pais, NombreContacto, CargoContacto, Correo FROM Proveedor WHERE RUC = ?", parameters=(str(itm[0]),),
                                     select=True)

            print(total_detalles_Provee)
            parts_addres = str(total_detalles_Provee[0][0]).split("_")

            self.ln_nombreP.setText(parts_addres[1])
            self.ln_numeroDirP.setText(str(parts_addres[2]))
            self.ln_departamentoP.setText(parts_addres[3])

            all_word = total_detalles_Provee[0][1] + "_" + total_detalles_Provee[0][2] + "_" + total_detalles_Provee[0][3] + "_"+ total_detalles_Provee[0][4] + "_" + total_detalles_Provee[0][5]


            if not os.path.exists("temporal.txt"):
                with open("temporal.txt", "w") as temporal:
                    pass

            with open("temporal.txt", "w+") as temporal:
                temporal.write(str(all_word))


        except Exception as e:
            msbox.setTxt("Error",
                         f"Error Critico\nInformar al desarrollador\nError:{type(e).__name__}\n{e.__str__()}")
            msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
            msbox.exec_()

        del conx, msbox

    """Meétodo que actualizara el comboBox del apartado productos
        Despues de haber agregado un nuevo proveedor."""
    def updateComboBoxFromProducts(self):
        conx = Crud_DB()

        news_suppliers = []

        suppliers = conx.runQuery("Exec usp_getNameProveedor",(),select = True)

        for supp in suppliers:
            news_suppliers.append(supp[0])

        # Primero limpiamos los items para luego actualizarlos
        self.cb_proveed.clear()
        self.cb_proveed.addItems(news_suppliers)
