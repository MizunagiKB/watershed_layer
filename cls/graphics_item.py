# -*- coding: utf-8 -*-
"""
    @brief OpenCVのイメージ管理用クラス
    @author MizunagiKB
"""
# ------------------------------------------------------------------ import(s)
from PyQt5 import Qt, QtCore, QtWidgets

import yaml

import cls.cv_image


# ----------------------------------------------------------------------------
class CLayerInformation(object):

    COLOR_MUL = 0.75

    def __init__(self, o_color):
        self.m_pen = Qt.QPen()
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
    """Watershedの基準点となる、Pin(Marker)クラス
    """

    def focusInEvent(self, event):
        """フォーカス取得イベント

        Args:
            event:
        """
        super(CGPinItem, self).focusInEvent(event)

        o_gitem = self.parentItem().get_current_tree_item(self)
        if o_gitem is not None:
            o_widget = self.parentItem().m_uiface.treewidget_layer
            o_widget.setCurrentItem(o_gitem)

    def mouseReleaseEvent(self, event):
        """マウスボタン（Release）イベント
        """
        super(CGPinItem, self).mouseReleaseEvent(event)

        self.parentItem().update_pin()


# ----------------------------------------------------------------------------
class CGWatershedItem(QtWidgets.QGraphicsPixmapItem):
    """
    """

    def __init__(self, parent):
        """コンストラクタ
        """

        super(CGWatershedItem, self).__init__()

        self.m_o_cvimage = cls.cv_image.CCVWatershed()

        self.m_parent = parent

        self.m_uiface = parent.uiface
        self.m_uiface.action_FileOpen.triggered.connect(self.action_FileOpen)
        self.m_uiface.action_FileSaveAs.triggered.connect(self.action_FileSaveAs)
        self.m_uiface.action_FileImportPicture.triggered.connect(self.action_FileImportPicture)
        self.m_uiface.action_FileExportPicture.triggered.connect(self.action_FileExportPicture)
        self.m_uiface.action_EditColor.triggered.connect(self.action_EditColor)

        self.m_uiface.action_ViewOriginal.triggered.connect(self.action_ViewOriginal)
        self.m_uiface.action_ViewOriginal.changed.connect(self.update_ui)
        self.m_uiface.action_ViewOverlay.triggered.connect(self.action_ViewOverlay)
        self.m_uiface.action_ViewOverlay.changed.connect(self.update_ui)
        self.m_uiface.action_ViewWatershed.triggered.connect(self.action_ViewWatershed)
        self.m_uiface.action_ViewWatershed.changed.connect(self.update_ui)

        self.m_uiface.treewidget_layer.currentItemChanged.connect(self.currentItemChanged)
        self.m_uiface.treewidget_layer.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.layer_widget_init()

    # ------------------------------------------------------------------------
    def iter_layer(self):
        """TreeWidget(layer)に設定されているdata取得
        """

        o_widget = self.m_uiface.treewidget_layer

        for n_layer_index in range(o_widget.topLevelItemCount()):
            yield o_widget.topLevelItem(n_layer_index)

    # ------------------------------------------------------------------------
    def iter_pin(self, o_layer):
        """TreeWidget(pin)に設定されているdata取得
        """

        o_widget = self.m_uiface.treewidget_layer

        for n_pin_index in range(o_layer.childCount()):
            yield o_layer.child(n_pin_index)

    # ------------------------------------------------------------------------
    def layer_widget_init(self):
        """レイヤーの初期化
        """

        self.remove_all_pin()

        o_widget = self.m_uiface.treewidget_layer
        o_widget.clear()
        o_widget.setColumnCount(2)

        n_index = 0
        for ary_color in self.m_o_cvimage.m_narray_color:
            o_layer_info = CLayerInformation(
                Qt.QColor(ary_color[2], ary_color[1], ary_color[0])
            )

            o_layer = QtWidgets.QTreeWidgetItem()
            o_layer.setText(0, "[]")
            if n_index == 0:
                o_layer.setText(1, "Base")
                o_layer.setData(0, QtCore.Qt.UserRole, None)
            else:
                o_layer.setText(1, "Layer %d" % (n_index + 0,))
                o_layer.setData(0, QtCore.Qt.UserRole, o_layer_info)
                o_layer.setBackground(0, o_layer_info.m_brush)

            o_widget.addTopLevelItem(o_layer)
            n_index += 1

        o_widget.setCurrentItem(o_widget.topLevelItem(0))

    def get_current_layer(self):

        o_widget = self.m_uiface.treewidget_layer
        o_item = o_widget.currentItem()
        o_item_data = o_item.data(0, QtCore.Qt.UserRole)
        if isinstance(o_item_data, CLayerInformation) is True:
            return o_item
        elif o_item_data is not None:
            return o_item.parent()
        else:
            return None

    def load(self, image_pathname):
        self.remove_all_pin()
        self.m_o_cvimage.load(image_pathname)
        self.filter_watershed()

    def filter_watershed(self):
        """画像情報の反映処理
        """

        if self.m_uiface.action_ViewOriginal.isChecked() is True:
            alpha = 1.0
        elif self.m_uiface.action_ViewOverlay.isChecked() is True:
            alpha = 0.5
        else:
            alpha = 0.0

        cvimage_result = self.m_o_cvimage.watershed(alpha)

        if cvimage_result is not None:
            o_pixmap = cls.cv_image.conv_cvimage_to_pixmap(cvimage_result)
            self.setPixmap(o_pixmap)

    def update_pin(self):
        """ピン情報の反映処理
        """

        self.m_o_cvimage.marker_clr()

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

                self.m_o_cvimage.marker_set(
                    o_point,
                    n_layer_index
                )
            n_layer_index += 1

        self.filter_watershed()

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
                for o_pin in self.iter_pin(o_layer):
                    o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                    o_gitem.setPen(o_layer_info.m_pin_pen)
                    o_gitem.setBrush(o_layer_info.m_pin_brush)

        self.m_o_cvimage.set_color_list(list_color)
        self.filter_watershed()

    def update_ui(self):
        pass

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
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges, True)
            o_gitem.installSceneEventFilter(self)

            o_pin = QtWidgets.QTreeWidgetItem()
            o_pin.setText(1, "Pin")
            o_pin.setData(
                0,
                QtCore.Qt.UserRole,
                o_gitem
            )

            o_layer.addChild(o_pin)

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

    def dropEvent(self, event):
        print(event)

    def action_FileOpen(self):
        """ファイル入力
        """

        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.m_parent,
            "Open Yaml File",
            "ws_layer Supported File", "Yaml files (*.yml *.yaml)"
        )

        if path:

            with open(path, "rb") as h_reader:
                list_savedata = yaml.load(h_reader.read())

                self.remove_all_pin()

                o_widget = self.m_uiface.treewidget_layer
                o_widget.clear()
                o_widget.setColumnCount(2)

                n_index = 0
                for dict_layer_info in list_savedata:
                    dict_color = dict_layer_info["color"]
                    o_layer_info = CLayerInformation(
                        Qt.QColor(dict_color["r"], dict_color["g"], dict_color["b"])
                    )

                    o_layer = QtWidgets.QTreeWidgetItem()
                    o_layer.setText(0, "[]")
                    o_layer.setText(1, dict_layer_info["name"])
                    o_layer.setData(
                        0,
                        QtCore.Qt.UserRole,
                        o_layer_info
                    )
                    o_layer.setBackground(0, o_layer_info.m_brush)

                    for dict_pos in dict_layer_info["list_pin"]:
                        o_pos = Qt.QPoint(dict_pos["x"], dict_pos["y"])
                        self.append_pin(o_layer, o_pos)

                    o_widget.addTopLevelItem(o_layer)
                    n_index += 1

                o_widget.setCurrentItem(o_widget.topLevelItem(0))

                self.update_color()
                self.update_pin()


    def action_FileSaveAs(self):
        """ファイル出力
        """
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.m_parent,
            "Save Picture File",
            "export.yaml"
        )

        if path:
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

            with open(path, "wb") as h_writer:
                h_writer.write(
                    yaml.dump(list_savedata, encoding="utf-8")
                )

    def action_FileImportPicture(self):
        """画像の読み込み処理
        """

        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Open Yaml File",
            "ws_layer Supported File", "Yaml files (*.jpg *.jpeg *.png)"
        )

        if path:
            self.load(path)

    def action_FileExportPicture(self):
        """ファイル出力
        """
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Save Picture File",
            "export.png"
        )

        if path:

            if self.m_uiface.action_ViewOriginal.isChecked() is True:
                alpha = 1.0
            elif self.m_uiface.action_ViewOverlay.isChecked() is True:
                alpha = 0.5
            else:
                alpha = 0.0

            cvimage = self.m_o_cvimage.watershed(alpha)
            self.m_o_cvimage.save(path, cvimage)

    def action_ViewOriginal(self):
        self.m_uiface.action_ViewOriginal.setChecked(True)
        self.m_uiface.action_ViewOverlay.setChecked(False)
        self.m_uiface.action_ViewWatershed.setChecked(False)
        self.filter_watershed()

    def action_ViewOverlay(self):
        self.m_uiface.action_ViewOriginal.setChecked(False)
        self.m_uiface.action_ViewOverlay.setChecked(True)
        self.m_uiface.action_ViewWatershed.setChecked(False)
        self.filter_watershed()

    def action_ViewWatershed(self):
        self.m_uiface.action_ViewOriginal.setChecked(False)
        self.m_uiface.action_ViewOverlay.setChecked(False)
        self.m_uiface.action_ViewWatershed.setChecked(True)
        self.filter_watershed()

    def keyPressEvent(self, event):
        """キーボード入力イベント

        Args:
            evt (QKeyEvent):
                キーイベント
        """

        if event.key() == 0x20:
            pass
        elif event.key() == 0x1000003:
            o_gitem = self.focusItem()
            if isinstance(o_gitem, CGPinItem) is True:
                # deleteキーで削除
                self.remove_pin(self.get_current_tree_item(o_gitem))
                self.update_pin()

    def keyReleaseEvent(self, event):
        if event.key() == 0x20:
            pass

    def mousePressEvent(self, event):
        """
        Args:
            event (QMouseEvent):
        """

        super(CGWatershedItem, self).mousePressEvent(event)

        if event.button() == QtCore.Qt.LeftButton:
            o_layer = self.get_current_layer()

            self.append_pin(o_layer, event.pos())
            self.update_pin()

    def currentItemChanged(self, current, previous):
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
            if edit_layer_information_color(item) is True:
                self.update_color()
        elif isinstance(o_item, CGPinItem) is True:
            pass

    def action_EditColor(self):

        o_layer = self.get_current_layer()

        if o_layer is not None:
            if edit_layer_information_color(o_layer) is True:
                self.update_color()


# ============================================================================
def edit_layer_information_color(o_layer):

    o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)

    o_dlg = QtWidgets.QColorDialog()
    o_dlg.setCurrentColor(o_layer_info.m_o_color)

    if o_dlg.exec() == QtWidgets.QDialog.Accepted:

        o_layer_info.set_color(o_dlg.selectedColor())

        o_layer.setBackground(0, o_layer_info.m_brush)

        return True

    else:
        return False



# [EOF]
