import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ColorUtils import *
from ColorPicker import ColorPicker

def changeStyleSheet(object : any, stylesheet : str) -> None: # Made to avoid stylesheet conflict crash error
    if object.styleSheet() != stylesheet:
        object.setStyleSheet(stylesheet)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Picker ex1")

        self.setFixedWidth(280)
        self.setFixedHeight(240)
        
        self.setStyleSheet("QWidget{ background-color: #1a1a1a; }")

        self.picker = ColorPicker("", self)
        self.picker.move(20,20)
        self.picker.setFixedSize(200,200)

        self.picker.color_changed.connect(lambda: changeStyleSheet(self,f"background-color: {self.picker.getColorHEX()};"))

        self.show()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())