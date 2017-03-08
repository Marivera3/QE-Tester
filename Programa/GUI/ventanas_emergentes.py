from PyQt4 import QtGui
import sys
import time

__author__ = "Maximiliano Rivera"


class VentanaExit(QtGui.QDialog):

    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        self.setWindowTitle('QE Tester')
        self.setGeometry(500, 400, 200, 100)

        self.exit_label = QtGui.QLabel(
            '¿Estas seguro que quieres salir?', self)

        self.boton_yes = QtGui.QPushButton('&Si', self)
        self.boton_yes.resize(self.boton_yes.sizeHint())
        self.boton_yes.clicked.connect(
            self.salir)

        self.boton_no = QtGui.QPushButton('&No', self)
        self.boton_no.resize(self.boton_no.sizeHint())
        self.boton_no.clicked.connect(self.aun_no)

        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()

        hbox.addWidget(self.boton_yes)
        # hbox.addStretch(1)
        hbox.addWidget(self.boton_no)

        vbox.addWidget(self.exit_label)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def salir(self):
        sys.exit()

    def aun_no(self):
        self.hide()


class Pausa(QtGui.QDialog):

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.init_GUI()

    def init_GUI(self):
        self.setWindowTitle('QE Tester - Pausado')
        self.setGeometry(500, 400, 200, 100)

        self.exit_label = QtGui.QLabel(
            "Medición Pausada", self)

        self.boton_continuar = QtGui.QPushButton('&Continuar midiendo', self)
        self.boton_continuar.resize(self.boton_continuar.sizeHint())
        self.boton_continuar.clicked.connect(self.despausar)

        self.boton_salir = QtGui.QPushButton('&Salir', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.main.exit_)

        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()

        hbox.addWidget(self.boton_continuar)
        hbox.addStretch(1)
        hbox.addWidget(self.boton_salir)
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.exit_label)
        hbox2.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def despausar(self):
        self.hide()
        #self.main.statusBar().showMessage('Volviendo en unos segundos...')
        time.sleep(3)

    def keyPressEvent(self, event):
        if event.text() == "q":
            self.main.exit_()

        elif event.text() == "p":
            self.despausar()


class VolverInicio(QtGui.QDialog):

    def __init__(self, parent, other_window=None):
        super().__init__()
        self.parent = parent
        self.other_window = other_window
        self.init_GUI()

    def init_GUI(self):
        self.setWindowTitle('QE Tester')
        self.setGeometry(500, 400, 200, 100)

        self.exit_label = QtGui.QLabel(
            '¿Estas seguro que quieres volver al inicio?', self)

        self.boton_yes = QtGui.QPushButton('&Si', self)
        self.boton_yes.resize(self.boton_yes.sizeHint())
        self.boton_yes.clicked.connect(
            self.salir)

        self.boton_no = QtGui.QPushButton('&No', self)
        self.boton_no.resize(self.boton_no.sizeHint())
        self.boton_no.clicked.connect(self.aun_no)

        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()

        hbox.addWidget(self.boton_yes)
        # hbox.addStretch(1)
        hbox.addWidget(self.boton_no)

        vbox.addWidget(self.exit_label)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def salir(self):
        self.hide()
        if self.other_window:
            self.parent.hide()
            self.other_window.show()

        return True

    def aun_no(self):
        self.hide()


class ProblemaNombre(QtGui.QDialog):

    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        self.setWindowTitle('QE Tester')
        self.setGeometry(500, 400, 200, 100)

        self.exit_label = QtGui.QLabel(
            'Error nombre ya existe o el tiempo de exposición esta incorrecto', self)

        self.boton_yes = QtGui.QPushButton('&Aceptar', self)
        self.boton_yes.resize(self.boton_yes.sizeHint())
        self.boton_yes.clicked.connect(
            self.salir)

        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()

        hbox.addWidget(self.boton_yes)

        vbox.addWidget(self.exit_label)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def salir(self):
        self.hide()
