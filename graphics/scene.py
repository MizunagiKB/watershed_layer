# -*- coding: utf-8 -*-
"""
    @brief グラフィックス表示部
    @author MizunagiKB
"""
# ------------------------------------------------------------------ import(s)
import os

from PyQt5 import QtWidgets


# ------------------------------------------------------------------- class(s)
class CGScene(QtWidgets.QGraphicsScene):
    """ """

    def __init__(self, parent):
        """コンストラクタ"""

        super(CGScene, self).__init__(parent)

    def dragEnterEvent(self, event):
        """
        Args:
            event (QDragEnterEvent):
        """

        if event.mimeData().hasFormat("text/uri-list") is True:
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list") is True:
            event.acceptProposedAction()

    def dropEvent(self, event):
        """
        Args:
            event (QDropEvent):
        """

        if event.mimeData().hasFormat("text/uri-list") is True:
            for o_url in event.mimeData().urls():
                pathname = o_url.toLocalFile()
                _, ext = os.path.splitext(pathname)
                if ext.lower() in (".png", ".jpg", ".jpeg"):
                    self.parent().m_gwatershed.import_picture(pathname)
                    event.acceptProposedAction()
                    break
