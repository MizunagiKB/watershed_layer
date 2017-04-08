# -*- coding: utf-8 -*-
"""
    @brief グラフィックス表示部
    @author MizunagiKB
"""
# ------------------------------------------------------------------ import(s)
import os

from PyQt5 import QtCore, QtGui, QtWidgets

import graphics.graphics_item
import graphics.scene


# ----------------------------------------------------------------------------
class CGView(QtWidgets.QGraphicsView):
    """
    """

    # ------------------------------------------------------------------------
    def __init__(self, parent):
        """コンストラクタ
        """

        super(CGView, self).__init__()

        self.setAcceptDrops(True)

        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.AnchorUnderMouse
        )

        self.setViewportUpdateMode(
            QtWidgets.QGraphicsView.FullViewportUpdate
        )

        self.setInteractive(True)

        self.m_gwatershed = graphics.graphics_item.CGWatershedItem(parent)

        o_gscene = graphics.scene.CGScene(self)
        o_gscene.addItem(self.m_gwatershed)

        self.setScene(o_gscene)

        o_pixmap = QtGui.QPixmap(32, 32)
        o_pixmap.fill(QtGui.QColor(31, 37, 43))

        self.setBackgroundBrush(QtGui.QBrush(o_pixmap))

    # ------------------------------------------------------------------------
    def keyPressEvent(self, event):
        """
        Args:
            event (QKeyEvent):
        """

        super(CGView, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Space:
            self.m_gwatershed.m_b_dragging = True
            self.setDragMode(
                QtWidgets.QGraphicsView.ScrollHandDrag
            )
        elif event.key() in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
            list_gitem = [gitem for gitem in self.m_gwatershed.iter_selected_pin()]
            for gitem in list_gitem:
                self.m_gwatershed.remove_pin(gitem)
                self.m_gwatershed.update_pin()

    # ------------------------------------------------------------------------
    def keyReleaseEvent(self, event):
        """
        Args:
            event (QKeyEvent):
        """

        super(CGView, self).keyReleaseEvent(event)

        self.setDragMode(
            QtWidgets.QGraphicsView.NoDrag
        )
        self.m_gwatershed.m_b_dragging = False

    # ------------------------------------------------------------------------
    def wheelEvent(self, event):
        """ホイール操作による拡大縮小処理

        Args:
            event (QWheelEvent):
        """

        f_value = 0
        f_value += event.angleDelta().x()
        f_value += event.angleDelta().y()
        f_factor = pow(1.2, f_value / 240.0)
        self.scale(f_factor, f_factor)



# [EOF]
