from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Maincam(object):
    def setupUi(self, Maincam):
        Maincam.setObjectName("Maincam")
        Maincam.resize(1076, 551)
        self.centralwidget = QtWidgets.QWidget(Maincam)
        self.centralwidget.setObjectName("centralwidget")

        self.input = QtWidgets.QLabel(self.centralwidget)
        self.input.setGeometry(QtCore.QRect(0, 20, 521, 341))
        self.input.setAlignment(QtCore.Qt.AlignCenter)
        self.input.setText("입력")
        self.input.setScaledContents(True)
        self.input.setObjectName("input")

        self.output = QtWidgets.QLabel(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(550, 20, 511, 341))
        self.output.setAlignment(QtCore.Qt.AlignCenter)
        self.output.setText("결과")
        self.output.setScaledContents(True)
        self.output.setObjectName("output")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(520, 0, 31, 371))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 400, 181, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setText("사진파일 불러오기")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 400, 181, 81))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setText("캠 화면으로 전환")
        self.pushButton_2.setObjectName("pushButton_2")

        Maincam.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Maincam)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1076, 22))
        self.menubar.setObjectName("menubar")
        Maincam.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Maincam)
        self.statusbar.setObjectName("statusbar")
        Maincam.setStatusBar(self.statusbar)

        self.retranslateUi(Maincam)
        QtCore.QMetaObject.connectSlotsByName(Maincam)

    def retranslateUi(self, Maincam):
        _translate = QtCore.QCoreApplication.translate
        Maincam.setWindowTitle(_translate("Maincam", "Maincam"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_Maincam()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
