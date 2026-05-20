from PyQt6.QtGui import QPixmap
from view.product_wind_ui import Ui_Form
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from service.database import DBService

class ProductForm(QWidget, Ui_Form):
    def __init__(self, user=None):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.product_list = DBService().get_serv()
        if self.user:
            self.name_l.setText(self.user.username)
        if self.product_list:
            self.display_product(self.product_list)
            filt_dict = {product.id_type: product.name for product in self.product_list}
            self.filt_cb.addItem("Все Типы", 0)
            for type_id, name_type in filt_dict.items():
                self.filt_cb.addItem(name_type, type_id)
            self.sort_cb.addItem("Ничего", 0)
            self.sort_cb.addItem("По возрастанию", 1)
            self.sort_cb.addItem("По убыванию", 2)
        if not self.user or not self.user.role_id in (1, 2):
            self.search_l.hide()
            self.filt_cb.hide()
            self.sort_cb.hide()
        if self.user and self.user.role_id == 1:
            self.add_btn.clicked.connect(self.add)
        else:
            self.add_btn.hide()
        self.search_l.textChanged.connect(lambda: self.dop_func())
        self.filt_cb.currentIndexChanged.connect(lambda: self.dop_func())
        self.sort_cb.currentIndexChanged.connect(lambda: self.dop_func())
        self.exit_btn.clicked.connect(lambda: self.exit())

    def display_product(self, product_list):
        old = self.scrollArea.takeWidget()
        if old:
            old.deleteLater()
        self.display_widget = QWidget()
        self.scrollArea.setWidget(self.display_widget)
        self.product_layout = QVBoxLayout()
        self.display_widget.setLayout(self.product_layout)

        for product in product_list:
            product_widget = QWidget()
            product_layout = QHBoxLayout()
            product_widget.setLayout(product_layout)
            self.product_layout.addWidget(product_widget)
            if product.discount > 0:
                disc_price = round(product.price * (1 - product.discount / 100), 2)
                price_text = f"<s style= 'color: red'>{product.price}</s> {disc_price}"
            else:
                price_text = str(product.price)
            if self.user and self.user.role_id == 1:
                btn = QPushButton("Удалить")
                btn.clicked.connect(lambda ch, sid=product.id_service: self.delete(sid))
                product_layout.addWidget(btn)
            photo_l = QLabel()
            photo_l.setFixedSize(200, 200)
            photo_l.setStyleSheet("border: 1px solid black")
            photo = product.photo if product.photo else QPixmap("data/image.png")
            photo_l.setPixmap(photo.scaled(photo_l.size()))
            product_layout.addWidget(photo_l)
            info_l = QLabel(f"{product.naming}<br>"
                            f"{product.descrip}<br>"
                            f"{price_text}<br>")
            info_l.setFixedHeight(200)
            info_l.setStyleSheet("border: 1px solid black")
            info_l.setWordWrap(True)
            product_layout.addWidget(info_l)
            disc_l = QLabel(f"Текущая скидка {product.discount}")
            disc_l.setFixedHeight(200)
            disc_l.setStyleSheet("border: 1px solid black")
            disc_l.setWordWrap(True)
            product_layout.addWidget(disc_l)

    def dop_func(self):
        searcher = self.search_l.text().split()
        filt = self.filt_cb.currentData()
        sorter = self.sort_cb.currentData()
        dop_list = self.product_list
        if searcher:
            dop_list = [p for p in dop_list if all(word in f"{p.naming} {p.descrip} {p.name}".lower() for word in searcher)]
        if filt != 0:
            dop_list = [product for product in dop_list if product.id_type == filt]
        if sorter != 0:
            dop_list = sorted(dop_list, key=lambda product: product.price, reverse= False if sorter == 1  else True)

        self.display_product(dop_list)

    def add(self):
        from service.add_wind import AddProd
        dialog = AddProd(self)
        if dialog.exec():
            self.product_list = DBService().get_serv()
            if self.product_list:
                self.display_product(self.product_list)

    def delete(self, id_service):
        DBService().delete(id_service)
        self.product_list = DBService().get_serv()
        self.display_product(self.product_list)

    def exit(self):
        from service.auth import AuthWind
        self.wind = AuthWind()
        self.wind.show()
        self.close()