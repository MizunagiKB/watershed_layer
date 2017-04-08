# -*- coding: utf-8 -*-
"""
    @brief OpenCVのイメージ管理用クラス
    @author MizunagiKB
"""
# ------------------------------------------------------------------ import(s)
import os
import time

from PyQt5 import Qt, QtCore, QtWidgets, QtGui

import yaml

import graphics.cv_image


# ----------------------------------------------------------------------------
class CLayerInformation(object):
    """
    """

    COLOR_MUL = 0.75

    def __init__(self, o_color):
        self.m_pen = QtGui.QPen()
        #self.m_pen.setStyle(QtCore.Qt.NoPen)
        self.m_pen.setStyle(QtCore.Qt.SolidLine)

        self.m_pin_pen = Qt.QPen()
        #self.m_pen.setStyle(QtCore.Qt.NoPen)
        self.m_pin_pen.setStyle(QtCore.Qt.SolidLine)

        self.m_brush = Qt.QBrush()
        #self.m_brush.setStyle(QtCore.Qt.NoBrush)
        self.m_brush.setStyle(QtCore.Qt.SolidPattern)

        self.m_pin_brush = Qt.QBrush()
        #self.m_pin_brush.setStyle(QtCore.Qt.NoBrush)
        self.m_pin_brush.setStyle(QtCore.Qt.SolidPattern)

        self.set_color(o_color)

    def set_color(self, o_color):
        self.m_o_color = o_color
        self.m_o_pin_color = Qt.QColor(
            o_color.red() * self.COLOR_MUL,
            o_color.green() * self.COLOR_MUL,
            o_color.blue() * self.COLOR_MUL
        )
        self.m_pen.setColor(self.m_o_pin_color)
        self.m_pin_pen.setColor(Qt.QColor(255, 255, 255))
        self.m_brush.setColor(self.m_o_color)
        self.m_pin_brush.setColor(self.m_o_pin_color)


# ----------------------------------------------------------------------------
class CGPinItem(QtWidgets.QGraphicsRectItem):
    """Watershedのマーカー位置とインデックスを保持するクラス
    """

    def mousePressEvent(self, event):
        """マウスボタン（Press）イベント

        Args:
            event (QGraphicsSceneMouseEvent):
        """
        super(CGPinItem, self).mousePressEvent(event)

        o_gitem = self.parentItem().get_current_tree_item(self)
        if o_gitem is not None:
            o_widget = self.parentItem().m_treewidget_layer
            o_widget.setCurrentItem(o_gitem)

    def mouseReleaseEvent(self, event):
        """マウスボタン（Release）イベント

        Args:
            event (QGraphicsSceneMouseEvent):
        """
        super(CGPinItem, self).mouseReleaseEvent(event)

        self.parentItem().update_color()
        self.parentItem().update_pin()
        self.parentItem().filter_watershed()


# ----------------------------------------------------------------------------
class CGWatershedItem(QtWidgets.QGraphicsPixmapItem):
    """
    """

    def __init__(self, parent):
        """コンストラクタ
        """

        super(CGWatershedItem, self).__init__()

        self.m_parent = parent
        self.m_treewidget_layer = parent.m_uiface.treewidget_layer

        self.m_o_cvfilter = graphics.cv_image.CCVFilter()

        self.m_b_dragging = False
        self.m_n_overlay_alpha = 50
        self.m_picture_pathname = None
        self.m_wshed_pathname = None

        parent.m_uiface.action_FileOpen.triggered.connect(self.action_FileOpen)
        parent.m_uiface.action_FileSave.triggered.connect(self.action_FileSave)
        parent.m_uiface.action_FileSaveAs.triggered.connect(self.action_FileSaveAs)
        parent.m_uiface.action_FileImportPicture.triggered.connect(self.action_FileImportPicture)
        parent.m_uiface.action_FileExportPicture.triggered.connect(self.action_FileExportPicture)
        parent.m_uiface.action_EditColor.triggered.connect(self.action_EditColor)

        parent.m_uiface.action_ViewOriginal.triggered.connect(self.action_ViewOriginal)
        parent.m_uiface.action_ViewOverlay.triggered.connect(self.action_ViewOverlay)
        parent.m_uiface.action_ViewWatershed.triggered.connect(self.action_ViewWatershed)

        parent.m_uiface.tb_layer_append.clicked.connect(self.tb_layer_append_clicked)
        parent.m_uiface.tb_layer_remove.clicked.connect(self.tb_layer_remove_clicked)

        parent.m_uiface.slider_overlay.sliderReleased.connect(self.slider_sliderReleased)
        parent.m_uiface.slider_r.sliderReleased.connect(self.slider_sliderReleased_color)
        parent.m_uiface.slider_g.sliderReleased.connect(self.slider_sliderReleased_color)
        parent.m_uiface.slider_b.sliderReleased.connect(self.slider_sliderReleased_color)

        parent.m_uiface.lineedit_name.textChanged.connect(self.lineedit_textChanged)

        parent.m_uiface.treewidget_layer.currentItemChanged.connect(self.currentItemChanged)
        parent.m_uiface.treewidget_layer.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)

        self.layer_widget_init()

    # ------------------------------------------------------------------------
    def iter_layer(self):
        """TreeWidget(layer)に設定されているdata取得
        """

        o_widget = self.m_treewidget_layer

        for n_layer_index in range(o_widget.topLevelItemCount()):
            yield o_widget.topLevelItem(n_layer_index)

    # ------------------------------------------------------------------------
    def iter_pin(self, o_layer):
        """TreeWidget(pin)に設定されているdata取得
        """

        for n_pin_index in range(o_layer.childCount()):
            yield o_layer.child(n_pin_index)

    # ------------------------------------------------------------------------
    def iter_selected_pin(self):
        """TreeWidget(pin)に設定されているdata取得
        """

        o_widget = self.m_treewidget_layer

        for o_item in o_widget.selectedItems():
            gitem = o_item.data(0, QtCore.Qt.UserRole)
            if isinstance(gitem, CGPinItem) is True:
                yield o_item

    # ------------------------------------------------------------------------
    def layer_widget_init(self):
        """レイヤーの初期化
        """

        self.remove_all_pin()

        o_widget = self.m_treewidget_layer
        o_widget.clear()
        o_widget.setColumnCount(2)

        initial_list_color = [
            Qt.QColor(0xFF, 0xFF, 0xFF),
            Qt.QColor(0xFF, 0x00, 0x00),
            Qt.QColor(0x00, 0xFF, 0x00),
            Qt.QColor(0x00, 0x00, 0xFF)
        ]

        for n_index, o_color in enumerate(initial_list_color):
            o_layer = QtWidgets.QTreeWidgetItem()
            o_layer.setText(0, "")
            if n_index == 0:
                o_layer.setText(1, "Base")
                o_layer.setData(0, QtCore.Qt.UserRole, None)
            else:
                o_layer_info = CLayerInformation(o_color)
                o_layer.setText(1, "Layer%d" % (n_index,))
                o_layer.setData(0, QtCore.Qt.UserRole, o_layer_info)

                o_pixmap = QtGui.QPixmap(48, 16)
                o_pixmap.fill(o_layer_info.m_o_color)
                o_layer.setIcon(0, QtGui.QIcon(o_pixmap))

            o_widget.addTopLevelItem(o_layer)

        self.update_color()

        o_widget.setCurrentItem(o_widget.topLevelItem(1))

    # ------------------------------------------------------------------------
    def get_current_layer(self):
        """選択中のレイヤー（TreeWidgetItem）の取得

        Returns:
            TreeWidgetItem:
        """

        o_widget = self.m_treewidget_layer

        o_item = o_widget.currentItem()
        if o_item is not None:
            o_item_data = o_item.data(0, QtCore.Qt.UserRole)
            if o_item_data is None:
                pass
            elif isinstance(o_item_data, CLayerInformation) is True:
                return o_item
            elif isinstance(o_item_data, CGPinItem) is True:
                return o_item.parent()

        return None

    # ------------------------------------------------------------------------
    def import_picture(self, pathname):

        o_dlg = QtWidgets.QProgressDialog(self.m_parent)
        o_dlg.setWindowModality(QtCore.Qt.WindowModal)
        o_dlg.setValue(0)
        o_dlg.setModal(True)
        o_dlg.show()

        cvimage = graphics.cv_image.load(pathname)
        o_dlg.setValue(20)

        if cvimage is not None:
            self.remove_all_pin()
            o_dlg.setValue(40)
            self.m_o_cvfilter.attach(cvimage)
            o_dlg.setValue(80)
            self.m_picture_pathname = pathname
            o_dlg.setValue(80)
            self.filter_watershed()

        o_dlg.setValue(100)
        time.sleep(0.2)
        o_dlg.close()

    def save(self, wshed_pathname):
        list_savedata = []
        for o_layer in self.iter_layer():
            dict_layer_info = {
                "name": o_layer.text(1)
            }
            o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)
            if o_layer_info is None:
                dict_layer_info["color"] = {
                    "r": 0,
                    "g": 0,
                    "b": 0
                }
            else:
                dict_layer_info["color"] = {
                    "r": o_layer_info.m_o_color.red(),
                    "g": o_layer_info.m_o_color.green(),
                    "b": o_layer_info.m_o_color.blue()
                }
            list_pin = []
            for o_pin in self.iter_pin(o_layer):
                o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                list_pin.append(
                    {
                        "x": o_gitem.rect().x(),
                        "y": o_gitem.rect().y()
                    }
                )

            dict_layer_info["list_pin"] = list_pin

            list_savedata.append(dict_layer_info)

        with open(wshed_pathname, "wb") as h_writer:
            h_writer.write(
                yaml.dump(list_savedata, encoding="utf-8")
            )
            if self.m_wshed_pathname is None:
                self.m_wshed_pathname = wshed_pathname

    def filter_watershed(self):
        """画像情報の反映処理
        """

        if self.m_parent.m_uiface.action_ViewOriginal.isChecked() is True:
            alpha = 1.0
        elif self.m_parent.m_uiface.action_ViewOverlay.isChecked() is True:
            alpha = (100 - self.m_n_overlay_alpha) / 100.0
        else:
            alpha = 0.0

        cvimage_result = self.m_o_cvfilter.watershed(alpha)

        if cvimage_result is not None:
            o_pixmap = conv_cvimage_to_pixmap(cvimage_result)
            self.setPixmap(o_pixmap)

    def update_pin(self):
        """ピン情報の反映処理
        """

        self.m_o_cvfilter.marker_clear()

        n_layer_index = 0
        for o_layer in self.iter_layer():
            for o_pin in self.iter_pin(o_layer):
                o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                o_point = o_gitem.mapToParent(
                    o_gitem.rect().x() + 8,
                    o_gitem.rect().y() + 8
                )

                o_pin.setText(
                    1,
                    "Pin(%(x)d, %(y)d)" % {
                        "x": o_point.x(),
                        "y": o_point.y()
                    }
                )

                self.m_o_cvfilter.marker_set(
                    o_point.x(), o_point.y(),
                    n_layer_index
                )
            n_layer_index += 1

    def update_color(self):
        """カラー情報の反映処理
        """

        list_color = []

        for o_layer in self.iter_layer():
            o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)
            if o_layer_info is None:
                list_color.append(Qt.QColor(0, 0, 0))
            else:
                list_color.append(o_layer_info.m_o_color)

                o_pixmap = QtGui.QPixmap(48, 16)
                o_pixmap.fill(o_layer_info.m_o_color)
                o_layer.setIcon(0, QtGui.QIcon(o_pixmap))

                for o_pin in self.iter_pin(o_layer):
                    o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                    o_gitem.setPen(o_layer_info.m_pin_pen)
                    o_gitem.setBrush(o_layer_info.m_pin_brush)

        self.m_o_cvfilter.update_ary_color(list_color)

    # ------------------------------------------------------------------------
    def append_pin(self, o_layer, o_pos):
        """指定したレイヤーにPinを追加

        Args:
            o_layer (QTreeWidgetItem):
                追加対象のレイヤー
            o_pos (QPoint):
                追加する座標

        Returns:
            CGPinItem:
                追加したPinを戻します。
        """

        if o_layer is None:

            return None

        else:
            o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)

            o_gitem = CGPinItem(
                o_pos.x() - 8, o_pos.y() - 8, 16, 16
            )
            o_gitem.setPen(o_layer_info.m_pin_pen)
            o_gitem.setBrush(o_layer_info.m_pin_brush)
            o_gitem.setParentItem(self)
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
#            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges, True)
#            o_gitem.installSceneEventFilter(self)

            o_pin = QtWidgets.QTreeWidgetItem()
            o_pin.setText(1, "Pin")
            o_pin.setData(
                0,
                QtCore.Qt.UserRole,
                o_gitem
            )

            o_layer.addChild(o_pin)

            self.update_color()
            self.update_pin()
            self.filter_watershed()

            return o_pin

    # ------------------------------------------------------------------------
    def remove_pin(self, o_remove_pin):

        for o_layer in self.iter_layer():
            for o_pin in self.iter_pin(o_layer):
                if o_pin is not None and o_remove_pin == o_pin:
                    o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                    if o_gitem is not None:
                        o_remove_pin.setData(0, QtCore.Qt.UserRole, None)
                        o_layer.removeChild(o_remove_pin)
                        o_gitem.setParentItem(None)
                        o_gitem.scene().removeItem(o_gitem)

                        self.update_color()
                        self.update_pin()
                        self.filter_watershed()

                        break

    # ------------------------------------------------------------------------
    def remove_all_pin(self):

        for o_layer in self.iter_layer():
            list_o_pin = []
            for o_pin in self.iter_pin(o_layer):
                list_o_pin.append(o_pin)

            for o_pin in list_o_pin:
                o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                if o_gitem is not None:
                    o_layer.removeChild(o_pin)
                    o_gitem.scene().removeItem(o_gitem)

    # ------------------------------------------------------------------------
    def get_current_tree_item(self, o_gitem):
        """CGPinItemに対応するQTreeWidgetItemを取得します。

        Args:
            o_gitem:

        Returns:
            CGPinItem:
        """

        if o_gitem is not None:
            for o_layer in self.iter_layer():
                for o_pin in self.iter_pin(o_layer):
                    if o_pin.data(0, QtCore.Qt.UserRole) == o_gitem:
                        return o_pin
        return None

    # ------------------------------------------------------------------------
    def tb_layer_append_clicked(self):

        o_widget = self.m_treewidget_layer

        o_layer_info = CLayerInformation(
            Qt.QColor(0xFF, 0x00, 0x00)
        )

        o_layer = QtWidgets.QTreeWidgetItem()
        o_layer.setText(0, "")
        o_layer.setText(1, "new Layer")
        o_layer.setData(0, QtCore.Qt.UserRole, o_layer_info)

        o_pixmap = QtGui.QPixmap(48, 16)
        o_pixmap.fill(o_layer_info.m_o_color)
        o_layer.setIcon(0, QtGui.QIcon(o_pixmap))

        o_widget.addTopLevelItem(o_layer)

        self.update_color()
        self.update_pin()
        self.filter_watershed()

    # ------------------------------------------------------------------------
    def tb_layer_remove_clicked(self):

        o_layer = self.get_current_layer()
        if o_layer is not None:
            o_layer.setData(0, QtCore.Qt.UserRole, None)

            list_o_pin = [o_pin for o_pin in self.iter_pin(o_layer)]
            for o_pin in list_o_pin:
                o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                if o_gitem is not None:
                    o_gitem.scene().removeItem(o_gitem)
                o_layer.removeChild(o_pin)

            self.m_treewidget_layer.headerItem().removeChild(o_layer)

            self.update_color()
            self.update_pin()
            self.filter_watershed()

    # ------------------------------------------------------------------------
    def slider_sliderReleased(self):
        self.m_n_overlay_alpha = self.m_parent.m_uiface.slider_overlay.value()
        self.filter_watershed()

    # ------------------------------------------------------------------------
    def slider_sliderReleased_color(self):
        o_layer = self.get_current_layer()
        if o_layer is not None:
            o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)
            if o_layer_info is not None:
                o_layer_info.set_color(
                    Qt.QColor(
                        self.m_parent.m_uiface.slider_r.value(),
                        self.m_parent.m_uiface.slider_g.value(),
                        self.m_parent.m_uiface.slider_b.value()
                    )
                )

        self.update_color()
        self.update_pin()
        self.filter_watershed()

    # ------------------------------------------------------------------------
    def action_FileOpen(self):
        """ファイル入力
        """

        o_dlg = QtWidgets.QFileDialog(self.m_parent)
        o_dlg.setWindowModality(QtCore.Qt.WindowModal)
        o_dlg.setNameFilter("Watershed files (*.wshed)")
        o_dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        o_dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        o_dlg.setModal(True)

        def signal_finished(result):
            if result == QtWidgets.QDialog.Accepted:
                for pathname in o_dlg.selectedFiles():
                    with open(pathname, "rb") as h_reader:
                        list_savedata = yaml.load(h_reader.read())

                        self.remove_all_pin()

                        o_widget = self.m_parent.m_uiface.treewidget_layer
                        o_widget.clear()
                        o_widget.setColumnCount(2)

                        for n_index, dict_layer_info in enumerate(list_savedata):
                            o_color = Qt.QColor(
                                dict_layer_info["color"]["r"],
                                dict_layer_info["color"]["g"],
                                dict_layer_info["color"]["b"]
                            )

                            o_layer = QtWidgets.QTreeWidgetItem()
                            o_layer.setText(0, "")
                            if n_index == 0:
                                o_layer.setText(1, "Base")
                                o_layer.setData(0, QtCore.Qt.UserRole, None)
                            else:
                                o_layer_info = CLayerInformation(o_color)
                                o_layer.setText(1, dict_layer_info["name"])
                                o_layer.setData(0, QtCore.Qt.UserRole, o_layer_info)

                                o_pixmap = QtGui.QPixmap(48, 16)
                                o_pixmap.fill(o_layer_info.m_o_color)
                                o_layer.setIcon(0, QtGui.QIcon(o_pixmap))

                            for dict_pos in dict_layer_info["list_pin"]:
                                o_pos = Qt.QPoint(dict_pos["x"], dict_pos["y"])
                                self.append_pin(o_layer, o_pos)

                            o_widget.addTopLevelItem(o_layer)

                        o_widget.setCurrentItem(o_widget.topLevelItem(1))

                        self.update_color()
                        self.update_pin()
                        self.filter_watershed()

                        self.m_wshed_pathname = pathname
                        break

        o_dlg.finished.connect(signal_finished)
        o_dlg.show()

    # ------------------------------------------------------------------------
    def action_FileSave(self):
        if self.m_wshed_pathname is not None and os.path.exists(self.m_wshed_pathname) is True:
            self.save(self.m_wshed_pathname)
        else:
            self.action_FileSaveAs()

    # ------------------------------------------------------------------------
    def action_FileSaveAs(self):
        """ファイル出力
        """

        o_dlg = QtWidgets.QFileDialog(self.m_parent)
        o_dlg.setWindowModality(QtCore.Qt.WindowModal)
        o_dlg.setNameFilter("Watershed files (*.wshed)")
        o_dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        o_dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        o_dlg.setModal(True)

        def signal_finished(result):
            if result == QtWidgets.QDialog.Accepted:
                for pathname in o_dlg.selectedFiles():
                    self.save(pathname)

        o_dlg.finished.connect(signal_finished)
        o_dlg.show()

    # ------------------------------------------------------------------------
    def action_FileImportPicture(self):
        """画像の読み込み処理
        """

        o_dlg = QtWidgets.QFileDialog(self.m_parent)
        o_dlg.setWindowModality(QtCore.Qt.WindowModal)
        o_dlg.setNameFilter("Picture files (*.jpg *.jpeg *.png)")
        o_dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        o_dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        o_dlg.setModal(True)

        def signal_finished(result):
            if result == QtWidgets.QDialog.Accepted:
                for pathname in o_dlg.selectedFiles():
                    self.import_picture(pathname)

        o_dlg.finished.connect(signal_finished)
        o_dlg.show()

    # ------------------------------------------------------------------------
    def action_FileExportPicture(self):
        """ファイル出力
        """
        o_dlg = QtWidgets.QFileDialog(self.m_parent)
        o_dlg.setWindowModality(QtCore.Qt.WindowModal)
        o_dlg.setNameFilter("Picture files (*.jpg *.jpeg *.png)")
        o_dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        o_dlg.setModal(True)

        def signal_finished(result):
            if result == QtWidgets.QDialog.Accepted:
                for pathname in o_dlg.selectedFiles():
                    _, ext = os.path.splitext(pathname)
                    if ext.lower() in (".jpg", ".jpeg", ".png"):
                        if self.m_parent.m_uiface.action_ViewOriginal.isChecked() is True:
                            alpha = 1.0
                        elif self.m_parent.m_uiface.action_ViewOverlay.isChecked() is True:
                            alpha = (100 - self.m_n_overlay_alpha) / 100.0
                        else:
                            alpha = 0.0

                        cvimage = self.m_o_cvfilter.watershed(alpha)
                        graphics.cv_image.save(pathname, cvimage)
                    break

        o_dlg.finished.connect(signal_finished)
        o_dlg.show()

    def action_ViewOriginal(self):
        self.m_parent.m_uiface.action_ViewOriginal.setChecked(True)
        self.m_parent.m_uiface.action_ViewOverlay.setChecked(False)
        self.m_parent.m_uiface.action_ViewWatershed.setChecked(False)
        self.filter_watershed()

    def action_ViewOverlay(self):
        self.m_parent.m_uiface.action_ViewOriginal.setChecked(False)
        self.m_parent.m_uiface.action_ViewOverlay.setChecked(True)
        self.m_parent.m_uiface.action_ViewWatershed.setChecked(False)
        self.filter_watershed()

    def action_ViewWatershed(self):
        self.m_parent.m_uiface.action_ViewOriginal.setChecked(False)
        self.m_parent.m_uiface.action_ViewOverlay.setChecked(False)
        self.m_parent.m_uiface.action_ViewWatershed.setChecked(True)
        self.filter_watershed()

    def mousePressEvent(self, event):
        """
        Args:
            event (QMouseEvent):
        """

        super(CGWatershedItem, self).mousePressEvent(event)

        if self.m_b_dragging is not True:
            if event.button() == QtCore.Qt.LeftButton:
                o_layer = self.get_current_layer()
                self.append_pin(o_layer, event.pos())
                self.update_pin()
                self.filter_watershed()

    def lineedit_textChanged(self, text):
        o_layer = self.get_current_layer()
        if o_layer is not None:
            o_layer.setText(1, text)

    def currentItemChanged(self, current, previous):
        o_layer = self.get_current_layer()
        if o_layer is not None:
            o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)
            if isinstance(o_layer_info, CLayerInformation) is True:

                self.m_parent.m_uiface.lineedit_name.setText(o_layer.text(1))

                self.m_parent.m_uiface.slider_r.setSliderPosition(o_layer_info.m_o_color.red())
                self.m_parent.m_uiface.slider_g.setSliderPosition(o_layer_info.m_o_color.green())
                self.m_parent.m_uiface.slider_b.setSliderPosition(o_layer_info.m_o_color.blue())

        if current is not None:
            o_item = current.data(0, QtCore.Qt.UserRole)
            if isinstance(o_item, CGPinItem) is True:
                for o_layer in self.iter_layer():
                    for o_pin in self.iter_pin(o_layer):
                        o_pin_data = o_pin.data(0, QtCore.Qt.UserRole)
                        if o_pin_data is not None:
                            o_pin_data.setSelected(False)

                o_item.setSelected(True)


    def itemDoubleClicked(self, item, column):
        o_item = item.data(0, QtCore.Qt.UserRole)

        if o_item is None:
            pass
        elif isinstance(o_item, CLayerInformation) is True:
            if edit_layer_information_color(self.m_parent, item) is True:
                self.update_color()
                self.update_pin()
                self.filter_watershed()
        elif isinstance(o_item, CGPinItem) is True:
            pass

    def action_EditColor(self):

        o_layer = self.get_current_layer()

        if o_layer is not None:
            if edit_layer_information_color(self.m_parent, o_layer) is True:
                self.currentItemChanged(o_layer, o_layer)
                self.update_color()
                self.update_pin()
                self.filter_watershed()


# ============================================================================
def edit_layer_information_color(parent, o_layer):

    o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)

    o_dlg = QtWidgets.QColorDialog(parent)
    o_dlg.setWindowModality(QtCore.Qt.WindowModal)
    o_dlg.setCurrentColor(o_layer_info.m_o_color)
    o_dlg.setModal(True)

    if o_dlg.exec() == QtWidgets.QDialog.Accepted:

        o_layer_info.set_color(o_dlg.selectedColor())

        return True

    else:
        return False


# ============================================================================
def conv_cvimage_to_pixmap(cvimage_src):
    """OpenCV画像からQPixmapに変換

    Args:
        cvimage_src (cv2::image):
    """

    # 色情報の並びを変更（BGR to RGB）
    cvimage_dst = graphics.cv_image.colororder_bgr_to_rgb(cvimage_src)

    o_image = Qt.QImage(
        cvimage_dst,
        cvimage_dst.shape[1],
        cvimage_dst.shape[0],
        cvimage_dst.shape[1] * 3,
        Qt.QImage.Format_RGB888
    )

    result_o_pixmap = QtGui.QPixmap()
    result_o_pixmap.convertFromImage(o_image)

    return result_o_pixmap



# [EOF]
