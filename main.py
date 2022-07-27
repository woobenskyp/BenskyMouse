from PySide6.QtWidgets import QApplication
from BenskyMouseGui import BenskyMouseGui
import ctypes.wintypes


app = QApplication([])

gui = BenskyMouseGui()
gui.show()
app.exec()

















