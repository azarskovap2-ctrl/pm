from service.database import DBService
from PyQt6.QtWidgets import QWidget, QMessageBox
from view.auth_wind_ui import Ui_Form

class AuthWind(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.enter_btn.clicked.connect(lambda: self.auth())
        self.guest_btn.clicked.connect(lambda: self.open_wind())

    def auth(self):
        login = self.login_l.text().strip()
        password = self.password_l.text().strip()
        if not login or not password:
            QMessageBox.warning(None, "Ошибка", "Неверный логин или пароль")
        user = DBService().get_user(login, password)
        if user:
            self.open_wind(user)
        return None

    def open_wind(self, user=None):
        from service.product_form import ProductForm
        self.wind = ProductForm(user)
        self.wind.show()
        self.close()