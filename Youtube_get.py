#import youtube_dl
#coding=gbk
import  sys
from gui.MyApp import *
def main():

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
    sys.exit()

if __name__ == "__main__":
   main()
   
   




