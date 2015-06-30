# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './src/alfanous-desktop/UI/aboutDlg.ui'
#
# Created: Tue Jun 30 12:27:37 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(545, 441)
        Dialog.setFocusPolicy(QtCore.Qt.NoFocus)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.o_about = QtGui.QTextBrowser(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.o_about.sizePolicy().hasHeightForWidth())
        self.o_about.setSizePolicy(sizePolicy)
        self.o_about.setMinimumSize(QtCore.QSize(300, 25))
        self.o_about.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.o_about.setFont(font)
        self.o_about.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.o_about.setToolTip("")
        self.o_about.setAutoFillBackground(False)
        self.o_about.setStyleSheet("background-color:Transparent;")
        self.o_about.setFrameShape(QtGui.QFrame.WinPanel)
        self.o_about.setFrameShadow(QtGui.QFrame.Sunken)
        self.o_about.setLineWidth(2)
        self.o_about.setDocumentTitle("")
        self.o_about.setUndoRedoEnabled(False)
        self.o_about.setReadOnly(True)
        self.o_about.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'ArabeyesQr\'; font-size:14pt; font-weight:600; color:#ff0000;\">AlfanousDesktop </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'ArabeyesQr\'; font-size:14pt;\">version </span><span style=\" font-family:\'ArabeyesQr\'; font-size:14pt; font-weight:600;\">0.7.20</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'ArabeyesQr\'; font-size:14pt;\">release </span><span style=\" font-family:\'ArabeyesQr\'; font-size:14pt; font-weight:600;\">Kahraman</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'ArabeyesQr\'; font-size:14pt; font-weight:600;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'ArabeyesQr\'; font-size:10pt;\">(c) 2010-2015 Alfanous Team. </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'ArabeyesQr\'; font-size:10pt;\">All rights reserved under </span><span style=\" font-family:\'ArabeyesQr\'; font-size:10pt; font-weight:600;\">AGPL </span><span style=\" font-family:\'ArabeyesQr\'; font-size:10pt;\">license</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:10pt; font-weight:600; color:#000000;\">Website </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.alfanous.org\"><span style=\" text-decoration: underline; color:#0000ff;\">www.alfanous.org</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans\'; font-size:10pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\'; font-size:10pt; font-weight:600; color:#000000;\">Mailinglist</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://groups.google.com/group/alfanous/\"><span style=\" text-decoration: underline; color:#0000ff;\">alfanous@googlegroup.com </span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px; font-family:\'Sans\'; font-size:10pt;\"><br /></p></body></html>")
        self.o_about.setOverwriteMode(False)
        self.o_about.setAcceptRichText(True)
        self.o_about.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.o_about.setOpenExternalLinks(True)
        self.o_about.setOpenLinks(True)
        self.o_about.setObjectName("o_about")
        self.verticalLayout_3.addWidget(self.o_about)
        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.o_about_4 = QtGui.QTextBrowser(self.tab_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.o_about_4.sizePolicy().hasHeightForWidth())
        self.o_about_4.setSizePolicy(sizePolicy)
        self.o_about_4.setMinimumSize(QtCore.QSize(300, 25))
        self.o_about_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.o_about_4.setFont(font)
        self.o_about_4.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.o_about_4.setToolTip("")
        self.o_about_4.setAutoFillBackground(False)
        self.o_about_4.setStyleSheet("background-color:Transparent;")
        self.o_about_4.setFrameShape(QtGui.QFrame.WinPanel)
        self.o_about_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.o_about_4.setLineWidth(2)
        self.o_about_4.setDocumentTitle("")
        self.o_about_4.setUndoRedoEnabled(False)
        self.o_about_4.setReadOnly(True)
        self.o_about_4.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:18px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; color:#333333;\">This project is maintained by:</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:16px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Assem Chelli (API)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:16px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Muhammad Shaban  (packaging to Fedora Linux)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:16px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Zaki Smahi (Firefox toolbar)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:16px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Muslih Aqqad (Design)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:16px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Zineb Laouici  (Facebook/G+ pages)</span></li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")
        self.o_about_4.setOverwriteMode(True)
        self.o_about_4.setAcceptRichText(True)
        self.o_about_4.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.o_about_4.setOpenExternalLinks(False)
        self.o_about_4.setOpenLinks(False)
        self.o_about_4.setObjectName("o_about_4")
        self.horizontalLayout_2.addWidget(self.o_about_4)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.o_about_5 = QtGui.QTextBrowser(self.tab_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.o_about_5.sizePolicy().hasHeightForWidth())
        self.o_about_5.setSizePolicy(sizePolicy)
        self.o_about_5.setMinimumSize(QtCore.QSize(300, 25))
        self.o_about_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.o_about_5.setFont(font)
        self.o_about_5.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.o_about_5.setToolTip("")
        self.o_about_5.setAutoFillBackground(False)
        self.o_about_5.setStyleSheet("background-color:Transparent;")
        self.o_about_5.setFrameShape(QtGui.QFrame.WinPanel)
        self.o_about_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.o_about_5.setLineWidth(2)
        self.o_about_5.setDocumentTitle("")
        self.o_about_5.setUndoRedoEnabled(False)
        self.o_about_5.setReadOnly(True)
        self.o_about_5.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:18px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; color:#333333;\">AlfanousDesktop is translated by:</span></p>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Arabic</span><span style=\" font-size:16px;\">: Abdelmonam Kouka, Assem Chelli, LionArt (ghazi.nocturne), Karim Oulad Chalha, Zarrabi</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Indonesian</span><span style=\" font-size:16px;\">: Amy Cidra, Arif Rahman Hakim, Muslih Al aqaad</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Malay</span><span style=\" font-size:16px;\">: Muhammad Fariz</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Spanish</span><span style=\" font-size:16px;\">: Ricardo Hermosilla</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">French: </span><span style=\" font-size:16px;\">Mohamed Nadjib Mami, Mahmoud Halit</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Albanian: </span><span style=\" font-size:16px;\">\'lavhal\'</span></li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")
        self.o_about_5.setOverwriteMode(True)
        self.o_about_5.setAcceptRichText(True)
        self.o_about_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.o_about_5.setOpenExternalLinks(False)
        self.o_about_5.setOpenLinks(False)
        self.o_about_5.setObjectName("o_about_5")
        self.horizontalLayout_3.addWidget(self.o_about_5)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.o_about_2 = QtGui.QTextBrowser(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.o_about_2.sizePolicy().hasHeightForWidth())
        self.o_about_2.setSizePolicy(sizePolicy)
        self.o_about_2.setMinimumSize(QtCore.QSize(300, 25))
        self.o_about_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.o_about_2.setFont(font)
        self.o_about_2.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.o_about_2.setToolTip("")
        self.o_about_2.setAutoFillBackground(False)
        self.o_about_2.setStyleSheet("background-color:Transparent;")
        self.o_about_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.o_about_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.o_about_2.setLineWidth(2)
        self.o_about_2.setDocumentTitle("")
        self.o_about_2.setUndoRedoEnabled(False)
        self.o_about_2.setReadOnly(True)
        self.o_about_2.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is the list of contributors to Alfanous project of all time:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-coding\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">C</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">oding</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">API &amp; JSON interface: </span><a href=\"https://github.com/assem-ch\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">A~CH</span></a></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Desktop Interface: </span><a href=\"https://github.com/assem-ch\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">A~CH</span></a><span style=\" font-size:16px;\">, </span><a href=\"https://github.com/sohaibafifi\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Sohaib Afifi</span></a></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Web Interface: </span><a href=\"https://github.com/assem-ch\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">A~CH</span></a><span style=\" font-size:16px;\"> , </span><a href=\"https://github.com/01walid\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Walid Ziouche</span></a><span style=\" font-size:16px;\">, </span><a href=\"https://github.com/sneetsher\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Abdellah Chelli</span></a><span style=\" font-size:16px;\"> , </span><a href=\"https://github.com/mdebbar\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Mouad Debbar</span></a><span style=\" font-size:16px;\">, </span><a href=\"https://github.com/islamoc\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Mennouchi Islam Azeddine</span></a><span style=\" font-size:16px;\">, </span><a href=\"https://github.com/muslih\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Muslih al aqaad</span></a><span style=\" font-size:16px;\">, </span><a href=\"https://github.com/tedj\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Tedjeddine Meabeo</span></a><span style=\" font-size:16px;\"> , , Ahmed Ramadan</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Firefox toolbar: </span><a href=\"https://github.com/zsmahi\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Zakaria Smahi</span></a></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">PyArabic(Integrated): Taha Zerrouki, A~CH, Ahimta~</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Windows Store : </span><a href=\"https://github.com/luffy-dam\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Mohamed Anas Mostefaoui(FenyLab)</span></a></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-research\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">R</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">esearch</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">2009-2010: Engineer Thesis</span></li>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Title</span><span style=\" font-size:16px;\">: Développement d\'un moteur de recherche et d\'indexation dans les documents coraniques</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">University</span><span style=\" font-size:16px;\">: </span><a href=\"http://www.esi.dz/\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">ESI</span></a><span style=\" font-size:16px;\"> - Algiers</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Collaborators</span><span style=\" font-size:16px;\">: A~CH (Student), Merouane Dahmani (Student), Taha Zerrouki ( Supervisor), Pr. Amar Balla ( Supervisor)</span></li></ul>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">March 2011: Arabic Research paper</span></li>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Title</span><span style=\" font-size:16px;\">: An Application Programming Interface for indexing and search in Noble Quran</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Original title</span><span style=\" font-size:16px;\">: مكتبة برمجية للفهرسة والبحث في القرآن الكريم</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Conference</span><span style=\" font-size:16px;\">: NITS 2011 KSA</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Collaborators</span><span style=\" font-size:16px;\">: A~CH, Merouane Dahmani, Taha Zerrouki, Pr. Amar Balla</span></li></ul>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">May 2012: English Research paper</span></li></ul>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Title</span><span style=\" font-size:16px;\">:. Advanced Search in Quran: Classification and Proposition of All Possible Features</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Conference</span><span style=\" font-size:16px;\">: A pre-conference workshop in LREC 2012 Turkey which is about ”LRE-Rel: Language Resource and Evaluation for Religious Texts”</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Collaborators</span><span style=\" font-size:16px;\">: A~CH, Taha Zerrouki, Pr. Amar Balla</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-graphics--design\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">G</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">raphics &amp; Design</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Icons,Logos: Abdellah Chelli, Muslih Al-Aqaad, Ahmed Ramadan, Moussa Drihem, Salaheddine Chelli</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Wallpapers: Aji Fatwa, Abd Madjid Kemari, Walid Boumaza</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Joomla Template: Muslih Al-aqaad</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-packaging\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">P</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">ackaging</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Windows NSIS installer: A~CH</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Ubuntu/Sabily DEB package: Ahmed Almahmoudy</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Fedora/OpenSuse/Ojuba RPM package: Muhammad Shaban</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Arch-linux package: Walid Ziouche, Sohaib Afifi</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-resource-enriching\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">R</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">esource Enriching</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Word index: Taha Zerrouki, A~CH, Asmaa Mhimeh, Rahma Maaref</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Aya index: {Tanzil Project}, Taha Zerrouki (Subjects), Muhi-uddin (Indian mushaf pages)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Translations: {Tanzil Project},</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-documentation\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">D</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">ocumentation</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Wiki: A~CH, Abdellah Chelli</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-writing\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">W</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">riting</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">News : Mohamed M Sayed, Yasser Ghemit, Kacem Boukraa, Asmaa Mhimeh,</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Blog posts: Muslih Al-aqaad, Ahmed Jumal, Aji Fatwa</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-community-management\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">C</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">ommunity Management</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Yasmine Hoadjli</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Zineb Laouici</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Meriem Bounif</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-translation\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">T</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">ranslation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#777777;\">To help in translation, contact us in the mailing list &lt;alfanous[at]googlegroups[dotcom]&gt;</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Desktop application</span></li>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Arabic: Abdelmonam Kouka, Assem Chelli, LionArt (ghazi.nocturne), Karim Oulad Chalha, Zarrabi</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Indonesian: Arif Rahman Hakim, Muslih Al aqaad</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Malay: Muhammad Fariz</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Spanish: Ricardo Hermosilla</span></li></ul>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Main Web Interface</span></li>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Arabic: A~CH, Yasmine Houadjli, Merwan Ali</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">French: Zineb Pub, Yasmine Houadjli, Abdelkarim Aries, Nassim rehali, Nasreddine Cheniki</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Indonesian: Ahmed Jumal , Amy cidra, Mahyuddin Susanto</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Japanese: Abdelkarim Aries</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Spanish: Khireddine Chekraoui</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Portuguese: Jonathan Da Fonseca</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">German: Dennis Baudys</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Malay: \'abuyop\'</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Kurdish:</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Malayalam: \'STyM Alfazz\' &lt;</span><a href=\"https://launchpad.net/~alfasst\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">https://launchpad.net/~alfasst</span></a><span style=\" font-size:16px;\">&gt;</span></li></ul>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Mobile Web interface</span></li></ul>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Bosnian: Armin Kazi</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Brazilian Portuguese: Aieon.corp(LP)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">French: Karim Oulad Chalha, \'yass-pard\'</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Indonesian: Mahyuddin Susanto,</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Italian: \'Guybrush88\'</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Japanese: Abdelkarim Aries</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Malay: \'abuyop\'</span></li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"user-content-test--support\"></a><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">T</span><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:large; font-weight:600; color:#333333;\">est &amp; Support</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Test: </span><a href=\"https://github.com/01walid\"><span style=\" font-size:16px; text-decoration: underline; color:#4183c4; background-color:#000000;\">Walid Ziouche</span></a><span style=\" font-size:16px;\">, Zakaria Smahi, Muslih Alaqaad,</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Bugs: Oussama Chammam, Ahmed Salem, xsoh, Yacer~, Jounathan~, BenSali~ , Many persons from the community, thanks to all.</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Vulns: Jalil~</span></li></ul></body></html>")
        self.o_about_2.setOverwriteMode(True)
        self.o_about_2.setAcceptRichText(True)
        self.o_about_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.o_about_2.setOpenExternalLinks(False)
        self.o_about_2.setOpenLinks(False)
        self.o_about_2.setObjectName("o_about_2")
        self.verticalLayout_2.addWidget(self.o_about_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.tab_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.o_about_3 = QtGui.QTextBrowser(self.tab_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.o_about_3.sizePolicy().hasHeightForWidth())
        self.o_about_3.setSizePolicy(sizePolicy)
        self.o_about_3.setMinimumSize(QtCore.QSize(300, 25))
        self.o_about_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.o_about_3.setFont(font)
        self.o_about_3.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.o_about_3.setToolTip("")
        self.o_about_3.setAutoFillBackground(False)
        self.o_about_3.setStyleSheet("background-color:Transparent;")
        self.o_about_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.o_about_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.o_about_3.setLineWidth(2)
        self.o_about_3.setDocumentTitle("")
        self.o_about_3.setUndoRedoEnabled(False)
        self.o_about_3.setReadOnly(True)
        self.o_about_3.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\">We gratefully acknowledge the following:</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Sabily team (sabily.org)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Linux Arab Community (linuxac.org)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">IT Scoop (it-scoop.com)</span></li>\n"
"<li style=\" font-family:\'Helvetica Neue,Helvetica,Segoe UI,Arial,freesans,sans-serif\'; font-size:16px; color:#333333;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px;\">Tech echo (tech-echo.com)</span></li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")
        self.o_about_3.setOverwriteMode(True)
        self.o_about_3.setAcceptRichText(True)
        self.o_about_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.o_about_3.setOpenExternalLinks(False)
        self.o_about_3.setOpenLinks(False)
        self.o_about_3.setObjectName("o_about_3")
        self.horizontalLayout.addWidget(self.o_about_3)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("Dialog", "Maintainers", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("Dialog", "Translators", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Contributors", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Dialog", "Acknowledgment", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))

