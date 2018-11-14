# Copyright (C) 2018 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland
#     Multimedia Signal Processing Group
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Mehmet Tuzmen, master student
# Organisation: Multimedia Signal Processing Group (MMSPG), EPFL


import sys
import argparse
import ctypes
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--image', default='', type=str,
                    help='The filename of the image to draw inpainting mask')

parser.add_argument('--pen_width', default=12, type=int,
                    help='The width of the inpainting pen')


class Drawer(QWidget):
    newPoint = pyqtSignal(QPoint)

    def __init__(self, image_path, width, height, pen_width, parent=None):
        QWidget.__init__(self, parent)
        self.path = QPainterPath()
        self.image_path = image_path
        self.width = ctypes.windll.user32.GetSystemMetrics(0)
        self.height = ctypes.windll.user32.GetSystemMetrics(0)/2
        self.pen_width = pen_width

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)
        painter.drawPixmap(QRect(0, 0, self.width, self.height), pixmap)

        painter.setPen(QPen(Qt.black, self.pen_width))
        painter.drawPath(self.path)

    def mousePressEvent(self, event):
        if event.pos().y() >= self.height:
            return

        self.path.moveTo(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        if event.pos().y() >= self.height:
            return

        self.path.lineTo(event.pos())
        self.newPoint.emit(event.pos())
        self.update()

    def sizeHint(self):
        return QSize(self.width, self.height)

    def reset(self):
        self.path = QPainterPath()
        self.update()


class InpaintingMaskCreationApp(QWidget):

    def __init__(self, img_path, pen_width):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.title = 'Inpaint Application'
        self.input = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = Image.open(img_path)
        self.width = img.width
        self.height = img.height
        self.pen_width = pen_width

        self.drawer = Drawer(img_path, self.width, self.height, self.pen_width, self)
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.layout().addWidget(self.drawer)
        self.layout().addWidget(QPushButton("Inpaint!", clicked=self.inpaint))
        self.show()

    def inpaint(self):
        mask = QImage(ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(0)/2, QImage.Format_RGB32)
        #mask = QImage(1024, 1024, QImage.Format_RGB32)

        mask.fill(qRgb(255, 255, 255))
        painter = QPainter()
        painter.begin(mask)
        painter.setPen(QPen(Qt.black, self.pen_width))
        painter.drawPath(self.drawer.path)
        painter.end()
        mask.scaled(self.width, self.height)
        result = mask.scaled(self.width, self.height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        result.invertPixels()
        result.save("./mask.jpg", "jpg")
        self.drawer.reset()


if __name__ == '__main__':
    args = parser.parse_args()
    app = QApplication(sys.argv)
    ex = InpaintingMaskCreationApp(args.image, args.pen_width)
    #ex.setFixedHeight(ctypes.windll.user32.GetSystemMetrics(1))
    #ex.setFixedWidth(ctypes.windll.user32.GetSystemMetrics(0))
    ex.showFullScreen()
    #ex.showMaximized()
    sys.exit(app.exec_())
