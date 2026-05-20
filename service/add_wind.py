from PyQt6.QtWidgets import QDialog, QMessageBox
from view.add_wind_ui import Ui_Dialog
from service.database import DBService

class AddProd(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = DBService()
        self._load_ref()
        self.save_btn.clicked.connect(lambda: self.save())
        self.cancel_btn.clicked.connect(lambda: self.reject())

    def _load_ref(self):
        refs = self.db.get_ref()
        if not refs:
            return
        for id_type, name in refs["types"]:
            self.type_cb.addItem(name, id_type)

    def save(self):
        naming = self.name_l.text().strip()
        if not naming:
            QMessageBox.warning(self, "Ошибка", "Поле название обязательно")
            return
        descrip = self.desc_l.text().strip()
        price = self.price_box.value()
        discount = self.disc_box.value()
        id_type = self.type_cb.currentData()
        photo = self.photo_l.text().strip() or None

        ok = self.db.add_serv(naming, descrip, price, discount, id_type, photo)
        if ok:
            QMessageBox.information(self, "Успех", "Успешно добавлено")
            self.accept()