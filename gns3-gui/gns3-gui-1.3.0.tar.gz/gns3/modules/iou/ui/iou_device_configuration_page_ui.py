# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/grossmj/PycharmProjects/gns3-gui/gns3/modules/iou/ui/iou_device_configuration_page.ui'
#
# Created: Wed Feb 25 11:53:17 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_iouDeviceConfigPageWidget(object):
    def setupUi(self, iouDeviceConfigPageWidget):
        iouDeviceConfigPageWidget.setObjectName(_fromUtf8("iouDeviceConfigPageWidget"))
        iouDeviceConfigPageWidget.resize(392, 473)
        self.verticalLayout = QtGui.QVBoxLayout(iouDeviceConfigPageWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.uiTabWidget = QtGui.QTabWidget(iouDeviceConfigPageWidget)
        self.uiTabWidget.setObjectName(_fromUtf8("uiTabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.uiGeneralgroupBox = QtGui.QGroupBox(self.tab)
        self.uiGeneralgroupBox.setStyleSheet(_fromUtf8(""))
        self.uiGeneralgroupBox.setObjectName(_fromUtf8("uiGeneralgroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.uiGeneralgroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.uiNameLabel = QtGui.QLabel(self.uiGeneralgroupBox)
        self.uiNameLabel.setObjectName(_fromUtf8("uiNameLabel"))
        self.gridLayout.addWidget(self.uiNameLabel, 0, 0, 1, 1)
        self.uiNameLineEdit = QtGui.QLineEdit(self.uiGeneralgroupBox)
        self.uiNameLineEdit.setObjectName(_fromUtf8("uiNameLineEdit"))
        self.gridLayout.addWidget(self.uiNameLineEdit, 0, 1, 1, 1)
        self.uiIOUImageLabel = QtGui.QLabel(self.uiGeneralgroupBox)
        self.uiIOUImageLabel.setObjectName(_fromUtf8("uiIOUImageLabel"))
        self.gridLayout.addWidget(self.uiIOUImageLabel, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.uiIOUImageLineEdit = QtGui.QLineEdit(self.uiGeneralgroupBox)
        self.uiIOUImageLineEdit.setObjectName(_fromUtf8("uiIOUImageLineEdit"))
        self.horizontalLayout_5.addWidget(self.uiIOUImageLineEdit)
        self.uiIOUImageToolButton = QtGui.QToolButton(self.uiGeneralgroupBox)
        self.uiIOUImageToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.uiIOUImageToolButton.setObjectName(_fromUtf8("uiIOUImageToolButton"))
        self.horizontalLayout_5.addWidget(self.uiIOUImageToolButton)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.uiInitialConfigLabel = QtGui.QLabel(self.uiGeneralgroupBox)
        self.uiInitialConfigLabel.setObjectName(_fromUtf8("uiInitialConfigLabel"))
        self.gridLayout.addWidget(self.uiInitialConfigLabel, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.uiInitialConfigLineEdit = QtGui.QLineEdit(self.uiGeneralgroupBox)
        self.uiInitialConfigLineEdit.setObjectName(_fromUtf8("uiInitialConfigLineEdit"))
        self.horizontalLayout_4.addWidget(self.uiInitialConfigLineEdit)
        self.uiInitialConfigToolButton = QtGui.QToolButton(self.uiGeneralgroupBox)
        self.uiInitialConfigToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.uiInitialConfigToolButton.setObjectName(_fromUtf8("uiInitialConfigToolButton"))
        self.horizontalLayout_4.addWidget(self.uiInitialConfigToolButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 1, 1, 1)
        self.uiConsolePortLabel = QtGui.QLabel(self.uiGeneralgroupBox)
        self.uiConsolePortLabel.setObjectName(_fromUtf8("uiConsolePortLabel"))
        self.gridLayout.addWidget(self.uiConsolePortLabel, 3, 0, 1, 1)
        self.uiConsolePortSpinBox = QtGui.QSpinBox(self.uiGeneralgroupBox)
        self.uiConsolePortSpinBox.setMaximum(65535)
        self.uiConsolePortSpinBox.setObjectName(_fromUtf8("uiConsolePortSpinBox"))
        self.gridLayout.addWidget(self.uiConsolePortSpinBox, 3, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.uiGeneralgroupBox)
        self.uiOtherSettingsGroupBox = QtGui.QGroupBox(self.tab)
        self.uiOtherSettingsGroupBox.setObjectName(_fromUtf8("uiOtherSettingsGroupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.uiOtherSettingsGroupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.uiL1KeepalivesCheckBox = QtGui.QCheckBox(self.uiOtherSettingsGroupBox)
        self.uiL1KeepalivesCheckBox.setEnabled(True)
        self.uiL1KeepalivesCheckBox.setChecked(False)
        self.uiL1KeepalivesCheckBox.setObjectName(_fromUtf8("uiL1KeepalivesCheckBox"))
        self.gridLayout_2.addWidget(self.uiL1KeepalivesCheckBox, 0, 0, 1, 2)
        self.uiDefaultValuesCheckBox = QtGui.QCheckBox(self.uiOtherSettingsGroupBox)
        self.uiDefaultValuesCheckBox.setChecked(True)
        self.uiDefaultValuesCheckBox.setObjectName(_fromUtf8("uiDefaultValuesCheckBox"))
        self.gridLayout_2.addWidget(self.uiDefaultValuesCheckBox, 1, 0, 1, 2)
        self.uiRamLabel = QtGui.QLabel(self.uiOtherSettingsGroupBox)
        self.uiRamLabel.setObjectName(_fromUtf8("uiRamLabel"))
        self.gridLayout_2.addWidget(self.uiRamLabel, 2, 0, 1, 1)
        self.uiRamSpinBox = QtGui.QSpinBox(self.uiOtherSettingsGroupBox)
        self.uiRamSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiRamSpinBox.sizePolicy().hasHeightForWidth())
        self.uiRamSpinBox.setSizePolicy(sizePolicy)
        self.uiRamSpinBox.setMinimum(32)
        self.uiRamSpinBox.setMaximum(65535)
        self.uiRamSpinBox.setSingleStep(32)
        self.uiRamSpinBox.setProperty("value", 128)
        self.uiRamSpinBox.setObjectName(_fromUtf8("uiRamSpinBox"))
        self.gridLayout_2.addWidget(self.uiRamSpinBox, 2, 1, 1, 1)
        self.uiNvramLabel = QtGui.QLabel(self.uiOtherSettingsGroupBox)
        self.uiNvramLabel.setObjectName(_fromUtf8("uiNvramLabel"))
        self.gridLayout_2.addWidget(self.uiNvramLabel, 3, 0, 1, 1)
        self.uiNvramSpinBox = QtGui.QSpinBox(self.uiOtherSettingsGroupBox)
        self.uiNvramSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiNvramSpinBox.sizePolicy().hasHeightForWidth())
        self.uiNvramSpinBox.setSizePolicy(sizePolicy)
        self.uiNvramSpinBox.setMinimum(32)
        self.uiNvramSpinBox.setMaximum(65535)
        self.uiNvramSpinBox.setSingleStep(32)
        self.uiNvramSpinBox.setProperty("value", 128)
        self.uiNvramSpinBox.setObjectName(_fromUtf8("uiNvramSpinBox"))
        self.gridLayout_2.addWidget(self.uiNvramSpinBox, 3, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.uiOtherSettingsGroupBox)
        spacerItem = QtGui.QSpacerItem(260, 301, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.uiTabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.groupBox = QtGui.QGroupBox(self.tab_2)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.uiEthernetAdaptersLabel = QtGui.QLabel(self.groupBox)
        self.uiEthernetAdaptersLabel.setObjectName(_fromUtf8("uiEthernetAdaptersLabel"))
        self.gridLayout_3.addWidget(self.uiEthernetAdaptersLabel, 0, 0, 1, 1)
        self.uiEthernetAdaptersSpinBox = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiEthernetAdaptersSpinBox.sizePolicy().hasHeightForWidth())
        self.uiEthernetAdaptersSpinBox.setSizePolicy(sizePolicy)
        self.uiEthernetAdaptersSpinBox.setMaximum(16)
        self.uiEthernetAdaptersSpinBox.setSingleStep(2)
        self.uiEthernetAdaptersSpinBox.setObjectName(_fromUtf8("uiEthernetAdaptersSpinBox"))
        self.gridLayout_3.addWidget(self.uiEthernetAdaptersSpinBox, 0, 1, 1, 1)
        self.uiSerialAdaptersLabel = QtGui.QLabel(self.groupBox)
        self.uiSerialAdaptersLabel.setObjectName(_fromUtf8("uiSerialAdaptersLabel"))
        self.gridLayout_3.addWidget(self.uiSerialAdaptersLabel, 1, 0, 1, 1)
        self.uiSerialAdaptersSpinBox = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiSerialAdaptersSpinBox.sizePolicy().hasHeightForWidth())
        self.uiSerialAdaptersSpinBox.setSizePolicy(sizePolicy)
        self.uiSerialAdaptersSpinBox.setMaximum(16)
        self.uiSerialAdaptersSpinBox.setSingleStep(2)
        self.uiSerialAdaptersSpinBox.setObjectName(_fromUtf8("uiSerialAdaptersSpinBox"))
        self.gridLayout_3.addWidget(self.uiSerialAdaptersSpinBox, 1, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 347, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 1, 0, 1, 1)
        self.uiTabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.uiTabWidget)

        self.retranslateUi(iouDeviceConfigPageWidget)
        self.uiTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(iouDeviceConfigPageWidget)

    def retranslateUi(self, iouDeviceConfigPageWidget):
        iouDeviceConfigPageWidget.setWindowTitle(_translate("iouDeviceConfigPageWidget", "IOU device configuration", None))
        self.uiGeneralgroupBox.setTitle(_translate("iouDeviceConfigPageWidget", "General", None))
        self.uiNameLabel.setText(_translate("iouDeviceConfigPageWidget", "Name:", None))
        self.uiIOUImageLabel.setText(_translate("iouDeviceConfigPageWidget", "IOU image path:", None))
        self.uiIOUImageToolButton.setText(_translate("iouDeviceConfigPageWidget", "&Browse...", None))
        self.uiInitialConfigLabel.setText(_translate("iouDeviceConfigPageWidget", "Initial startup-config:", None))
        self.uiInitialConfigToolButton.setText(_translate("iouDeviceConfigPageWidget", "&Browse...", None))
        self.uiConsolePortLabel.setText(_translate("iouDeviceConfigPageWidget", "Console port:", None))
        self.uiOtherSettingsGroupBox.setTitle(_translate("iouDeviceConfigPageWidget", "Other settings", None))
        self.uiL1KeepalivesCheckBox.setText(_translate("iouDeviceConfigPageWidget", "Enable layer 1 keepalive messages (testing only)", None))
        self.uiDefaultValuesCheckBox.setText(_translate("iouDeviceConfigPageWidget", "Use default IOU values for memories", None))
        self.uiRamLabel.setText(_translate("iouDeviceConfigPageWidget", "RAM size:", None))
        self.uiRamSpinBox.setSuffix(_translate("iouDeviceConfigPageWidget", " MB", None))
        self.uiNvramLabel.setText(_translate("iouDeviceConfigPageWidget", "NVRAM size:", None))
        self.uiNvramSpinBox.setSuffix(_translate("iouDeviceConfigPageWidget", " KB", None))
        self.uiTabWidget.setTabText(self.uiTabWidget.indexOf(self.tab), _translate("iouDeviceConfigPageWidget", "General settings", None))
        self.groupBox.setTitle(_translate("iouDeviceConfigPageWidget", "Adapters", None))
        self.uiEthernetAdaptersLabel.setText(_translate("iouDeviceConfigPageWidget", "Ethernet adapters:", None))
        self.uiEthernetAdaptersSpinBox.setToolTip(_translate("iouDeviceConfigPageWidget", "1 adapter equals 4 Ethernet interfaces", None))
        self.uiSerialAdaptersLabel.setText(_translate("iouDeviceConfigPageWidget", "Serial adapters:", None))
        self.uiSerialAdaptersSpinBox.setToolTip(_translate("iouDeviceConfigPageWidget", "1 adapter equals 4 serial interfaces", None))
        self.uiTabWidget.setTabText(self.uiTabWidget.indexOf(self.tab_2), _translate("iouDeviceConfigPageWidget", "Network", None))

