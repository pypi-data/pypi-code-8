# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/grossmj/PycharmProjects/gns3-gui/gns3/ui/general_preferences_page.ui'
#
# Created: Fri Mar 13 15:27:54 2015
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

class Ui_GeneralPreferencesPageWidget(object):
    def setupUi(self, GeneralPreferencesPageWidget):
        GeneralPreferencesPageWidget.setObjectName(_fromUtf8("GeneralPreferencesPageWidget"))
        GeneralPreferencesPageWidget.resize(467, 536)
        self.verticalLayout = QtGui.QVBoxLayout(GeneralPreferencesPageWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.uiMiscTabWidget = QtGui.QTabWidget(GeneralPreferencesPageWidget)
        self.uiMiscTabWidget.setObjectName(_fromUtf8("uiMiscTabWidget"))
        self.uiGeneralTab = QtGui.QWidget()
        self.uiGeneralTab.setObjectName(_fromUtf8("uiGeneralTab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.uiGeneralTab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.uiStyleGroupBox = QtGui.QGroupBox(self.uiGeneralTab)
        self.uiStyleGroupBox.setObjectName(_fromUtf8("uiStyleGroupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.uiStyleGroupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.uiStyleComboBox = QtGui.QComboBox(self.uiStyleGroupBox)
        self.uiStyleComboBox.setObjectName(_fromUtf8("uiStyleComboBox"))
        self.verticalLayout_4.addWidget(self.uiStyleComboBox)
        self.gridLayout_6.addWidget(self.uiStyleGroupBox, 1, 0, 1, 1)
        self.uiLocalPathsGroupBox = QtGui.QGroupBox(self.uiGeneralTab)
        self.uiLocalPathsGroupBox.setObjectName(_fromUtf8("uiLocalPathsGroupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.uiLocalPathsGroupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.uiProjectsPathLabel = QtGui.QLabel(self.uiLocalPathsGroupBox)
        self.uiProjectsPathLabel.setObjectName(_fromUtf8("uiProjectsPathLabel"))
        self.gridLayout_3.addWidget(self.uiProjectsPathLabel, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.uiProjectsPathLineEdit = QtGui.QLineEdit(self.uiLocalPathsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiProjectsPathLineEdit.sizePolicy().hasHeightForWidth())
        self.uiProjectsPathLineEdit.setSizePolicy(sizePolicy)
        self.uiProjectsPathLineEdit.setObjectName(_fromUtf8("uiProjectsPathLineEdit"))
        self.horizontalLayout_2.addWidget(self.uiProjectsPathLineEdit)
        self.uiProjectsPathToolButton = QtGui.QToolButton(self.uiLocalPathsGroupBox)
        self.uiProjectsPathToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.uiProjectsPathToolButton.setObjectName(_fromUtf8("uiProjectsPathToolButton"))
        self.horizontalLayout_2.addWidget(self.uiProjectsPathToolButton)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.uiImagesPathLabel = QtGui.QLabel(self.uiLocalPathsGroupBox)
        self.uiImagesPathLabel.setObjectName(_fromUtf8("uiImagesPathLabel"))
        self.gridLayout_3.addWidget(self.uiImagesPathLabel, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.uiImagesPathLineEdit = QtGui.QLineEdit(self.uiLocalPathsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiImagesPathLineEdit.sizePolicy().hasHeightForWidth())
        self.uiImagesPathLineEdit.setSizePolicy(sizePolicy)
        self.uiImagesPathLineEdit.setObjectName(_fromUtf8("uiImagesPathLineEdit"))
        self.horizontalLayout_4.addWidget(self.uiImagesPathLineEdit)
        self.uiImagesPathToolButton = QtGui.QToolButton(self.uiLocalPathsGroupBox)
        self.uiImagesPathToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.uiImagesPathToolButton.setObjectName(_fromUtf8("uiImagesPathToolButton"))
        self.horizontalLayout_4.addWidget(self.uiImagesPathToolButton)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.gridLayout_6.addWidget(self.uiLocalPathsGroupBox, 0, 0, 1, 1)
        self.uiConfigurationFileGroupBox = QtGui.QGroupBox(self.uiGeneralTab)
        self.uiConfigurationFileGroupBox.setObjectName(_fromUtf8("uiConfigurationFileGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.uiConfigurationFileGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.uiImportConfigurationFilePushButton = QtGui.QPushButton(self.uiConfigurationFileGroupBox)
        self.uiImportConfigurationFilePushButton.setObjectName(_fromUtf8("uiImportConfigurationFilePushButton"))
        self.horizontalLayout.addWidget(self.uiImportConfigurationFilePushButton)
        self.uiExportConfigurationFilePushButton = QtGui.QPushButton(self.uiConfigurationFileGroupBox)
        self.uiExportConfigurationFilePushButton.setObjectName(_fromUtf8("uiExportConfigurationFilePushButton"))
        self.horizontalLayout.addWidget(self.uiExportConfigurationFilePushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.uiConfigurationFileLabel = QtGui.QLabel(self.uiConfigurationFileGroupBox)
        self.uiConfigurationFileLabel.setObjectName(_fromUtf8("uiConfigurationFileLabel"))
        self.gridLayout.addWidget(self.uiConfigurationFileLabel, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.uiConfigurationFileGroupBox, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 3, 0, 1, 1)
        self.uiMiscTabWidget.addTab(self.uiGeneralTab, _fromUtf8(""))
        self.uiConsoleTab = QtGui.QWidget()
        self.uiConsoleTab.setObjectName(_fromUtf8("uiConsoleTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.uiConsoleTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.uiTelnetConsoleSettingsGroupBox = QtGui.QGroupBox(self.uiConsoleTab)
        self.uiTelnetConsoleSettingsGroupBox.setObjectName(_fromUtf8("uiTelnetConsoleSettingsGroupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.uiTelnetConsoleSettingsGroupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.uiTelnetConsolePreconfiguredCommandLabel = QtGui.QLabel(self.uiTelnetConsoleSettingsGroupBox)
        self.uiTelnetConsolePreconfiguredCommandLabel.setObjectName(_fromUtf8("uiTelnetConsolePreconfiguredCommandLabel"))
        self.gridLayout_4.addWidget(self.uiTelnetConsolePreconfiguredCommandLabel, 0, 0, 1, 1)
        self.uiTelnetConsolePreconfiguredCommandComboBox = QtGui.QComboBox(self.uiTelnetConsoleSettingsGroupBox)
        self.uiTelnetConsolePreconfiguredCommandComboBox.setObjectName(_fromUtf8("uiTelnetConsolePreconfiguredCommandComboBox"))
        self.gridLayout_4.addWidget(self.uiTelnetConsolePreconfiguredCommandComboBox, 1, 0, 1, 1)
        self.uiTelnetConsoleCommandLabel = QtGui.QLabel(self.uiTelnetConsoleSettingsGroupBox)
        self.uiTelnetConsoleCommandLabel.setObjectName(_fromUtf8("uiTelnetConsoleCommandLabel"))
        self.gridLayout_4.addWidget(self.uiTelnetConsoleCommandLabel, 3, 0, 1, 1)
        self.uiTelnetConsoleCommandLineEdit = QtGui.QLineEdit(self.uiTelnetConsoleSettingsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiTelnetConsoleCommandLineEdit.sizePolicy().hasHeightForWidth())
        self.uiTelnetConsoleCommandLineEdit.setSizePolicy(sizePolicy)
        self.uiTelnetConsoleCommandLineEdit.setObjectName(_fromUtf8("uiTelnetConsoleCommandLineEdit"))
        self.gridLayout_4.addWidget(self.uiTelnetConsoleCommandLineEdit, 4, 0, 1, 2)
        self.uiTelnetConsolePreconfiguredCommandPushButton = QtGui.QPushButton(self.uiTelnetConsoleSettingsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiTelnetConsolePreconfiguredCommandPushButton.sizePolicy().hasHeightForWidth())
        self.uiTelnetConsolePreconfiguredCommandPushButton.setSizePolicy(sizePolicy)
        self.uiTelnetConsolePreconfiguredCommandPushButton.setObjectName(_fromUtf8("uiTelnetConsolePreconfiguredCommandPushButton"))
        self.gridLayout_4.addWidget(self.uiTelnetConsolePreconfiguredCommandPushButton, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.uiTelnetConsoleSettingsGroupBox)
        self.uiSerialConsoleSettingsGroupBox = QtGui.QGroupBox(self.uiConsoleTab)
        self.uiSerialConsoleSettingsGroupBox.setObjectName(_fromUtf8("uiSerialConsoleSettingsGroupBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.uiSerialConsoleSettingsGroupBox)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.uiSerialConsoleCommandLabel = QtGui.QLabel(self.uiSerialConsoleSettingsGroupBox)
        self.uiSerialConsoleCommandLabel.setObjectName(_fromUtf8("uiSerialConsoleCommandLabel"))
        self.gridLayout_5.addWidget(self.uiSerialConsoleCommandLabel, 3, 0, 1, 1)
        self.uiSerialConsolePreconfiguredCommandLabel = QtGui.QLabel(self.uiSerialConsoleSettingsGroupBox)
        self.uiSerialConsolePreconfiguredCommandLabel.setObjectName(_fromUtf8("uiSerialConsolePreconfiguredCommandLabel"))
        self.gridLayout_5.addWidget(self.uiSerialConsolePreconfiguredCommandLabel, 0, 0, 1, 1)
        self.uiSerialConsolePreconfiguredCommandComboBox = QtGui.QComboBox(self.uiSerialConsoleSettingsGroupBox)
        self.uiSerialConsolePreconfiguredCommandComboBox.setObjectName(_fromUtf8("uiSerialConsolePreconfiguredCommandComboBox"))
        self.gridLayout_5.addWidget(self.uiSerialConsolePreconfiguredCommandComboBox, 1, 0, 1, 1)
        self.uiSerialConsoleCommandLineEdit = QtGui.QLineEdit(self.uiSerialConsoleSettingsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiSerialConsoleCommandLineEdit.sizePolicy().hasHeightForWidth())
        self.uiSerialConsoleCommandLineEdit.setSizePolicy(sizePolicy)
        self.uiSerialConsoleCommandLineEdit.setObjectName(_fromUtf8("uiSerialConsoleCommandLineEdit"))
        self.gridLayout_5.addWidget(self.uiSerialConsoleCommandLineEdit, 4, 0, 1, 2)
        self.uiSerialConsolePreconfiguredCommandPushButton = QtGui.QPushButton(self.uiSerialConsoleSettingsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiSerialConsolePreconfiguredCommandPushButton.sizePolicy().hasHeightForWidth())
        self.uiSerialConsolePreconfiguredCommandPushButton.setSizePolicy(sizePolicy)
        self.uiSerialConsolePreconfiguredCommandPushButton.setObjectName(_fromUtf8("uiSerialConsolePreconfiguredCommandPushButton"))
        self.gridLayout_5.addWidget(self.uiSerialConsolePreconfiguredCommandPushButton, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.uiSerialConsoleSettingsGroupBox)
        self.uiConsoleMiscGroupBox = QtGui.QGroupBox(self.uiConsoleTab)
        self.uiConsoleMiscGroupBox.setObjectName(_fromUtf8("uiConsoleMiscGroupBox"))
        self.gridLayout_7 = QtGui.QGridLayout(self.uiConsoleMiscGroupBox)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.uiCloseConsoleWindowsOnDeleteCheckBox = QtGui.QCheckBox(self.uiConsoleMiscGroupBox)
        self.uiCloseConsoleWindowsOnDeleteCheckBox.setObjectName(_fromUtf8("uiCloseConsoleWindowsOnDeleteCheckBox"))
        self.gridLayout_7.addWidget(self.uiCloseConsoleWindowsOnDeleteCheckBox, 0, 0, 1, 1)
        self.uiBringConsoleWindowToFrontCheckBox = QtGui.QCheckBox(self.uiConsoleMiscGroupBox)
        self.uiBringConsoleWindowToFrontCheckBox.setObjectName(_fromUtf8("uiBringConsoleWindowToFrontCheckBox"))
        self.gridLayout_7.addWidget(self.uiBringConsoleWindowToFrontCheckBox, 1, 0, 1, 1)
        self.uiSlowConsoleAllLabel = QtGui.QLabel(self.uiConsoleMiscGroupBox)
        self.uiSlowConsoleAllLabel.setObjectName(_fromUtf8("uiSlowConsoleAllLabel"))
        self.gridLayout_7.addWidget(self.uiSlowConsoleAllLabel, 2, 0, 1, 1)
        self.uiDelayConsoleAllSpinBox = QtGui.QSpinBox(self.uiConsoleMiscGroupBox)
        self.uiDelayConsoleAllSpinBox.setMaximum(10000)
        self.uiDelayConsoleAllSpinBox.setProperty("value", 500)
        self.uiDelayConsoleAllSpinBox.setObjectName(_fromUtf8("uiDelayConsoleAllSpinBox"))
        self.gridLayout_7.addWidget(self.uiDelayConsoleAllSpinBox, 3, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.uiConsoleMiscGroupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.uiMiscTabWidget.addTab(self.uiConsoleTab, _fromUtf8(""))
        self.uiSceneTab = QtGui.QWidget()
        self.uiSceneTab.setObjectName(_fromUtf8("uiSceneTab"))
        self.gridLayout_8 = QtGui.QGridLayout(self.uiSceneTab)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.uiSceneWidthLabel = QtGui.QLabel(self.uiSceneTab)
        self.uiSceneWidthLabel.setObjectName(_fromUtf8("uiSceneWidthLabel"))
        self.gridLayout_8.addWidget(self.uiSceneWidthLabel, 0, 0, 1, 1)
        self.uiSceneHeightLabel = QtGui.QLabel(self.uiSceneTab)
        self.uiSceneHeightLabel.setObjectName(_fromUtf8("uiSceneHeightLabel"))
        self.gridLayout_8.addWidget(self.uiSceneHeightLabel, 2, 0, 1, 1)
        self.uiRectangleSelectedItemCheckBox = QtGui.QCheckBox(self.uiSceneTab)
        self.uiRectangleSelectedItemCheckBox.setChecked(True)
        self.uiRectangleSelectedItemCheckBox.setObjectName(_fromUtf8("uiRectangleSelectedItemCheckBox"))
        self.gridLayout_8.addWidget(self.uiRectangleSelectedItemCheckBox, 4, 0, 1, 2)
        self.uiDrawLinkStatusPointsCheckBox = QtGui.QCheckBox(self.uiSceneTab)
        self.uiDrawLinkStatusPointsCheckBox.setChecked(True)
        self.uiDrawLinkStatusPointsCheckBox.setObjectName(_fromUtf8("uiDrawLinkStatusPointsCheckBox"))
        self.gridLayout_8.addWidget(self.uiDrawLinkStatusPointsCheckBox, 5, 0, 1, 1)
        self.uiLinkManualModeCheckBox = QtGui.QCheckBox(self.uiSceneTab)
        self.uiLinkManualModeCheckBox.setChecked(True)
        self.uiLinkManualModeCheckBox.setObjectName(_fromUtf8("uiLinkManualModeCheckBox"))
        self.gridLayout_8.addWidget(self.uiLinkManualModeCheckBox, 6, 0, 1, 2)
        self.uiLabelPreviewLabel = QtGui.QLabel(self.uiSceneTab)
        self.uiLabelPreviewLabel.setObjectName(_fromUtf8("uiLabelPreviewLabel"))
        self.gridLayout_8.addWidget(self.uiLabelPreviewLabel, 7, 0, 1, 1)
        self.uiDefaultLabelStylePlainTextEdit = QtGui.QPlainTextEdit(self.uiSceneTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiDefaultLabelStylePlainTextEdit.sizePolicy().hasHeightForWidth())
        self.uiDefaultLabelStylePlainTextEdit.setSizePolicy(sizePolicy)
        self.uiDefaultLabelStylePlainTextEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.uiDefaultLabelStylePlainTextEdit.setReadOnly(True)
        self.uiDefaultLabelStylePlainTextEdit.setObjectName(_fromUtf8("uiDefaultLabelStylePlainTextEdit"))
        self.gridLayout_8.addWidget(self.uiDefaultLabelStylePlainTextEdit, 8, 0, 1, 2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.uiDefaultLabelFontPushButton = QtGui.QPushButton(self.uiSceneTab)
        self.uiDefaultLabelFontPushButton.setObjectName(_fromUtf8("uiDefaultLabelFontPushButton"))
        self.horizontalLayout_5.addWidget(self.uiDefaultLabelFontPushButton)
        self.uiDefaultLabelColorPushButton = QtGui.QPushButton(self.uiSceneTab)
        self.uiDefaultLabelColorPushButton.setObjectName(_fromUtf8("uiDefaultLabelColorPushButton"))
        self.horizontalLayout_5.addWidget(self.uiDefaultLabelColorPushButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.gridLayout_8.addLayout(self.horizontalLayout_5, 9, 0, 1, 2)
        spacerItem4 = QtGui.QSpacerItem(20, 201, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem4, 10, 1, 1, 1)
        self.uiSceneHeightSpinBox = QtGui.QSpinBox(self.uiSceneTab)
        self.uiSceneHeightSpinBox.setMinimum(500)
        self.uiSceneHeightSpinBox.setMaximum(1000000)
        self.uiSceneHeightSpinBox.setSingleStep(100)
        self.uiSceneHeightSpinBox.setProperty("value", 1000)
        self.uiSceneHeightSpinBox.setObjectName(_fromUtf8("uiSceneHeightSpinBox"))
        self.gridLayout_8.addWidget(self.uiSceneHeightSpinBox, 3, 0, 1, 2)
        self.uiSceneWidthSpinBox = QtGui.QSpinBox(self.uiSceneTab)
        self.uiSceneWidthSpinBox.setMinimum(500)
        self.uiSceneWidthSpinBox.setMaximum(1000000)
        self.uiSceneWidthSpinBox.setSingleStep(100)
        self.uiSceneWidthSpinBox.setProperty("value", 2000)
        self.uiSceneWidthSpinBox.setObjectName(_fromUtf8("uiSceneWidthSpinBox"))
        self.gridLayout_8.addWidget(self.uiSceneWidthSpinBox, 1, 0, 1, 2)
        self.uiMiscTabWidget.addTab(self.uiSceneTab, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.uiLaunchNewProjectDialogCheckBox = QtGui.QCheckBox(self.tab)
        self.uiLaunchNewProjectDialogCheckBox.setChecked(True)
        self.uiLaunchNewProjectDialogCheckBox.setObjectName(_fromUtf8("uiLaunchNewProjectDialogCheckBox"))
        self.verticalLayout_2.addWidget(self.uiLaunchNewProjectDialogCheckBox)
        self.uiAutoScreenshotCheckBox = QtGui.QCheckBox(self.tab)
        self.uiAutoScreenshotCheckBox.setChecked(True)
        self.uiAutoScreenshotCheckBox.setObjectName(_fromUtf8("uiAutoScreenshotCheckBox"))
        self.verticalLayout_2.addWidget(self.uiAutoScreenshotCheckBox)
        self.uiCheckForUpdateCheckBox = QtGui.QCheckBox(self.tab)
        self.uiCheckForUpdateCheckBox.setChecked(True)
        self.uiCheckForUpdateCheckBox.setObjectName(_fromUtf8("uiCheckForUpdateCheckBox"))
        self.verticalLayout_2.addWidget(self.uiCheckForUpdateCheckBox)
        self.uiCrashReportCheckBox = QtGui.QCheckBox(self.tab)
        self.uiCrashReportCheckBox.setChecked(True)
        self.uiCrashReportCheckBox.setObjectName(_fromUtf8("uiCrashReportCheckBox"))
        self.verticalLayout_2.addWidget(self.uiCrashReportCheckBox)
        self.uiSlowStartAllLabel = QtGui.QLabel(self.tab)
        self.uiSlowStartAllLabel.setObjectName(_fromUtf8("uiSlowStartAllLabel"))
        self.verticalLayout_2.addWidget(self.uiSlowStartAllLabel)
        self.uiSlowStartAllSpinBox = QtGui.QSpinBox(self.tab)
        self.uiSlowStartAllSpinBox.setMinimum(0)
        self.uiSlowStartAllSpinBox.setMaximum(10000)
        self.uiSlowStartAllSpinBox.setProperty("value", 0)
        self.uiSlowStartAllSpinBox.setObjectName(_fromUtf8("uiSlowStartAllSpinBox"))
        self.verticalLayout_2.addWidget(self.uiSlowStartAllSpinBox)
        spacerItem5 = QtGui.QSpacerItem(20, 318, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.uiMiscTabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.uiMiscTabWidget)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem6 = QtGui.QSpacerItem(324, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.uiRestoreDefaultsPushButton = QtGui.QPushButton(GeneralPreferencesPageWidget)
        self.uiRestoreDefaultsPushButton.setObjectName(_fromUtf8("uiRestoreDefaultsPushButton"))
        self.horizontalLayout_6.addWidget(self.uiRestoreDefaultsPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.retranslateUi(GeneralPreferencesPageWidget)
        self.uiMiscTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(GeneralPreferencesPageWidget)

    def retranslateUi(self, GeneralPreferencesPageWidget):
        GeneralPreferencesPageWidget.setWindowTitle(_translate("GeneralPreferencesPageWidget", "General", None))
        self.uiStyleGroupBox.setTitle(_translate("GeneralPreferencesPageWidget", "Style", None))
        self.uiLocalPathsGroupBox.setTitle(_translate("GeneralPreferencesPageWidget", "Local paths", None))
        self.uiProjectsPathLabel.setText(_translate("GeneralPreferencesPageWidget", "My projects:", None))
        self.uiProjectsPathLineEdit.setToolTip(_translate("GeneralPreferencesPageWidget", "Directory where your GNS3 projects are stored", None))
        self.uiProjectsPathToolButton.setText(_translate("GeneralPreferencesPageWidget", "&Browse...", None))
        self.uiImagesPathLabel.setText(_translate("GeneralPreferencesPageWidget", "My binary images:", None))
        self.uiImagesPathLineEdit.setToolTip(_translate("GeneralPreferencesPageWidget", "Directory where your binary images (e.g. IOS) are stored", None))
        self.uiImagesPathToolButton.setText(_translate("GeneralPreferencesPageWidget", "&Browse...", None))
        self.uiConfigurationFileGroupBox.setTitle(_translate("GeneralPreferencesPageWidget", "Configuration file", None))
        self.uiImportConfigurationFilePushButton.setText(_translate("GeneralPreferencesPageWidget", "&Import", None))
        self.uiExportConfigurationFilePushButton.setText(_translate("GeneralPreferencesPageWidget", "&Export", None))
        self.uiConfigurationFileLabel.setText(_translate("GeneralPreferencesPageWidget", "Unknown location", None))
        self.uiMiscTabWidget.setTabText(self.uiMiscTabWidget.indexOf(self.uiGeneralTab), _translate("GeneralPreferencesPageWidget", "General", None))
        self.uiTelnetConsoleSettingsGroupBox.setTitle(_translate("GeneralPreferencesPageWidget", "Console settings for Telnet connections", None))
        self.uiTelnetConsolePreconfiguredCommandLabel.setText(_translate("GeneralPreferencesPageWidget", "Preconfigured commands:", None))
        self.uiTelnetConsoleCommandLabel.setText(_translate("GeneralPreferencesPageWidget", "Console application command:", None))
        self.uiTelnetConsoleCommandLineEdit.setToolTip(_translate("GeneralPreferencesPageWidget", "<html><head/><body><p>Command line replacements:</p><p>%h = device server </p><p>%p = device port</p><p>%d = device hostname</p></body></html>", None))
        self.uiTelnetConsolePreconfiguredCommandPushButton.setText(_translate("GeneralPreferencesPageWidget", "&Set", None))
        self.uiSerialConsoleSettingsGroupBox.setTitle(_translate("GeneralPreferencesPageWidget", "Console settings for local serial connections", None))
        self.uiSerialConsoleCommandLabel.setText(_translate("GeneralPreferencesPageWidget", "Console application command:", None))
        self.uiSerialConsolePreconfiguredCommandLabel.setText(_translate("GeneralPreferencesPageWidget", "Preconfigured commands:", None))
        self.uiSerialConsoleCommandLineEdit.setToolTip(_translate("GeneralPreferencesPageWidget", "<html><head/><body><p>Command line replacements:</p><p>%d = device hostname</p><p>%s = device pipe file</p></body></html>", None))
        self.uiSerialConsolePreconfiguredCommandPushButton.setText(_translate("GeneralPreferencesPageWidget", "&Set", None))
        self.uiConsoleMiscGroupBox.setTitle(_translate("GeneralPreferencesPageWidget", "Miscellaneous", None))
        self.uiCloseConsoleWindowsOnDeleteCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Close any connected console window when deleting a node", None))
        self.uiBringConsoleWindowToFrontCheckBox.setToolTip(_translate("GeneralPreferencesPageWidget", "<html>This option will attempt to bring existing opened console window to front, instead of opening a new window.<br>If no existing opened console window exists, it will start a new  console window.</html>", None))
        self.uiBringConsoleWindowToFrontCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Bring console window to front (experimental feature)", None))
        self.uiSlowConsoleAllLabel.setText(_translate("GeneralPreferencesPageWidget", "Delay between each console launch when consoling to all devices:", None))
        self.uiDelayConsoleAllSpinBox.setSuffix(_translate("GeneralPreferencesPageWidget", " ms", None))
        self.uiMiscTabWidget.setTabText(self.uiMiscTabWidget.indexOf(self.uiConsoleTab), _translate("GeneralPreferencesPageWidget", "Console applications", None))
        self.uiSceneWidthLabel.setText(_translate("GeneralPreferencesPageWidget", "Default width:", None))
        self.uiSceneHeightLabel.setText(_translate("GeneralPreferencesPageWidget", "Default height:", None))
        self.uiRectangleSelectedItemCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Draw a rectangle when an item is selected", None))
        self.uiDrawLinkStatusPointsCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Draw link status points", None))
        self.uiLinkManualModeCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Always use manual mode when adding links", None))
        self.uiLabelPreviewLabel.setText(_translate("GeneralPreferencesPageWidget", "Default label style:", None))
        self.uiDefaultLabelStylePlainTextEdit.setPlainText(_translate("GeneralPreferencesPageWidget", "AaBbYyZz", None))
        self.uiDefaultLabelFontPushButton.setText(_translate("GeneralPreferencesPageWidget", "&Select default font", None))
        self.uiDefaultLabelColorPushButton.setText(_translate("GeneralPreferencesPageWidget", "&Select default color", None))
        self.uiSceneHeightSpinBox.setSuffix(_translate("GeneralPreferencesPageWidget", " pixels", None))
        self.uiSceneWidthSpinBox.setSuffix(_translate("GeneralPreferencesPageWidget", " pixels", None))
        self.uiMiscTabWidget.setTabText(self.uiMiscTabWidget.indexOf(self.uiSceneTab), _translate("GeneralPreferencesPageWidget", "Topology view", None))
        self.uiLaunchNewProjectDialogCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Launch the new project dialog on startup", None))
        self.uiAutoScreenshotCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Automatically take a screenshot when saving a project", None))
        self.uiCheckForUpdateCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Automatically check for update", None))
        self.uiCrashReportCheckBox.setText(_translate("GeneralPreferencesPageWidget", "Automatically send crash reports", None))
        self.uiSlowStartAllLabel.setText(_translate("GeneralPreferencesPageWidget", "Delay between each device start when starting all devices:", None))
        self.uiSlowStartAllSpinBox.setSuffix(_translate("GeneralPreferencesPageWidget", " seconds", None))
        self.uiMiscTabWidget.setTabText(self.uiMiscTabWidget.indexOf(self.tab), _translate("GeneralPreferencesPageWidget", "Miscellaneous", None))
        self.uiRestoreDefaultsPushButton.setText(_translate("GeneralPreferencesPageWidget", "Restore defaults", None))

