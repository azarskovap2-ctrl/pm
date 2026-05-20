# import sys
# from PyQt6.QtWidgets import *
# from service.auth import *
#
# app = QApplication(sys.argv)
# wind = AuthWind()
# wind.show()
# sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import *
from service.auth import *

app = QApplication(sys.argv)
wind = AuthWind()
wind.show()
sys.exit(app.exec())
