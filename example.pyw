import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

from ColorUtils import *
from ColorPicker import ColorPicker

def changeStyleSheet(object : any, stylesheet : str) -> None: # Made to avoid stylesheet conflict crash error
    if object.styleSheet() != stylesheet:
        object.setStyleSheet(stylesheet)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Picker")

        self.setFixedWidth(370)
        self.setFixedHeight(300)
        
        self.setStyleSheet("QWidget{ background-color: #1a1a1a; }")

        self.picker = ColorPicker("", self)

        self.picker.move(20,20)

        self.picker.setFixedSize(200,200)

        self.color = QLabel("#ff0000",self.picker.parent())
        self.color.setAlignment(Qt.AlignCenter)
        self.color.setGeometry(self.picker.x(), self.picker.y() + self.picker.height()  + 10,self.picker.width(),50)

        self.colorText = QLabel("",self.picker.parent())
        self.colorText.setGeometry(self.color.x() + self.color.width() + 10,self.color.y(),50,50)
        self.colorText.setText("R: 255\nG: 0\nB: 0")
        self.colorText.setStyleSheet("color: #ffffff;")

        self.color.setStyleSheet("background-color: #ff0000;border-radius: 5px;")
        
        self.picker.color_changed.connect(lambda: changeStyleSheet(self.color,f"""
                                                                background-color: hsv({self.picker.realHue},{self.picker.S * 100}%,{self.picker.V * 100}%);
                                                                border-radius: 5px;
                                                              """))
        
        self.picker.color_changed.connect(lambda: self.colorText.setText(f"R: {int(self.picker.RGB[0])}\nG: {int(self.picker.RGB[1])}\nB: {int(self.picker.RGB[2])}"))

        self.picker.color_changed.connect(lambda: self.color.setText(self.picker.getColorHEX()))
        self.picker.color_changed.connect(lambda: changeStyleSheet(self.color,f"""color: {optimal_hex_for_readability(*self.picker.getColorRGB())};
                                                                background-color: hsv({self.picker.realHue},{self.picker.S * 100}%,{self.picker.V * 100}%);
                                                                border-radius: 5px;
                                                              """))
        
        self.palletes = []
        for i in range(6):
            pallete = QPushButton(generate_monochromatic_colors("#ff0000")[i],self.picker.parent())
            pallete.setGeometry(self.picker.width()+self.picker.x()+80, self.picker.y()+ i*40 + 5*i,50,40)
            pallete.setStyleSheet(f"color: {optimal_hex_for_readability(*hex_to_rgb('#ff0000'))};background-color: {generate_monochromatic_colors('#ff0000')[i]};border-radius: 5px;")

            self.palletes.append(pallete)
        
        self.palletes[0].clicked.connect(lambda: print(self.palletes[0].text()))
        self.palletes[0].clicked.connect(lambda: self.picker.setColorHEX(self.palletes[0].text()))

        self.palletes[1].clicked.connect(lambda: print(self.palletes[1].text()))
        self.palletes[1].clicked.connect(lambda: self.picker.setColorHEX(self.palletes[1].text()))

        self.palletes[2].clicked.connect(lambda: print(self.palletes[2].text()))
        self.palletes[2].clicked.connect(lambda: self.picker.setColorHEX(self.palletes[2].text()))

        self.palletes[3].clicked.connect(lambda: print(self.palletes[3].text()))
        self.palletes[3].clicked.connect(lambda: self.picker.setColorHEX(self.palletes[3].text()))

        self.palletes[4].clicked.connect(lambda: print(self.palletes[4].text()))
        self.palletes[4].clicked.connect(lambda: self.picker.setColorHEX(self.palletes[4].text()))

        self.palletes[5].clicked.connect(lambda: print(self.palletes[5].text())) # idk why loops dont work on this
        self.palletes[5].clicked.connect(lambda: self.picker.setColorHEX(self.palletes[5].text()))

        self.picker.color_changed.connect(lambda: changePalleteVisual(self.palletes,generate_monochromatic_colors(self.picker.getColorHEX())))

        self.show()

def changePalleteVisual(obj : list[QLabel] , color : list[str]):
    for i, label in enumerate(obj):
        label.setText(color[i])
        label.setStyleSheet(f"color: {optimal_hex_for_readability(*hex_to_rgb(color[i]))};background-color: {color[i]};border-radius: 5px;")

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())