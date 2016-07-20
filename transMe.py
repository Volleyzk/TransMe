# -*- coding: utf-8 -*-
"""
Date     : 2016/07/19 18:55:56
FileName : transMe.py
Author   : septicmk
"""

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtWebKit import QWebView
import youdao_dict as yd

import imgs_rc

class Info(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Info, self).__init__(parent)

        self.resize(460,420)
        self.setStyleSheet("background-color:#3B4141;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.web_view = QWebView()
        self.layout.addWidget(self.web_view)

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIconMenu.setStyleSheet("color:#ffffff")

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon(":/imgs/dictionary-icon.png"))
        self.trayIcon.show()

    def handle_clicked(self):
        x = QtGui.QCursor.pos().x()
        y = QtGui.QCursor.pos().y()

    def query(self):
        cpb = QtGui.QApplication.clipboard()

        def func():
            translation,explains,web=yd.query(str(cpb.text(1).toUtf8()))
            if translation == None:
                html = u'''
                <style type="text/css">
                body {
                    font-family: Monaco, Consolas, "Lucida Console", monospace,"微软雅黑";
                }
                </style>
                <h2 style="color: #ffffff">
                没有找到对应释义
                </h2>
                '''
            else:
                html = u'''
                <style type="text/css">
                body {
                    font-family: Monaco, Consolas, "Lucida Console", monospace,"微软雅黑";
                }
                </style>
                <h2 style="color: #ffffff">
                %(translation)s
                </h2>

                <span style="color: #cccccc; font-weight: bold; font-size: 18px">● 基本翻译:</span>
                <p style="color: #eeeeee"> %(explains)s </p>

                <span style="color: #cccccc; font-weight: bold; font-size: 18px">● 网络释意:</span>
                <p style="color: #eeeeee"> %(web)s </p>''' % locals()
            self.web_view.setHtml(html)
            self.web_view.reload()
            self.move(QtGui.QCursor.pos())
            self.show()
        cpb.selectionChanged.connect(func)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    info = Info()
    info.query()
    app.exec_()

