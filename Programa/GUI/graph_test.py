__author__ = "Maximiliano Rivera"

import os
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QLabel, QPixmap, QWidget, QPalette
from PyQt4.QtGui import QPen, QBrush,  QApplication, QDialog, QGraphicsView, QGraphicsScene, QGridLayout, QPushButton
from PyQt4.QtCore import QPointF, QRectF, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import parser_cam

import ventanas_emergentes as VE


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

graph = uic.loadUiType(get_absolute_path("ui\graph.ui"))


class MainWindow(*graph):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

        self.datos = dict()

        volver_inicio = QtGui.QAction(QtGui.QIcon(None), '&Inicio', self)
        volver_inicio.setShortcut('I')
        volver_inicio.setStatusTip('Volver a la ventana inicial')
        volver_inicio.triggered.connect(self.volverinicio)

        salir = QtGui.QAction(QtGui.QIcon(None), '&Salir', self)
        salir.setShortcut('Q')
        salir.setStatusTip('Terminar la aplicación')
        salir.triggered.connect(self.exit_)  # Seguro que quiere salir?

        pause = QtGui.QAction(QtGui.QIcon(None), '&Pausar', self)
        pause.setShortcut('P')
        pause.setStatusTip('Pausar la aplicación')
        pause.triggered.connect(self.pausa)

        menubar = self.menuBar()

        archivo_menu = menubar.addMenu('&Archivo')
        archivo_menu.addAction(volver_inicio)
        archivo_menu.addAction(pause)
        archivo_menu.addAction(salir)

        self.statusBar().showMessage('Listo')

        self.texto.setText("Verificando si esta la Ganancia de Conversión...")

        """
        Primero que todo, si no hay Convertion Gain, hay que pedirla/obtenerla
        Obteniendo la Convertion Gain,
        La idea es hacer se tomen los puntos uno por uno e ir mostrandolos en el grafico.
        """

        self.aceptar.clicked.connect(self.submit_datos)

    def exit_(self):
        ventana = VE.VentanaExit().exec_()

    def pausa(self):
        self.statusBar().showMessage('Pausa, se volverá a medir luego de despausar')
        ventana = VE.Pausa(self).exec_()
        self.statusBar().showMessage('Listo')

    def volverinicio(self):
        ventana = VE.VolverInicio(self, other_window=self.parent).exec_()

    def submit_datos(self):
        nombre = self.textnombre.text()
        tiempoexpo = self.texttiempo.text()
        self.textnombre.setText("")
        self.texttiempo.setText("")
        if nombre:
            if nombre in self.datos.keys():
                VE.ProblemaNombre().exec_()
            elif not parser_cam.isfloat(tiempoexpo):
                VE.ProblemaNombre().exec_()
            else:
                self.datos[nombre] = tiempoexpo




if __name__ == '__main__':

    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
