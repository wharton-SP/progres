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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

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
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(460, 100, 86, 26))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuTest = QMenu(self.menubar)
        self.menuTest.setObjectName(u"menuTest")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuTest.menuAction())
        self.menuTest.addAction(self.actionLeka)
        self.menuTest.addAction(self.actionMerde)
        self.menuTest.addSeparator()
        self.menuTest.addAction(self.actionOka)
        self.menuTest.addAction(self.actionKos)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLeka.setText(QCoreApplication.translate("MainWindow", u"Leka", None))
        self.actionMerde.setText(QCoreApplication.translate("MainWindow", u"Merde", None))
        self.actionOka.setText(QCoreApplication.translate("MainWindow", u"Oka", None))
        self.actionKos.setText(QCoreApplication.translate("MainWindow", u"Kosa", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.menuTest.setTitle(QCoreApplication.translate("MainWindow", u"Test", None))
    # retranslateUi

