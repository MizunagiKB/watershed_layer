# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockwidget_layer = QtWidgets.QDockWidget(MainWindow)
        self.dockwidget_layer.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockwidget_layer.setObjectName("dockwidget_layer")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.dockWidgetContents_4)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.slider_overlay = QtWidgets.QSlider(self.dockWidgetContents_4)
        self.slider_overlay.setMaximum(100)
        self.slider_overlay.setProperty("value", 50)
        self.slider_overlay.setSliderPosition(50)
        self.slider_overlay.setTracking(True)
        self.slider_overlay.setOrientation(QtCore.Qt.Horizontal)
        self.slider_overlay.setInvertedAppearance(False)
        self.slider_overlay.setInvertedControls(False)
        self.slider_overlay.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider_overlay.setObjectName("slider_overlay")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.slider_overlay)
        self.verticalLayout.addLayout(self.formLayout)
        self.line_2 = QtWidgets.QFrame(self.dockWidgetContents_4)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.treewidget_layer = QtWidgets.QTreeWidget(self.dockWidgetContents_4)
        self.treewidget_layer.setDragEnabled(False)
        self.treewidget_layer.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.treewidget_layer.setAlternatingRowColors(False)
        self.treewidget_layer.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.treewidget_layer.setAutoExpandDelay(3)
        self.treewidget_layer.setUniformRowHeights(False)
        self.treewidget_layer.setAnimated(True)
        self.treewidget_layer.setColumnCount(2)
        self.treewidget_layer.setObjectName("treewidget_layer")
        self.treewidget_layer.headerItem().setText(0, "[]")
        self.treewidget_layer.headerItem().setText(1, "name")
        self.treewidget_layer.header().setCascadingSectionResizes(True)
        self.treewidget_layer.header().setDefaultSectionSize(32)
        self.treewidget_layer.header().setHighlightSections(False)
        self.treewidget_layer.header().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.treewidget_layer)
        self.line = QtWidgets.QFrame(self.dockWidgetContents_4)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents_4)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineedit_name = QtWidgets.QLineEdit(self.dockWidgetContents_4)
        self.lineedit_name.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_name.sizePolicy().hasHeightForWidth())
        self.lineedit_name.setSizePolicy(sizePolicy)
        self.lineedit_name.setMaxLength(64)
        self.lineedit_name.setReadOnly(True)
        self.lineedit_name.setObjectName("lineedit_name")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineedit_name)
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents_4)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.dockWidgetContents_4)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.slider_g = QtWidgets.QSlider(self.dockWidgetContents_4)
        self.slider_g.setMaximum(255)
        self.slider_g.setPageStep(8)
        self.slider_g.setOrientation(QtCore.Qt.Horizontal)
        self.slider_g.setObjectName("slider_g")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.slider_g)
        self.label_5 = QtWidgets.QLabel(self.dockWidgetContents_4)
        self.label_5.setObjectName("label_5")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.slider_b = QtWidgets.QSlider(self.dockWidgetContents_4)
        self.slider_b.setMaximum(255)
        self.slider_b.setPageStep(8)
        self.slider_b.setOrientation(QtCore.Qt.Horizontal)
        self.slider_b.setObjectName("slider_b")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.slider_b)
        self.slider_r = QtWidgets.QSlider(self.dockWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider_r.sizePolicy().hasHeightForWidth())
        self.slider_r.setSizePolicy(sizePolicy)
        self.slider_r.setMaximum(255)
        self.slider_r.setPageStep(8)
        self.slider_r.setOrientation(QtCore.Qt.Horizontal)
        self.slider_r.setObjectName("slider_r")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.slider_r)
        self.verticalLayout.addLayout(self.formLayout_3)
        self.dockwidget_layer.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockwidget_layer)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.toolBar_3 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_3.setObjectName("toolBar_3")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_3)
        self.action_FileOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/res/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_FileOpen.setIcon(icon)
        self.action_FileOpen.setObjectName("action_FileOpen")
        self.action_FileQuit = QtWidgets.QAction(MainWindow)
        self.action_FileQuit.setObjectName("action_FileQuit")
        self.action_FileSave = QtWidgets.QAction(MainWindow)
        self.action_FileSave.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/res/res/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_FileSave.setIcon(icon1)
        self.action_FileSave.setObjectName("action_FileSave")
        self.action_ViewWatershed = QtWidgets.QAction(MainWindow)
        self.action_ViewWatershed.setCheckable(True)
        self.action_ViewWatershed.setObjectName("action_ViewWatershed")
        self.action_ViewAutoUpdate = QtWidgets.QAction(MainWindow)
        self.action_ViewAutoUpdate.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/res/res/arrow_refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_ViewAutoUpdate.setIcon(icon2)
        self.action_ViewAutoUpdate.setObjectName("action_ViewAutoUpdate")
        self.action_EditColor = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/res/res/color_wheel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_EditColor.setIcon(icon3)
        self.action_EditColor.setObjectName("action_EditColor")
        self.action_FileExportPicture = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/res/res/picture_save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_FileExportPicture.setIcon(icon4)
        self.action_FileExportPicture.setObjectName("action_FileExportPicture")
        self.action_FileSaveAs = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/res/res/disk_multiple.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_FileSaveAs.setIcon(icon5)
        self.action_FileSaveAs.setObjectName("action_FileSaveAs")
        self.action_FileImportPicture = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/res/res/folder_picture.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_FileImportPicture.setIcon(icon6)
        self.action_FileImportPicture.setObjectName("action_FileImportPicture")
        self.action_ViewOriginal = QtWidgets.QAction(MainWindow)
        self.action_ViewOriginal.setCheckable(True)
        self.action_ViewOriginal.setObjectName("action_ViewOriginal")
        self.action_ViewOverlay = QtWidgets.QAction(MainWindow)
        self.action_ViewOverlay.setCheckable(True)
        self.action_ViewOverlay.setChecked(True)
        self.action_ViewOverlay.setObjectName("action_ViewOverlay")
        self.toolBar.addAction(self.action_FileOpen)
        self.toolBar.addAction(self.action_FileSave)
        self.toolBar.addAction(self.action_FileSaveAs)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_FileImportPicture)
        self.toolBar.addAction(self.action_FileExportPicture)
        self.toolBar_2.addAction(self.action_EditColor)
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.action_ViewAutoUpdate)
        self.toolBar_3.addAction(self.action_ViewOriginal)
        self.toolBar_3.addAction(self.action_ViewOverlay)
        self.toolBar_3.addAction(self.action_ViewWatershed)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "watershed_region"))
        self.label.setText(_translate("MainWindow", "Overlay Level"))
        self.label_2.setText(_translate("MainWindow", "LayerName"))
        self.label_3.setText(_translate("MainWindow", "Red"))
        self.label_4.setText(_translate("MainWindow", "Green"))
        self.label_5.setText(_translate("MainWindow", "Blue"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.toolBar_3.setWindowTitle(_translate("MainWindow", "toolBar_3"))
        self.action_FileOpen.setText(_translate("MainWindow", "Open..."))
        self.action_FileOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_FileQuit.setText(_translate("MainWindow", "Quit"))
        self.action_FileSave.setText(_translate("MainWindow", "Save"))
        self.action_FileSave.setToolTip(_translate("MainWindow", "Save"))
        self.action_FileSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_ViewWatershed.setText(_translate("MainWindow", "Watershed"))
        self.action_ViewWatershed.setToolTip(_translate("MainWindow", "Watershed"))
        self.action_ViewAutoUpdate.setText(_translate("MainWindow", "ViewAutoUpdate"))
        self.action_EditColor.setText(_translate("MainWindow", "Color"))
        self.action_FileExportPicture.setText(_translate("MainWindow", "Export Picture..."))
        self.action_FileSaveAs.setText(_translate("MainWindow", "SaveAs..."))
        self.action_FileImportPicture.setText(_translate("MainWindow", "Import Picture..."))
        self.action_ViewOriginal.setText(_translate("MainWindow", "Original"))
        self.action_ViewOriginal.setToolTip(_translate("MainWindow", "Original"))
        self.action_ViewOverlay.setText(_translate("MainWindow", "Overlay"))
        self.action_ViewOverlay.setToolTip(_translate("MainWindow", "Overlay"))

import resource_rc
