# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viewyVnOeC.ui'
##
## Created by: Qt User Interface Compiler version 5.15.11
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(310, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 30, 291, 481))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.getTextBtn = QPushButton(self.verticalLayoutWidget)
        self.getTextBtn.setObjectName(u"getTextBtn")

        self.verticalLayout.addWidget(self.getTextBtn)

        self.textEdit = QTextEdit(self.verticalLayoutWidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setAcceptRichText(False)

        self.verticalLayout.addWidget(self.textEdit)

        self.startRaceBtn = QPushButton(self.verticalLayoutWidget)
        self.startRaceBtn.setObjectName(u"startRaceBtn")

        self.verticalLayout.addWidget(self.startRaceBtn)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.speedSlider = QSlider(self.verticalLayoutWidget)
        self.speedSlider.setObjectName(u"speedSlider")
        self.speedSlider.setEnabled(True)
        self.speedSlider.setMaximum(1000)
        self.speedSlider.setValue(100)
        self.speedSlider.setOrientation(Qt.Horizontal)
        self.speedSlider.setTickPosition(QSlider.TicksBelow)
        self.speedSlider.setTickInterval(50)

        self.horizontalLayout.addWidget(self.speedSlider)

        self.speedLine = QLineEdit(self.verticalLayoutWidget)
        self.speedLine.setObjectName(u"speedLine")
        self.speedLine.setMaximumSize(QSize(50, 32))

        self.horizontalLayout.addWidget(self.speedLine)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.solveChallengeBtn = QPushButton(self.verticalLayoutWidget)
        self.solveChallengeBtn.setObjectName(u"solveChallengeBtn")
        self.solveChallengeBtn.setEnabled(True)

        self.verticalLayout.addWidget(self.solveChallengeBtn)

        self.closeAll = QPushButton(self.verticalLayoutWidget)
        self.closeAll.setObjectName(u"closeAll")

        self.verticalLayout.addWidget(self.closeAll)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.getTextBtn.setText(QCoreApplication.translate("MainWindow", u"Get text", None))
        self.startRaceBtn.setText(QCoreApplication.translate("MainWindow", u"Start race", None))
        self.solveChallengeBtn.setText(QCoreApplication.translate("MainWindow", u"Solve challenge", None))
        self.closeAll.setText(QCoreApplication.translate("MainWindow", u"Close all", None))
    # retranslateUi
