from PyQt5.QtGui import  QIcon
from PyQt5.QtWidgets import  QPushButton
from PyQt5.QtCore import QSize
class AeroButton(QPushButton):
    def __init__(self, a, b,parent=None):
        super(AeroButton, self).__init__(parent)
        self.setEnabled(True)
        self.a= a
        self.b= b
        self.count = 0
        self.InitIcon()
        self.setStyleSheet('''QPushButton{
               height:30px;
               border-radius: 15px;}''')
    def InitIcon(self):
        self.setIcon(QIcon(self.a))
        self.setIconSize(QSize(30, 30))
        self.setIconSize(self.iconSize())
    def enterEvent(self, *args, **kwargs):
        self.setIcon(QIcon(self.b))

    def leaveEvent(self, event):
        self.hovered = False
        self.setIcon(QIcon(self.a))

