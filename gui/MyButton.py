
from PyQt5.QtWidgets import  QPushButton

class MyButton(QPushButton):#QtWidgets.QWidget):
    """description of class"""
    def __init__(self,arg,icon_path1,icon_path2):
         super(MyButton,self).__init__(arg)
         self.setEnabled(True)
         self.icon_path1=icon_path1
         self.icon_path2=icon_path2
         self.setStyleSheet('''QPushButton{
          background:url('''+self.icon_path1+''');
          background-repeat:no-repeat;
          color:white;
          font-size:15px;
          min-height: 45px;
          max-width:233px;
          background-position:Left;
          border-radius: 1px;}''')
         # self.setIcon(QIcon(self.Icon_path))
         # self.setIconSize(QSize(30, 30))
         # self.setFixedSize(self.iconSize())
    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet('''QPushButton{
                  background:url(''' +self.icon_path2 + ''');
                  background-repeat:no-repeat;
                  color:white;
                  font-size:15px;
                  min-height: 45px;
                  max-width:233px;
                  background-position:Left;
                  border-radius: 1px;}''')
    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet('''QPushButton{
                  background:url(''' + self.icon_path1 + ''');
                  background-repeat:no-repeat;
                  color:white;
                  font-size:15px;
                  min-height: 45px;
                  max-width:233px;
                  background-position:Left;
                  border-radius: 1px;}''')
