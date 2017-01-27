""" Modulo que representa a la gui"""

import os
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QLabel, QPixmap, QWidget, QPalette
from PyQt4.QtGui import QPen, QBrush,  QApplication, QDialog, QGraphicsView, QGraphicsScene, QGridLayout, QPushButton
from PyQt4.QtCore import QPointF, QRectF, Qt


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

splash_dialog_ui = uic.loadUiType(get_absolute_path(".\splash_dialog.ui"))
signin_dialog_ui = uic.loadUiType(get_absolute_path(".\signin_dialog.ui"))
signup_dialog_ui = uic.loadUiType(get_absolute_path(".\signup_dialog.ui"))
chat_ui = uic.loadUiType(get_absolute_path(".\chat.ui"))
menu_prin_ui = uic.loadUiType(get_absolute_path(".\menu_prin.ui"))


class GUI:

    def __init__(self):
        self.splash_dialog = SplashDialog()
        self.signin_dialog = SignInDialog()
        self.signup_dialog = SignUpDialog()
        self.chat = Chat()
        self.menu_prin = MenuPrincipal()

        self.__bind_signals()
        self.splash_dialog.show()
        self.splash_dialog.raise_()

        self.username = None
        self.password = None

    def on_signin_dialog_signin_button_click(self, username, password):
        """Callback luego de presionar el botón `Ingresar` en diálogo de ingreso.
        # Aca ver si existe o no

        Retorna:
            bool -- si el ingreso es exitoso, es verdadero. En otro caso, falso.
        """
        return True

    def on_signup_dialog_signup_button_click(self, username, password, confirm_password):
        """Callback luego de presionar el botón `Registrarse` en diálogo de registro.

        Retorna:
            bool -- si el registro es exitoso, es verdadero. En otro caso, falso.
        """
        return True

    def on_chat_load(self):
        pass

    def on_menu_prin_load(self):

        pass

    def __bind_signals(self):
        # SplashDialog signals
        self.splash_dialog.signInButton.clicked.connect(
            self.__on_splash_dialog_signin_button_click
        )
        self.splash_dialog.signUpButton.clicked.connect(
            self.__on_splash_dialog_signup_button_click
        )
        # SignInDialog signals
        self.signin_dialog.signInButton.clicked.connect(
            self.__on_signin_dialog_signin_button_click
        )
        self.signin_dialog.backButton.clicked.connect(
            self.__on_signin_dialog_back_button_click
        )

        # SignUpDialog signals
        self.signup_dialog.signUpButton.clicked.connect(
            self.__on_signup_dialog_signup_button_click
        )
        self.signup_dialog.backButton.clicked.connect(
            self.__on_signup_dialog_back_button_click
        )

        # MenuPrincipal signals
        self.menu_prin.nueva_sala.clicked.connect(
            self.__on_menu_prin_nueva_sala_click
        )
        self.menu_prin.unir_sala.clicked.connect(
            self.__on_menu_prin_unir_sala_click
        )
        self.menu_prin.log_off.clicked.connect(
            self.__on_menu_prin_log_off_click
        )

    def __on_splash_dialog_signin_button_click(self):
        self.__toggle_windows(self.signin_dialog, self.splash_dialog)

    def __on_splash_dialog_signup_button_click(self):
        self.__toggle_windows(self.signup_dialog, self.splash_dialog)

    def __on_signin_dialog_signin_button_click(self):
        self.username = self.signin_dialog.usernameLineEdit.text()
        self.password = self.signin_dialog.passwordLineEdit.text()

        if self.on_signin_dialog_signin_button_click(self.username, self.password):
            self.menu_prin.welcomeLineEdit.setText(
                "Bienvenido {}".format(self.username)
            )
            self.on_menu_prin_load()
            self.__toggle_windows(self.menu_prin, self.signin_dialog)
        else:
            self.__show_critical_message_box(
                self.signin_dialog, """Ocurrió un error en el ingreso,
usuario incorrecto o clave incorrecta"""
            )

    def __on_signin_dialog_back_button_click(self):
        self.__toggle_windows(self.splash_dialog, self.signin_dialog)

    def __on_signup_dialog_signup_button_click(self):
        self.username = self.signup_dialog.usernameLineEdit.text()
        self.password = self.signup_dialog.passwordLineEdit.text()
        confirm_password = self.signup_dialog.confirmPasswordLineEdit.text()

        if self.password != confirm_password:
            self.__show_critical_message_box(
                self.signup_dialog, "Contrasennas no coinciden."
            )

        elif self.on_signup_dialog_signup_button_click(self.username, self.password, confirm_password):
            self.menu_prin.welcomeLineEdit.setText(
                "Bienvenido {}".format(self.username)
            )
            self.on_menu_prin_load()
            self.__toggle_windows(self.menu_prin, self.signup_dialog)
        else:
            self.__show_critical_message_box(
                self.signup_dialog, "Ocurrió un error en el registro. Su usuario ya existe"
            )

    def __on_signup_dialog_back_button_click(self):
        self.__toggle_windows(self.splash_dialog, self.signup_dialog)

    def __on_menu_prin_nueva_sala_click(self):
        self.__toggle_windows(self.chat, self.menu_prin)
        self.chat.connectedLabel.setText(
            "Conectado como {}".format(self.username)
        )

    def __on_menu_prin_unir_sala_click(self):
        self.__toggle_windows(self.chat, self.menu_prin)
        self.chat.connectedLabel.setText(
            "Conectado como {}".format(self.username)
        )
        # Falta arreglar Aca

    def __on_menu_prin_log_off_click(self):
        self.__toggle_windows(self.splash_dialog, self.menu_prin)

    def __reset_text_fields(self, text_fields):
        for text_field in text_fields:
            text_field.setText("")

    def __toggle_windows(self, incoming, outgoing):
        outgoing.close()
        text_fields = getattr(outgoing, "text_fields", None)
        if text_fields is not None:
            self.__reset_text_fields(text_fields)
        incoming.show()
        incoming.raise_()

    def __show_critical_message_box(self, parent, msg):
        QtGui.QMessageBox.critical(parent, "Programillo", msg)


class SplashDialog(*splash_dialog_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class SignInDialog(*signin_dialog_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.text_fields = (self.usernameLineEdit, self.passwordLineEdit)


class SignUpDialog(*signup_dialog_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.text_fields = (self.usernameLineEdit, self.passwordLineEdit,
                            self.confirmPasswordLineEdit)


class Chat(*chat_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.paint = Paint()
        self.btn_paint = QPushButton("Dibujar")
        self.btn_delete = QPushButton("Borrar")
        self.btn_clear = QPushButton("Clear")
        self.palabra = QLabel('Palabra: ', self)
        self.il_paint.addWidget(self.btn_paint)
        self.il_paint.addWidget(self.btn_delete)
        self.il_paint.addWidget(self.btn_clear)
        self.il_paint.addWidget(self.palabra)
        self.il_paint.addWidget(self.paint)
        self.btnDefault = "background-color: grey; border: 0; padding: 10px"
        self.btnActive = "background-color: orange; border: 0; padding: 10px"

        self.btn_paint.setStyleSheet(self.btnDefault)
        self.btn_delete.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)

        self.btn_paint.clicked.connect(self.isPaint)
        self.btn_delete.clicked.connect(self.isDelete)
        self.btn_clear.clicked.connect(self.isClear)

    def enable_button(self, b=True):
        self.btn_clear.setEnabled(b)
        self.btn_paint.setEnabled(b)
        self.btn_delete.setEnabled(b)

    def resizeEvent(self, event):
        self.paint.setSceneRect(QRectF(self.paint.viewport().rect()))

    def isPaint(self):
        if self.paint.isPaint == False:
            self.paint.isPaint = True
            self.btn_paint.setStyleSheet(self.btnActive)
        else:
            self.paint.isPaint = False
            self.btn_paint.setStyleSheet(self.btnDefault)

        self.paint.isDelete = False
        self.paint.isClear = False
        self.btn_delete.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)

    def isDelete(self):
        if self.paint.isDelete == False:
            self.paint.isDelete = True
            self.btn_delete.setStyleSheet(self.btnActive)
        else:
            self.paint.isDelete = False
            self.btn_delete.setStyleSheet(self.btnDefault)

        self.paint.isPaint = False
        self.paint.isClear = False
        self.btn_paint.setStyleSheet(self.btnDefault)
        self.btn_clear.setStyleSheet(self.btnDefault)

    def isClear(self):
        if self.paint.isClear == False:
            self.paint.isClear = True
            self.btn_clear.setStyleSheet(self.btnActive)
        else:
            self.paint.isClear = False
            self.btn_clear.setStyleSheet(self.btnDefault)

        self.paint.isPaint = False
        self.paint.isDelete = False
        self.btn_paint.setStyleSheet(self.btnDefault)
        self.btn_delete.setStyleSheet(self.btnDefault)
        self.paint.scene.clear()


class MenuPrincipal(*menu_prin_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.background_label = QLabel('', self)
        self.background_label.setPixmap(
            QPixmap(get_absolute_path(".\imagenes\\background3_1.jpg")).scaled(1000, 100))
        # self.background_label.lower()

        self.background_label.move(0, 20)

        salir = QtGui.QAction(QtGui.QIcon(None), '&Salir', self)
        salir.setShortcut('Q')
        salir.setStatusTip('Terminar la aplicación')
        salir.triggered.connect(self.exit_)  # Seguro que quiere salir?

        menubar = self.menuBar()

        archivo_menu = menubar.addMenu('&Archivo')
        archivo_menu.addAction(salir)

        self.statusBar().showMessage('Listo')

    def exit_(self):
        sys.exit()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    gui = GUI()
    app.exec_()
