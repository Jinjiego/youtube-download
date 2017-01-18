from PyQt5 import QtWidgets,QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import  QVBoxLayout
class MyBaseWidget(QtWidgets.QWidget):#QtWidgets.QWidget):
     # base wiidget ,it has no border,
    """description of class"""
    def __init__(self):
         super(MyBaseWidget,self).__init__()
         self.setContentsMargins(0,0,0,0)
         self.setAutoFillBackground(True) # this function must be called otherwise background picture setting error!
         self.setWindowFlags(Qt.FramelessWindowHint)

    # background can be set
    def setBackgrd(self,img_path):
         palette=QtGui.QPalette()
         icon=QtGui.QPixmap(img_path)
         palette.setBrush(self.backgroundRole(), QtGui.QBrush(icon)) #添加背景图片
         self.setPalette(palette)
    def addWidget2Grid(self,widget):
            pass
    def addWidget2VBox(self,widget):
        self.main_layout=QVBoxLayout()
        self.main_layout.addWidget(widget)
        self.setLayout(self.main_layout)