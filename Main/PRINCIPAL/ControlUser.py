import logging
import threading
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pyodbc import IntegrityError

from Main.TOOLS.Tools import MessageBX, Crud_DB, SimpleTools

logging.basicConfig(level=logging.DEBUG, format="%(threadName)-s %(message)s")


class Hilo_Details(threading.Thread):
    def __init__(self, cb_tipo, cb_cargos, cb_estados) -> object:
        super().__init__()
        self.cb_tipo = cb_tipo
        self.cb_cargos = cb_cargos
        self.cb_estados = cb_estados

        self.types = ["Av", "Jr", "Calle", "Psje"]
        self.typeW = ["ADMINISTRADOR", "CAJERO", "VENDEDOR", "TRANSPORTISTA "]
        self.states = ["Activo", "Inactivo"]

        self.conx = Crud_DB()

    def run(self):
        logging.info("Insercion de calles y cargos")

        veri = self.conx.runQuery("SELECT * FROM Cargos", (), select=True)

        if not veri:
            for x in self.typeW:
                self.conx.runQuery("INSERT INTO Cargos VALUES(?,?)", (x[0], x))
                time.sleep(0.5)

        self.cb_tipo.addItems(self.types)
        self.cb_cargos.addItems(self.typeW)
        self.cb_estados.addItems(self.states)

        logging.info("Apartado Administracdor -> Insercion de calles y cargos exitosa")

        del self.conx


class HiloRegisDetals(threading.Thread):
    def __init__(self, cd, user, pasw, car, state):
        super().__init__()
        self.cd = cd
        self.user = user
        self.pasw = pasw
        self.car = car
        self.state = state

        self.conx = Crud_DB()

    def run(self):
        logging.info("Insercion de los detalles de usuario")

        try:
            qury = "INSERT INTO DetallesUsuarios VALUES(?,?,?,?,?)"
            prmt = (self.cd, self.user, self.pasw, self.car, self.state)

            resul = self.conx.runQuery(query=qury, parameters=prmt)

            if resul:
                logging.info("Apartado Administracdor -> Insercion de los detalles de usuario exitosa")
        except Exception as e:
            logging.info(f"Apartado Administracdor -> Error {type(e).__name__}\n{e.__str__()}")


class ControlUser:
    def __init__(self, mainWiU, cb_tipDir, cb_typeWork, cb_estados, tb_usuarios, btnnuevoU,
                 btnmodificarU, btnguardarU, btneliminarU,
                 ln_dni, ln_nombre, ln_apTu, ln_amTu, ln_telefono, nombreDirU,
                 ln_numeroDirU, ln_departamentU, ln_username, ln_password
                 ):

        self.mainWindowCli = mainWiU

        # ComboBox
        self.cb_tipo = cb_tipDir
        self.cb_typeWork = cb_typeWork
        self.cb_estados = cb_estados

        self.tb_usuarios = tb_usuarios

        self.tb_usuarios.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # Se estable la politica del men
        self.tb_usuarios.customContextMenuRequested.connect(
            self.menuAccionUsers)  # Al presionar anticlick este llamara al menu

        # Botones
        self.btnnuevoU = btnnuevoU
        self.btnmodificarU = btnmodificarU
        self.btneliminarU = btneliminarU
        self.btnguardarU = btnguardarU

        """Conexion con los funciones respectivas de cada boton"""

        self.btnnuevoU.clicked.connect(self.newUser)
        self.btnguardarU.clicked.connect(self.saveUser)
        self.btnmodificarU.clicked.connect(self.modifyUser)
        self.btneliminarU.clicked.connect(self.deleteUser)

        self.ln_dniU = ln_dni
        self.ln_nombreU = ln_nombre
        self.ln_telefonoU = ln_telefono
        self.ln_apTu = ln_apTu
        self.ln_amTu = ln_amTu
        self.ln_nombreDirU = nombreDirU
        self.ln_numeroDirU = ln_numeroDirU
        self.ln_departamentU = ln_departamentU
        self.ln_username = ln_username
        self.ln_password = ln_password

        # Constante Temporal
        self.COD_EMPLEADO = None

        # Lista que contendra todos lineEDIT a revisar
        self.__list_LineEditWidgets = [self.ln_dniU, self.ln_nombreU, self.ln_telefonoU, self.ln_apTu,
                                       self.ln_amTu, self.ln_nombreDirU, self.ln_numeroDirU, self.ln_departamentU,
                                       self.ln_username, self.ln_password]

        # Lista que contendra todos ComboBox a revisar

        self.__list_ComboBoxWidgets = [self.cb_tipo, self.cb_typeWork, self.cb_estados, ]

        # Establecer los tipos de direcciones
        _hil = Hilo_Details(self.cb_tipo, cb_typeWork, cb_estados)
        _hil.start()
        _hil.join()

        del _hil

        # Bloquear las entradas
        self.enabled_EntriesP(True)

        # Mostrar todos los clientes
        self.mostrarUsuarios(self.tb_usuarios)

    def enabled_EntriesP(self, bool):
        for wid in self.__list_LineEditWidgets:
            wid.setReadOnly(bool)

    """Definir variables cuando los radiobuttones son marcados"""

    def newUser(self):
        """Se bloquea los botones"""
        self.btnmodificarU.setEnabled(False)
        self.btneliminarU.setEnabled(False)

        self.enabled_EntriesP(False)

    def saveUser(self):
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

            self.ln_verifiAlpha = [self.ln_nombreU, self.ln_apTu, self.ln_amTu, self.ln_nombreDirU,
                                   self.ln_departamentU, self.ln_username]

            self.ln_verifiNum = [self.ln_dniU, self.ln_telefonoU]

            self._areAlpha, self.indexsAlpha = ST.verifyLnAlpha(self.ln_verifiAlpha)

            # print(self.indexsAlpha) #Solo para mostrar indices resultantes

            self._areNumer, self.indexsNume = ST.verifyLnNumeric(self.ln_verifiNum)

            # print(self.indexsNume)  #Solo para mostrar indices resultantes

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
                    if len(self.ln_telefonoU.text()) != 9:
                        QMessageBox().warning(None, "Aviso",
                                              f"El número telefonico no debe ser menor o mayor a los 9 digitos ",
                                              QMessageBox.Ok)

                    else:
                        if len(self.ln_dniU.text()) != 8:
                            QMessageBox().warning(None, "Aviso",
                                                  f"El número Dni no debe ser menor o mayor a los 8 digitos ",
                                                  QMessageBox.Ok)
                        else:
                            try:
                                """Se crea un Codigo poniendo primeramente los caracteres PT y 5 primeros digitos del RUC"""
                                CdEmpleado = str(self.cb_typeWork.currentText())[:2] + self.ln_dniU.text()[:3]

                                # Unir la todos los componentes de direccion en 1 solo
                                self.addres = str(
                                    self.cb_tipo.currentText()) + "_" + self.ln_nombreDirU.text() + "_" + str(
                                    self.ln_numeroDirU.text()) + "_" + self.ln_departamentU.text()

                                """Primero se hace el registro a la tabla empleados """
                                query = "INSERT INTO Empleado VALUES(?,?,?,?,?,?,?)"
                                prmt = (CdEmpleado, self.ln_dniU.text(), self.ln_nombreU.text(),
                                        self.ln_apTu.text(), self.ln_amTu.text(), self.addres, self.ln_telefonoU.text())

                                result = conx.runQuery(query, prmt)

                                time.sleep(1)

                                """Ahora se prosigue a HASHEAR la contraseña con SHA256 usando el método hashPassword de la clase
                                        SimpleTools"""
                                hashPass = ST.hashPassword(self.ln_password.text())

                                """Despues de un tiempo de espera de 1 segundo  se prosigue insertando los datos en la tabla
                                        Detalles de Usuarios haciendo uso del hilo ya definido"""

                                self.regDetails = HiloRegisDetals(CdEmpleado, self.ln_username.text(),
                                                                  hashPass, self.cb_typeWork.currentText()[0],
                                                                  self.cb_estados.currentText()[0])

                                self.regDetails.start()
                                self.regDetails.join()

                                if result:
                                    ms_box.setTxt("Exito",
                                                  f"El Usuario {self.ln_nombreU.text()} se añadio con exito.")
                                    ms_box.insertIcon("Imagenes/accept.ico", QMessageBox.Information)
                                    ms_box.exec_()

                                    for wid in self.__list_LineEditWidgets:
                                        wid.clear()

                                    with open("temporal.txt", "w") as t:
                                        pass

                            except IntegrityError:
                                ms_box.setTxt("Error",
                                              f"Error Critico\n El Usuario {self.ln_nombreU.text()} ya se encuentra registrado")
                                ms_box.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
                                ms_box.exec_()

                            except Exception as e:
                                QMessageBox().warning(None,"Aviso","Usuario no encontrado\m¿Desea escoger usuario momentaneo?",QMessageBox.Yes)

        self.actualizarTabla()
        self.btnmodificarU.setEnabled(True)
        self.btneliminarU.setEnabled(True)

        del ms_box, conx  # Para no ocupar la memoria se elimina las ainstancias """

    def modifyUser(self):
        #self.ln_dniU.setReadOnly(True)

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


            self.btnnuevoU.setEnabled(True)
            self.btnguardarU.setEnabled(True)



        else:

            """Se crea 2 variables, la primera es una lista vacia, la segunda es una variable que contendra un booleano
                    si al verificar los campos el metodo retorna un false y una lista con los indices de los datos
                    erroneos los cuales se verificaran más adelante"""

            self.ln_verifiAlpha = [self.ln_nombreU, self.ln_apTu, self.ln_amTu, self.ln_nombreDirU,
                                   self.ln_departamentU, self.ln_username]

            self.ln_verifiNum = [self.ln_dniU, self.ln_telefonoU]

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
                    if len(self.ln_telefonoU.text()) != 9:
                        QMessageBox().warning(None, "Aviso",
                                              f"El número telefonico no debe ser menor o mayor a los 9 digitos ",
                                              QMessageBox.Ok)

                    else:
                        if len(self.ln_dniU.text()) != 8:
                            QMessageBox().warning(None, "Aviso",
                                                  f"El número Dni no debe ser menor o mayor a los 8 digitos ",
                                                  QMessageBox.Ok)
                        else:
                            time.sleep(0.5)

                            """Se crea un Codigo poniendo primeramente los caracteres PT y 5 primeros digitos del RUC"""
                            CdEmpleado = str(self.cb_typeWork.currentText())[:2] + self.ln_dniU.text()[:3]

                            # Unir la todos los componentes de direccion en 1 solo
                            self.addres = str(
                                self.cb_tipo.currentText()) + "_" + self.ln_nombreDirU.text() + "_" + str(
                                self.ln_numeroDirU.text()) + "_" + self.ln_departamentU.text()

                            self.params_Empleados = (self.ln_dniU.text(), self.ln_nombreU.text(),
                                                     self.ln_apTu.text(), self.ln_amTu.text(), self.addres,
                                                     self.ln_telefonoU.text(), self.COD_EMPLEADO)

                            """Ahora para actualizar la contraseña se prosigue  a HASHEARLO con SHA256 usando el método hashPassword de la clase
                                                                    SimpleTools"""
                            hashPass = ST.hashPassword(self.ln_password.text())

                            self.parm_Detalles = (self.ln_username.text(), hashPass,
                                                  self.cb_typeWork.currentText()[0], self.cb_estados.currentText()[0],
                                                  self.COD_EMPLEADO
                                                  )

                            try:

                                query_Empleados = "UPDATE Empleado SET Dni = ?, Nombre = ?, Ap_Paterno = ?, " \
                                                  "Ap_Materno = ?, Direccion=?, Telefono =? WHERE CodEmpleado = ?"

                                param = self.params_Empleados
                                result = conx.runQuery(query_Empleados, parameters=param)

                                time.sleep(1)
                                query_Detalles = "UPDATE DetallesUsuarios SET Usuario = ?, Contrasena = ?, Cargo = ?, " \
                                                 "Estado=? WHERE CodEmpleado = ? "

                                param = self.parm_Detalles
                                result = conx.runQuery(query_Detalles, parameters=param)

                                if result:
                                    msbox.setTxt("Exito",
                                                 f"¡La usuario {self.ln_nombreU.text()} ha sido actualizado con exito!")
                                    msbox.insertIcon("../Imagenes/accept.ico",
                                                     QtWidgets.QMessageBox.Information)
                                    msbox.exec_()

                                    for widge in self.__list_LineEditWidgets:
                                        widge.clear()

                                    # Se Habilita  los botones
                                    self.btnnuevoU.setEnabled(True)
                                    self.btnguardarU.setEnabled(True)

                                    # Actualizar la tabla
                                    self.actualizarTabla()

                                    with open("temporal.txt", "w") as temporal:
                                        pass



                            except Exception as e:
                                msbox.setTxt("Error", f"Informar al desarrollador\n{e.__str__()}")
                                msbox.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                                msbox.exec_()
        del conx, msbox

    def deleteUser(self):
        dialogos = MessageBX()
        conexion = Crud_DB()
        ST = SimpleTools()

        cod = self.ln_dniU.text()

        if cod != "":
            pregunta = QtWidgets.QMessageBox().warning(None, "Aviso",
                                                       f"¿Desea eliminar el usuario {self.ln_nombreU.text()}?",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.Yes)

            if pregunta == QtWidgets.QMessageBox.Yes:
                try:
                    query = "DELETE FROM DetallesUsuarios WHERE CodEmpleado = ? "
                    paramt = (self.COD_EMPLEADO,)

                    result = conexion.runQuery(query, paramt, select=False)

                    time.sleep(1)

                    query = "DELETE FROM Empleado WHERE CodEmpleado = ? "
                    paramt = (self.COD_EMPLEADO,)

                    result_2 = conexion.runQuery(query, paramt, select=False)

                    if result and result_2:
                        dialogos.setTxt("Exito", f"¡El usuario {self.ln_nombreU.text()} fue eliminado con exito!")
                        dialogos.insertIcon("../Imagenes/accept.ico", QtWidgets.QMessageBox.Information)
                        dialogos.exec_()

                        self.actualizarTabla()

                        #Activacion de los botones
                        self.btnnuevoU.setEnabled(True)
                        self.btnguardarU.setEnabled(True)
                        self.btnmodificarU.setEnabled(True)


                except Exception as e:
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
        self.tb_usuarios.clearContents()

        self.mostrarUsuarios(self.tb_usuarios)

    def mostrarUsuarios(self, table):
        conx = Crud_DB()
        query = """
        SELECT e.CodEmpleado, e.Nombre, e.Ap_Paterno+'_'+e.Ap_Materno,e.Telefono,
        e.Direccion, du.Usuario, du.Contrasena, c.Nombre, du.Estado
        FROM Empleado e 
        INNER JOIN DetallesUsuarios du ON du.CodEmpleado = e.CodEmpleado
        INNER JOIN Cargos c ON c.IdCargo = du.Cargo
        """
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
            table.setItem(fila, 6, QtWidgets.QTableWidgetItem(str(rowCliente[6])))
            table.setItem(fila, 7, QtWidgets.QTableWidgetItem(rowCliente[7]))

            pal = ""
            if result[0][8] == "A":
                pal = "ACTIVO"
            else:
                pal = "INACTIVO"

            table.setItem(fila, 8, QtWidgets.QTableWidgetItem(pal))

            fila += 1

        del conx

    def menuAccionUsers(self, posicition):
        self.menu = QtWidgets.QMenu()

        itemsGroup = QtWidgets.QActionGroup(self.mainWindowCli)
        itemsGroup.setExclusive(True)

        self.menu.addAction(QtWidgets.QAction("Seleccionar Fila", itemsGroup))

        itemsGroup.triggered.connect(self.selecUsers)
        self.menu.exec_(self.tb_usuarios.viewport().mapToGlobal(posicition))

    def selecUsers(self):
        conx = Crud_DB()
        msbox = MessageBX()

        self.enabled_EntriesP(False)
        #self.ln_dniU.setReadOnly(True)

        self.btnnuevoU.setEnabled(False)
        self.btnguardarU.setEnabled(False)

        self.btnmodificarU.setEnabled(True)
        self.btneliminarU.setEnabled(True)


        conx = Crud_DB()
        itm = []  # Lista que contendram los items seleccionados
        for item in self.tb_usuarios.selectedItems():  # Con for se recorre la fila seleccionada
            itm.append(item.text())  # Se agraga cada item pero convirtiendolo a un string
            #print(item.text())

        addre = str(itm[4]).split("_")

        # Separar los apellidos
        apts = str(itm[2]).split("_")

        self.ln_verifiNum = [self.ln_dniU, self.ln_telefonoU]

        self.ln_nombreU.setText(itm[1])

        self.ln_apTu.setText(apts[0])
        self.ln_amTu.setText(apts[1])

        self.ln_telefonoU.setText(itm[3])

        self.ln_nombreDirU.setText(addre[1])
        self.ln_numeroDirU.setText(addre[2])
        self.ln_departamentU.setText(addre[3])

        self.ln_username.setText(itm[5])
        self.ln_password.setText("----------------")

        self.COD_EMPLEADO = itm[0]  # Se guardar en la constante el cod de empleado
        try:

            dni = conx.runQuery(
                query="SELECT Dni FROM Empleado WHERE CodEmpleado = ?",
                parameters=(str(itm[0]),),
                select=True)

            self.ln_dniU.setText(dni[0][0])


        except Exception as e:
            msbox.setTxt("Error",
                         f"Error Critico\nInformar al desarrollador\nError:{type(e).__name__}\n{e.__str__()}")
            msbox.insertIcon("Imagenes/cancel.ico", QMessageBox.Warning)
            msbox.exec_()

        del conx, msbox
