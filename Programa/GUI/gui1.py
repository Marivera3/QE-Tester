"""GUI"""
"""juvenega@uc.cl"""

import os
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QLabel, QPixmap, QWidget, QPalette
from PyQt4.QtGui import QPen, QBrush,  QApplication, QDialog, QGraphicsView, QGraphicsScene, QGridLayout, QPushButton
from PyQt4.QtCore import QPointF, QRectF, Qt
import parser_cam

PATH_CAMARAS = "C:\\Users\\maxri\\Documents\\UC\\Ipre\\QE tester\\Programa\\Camaras"


def get_path_camara(path=PATH_CAMARAS):
    cameras = os.listdir(path)
    return cameras


def path_exist(path):
    return os.path.exists(path)


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


menu_ingreso_ui = uic.loadUiType(get_absolute_path("ui\menu_ingreso.ui"))
datos_ingreso_ui = uic.loadUiType(get_absolute_path("ui\datos_ingreso.ui"))
datos_mediciones_ui = uic.loadUiType(
    get_absolute_path("ui\datos_med.ui"))
datos_ingreso_error = uic.loadUiType(
    get_absolute_path("ui\datos_ingreso_error.ui"))
datos_mediciones_error = uic.loadUiType(
    get_absolute_path("ui\datos_med_error.ui"))


class GUI:

    def __init__(self):
        self.menu_ingreso = MenuIngreso()
        self.datos_ingreso = DatosIngreso()
        self.datos_mediciones = DatosMediciones()
        self.datos_ingreso_error = DatosIngresoError()
        self.datos_mediciones_error = DatosMedicionesError()

        self.menu_ingreso.show()

        self.__bind_signals()

        self._cameras = get_path_camara()

        self.camera_name = None
        self._hay_camara = False  # Es para saber si esta esta camara en los archivos

    @property
    def cameras(self):
        self._cameras = get_path_camara()
        return self._cameras

    @property
    def hay_camara(self):
        return self._hay_camara

    @hay_camara.setter
    def hay_camara(self, valor):
        self._hay_camara = valor

    def __bind_signals(self):

        # MenuIngreso signals
        self.menu_ingreso.Continuar.clicked.connect(
            self.__on_menu_ingreso_continuar_button_click)

        # DatosIngreso signals
        self.datos_ingreso.continuar.clicked.connect(
            self.__on_datos_ingreso_continuar_button_click)

        self.datos_ingreso.volver.clicked.connect(
            self.__on_datos_ingreso_volver_button_click)

        # DatosMediciones signals
        self.datos_mediciones.continuar.clicked.connect(
            self.__on_datos_mediciones_continuar_button_click)

        self.datos_mediciones.volver.clicked.connect(
            self.__on_datos_mediciones_volver_button_click)

    def __on_menu_ingreso_continuar_button_click(self):
        self.__toggle_windows(self.datos_ingreso, self.menu_ingreso)

    def __on_datos_ingreso_continuar_button_click(self):
        # Actualiza los datos
        self.camera_name = self.datos_ingreso.nombre_camara
        # self.datos_ingreso.area_camara
        print(self.datos_ingreso.ganancia_camara)

        # Verifica el usuario
        if parser_cam.hay_camara(self.datos_ingreso.nombre_camara, self.cameras):
            self.hay_camara = True
            """

            FALTA MODIFICAR LA LECTURA DE LAS CAMARAS

            """
            self.__toggle_windows(self.datos_mediciones, self.datos_ingreso)

        else:
            # Si no hay, por lo menos nombre y area.Avisar
            if self.datos_ingreso.nombre_camara and parser_cam.isfloat(self.datos_ingreso.area_camara):
                if self.datos_ingreso.ganancia_camara == "" or parser_cam.isfloat(self.datos_ingreso.ganancia_camara):
                    parser_cam.crear_camara(PATH_CAMARAS,
                                            self.datos_ingreso.nombre_camara,
                                            self.datos_ingreso.area_camara,
                                            self.datos_ingreso.ganancia_camara)

                    self.datos_ingreso.datos_a_blanco()
                    self.__toggle_windows(
                        self.datos_mediciones, self.datos_ingreso)
                else:
                    self.datos_ingreso_error.exec_()
            else:
                self.datos_ingreso_error.exec_()

    def __on_datos_ingreso_volver_button_click(self):
        if self.datos_ingreso.nombre_camara or self.datos_ingreso.area_camara or self.datos_ingreso.ganancia_camara:
            self.datos_ingreso.datos_a_blanco()

        self.__toggle_windows(self.menu_ingreso, self.datos_ingreso)

    def __on_datos_mediciones_continuar_button_click(self):
        if self.datos_mediciones.mediciones.isdigit() and path_exist(self.datos_mediciones.path):
            if self.hay_camara:
                parser_cam.nueva_seccion_camara(
                    PATH_CAMARAS, self.camera_name, self.datos_mediciones.mediciones, self.datos_mediciones.path)
            else:
                parser_cam.agregar_mediciones_old(
                    PATH_CAMARAS, self.camera_name, self.datos_mediciones.mediciones, self.datos_mediciones.path)
            # self.__toggle_windows(self.menu_ingreso, self.datos_mediciones)
        else:
            self.datos_mediciones_error.exec_()

    def __on_datos_mediciones_volver_button_click(self):
        if self.datos_ingreso.nombre_camara or self.datos_ingreso.area_camara or self.datos_ingreso.ganancia_camara:
            self.datos_ingreso.datos_a_blanco()

        if self.datos_mediciones.mediciones or self.datos_mediciones.path:
            self.datos_mediciones.datos_a_blanco()

        self.__toggle_windows(self.datos_ingreso, self.datos_mediciones)

    def __toggle_windows(self, incoming, outgoing):
        outgoing.close()

        incoming.show()
        incoming.raise_()


class MenuIngreso(*menu_ingreso_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('QE Tester')

        # Boton Salir
        self.Salir.setShortcut('Ctrl+Q')  # permite usar combinación de teclas
        self.Salir.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def exit_(self):
        sys.exit()


class DatosIngreso(*datos_ingreso_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('QE Tester')

        self._nombre_camara = self.nombre_camara_LineEdit
        self._area_camara = self.area_pixel_camara_LineEdit
        self._ganancia_camara = self.ganancia_camara_LineEdit

    @property
    def nombre_camara(self):
        return self._nombre_camara.text()

    @nombre_camara.setter
    def nombre_camara(self, valor):
        self._nombre_camara = valor

    @property
    def area_camara(self):
        return self._area_camara.text()

    @area_camara.setter
    def area_camara(self, valor):
        self._area_camara = valor

    @property
    def ganancia_camara(self):
        return self._ganancia_camara.text()

    @ganancia_camara.setter
    def ganancia_camara(self, valor):
        self._ganancia_camara = valor

    def datos_a_blanco(self):
        self._nombre_camara.setText("")
        self._area_camara.setText("")
        self._ganancia_camara.setText("")


class DatosMediciones(*datos_mediciones_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('QE Tester')

        self._mediciones = self.mediciones_LineEdit
        self._path = self.path_LineEdit

    @property
    def mediciones(self):
        return self._mediciones.text()

    @property
    def path(self):
        return self._path.text()

    def datos_a_blanco(self):
        self._mediciones.setText("")
        self._path.setText("")


class DatosIngresoError(*datos_ingreso_error):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('QE Tester')

        self.ok_button.clicked.connect(self.aun_no)

    def aun_no(self):
        self.hide()


class DatosMedicionesError(*datos_mediciones_error):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('QE Tester')

        self.ok_button.clicked.connect(self.aun_no)

    def aun_no(self):
        self.hide()

if __name__ == '__main__':

    app = QtGui.QApplication([])
    form = GUI()
    app.exec_()
