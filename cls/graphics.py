# -*- coding: utf-8 -*-
"""
    @brief グラフィックス表示部
    @author MizunagiKB
"""
# ------------------------------------------------------------------ import(s)
from PyQt5 import QtCore, QtGui, QtWidgets

import cls.graphics_item


# ----------------------------------------------------------------------------
class CGView(QtWidgets.QGraphicsView):
    """
    """

    def __init__(self, parent):
        """コンストラクタ
        """

        super(CGView, self).__init__()

        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.AnchorUnderMouse
        )

        self.setViewportUpdateMode(
            QtWidgets.QGraphicsView.FullViewportUpdate
        )

        self.m_o_gitem = cls.graphics_item.CGWatershedItem(parent)

        o_gscene = QtWidgets.QGraphicsScene()
        o_gscene.addItem(self.m_o_gitem)

        self.setScene(o_gscene)

        o_pixmap = QtGui.QPixmap(32, 32)
        o_pixmap.fill(QtGui.QColor(31, 37, 43))

        self.setBackgroundBrush(QtGui.QBrush(o_pixmap))

    def keyPressEvent(self, event):
        super(CGView, self).keyPressEvent(event)

        if event.key() == 0x20:
            self.m_o_gitem.m_b_dragging = True
            self.setDragMode(
                QtWidgets.QGraphicsView.ScrollHandDrag
            )
        elif event.key() == 0x1000003:
            list_gitem = [gitem for gitem in self.m_o_gitem.iter_selected_pin()]
            for gitem in list_gitem:
                self.m_o_gitem.remove_pin(gitem)
                self.m_o_gitem.update_pin()

    def keyReleaseEvent(self, event):
        super(CGView, self).keyReleaseEvent(event)

        self.setDragMode(
            QtWidgets.QGraphicsView.NoDrag
        )
        self.m_o_gitem.m_b_dragging = False

    def wheelEvent(self, event):
        """ホイール操作による拡大縮小処理
        """

        f_value = 0
        f_value += event.angleDelta().x()
        f_value += event.angleDelta().y()
        f_factor = pow(1.2, f_value / 240.0)
        self.scale(f_factor, f_factor)



# [EOF]
