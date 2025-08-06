# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionLeka = QAction(MainWindow)
        self.actionLeka.setObjectName(u"actionLeka")
        self.actionMerde = QAction(MainWindow)
        self.actionMerde.setObjectName(u"actionMerde")
        self.actionOka = QAction(MainWindow)
        self.actionOka.setObjectName(u"actionOka")
        self.actionKos = QAction(MainWindow)
        self.actionKos.setObjectName(u"actionKos")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sidePanel = QWidget(self.centralwidget)
        self.sidePanel.setObjectName(u"sidePanel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidePanel.sizePolicy().hasHeightForWidth())
        self.sidePanel.setSizePolicy(sizePolicy)
        self.sidePanel.setMinimumSize(QSize(150, 0))
        self.sidePanel.setMaximumSize(QSize(200, 16777215))
        self.sidePanel.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.gridLayout_2 = QGridLayout(self.sidePanel)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.navButtonReceiver = QPushButton(self.sidePanel)
        self.navButtonReceiver.setObjectName(u"navButtonReceiver")
        font = QFont()
        font.setPointSize(11)
        self.navButtonReceiver.setFont(font)
        self.navButtonReceiver.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.navButtonReceiver.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(79, 79, 118);\n"
"	border: none;\n"
"	padding: 16px 0px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(70, 70, 104);\n"
"}")

        self.verticalLayout.addWidget(self.navButtonReceiver)

        self.navButtonSender = QPushButton(self.sidePanel)
        self.navButtonSender.setObjectName(u"navButtonSender")
        self.navButtonSender.setFont(font)
        self.navButtonSender.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.navButtonSender.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(79, 79, 118);\n"
"	border: none;\n"
"	padding: 16px 0px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(70, 70, 104);\n"
"}")

        self.verticalLayout.addWidget(self.navButtonSender)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(3, 4)

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.sidePanel)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMaximumSize(QSize(16777215, 16777215))
        self.stackedWidget.setStyleSheet(u"background-color: rgb(44, 44, 65);")
        self.receiver = QWidget()
        self.receiver.setObjectName(u"receiver")
        self.gridLayout_3 = QGridLayout(self.receiver)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ipAddress = QLabel(self.receiver)
        self.ipAddress.setObjectName(u"ipAddress")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ipAddress.sizePolicy().hasHeightForWidth())
        self.ipAddress.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(24)
        self.ipAddress.setFont(font1)
        self.ipAddress.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.ipAddress)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.receiver)
        self.sender = QWidget()
        self.sender.setObjectName(u"sender")
        self.stackedWidget.addWidget(self.sender)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLeka.setText(QCoreApplication.translate("MainWindow", u"Leka", None))
        self.actionMerde.setText(QCoreApplication.translate("MainWindow", u"Merde", None))
        self.actionOka.setText(QCoreApplication.translate("MainWindow", u"Oka", None))
        self.actionKos.setText(QCoreApplication.translate("MainWindow", u"Kosa", None))
        self.navButtonReceiver.setText(QCoreApplication.translate("MainWindow", u"Recevoir", None))
        self.navButtonSender.setText(QCoreApplication.translate("MainWindow", u"Envoyer", None))
        self.ipAddress.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

