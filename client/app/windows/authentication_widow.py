from PyQt6.QtWidgets import QMainWindow

from app.ui.authentication_window import Ui_MainWindow
from app.classes.user import User
from .main_widow import MainApplicationGUI

class LoginApplicationGUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user: User = User()

        self.ui.registration.hide()
        self.ui.label_error_log.hide()
        self.ui.label_error_reg.hide()

        callBacks = [
            [self.ui.btn_login, self.auth],
            [self.ui.btn_register, self.registration],
            [self.ui.btn_go_login, self.swap_to_login],
            [self.ui.btn_go_register, self.swap_to_registration]
        ]
        for callback in callBacks:
            callback[0].clicked.connect(callback[1])

    
    def auth(self)->None:
        # username = self.ui.username_log.text()
        # password = self.ui.password_log.text()
        username = 'admin'
        password = 'admin'
        self.user.login(username, password)
        if self.user.is_authorized():
            self.auth_user()
        else:
            self.ui.label_error_log.setText(self.user.get_message())
            self.ui.label_error_log.show()

    
    def registration(self)->None:
        username = self.ui.username_reg.text()
        password_1 = self.ui.password_reg.text()
        password_2 = self.ui.password_reg_dop.text()
        self.user.registration(username, password_1, password_2)
        if self.user.is_authorized():
            self.auth_user()
        else:
            self.ui.label_error_reg.setText(self.user.get_message())
            self.ui.label_error_reg.show()


    def swap_to_registration(self)->None:
        self.ui.login.hide()
        self.ui.label_error_log.hide()
        self.ui.label_error_reg.hide()
        self.clear_all_edits()
        self.ui.registration.show()

    def swap_to_login(self)->None:
        self.ui.registration.hide()
        self.ui.label_error_log.hide()
        self.ui.label_error_reg.hide()
        self.clear_all_edits()
        self.ui.login.show()

    def clear_all_edits(self)->None:
        for edit in [self.ui.username_log, self.ui.password_log, self.ui.username_reg, self.ui.password_reg, self.ui.password_reg_dop]:
            edit.clear()

    def auth_user(self)->None:
        self.SecondWindow: MainApplicationGUI = MainApplicationGUI(user=self.user)
        self.close()
        self.SecondWindow.show()