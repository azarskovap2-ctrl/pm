from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox
from data.User import User
from data.Product import Product
import pymysql
class DBService:
    def __init__(self):
        self.conn = None
        try:
            self.conn = pymysql.connect(host="localhost", user="root", password="aanton06", database="photo_ate")
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка подключения {e}")

    def get_user(self, login, password):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT u.id_user, u.username, u.role_id, r.name FROM user u
                JOIN role r on r.role_id = u.role_id
                WHERE u.login = %s AND u.password =%s""", (str(login), str(password)))
                result = cur.fetchall()
                if result:
                    return User(*result[0])
                else:
                    QMessageBox.warning(None, "Ошибка", "Пользователь не найден")
                    return False
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка подключения {e}")
            return False

    def get_serv(self):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT s.id_service, s.naming, s.descrip, s.price, s.discount, s.id_type, ts.name, s.photo FROM service s
JOIN type_serv ts on ts.id_type = s.id_type""")
                result = cur.fetchall()
                product_list = []
                if result:
                    for product in result:
                        photo_pixmap = QPixmap(f"data/{product[7]}") if product[7] else None
                        product_list.append(Product(*product[:7], photo_pixmap))
                    return product_list

                else:
                    QMessageBox.warning(None, "Ошибка", "Товары не получены")
                    return False
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка подключения {e}")
            return False

    def get_ref(self):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT id_type, name FROM type_serv""")
                types = cur.fetchall()
                return {"types": types}
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка подключения {e}")
            return False

    def add_serv(self, naming, descrip, price, discount, id_type, photo):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""INSERT INTO service(naming, descrip, price, discount, id_type, photo) 
                VALUES (%s, %s, %s, %s, %s, %s)""", (naming, descrip, price, discount, id_type, photo))
                self.conn.commit()
                return True
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка подключения {e}")
            return False

    def delete(self, id_service):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""DELETE FROM service WHERE id_service = %s""", (id_service, ))
                self.conn.commit()
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Ошибка подключения {e}")
            return False