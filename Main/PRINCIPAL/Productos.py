import logging
import random
import threading
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from Main.TOOLS.Tools import Crud_DB, MessageBX, SimpleTools

logging.basicConfig(level=logging.DEBUG, format="%(threadName)-s %(message)s")


class HiloPutData(threading.Thread):
    def __init__(self, cb_measure, cb_cate, cb_supp):
        super().__init__()
        self.cb_measure = cb_measure
        self.cb_cate = cb_cate
        self.cb_supp = cb_supp

    def run(self):
        logging.info("Comenzó el hilo putData")
        self.con = Crud_DB()

        self.unidades_Medidas = [x[1] for x in self.con.runQuery("SELECT * FROM UnidadesMedida", (), select=True)]
        self.categorias = [cat[1] for cat in self.con.runQuery("SELECT * FROM Categoria", (), select=True)]
        self.proveedores = [prove[1] for prove in self.con.runQuery("SELECT * FROM Proveedor", (), select=True)]

        self.cb_measure.addItems(self.unidades_Medidas)
        self.cb_cate.addItems(self.categorias)
        self.cb_supp.addItems(self.proveedores)


class HiloIngresarMarc(threading.Thread):
    def __init__(self, marca, cb_measurement, cb_categories, cb_supplier, marca_name=None, marca_register=False):
        super().__init__()
        self.__mr = marca
        self.con = Crud_DB()
        self.msbox = MessageBX()

        self.cb_m = cb_measurement
        self.cb_c = cb_categories
        self.cb_s = cb_supplier

        self.name_marc = marca_name
        self.verifi_registro_mar = marca_register

        """Constantes que tendran los codigos necesarios para el registro del producto"""
        self.COD_MARCA = 0  # En el caso de querer  registrar la marca
        self.COD_U_MEDIDA = 0
        self.COD_PROVEEDOR = 0
        self.COD_CATEGORIA = 0

    def run(self):
        result = None

        if self.verifi_registro_mar:
            try:
                """SE REGISTRA LA MARCA CUANDO SE QUIERE GUARDAR EL PRODUCTO"""
                self.COD_MARCA = random.randint(1000, 9999)

                """Primero insertara la marca"""
                query = "INSERT INTO Marcas VALUES(?,?)"
                Prm = (self.COD_MARCA, self.__mr)

                result = self.con.runQuery(query, parameters=(Prm))
            except Exception as e:
                self.msbox.setTxt("Error", f"Informar al desarrollador\n{type(e).__name__}\n{e.__str__()}")
                self.msbox.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                self.msbox.exec_()

        else:
            """SE OBTIENE EL CODIGO DE LA MARCA AL QUERER ACTUALIZAR EL PRODUCTO"""
            result = self.con.runQuery("SELECT IdMarca from Marcas WHERE Marca = ?", (self.name_marc,), select=True)
            self.COD_MARCA = result[0][0]

        """Despues obtendra los cod de u/medida, proveedor, categoria"""

        self.u_medida = self.con.runQuery("SELECT CodUM FROM UnidadesMedida WHERE Unid_Med = ? ",
                                          parameters=(self.cb_m.currentText(),),
                                          select=True)

        self.cdCate = self.con.runQuery("SELECT Id FROM Categoria WHERE Nombre = ? ",
                                        parameters=(self.cb_c.currentText(),),
                                        select=True)

        self.cdProve = self.con.runQuery("SELECT RUC FROM Proveedor WHERE Nombre = ?",
                                         parameters=(self.cb_s.currentText(),),
                                         select=True)
        # print(self.u_medida, self.cdCate, self.cdProve)

        if result and self.cdCate and self.u_medida and self.cdProve:
            logging.info("Marca Registrada con exito y codigos obtenidos")
            self.COD_U_MEDIDA = self.u_medida[0][0]
            self.COD_PROVEEDOR = self.cdProve[0][0]
            self.COD_CATEGORIA = self.cdCate[0][0]

        else:
            QMessageBox().warning(None, "Error en la base de datos", "Al parece la base de datos esta dañada" +
                                  "\nContacte al desarrollador", QMessageBox.Ok)


class Product:
    def __init__(self, mainWindow, cb_measurement, cb_categories, cb_suppliers, tb_view, btnnuevo,
                 btnmodificar, btneliminar, btnguardar, btnBuscar, ln_buscarPro,
                 ln_cod, ln_nom, ln_des, ln_stock, ln_marca, ln_u_pedido, ln_precio
                 ):

        self.mainWindow = mainWindow

        self.cb_measurement = cb_measurement
        self.cb_categories = cb_categories
        self.cb_supplier = cb_suppliers
        self.tb_view = tb_view

        self.tb_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # Se estable la politica del meni
        self.tb_view.customContextMenuRequested.connect(self.menuAccion)  # Al presionar anticlick este llamara al menu

        self.btnnuevo = btnnuevo
        self.btnmodificar = btnmodificar
        self.btneliminar = btneliminar
        self.btnguardar = btnguardar
        self.btnBuscar = btnBuscar

        self.ln_buscaPro = ln_buscarPro

        """Conexion con los funciones respectivas de cada boton"""
        self.btnnuevo.clicked.connect(self.newProduct)
        self.btnguardar.clicked.connect(self.saveProduct)
        self.btnmodificar.clicked.connect(self.modifyProduct)
        self.btneliminar.clicked.connect(self.deleteProduct)

        self.ln_cod = ln_cod
        self.ln_nom = ln_nom
        self.ln_des = ln_des
        self.ln_stock = ln_stock
        self.ln_marca = ln_marca
        self.ln_u_pedido = ln_u_pedido
        self.ln_precio = ln_precio

        # Lista que contendra todos lineEDIT a revisar
        self.__list_LineEditWidgets = [self.ln_cod, self.ln_nom, self.ln_des, self.ln_stock, self.ln_marca,
                                       self.ln_u_pedido, self.ln_precio]

        # Lista que contendra todos ComboBox a revisar
        self.__list_ComboBoxWidgets = [self.cb_measurement, self.cb_categories, self.cb_supplier]
        # Crea una instancia de la clase personalizada MSBOX(cuadros de dialogo)

        """Se deshabilita los line edit"""
        self.enabled_Entries(True)

        self.putData()
        self.mostrarProductos(self.tb_view)  # Funcion que mostrara todos los productos de la base de datos

        self.COD_MARCA = 0  # En el caso de querer  registrar la marca
        self.COD_U_MEDIDA = 0
        self.COD_PROVEEDOR = 0
        self.COD_CATEGORIA = 0

    def putData(self):
        self.hilo = HiloPutData(self.cb_measurement, self.cb_categories, self.cb_supplier)
        self.hilo.start()
        self.hilo.join()

    def enabled_Entries(self, bool):

        self.ln_cod.setReadOnly(bool)
        self.ln_nom.setReadOnly(bool)
        self.ln_des.setReadOnly(bool)
        self.ln_stock.setReadOnly(bool)
        self.ln_marca.setReadOnly(bool)
        self.ln_u_pedido.setReadOnly(bool)

        # self.lbl_provee.setReadOnly(bool)

    def newProduct(self):
        """Se bloquea los botones"""
        self.btnmodificar.setEnabled(False)
        self.btneliminar.setEnabled(False)

        """Se habilita los LineEdit"""
        self.enabled_Entries(False)

    def saveProduct(self):
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
            if str(self.ln_stock.text()).isalpha() and str(self.ln_u_pedido.text()).isalpha() and str(
                    self.ln_precio.text()).isalpha():
                QMessageBox().warning(None, "Aviso", "Stock o Unidad de pedido o Precio deben ser números",
                                      QMessageBox.Ok)

            else:
                """SE REGISTRA LA MARCA CUANDO SE QUIERE GUARDAR EL PRODUCTO"""
                self.COD_MARCA = random.randint(1000, 9999)

                """Primero insertara la marca"""
                query = "INSERT INTO Marcas VALUES(?,?)"
                Prm = (self.COD_MARCA, self.ln_marca.text())

                result = conx.runQuery(query, parameters=(Prm))

                """
                #logging.info("Empezo el guardado de marca")
                self.hilo_register_measure = HiloIngresarMarc(self.ln_marca.text(), self.cb_measurement,
                                                              self.cb_categories, self.cb_supplier, marca_register=True)
                self.hilo_register_measure.start()
                self.hilo_register_measure.join()
                #logging.info("Termino  el guardado de marca")
                """

                time.sleep(0.5)
                #print(self.hilo_register_measure.COD_CATEGORIA)

                self.u_medida = conx.runQuery("SELECT CodUM FROM UnidadesMedida WHERE Unid_Med = ? ",
                                                  parameters=(self.cb_measurement.currentText(),),
                                                  select=True)

                self.cdCate = conx.runQuery("SELECT Id FROM Categoria WHERE Nombre = ? ",
                                                parameters=(self.cb_categories.currentText(),),
                                                select=True)

                self.cdProve = conx.runQuery("SELECT RUC FROM Proveedor WHERE Nombre = ?",
                                                 parameters=(self.cb_supplier.currentText(),),
                                                 select=True)
                # print(self.u_medida, self.cdCate, self.cdProve)

                if result and self.cdCate and self.u_medida and self.cdProve:
                    logging.info("Marca Registrada con exito y codigos obtenidos")
                    self.COD_U_MEDIDA = self.u_medida[0][0]
                    self.COD_PROVEEDOR = self.cdProve[0][0]
                    self.COD_CATEGORIA = self.cdCate[0][0]



                self.params = (
                str(self.ln_cod.text()), str(self.ln_nom.text()), str(self.COD_MARCA),
                float(self.ln_precio.text()), str(self.ln_des.text()),
                str(self.ln_stock.text()), str(self.COD_U_MEDIDA),
                str(self.COD_CATEGORIA),
                str(self.COD_PROVEEDOR ), str(self.ln_u_pedido.text()))

                try:
                    logging.info("Empezo el guardado de producto")
                    query = "INSERT INTO Producto VALUES(?,?,?,?,?,?,?,?,?,?) "
                    param = self.params
                    result = conx.runQuery(query, parameters=param, select=False)
                    logging.info("Termino el guardado de producto")


                    if result:
                        logging.info("Mensaje de guardado")

                        msbox.setTxt("Exito", f"La Producto {self.ln_nom.text()} se ha guardado con exito!")
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

        # del msbox, conx #Para no ocupar la memoria se elimina las ainstancias """

    def modifyProduct(self):
        # Lista que contendra todos lineEDIT a revisar
        self.__list_LineEditWidgets = [self.ln_cod, self.ln_nom, self.ln_des, self.ln_stock, self.ln_marca,
                                       self.ln_u_pedido, self.ln_precio]

        # Lista que contendra todos ComboBox a revisar
        self.__list_ComboBoxWidgets = [self.cb_measurement, self.cb_categories, self.cb_supplier]
        # Crea una instancia de la clase personalizada MSBOX(cuadros de dialogo)
        msbox = MessageBX()
        # Crea uns instancia de la clase que controla la base de datos
        conx = Crud_DB()
        ST = SimpleTools()

        if not ST.verifyEmties(self.__list_LineEditWidgets, list_lineEdit=True) or not ST.verifyEmties(
                self.__list_ComboBoxWidgets, list_comboBox=True):

            QMessageBox().warning(None, "Aviso", "Datos Incompletos\nPor favor rellena todos los campos",
                                  QMessageBox.Ok)

        else:
            if str(self.ln_stock.text()).isalpha() and str(self.ln_u_pedido.text()).isalpha() and str(
                    self.ln_precio.text()).isalpha():
                QMessageBox().warning(None, "Aviso", "Stock o Unidad de pedido o Precio deben ser números",
                                      QMessageBox.Ok)

            else:
                self.hilo_register_measure = HiloIngresarMarc(self.ln_marca.text(), self.cb_measurement,
                                                              self.cb_categories, self.cb_supplier,
                                                              marca_name=self.ln_marca.text(),
                                                              )
                self.hilo_register_measure.start()
                self.hilo_register_measure.join()

                time.sleep(0.5)

                self.params = (str(self.ln_nom.text()), str(self.hilo_register_measure.COD_MARCA),
                               str(self.ln_precio.text()), str(self.ln_des.text()),
                               str(self.ln_stock.text()), str(self.hilo_register_measure.COD_U_MEDIDA),
                               str(self.hilo_register_measure.COD_CATEGORIA),
                               str(self.hilo_register_measure.COD_PROVEEDOR), str(self.ln_u_pedido.text()),
                               str(self.ln_cod.text()))

                try:

                    query = """
                    UPDATE Producto SET Nombre = ?,
                    Marca = ?, Precio = ?, Descripcion = ?, Stock=?,
                    [U/Medida] = ?, Categoria =?, Proveedor = ?,
                    [U/Pedido] = ? WHERE Codigo = ?     
                    """
                    param = self.params
                    result = conx.runQuery(query, parameters=param, select=False)

                    if result:
                        msbox.setTxt("Exito", f"¡La Producto {self.ln_nom.text()} ha sido actualizadp con exito!")
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

    def deleteProduct(self):
        dialogos = MessageBX()
        conexion = Crud_DB()
        ST = SimpleTools()

        cod = self.ln_cod.text()

        if cod != "":
            pregunta = QtWidgets.QMessageBox().warning(None, "Aviso",
                                                       f"¿Desea eliminar el producto {self.ln_nom.text()}?",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.Yes)

            if pregunta == QtWidgets.QMessageBox.Yes:
                query = "DELETE FROM Producto WHERE Codigo = ? "
                paramt = (cod,)

                result = conexion.runQuery(query, paramt, select=False)

                if result:
                    try:
                        dialogos.setTxt("Exito", f"¡El producto {self.ln_nom.text()} fue eliminada con exito!")
                        dialogos.insertIcon("../Imagenes/accept.ico", QtWidgets.QMessageBox.Information)
                        dialogos.exec_()

                        self.actualizarTabla()

                    except Exception as e:
                        dialogos.setTxt("Error", f"Informar al desarrollador\n{e.__str__()}")
                        dialogos.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
                        dialogos.exec_()

        else:
            dialogos.setTxt("Error", "No haz seleccionado un item")
            dialogos.insertIcon("../Imagenes/cancel.ico", QtWidgets.QMessageBox.Warning)
            dialogos.exec_()

        for widge in self.__list_LineEditWidgets:
            widge.clear()

    def actualizarTabla(self):
        self.tb_view.clearContents()

        self.mostrarProductos(self.tb_view)

    def mostrarProductos(self, table):
        conx = Crud_DB()
        query = """
        select Codigo,pr.Nombre, pr.Descripcion,
        Stock, Precio,um.Unid_Med, p.Nombre,m.Marca, c.Nombre, [U/Pedido]
        from Producto pr  INNER JOIN  UnidadesMedida um On um.CodUM = pr.[U/Medida]
        INNER JOIN Marcas m ON m.IdMarca = pr.Marca
        INNER JOIN Proveedor p ON p.RUC = pr.Proveedor
        INNER JOIN  Categoria c ON c.Id = pr.Categoria
        
        """
        # Obtenemos las categorias de la base de datos
        result = conx.runQuery(query, (), select=True)

        fila = 0
        for row in result:
            table.setRowCount(fila + 1)
            table.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            table.setItem(fila, 1, QtWidgets.QTableWidgetItem(row[1]))
            table.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            table.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            table.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            table.setItem(fila, 5, QtWidgets.QTableWidgetItem(row[5]))
            table.setItem(fila, 6, QtWidgets.QTableWidgetItem(row[6]))#Proveedor
            table.setItem(fila, 7, QtWidgets.QTableWidgetItem(row[7]))
            table.setItem(fila, 8, QtWidgets.QTableWidgetItem(row[8]))
            table.setItem(fila, 9, QtWidgets.QTableWidgetItem(str(row[9])))

            fila += 1

    def menuAccion(self, posicition):
        self.menu = QtWidgets.QMenu()

        itemsGroup = QtWidgets.QActionGroup(self.mainWindow)
        itemsGroup.setExclusive(True)

        self.menu.addAction(QtWidgets.QAction("Seleccionar Fila", itemsGroup))

        itemsGroup.triggered.connect(self.seleccionarFila)
        self.menu.exec_(self.tb_view.viewport().mapToGlobal(posicition))

    def seleccionarFila(self):
        self.enabled_Entries(False)
        self.ln_cod.setReadOnly(True)

        self.btnnuevo.setEnabled(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        self.btnmodificar.setEnabled(True)

        conx = Crud_DB()
        itm = []  # Lista que contendram los items seleccionados
        for item in self.tb_view.selectedItems():  # Con for se recorre la fila seleccionada
            itm.append(item.text())  # Se agraga cada item pero convirtiendolo a un string

        que = """
        select Codigo,pr.Nombre, pr.Descripcion,
        Stock, Precio,
        um.Unid_Med, p.Nombre,m.Marca, c.Nombre, [U/Pedido]
        from Producto pr  INNER JOIN  UnidadesMedida um On um.CodUM = pr.[U/Medida]
        INNER JOIN Marcas m ON m.IdMarca = pr.Marca
        INNER JOIN Proveedor p ON p.RUC = pr.Proveedor
        INNER JOIN  Categoria c ON c.Id = pr.Categoria
        WHERE Codigo = ? """

        self.codProdu = str(itm[0])
        result = conx.runQuery(que, (self.codProdu,), select=True)

        for row in result:
            self.ln_cod.setText(row[0])
            self.ln_nom.setText(row[1])
            self.ln_des.setText(row[2])
            self.ln_stock.setText(str(row[3]))
            self.ln_marca.setText(str(row[7]))
            self.ln_u_pedido.setText(str(row[9]))
            self.ln_precio.setText(str(row[4]))
