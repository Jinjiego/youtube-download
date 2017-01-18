from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QMessageBox,QTableWidgetItem,QLabel, QLineEdit,
    QHBoxLayout,QGridLayout, QVBoxLayout,QSplitter,
    QProgressBar,QTableWidget,QMenu)
import re
from gui.my_resourse import *
from youtube_dlb import YoutubeDL
from  gui.MyBaseWidget import  *
from gui.ButtonTest import  *
from gui.MyButton import  *
class MyApp(QtWidgets.QWidget):

    def __init__(self):
        super(MyApp,self).__init__()
        self.setContentsMargins(0,0,0,0)
        self.setWindowOpacity(5)
        self.setWindowTitle("youtube-get")
        self.resize(1100,700)  #setWindowState(Qt.Qt.WindowMaximized)
        #mainWidget=QtWidgets.QWidget()  #窗口中的主Widget,不知如何在QMainWidow中加入布局
                                         #所以要设置一个Widget将其放置在QMainWindow 的中心
        #self.setWindowFlags(Qt.FramelessWindowHint)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor(0, 0, 0))  # 设置背景颜色
        self.setPalette(palette1)
        self.InitData()
        self.init3()

    def init3(self):
         icon = QtGui.QIcon()
         icon.addPixmap(QtGui.QPixmap(":/Images/Icon256x256.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
         self.setWindowIcon(icon)
         self.setWindowFlags(Qt.FramelessWindowHint)
         main_lay=QVBoxLayout()
         # ====================move widget to the center of screen==============================
         desktop = QtWidgets.QApplication.desktop()
         width = desktop.width()
         height = desktop.height()
         self.move((width - self.width()) / 2, (height - self.height()) / 2)
         self.setMouseTracking(True)
         #===================================================

         #=====================================================
         self.main_sp = QSplitter(Qt.Horizontal)
         self.main_sp.setContentsMargins(0,0,0,0)
         self.InitLeftWidget()
         self.InitRightWidget()

         self.main_sp.addWidget( self.LeftWidget)
         self.main_sp.setHandleWidth(0.1)
         self.main_sp.addWidget(self.RightWidget)
         self.main_sp.setStretchFactor(0,8)
         self.main_sp.setStretchFactor(1,6.5)
         self.main_sp.setContentsMargins(0,0,0,0)
         main_lay.addWidget(self.main_sp)
         main_lay.setContentsMargins(0,0,0,0)
         self.setLayout(main_lay)
    def closeEvent(self, QCloseEvent):

        promote=self.getDownloaingCount()
        reply=None
        if promote>=1:
            if QMessageBox.warning(self, "promote", "任务正在下载，确定退出吗？",
                                QMessageBox.Yes | QMessageBox.Cancel)== QMessageBox.Yes:
                super().closeEvent(QCloseEvent)
        else:
            super().closeEvent(QCloseEvent)

    def InitLeftWidget(self):
          #self.LeftWidget=QtWidgets.QWidget
          self.LeftWidget.setBackgrd(":/Images/tube_logo.jpg")
          left_layout=QGridLayout()
          left_layout.setRowStretch(1, 1)
          left_layout.setContentsMargins(0,0,0,0)
          self.finished = MyButton(self.tr("已完成"),":/Images/1.png",":/Images/1-1.png")

          self.finished.clicked.connect(self.Btn_finished_clicked)
          left_layout.addWidget(self.finished,2,2,1,2)
          self.downloading = MyButton(self.tr("正在下载"),":/Images/2.png",":/Images/2-1.png")
          left_layout.addWidget(self.downloading, 3, 2,1,2)
          self.Btn_config = MyButton(self.tr("设置"), ":/Images/3.png",":/Images/3-1.png")
          self.Btn_config.clicked.connect(self.Btn_finished_clicked)
          left_layout.addWidget(self.Btn_config , 4, 2, 1, 2)
          left_layout.setRowStretch(5, 3)
          left_layout.setColumnStretch(2,1)
          left_layout.setColumnStretch(1, 0)
          left_layout.setSpacing(0)
          left_layout.setAlignment(Qt.AlignLeft)
          self.LeftWidget.setLayout(left_layout)
    def InitData(self):
        self.DLT_List = [] # For storing downloding thread
        self.SBL = []      #
        self.URL_dict = {} # For
        self.Status=[]
        self.finished_clik_count=0
        # ===========================================================
        self.LeftWidget = MyBaseWidget()
        self.RightWidget = MyBaseWidget()
    def InitRightWidget(self):
        #self.RightWidget=QtWidgets.QWidget()
        self.RightWidget.setBackgrd(":/Images/right_back2.jpg")
        self.RightWidget.setWindowOpacity(0.0)
        main_right_layout=QVBoxLayout()
        self.Init_right_title()
        main_right_layout.addLayout(self.right_title_layout)

        self.Init_right_top()
        main_right_layout.addLayout( self.right_top_layout)
        self.Init_right_bottom()
        main_right_layout.addWidget(self.MyTable)

        # main_right_layout.setStretchFactor(self.right_title_layout,4)
        # main_right_layout.setStretchFactor(self.right_top_layout, 2)
        # main_right_layout.setStretchFactor(self.MyTable, 1)
        self.RightWidget.setLayout(main_right_layout)
    def Init_right_title(self):
        # ==================close Button=======================
        self.right_title_layout=QHBoxLayout()

        self.close_btn = AeroButton(":/Images/close_1.png", ":/Images/close_2.png")
        self.close_btn.clicked.connect(self.closeEvent)
        # ===================maxmal button============================
        self.maxmal_btn = AeroButton(":/Images/maxmal_1.png", ":/Images/maxmal_2.png")
        self.maxmal_btn.clicked.connect(self.showMaximized)
        # ===================minmal button=========================================
        self.minmal_btn = AeroButton(":/Images/minmal_1.png", ":/Images/minmal_2.png")
        self.minmal_btn.clicked.connect(self.showMinimized)
        #========================================================
        self.right_title_layout.addWidget(self.minmal_btn)
        self.right_title_layout.addWidget(self.maxmal_btn)
        self.right_title_layout.addWidget(self.close_btn)
        self.right_title_layout.setAlignment(Qt.AlignRight)
        self.right_title_layout.setContentsMargins(0, 0, 0, 0)
    def Init_right_top(self):
        self.right_top_layout = QGridLayout()
        self.url_Label = QLabel("Vedio URL:")
        self.Proxy_Label = QLabel("Proxy:")
        self.Vedio_url = QLineEdit()
        self.Vedio_url.setStyleSheet('''QLineEdit(max-width:200px) ''')
        self.Proxy_Url = QLineEdit()
        self.Proxy_Url.setText("https://127.0.0.1:1080")

        # self.path_label = QLabel('output：')
        # self.path = QLineEdit()
        # self.path.setText('download\\')
        self.Btn_dl = AeroButton(":/Images/dlb-1.png", ":/Images/dlb-2.png")
        self.Btn_dl.clicked.connect(self.Btn_dl_clicked)

        # self.main_layout.setSpacing(1)
        self.right_top_layout.addWidget(self.Proxy_Label, 1, 0)
        self.right_top_layout.addWidget(self.Proxy_Url, 1, 1)
        self.right_top_layout.addWidget(self.url_Label, 2, 0)
        self.right_top_layout.addWidget(self.Vedio_url, 2, 1)
        self.right_top_layout.addWidget(self.Btn_dl, 2, 3)
        #self.right_top_layout.addWidget(self.Btn_config,2,4)
        self.right_top_layout.setColumnStretch(5,1)
        self.right_top_layout.setColumnStretch(1,1)
        # self.right_top_layout.addWidget(self.path_label, 1, 3)
        # self.right_top_layout.addWidget(self.path, 1, 4)
    def Init_right_bottom(self):
        self.Horz_header = ['片名', '地址', '大小', '状态', '速度', '剩余时间']
        self.Horz_wid_ratio = [0.2, 0.2, 0.2, 0.3, 0.2, 0.1]
        self.MyTable = QTableWidget(15, len(self.Horz_header))
        self.MyTable.setContentsMargins(0,0,0,0)
        self.MyTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.MyTable.setWindowOpacity(0)
        self.MyTable.setStyleSheet('''background:transparent;
                                    selection-background-color:lightblue;''')
        self.MyTable.setStyleSheet('''background:transparent;
                                    selection-background-color:lightblue;QScrollBar{background: transparent;width: 10px;}''')
        self.MyTable.verticalHeader().setVisible(False);
        self.MyTable.horizontalHeader().setVisible(False);
        self.MyTable.customContextMenuRequested.connect(self.generateMenu)
        parent_width = self.MyTable.width()
        print('Table width:',parent_width)
        self.MyTable.setHorizontalHeaderLabels(self.Horz_header)
        self.MyTable.setShowGrid(False)
        self.MyTable.horizontalHeader().setStretchLastSection(True)
        for i in range(len(self.Horz_header)):
             print(i, parent_width * self.Horz_wid_ratio[i])
             self.MyTable.setColumnWidth(i, parent_width * self.Horz_wid_ratio[i])
    def generateMenu(self,pos):
        print(pos)

        row_num = -1
        for i in self.MyTable.selectionModel().selection().indexes():
            row_num = i.row()
        print("test")
        menu = QMenu()
        suspend = menu.addAction(u"暂停")
        goon = menu.addAction(u"继续")
        open_file_dir = menu.addAction(u"打开文件位置")
        action = menu.exec_(self.MyTable.mapToGlobal(pos))
        selected=self.MyTable.item(row_num, 1)

        if action == suspend:
           if selected:
              #test=QThread()
              #test.wait()
              #self.DLT_List[row_num].wait(10000)
              print(row_num, "线程挂起！")

        elif action == goon:
            if selected:
              print(u'您选了选项二，当前行文字内容是：', self.MyTable.item(row_num, 1).text())

        elif action == open_file_dir:
            if selected:
               print(u'您选了选项三，当前行文字内容是：', self.MyTable.item(row_num, 1).text())
        else:
            return
    def Btn_dl_clicked(self):
        # when button download clicked, append a download task to the end of table
        url_normed,check = self.verifyDlParameters()
        Id = len(self.DLT_List)
        user_opt = {"ID": Id, "url_list": [url_normed]}
        youtube_opts = {'proxy': self.Proxy_Url.text()}# "download_archive": []}
        if check == 100:  # 可以添加
            # print('+++++++++++++')
            self.URL_dict[url_normed]={'ID':Id,'position':Id,'status':1}
            self.DLT_List.append(YoutubeDL(params=youtube_opts, auto_init=True, user_opt=user_opt))
            self.SBL.append(QProgressBar())
            self.MyTable.setCellWidget(Id, 3, self.SBL[Id])
            newItem = QTableWidgetItem("未知")
            self.MyTable.setItem(Id, 0, newItem)
            self.MyTable.setItem(Id, 2, newItem)
            self.MyTable.setItem(Id, 4, newItem)
            newItem = QTableWidgetItem(self.Vedio_url.text())
            self.MyTable.setItem(Id, 1, newItem)

            self.DLT_List[-1].mySignal.connect(self.update_Dl_status)
            self.DLT_List[-1].exceptSignal.connect(self.dl_thread_except)
            self.DLT_List[-1].start()  # lunch the downloading thread.
            self.downloading.setText('正在下载('+str(self.getDownloaingCount())+')')
            print("The task has been added to the downloading list!")
        elif check ==101 :  # 下载异常
            expt=self.URL_dict[url_normed]['position']
            # print('restart task:' ,expt,url_normed)
            self.DLT_List[expt].params['proxy']=self.Proxy_Url.text()
            # print('restart task:', expt, url_normed)
            self.DLT_List[expt].user_opt["url_list"]=[url_normed]
            self.DLT_List[expt].start()
            self.URL_dict[url_normed]['status']=1
            self.downloading.setText('正在下载(' + str(self.getDownloaingCount()) + ')')
        elif check==1011: #正在下载

              QMessageBox.warning(self, "Warning", "The task has been added in downloading queue",
                                QMessageBox.Reset | QMessageBox.Help | QMessageBox.Cancel, QMessageBox.Reset)
        elif check==1010:  # finished
            QMessageBox.warning(self, "Warning", "Download finished!",
                                QMessageBox.Yes | QMessageBox.Cancel)
        elif check==102:
            QMessageBox.warning(self, "Warning", "invalid URL！",
                                QMessageBox.Reset | QMessageBox.Help | QMessageBox.Cancel, QMessageBox.Reset)
    def update_Dl_status(self, my_message):
        message = my_message.get('message')
        Id = my_message.get("ID")
        url_normed=self.getUrlwithId(Id)

        name = re.findall(re.compile(r"\[download\].*?Destination:.*?(.*)", re.S), message)
        if name: self.MyTable.setItem(Id, 0, QTableWidgetItem(name[0]))
        name=re.findall(re.compile(r"\[download\](.*)has already been downloaded", re.S),message)
        if name: self.MyTable.setItem(Id, 0, QTableWidgetItem(name[0]))
        complete = re.findall(r'\[download\](.*)%.*of.*?([0-9]+\.?[0-9]*\S*)', message)
        if complete and len(complete[0]) == 2:
            temp = complete[0]
            value = float(temp[0])
            self.SBL[Id].setValue(value)
            print('update status:',temp[1])
            self.MyTable.setItem(Id, 2, QTableWidgetItem(temp[1]))
            if abs(value - 100.0) < 1e-3:
                self.URL_dict[url_normed]['status'] = 0  # finished
                self.downloading.setText('正在下载(' + str(self.getDownloaingCount()) + ')')
        row = re.findall(re.compile(r".*?([0-9]+\.?[0-9]*)%.*of(.*)at(.*)ETA(.*)", re.S), message)
        if row and len(row[0]) >= 4:
            temp = row[0]
            # Horz_header=['片名','地址','大小','状态','速度','剩余时间']
            self.MyTable.setItem(Id, 4, QTableWidgetItem(temp[2]))
            self.MyTable.setItem(Id, 2, QTableWidgetItem(temp[1]))
            self.MyTable.setItem(Id, 5, QTableWidgetItem(temp[3]))
            # self.MyTable.setItem(Id,1, QTableWidgetItem(row[0][0]))
            self.SBL[Id].setValue(float(temp[0]))

    def getUrlwithId(self,id):
        for key in self.URL_dict.keys():
             if self.URL_dict[key]['ID']==id:
                  return key
        return None

    def getDownloaingCount(self):
        count=0
        for key in self.URL_dict.keys():
            if self.URL_dict[key]['status'] == 1:
                count+=1
        return count

    def dl_thread_except(self, message):
        except_ID = message.get("ID")
        url_normed = self.getUrlwithId(except_ID)
        self.URL_dict[url_normed]['status'] = -1  # 下载异常
        except_url = "Task " + str(except_ID)  # self.MyTable.item(except_ID,1)
        QMessageBox.warning(self, "Warning", except_url + " downloading error!",
                            QMessageBox.Reset | QMessageBox.Help | QMessageBox.Cancel, QMessageBox.Reset)
        print(" dl_thread_except() receive exception message!")
        self.DLT_List[except_ID].terminate()
        self.downloading.setText('正在下载(' + str(self.getDownloaingCount()) + ')')

    def verifyDlParameters(self):
        url_normed=self.Vedio_url.text()
        print("self.URL_dict.keys()----->", self.URL_dict.keys())
        pattern = re.compile(r'\s*http|https://.*?', re.S)
        if not re.match(pattern, url_normed):
            return url_normed,102
        if not re.match(pattern, self.Proxy_Url.text()):
            return url_normed,102
        if url_normed in self.URL_dict.keys()  :
            status=self.URL_dict[url_normed]['status']
            print(url_normed,":",status)
            if status==-1:#download error!
               return url_normed, 101
            elif status==0:
                return url_normed,1010
            elif status == 1:
                return url_normed, 1011

        return url_normed,100   #
    def mouseMoveEvent(self, QMouseEvent):
        if self.__leftButtonPress:
            globalPos = QMouseEvent.globalPos()
            self.move(globalPos - self.__movePoint)
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.__leftButtonPress = True
            self.__movePoint = QMouseEvent.pos()
    def Btn_finished_clicked(self):
          self.finished_clik_count+=1
          if self.finished_clik_count%2 ==1:
                  self.RightWidget.hide()

          else:
               self.RightWidget.show()
