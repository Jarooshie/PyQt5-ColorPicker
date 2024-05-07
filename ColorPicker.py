from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ColorUtils import *

def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

class HueMap(QLabel):
    color_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(HueMap, self).__init__(*args, **kwargs)

        self.H = 0

        self.setFixedSize(20,250)
        self.setScaledContents(True)

        self.setPixmap(QPixmap('assets/hue-map.png'))

        self._cursor = QLabel("",self.parent())

        self._cursor.setGeometry(self.x() - self.width() // 2,self.y() - self._cursor.height() // 2,40,8)

        self._cursor.setPixmap(QPixmap('assets/map_cursor.png'))
        self._cursor.setScaledContents(True)
        self._cursor.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._cursor.lower()

    def setHueMapWidth(self,width=20):
        self.setFixedWidth(width)

    def setHue(self, hue):
        self.cursor_posY = int((1-hue) * self.height())


        self._cursor.move(self.x() - self.width() // 2,self.cursor_posY - self._cursor.height() // 2 + self.y())

        self.H = hue

        self.color_changed.emit()

    def mousePressEvent(self, event):
        mouse = QCursor().pos()
        self._Y = mouse.y() - self.parent().frameGeometry().y()  - self.frameGeometry().y() - 30

        self.cursor_posY = clamp(self._Y,0,self.height())

        self._cursor.move(self.x() - self.width() // 2,self.cursor_posY - self._cursor.height() // 2 + self.y())

        self.H = 1 - self.cursor_posY / self.height()

        self.oldPos = event.globalPos()

        self.color_changed.emit()

    def mouseMoveEvent(self, event):
        mouse = QCursor().pos()
        self._Y = mouse.y() - self.parent().frameGeometry().y()  - self.frameGeometry().y() - 30

        self.cursor_posY = clamp(self._Y,0,self.height())


        self._cursor.move(self.x() - self.width() // 2,self.cursor_posY - self._cursor.height() // 2 + self.y())

        self.H = 1 - self.cursor_posY / self.height()

        self.oldPos = event.globalPos()

        self.color_changed.emit()


    def moveEvent(self, event):
        self._cursor.setGeometry(self.x() - self.width() // 2,self.y() - self._cursor.height() // 2,40,8)

class ColorPicker(QLabel):
    color_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ColorPicker, self).__init__(*args, **kwargs)

        self.H = 1.0
        self.S = 1.0
        self.V = 1.0

        self.RGB = hsv_to_rgb(self.H,self.S,self.V)

        self.realHue = 0

        self.setPixmap(QPixmap('assets/SV250x250.png'))
        self.setScaledContents(True)

        self.map = HueMap("", self.parent())

        self.map.move(self.width()+self.x()+20, self.y())

        self.map.color_changed.connect(self.changeHue)

        self._cursor = QLabel("",self.parent())


        self._cursor.setGeometry(self.x() + self.width() // 2,self.y() - self._cursor.height() // 2,10,10)
        self._cursor.setPixmap(QPixmap('assets/cursor.png'))
        self._cursor.setScaledContents(True)
        self._cursor.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._cursor.setObjectName("cursor")
        self._cursor.setStyleSheet("#cursor { background-color: none }")

        self.map.color_changed.connect(self.changeColorPickerHue)
        self.map.color_changed.connect(self.updateRGB)
        self.color_changed.connect(self.updateRGB)
        self.setStyleSheet("QWidget{background-color:#ff0000;}")

        self.map.color_changed.connect(self.color_changed.emit)

    def setHueMapWidth(self,width=20):
        self.map.setFixedWidth(width)

    def changeHue(self):
        self.H = self.map.H

    def changeColorPickerHue(self):
        self.realHue = (self.map.H * 360) % 360

        self.setStyleSheet(f"QWidget{{background-color:hsv({self.realHue}, 100%, 100%);}}")

    def getColorRGB(self):
        return hsv_to_rgb(self.H,self.S,self.V)
    
    def getColorHSL(self):
        return hsv_to_hsl(self.H,self.S,self.V)
    
    def getColorHSV(self):
        return (self.H,self.S,self.V)
    
    def getColorHEX(self):
        return rgb_to_hex(*self.getColorRGB())

    def updateRGB(self):
        self.RGB = hsv_to_rgb(self.H,self.S,self.V)

    def setSatuarationValue(self, sat, val):
        val = 1-val
        self.cursor_posX = int(sat * self.width())
        self.cursor_posY = int(val * self.height())

        self._cursor.move(self.cursor_posX - self._cursor.width() // 2 + self.x(),self.cursor_posY - self._cursor.height() // 2 + self.y())

        self.S = sat
        self.V = 1-val

        self.color_changed.emit()

    def setColorHEX(self, hex : str):
        h, s, v = hex_to_hsv(hex)
        self.map.setHue(h)
        self.setSatuarationValue(s,v + 0.001)

    def mousePressEvent(self, event):
        mouse = QCursor().pos()
        self._X = mouse.x() - self.parent().frameGeometry().x() - self.frameGeometry().x()
        self._Y = mouse.y() - self.parent().frameGeometry().y()  - self.frameGeometry().y() - 30

        self.cursor_posX = clamp(self._X,0,self.width())
        self.cursor_posY = clamp(self._Y,0,self.height())

        self._cursor.move(self.cursor_posX - self._cursor.width() // 2 + self.x(),self.cursor_posY - self._cursor.height() // 2 + self.y())

        self.S = self.cursor_posX / self.width()
        self.V = 1 - self.cursor_posY / self.height()

        self.oldPos = event.globalPos()

        
        self.color_changed.emit()

    def mouseMoveEvent(self, event):
        mouse = QCursor().pos()
        self._X = mouse.x() - self.parent().frameGeometry().x() - self.frameGeometry().x()
        self._Y = mouse.y() - self.parent().frameGeometry().y()  - self.frameGeometry().y() - 30

        self.cursor_posX = clamp(self._X,0,self.width())
        self.cursor_posY = clamp(self._Y,0,self.height())

        self._cursor.move(self.cursor_posX - self._cursor.width() // 2 + self.x(),self.cursor_posY - self._cursor.height() // 2 + self.y())

        self.S = self.cursor_posX / self.width()
        self.V = 1 - self.cursor_posY / self.height()

        self.oldPos = event.globalPos()

        self.color_changed.emit()

    def moveEvent(self, event):
        self.map.move(self.width()+self.x()+20, self.y())
        self._cursor.setGeometry(self.x() + self.width() - self._cursor.width() // 2,self.y() - self._cursor.height() // 2,10,10)

    def resizeEvent(self, event):
        self.map.setFixedHeight(self.height())