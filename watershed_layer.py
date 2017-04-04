# -*- coding: utf-8 -*-
"""
    @brief Watershedによる領域分割画像の生成アプリ
    @author MizunagiKB
"""
import sys

from PyQt5 import Qt, QtWidgets

import cls.graphics
import ui_main_window


# ----------------------------------------------------------------------------
class CMainWindow(QtWidgets.QMainWindow):
    """メインウインドウクラス
    """

    def __init__(self):
        """コンストラクタ
        """

        super(CMainWindow, self).__init__()

        self.uiface = ui_main_window.Ui_MainWindow()
        self.uiface.setupUi(self)

        self.m_o_view = cls.graphics.CGView(self)

        self.setCentralWidget(self.m_o_view)


# ============================================================================
def main():
    """Program Entry
    """

    o_app = QtWidgets.QApplication(sys.argv)

    o_main_window = CMainWindow()
    o_main_window.show()

    return o_app.exec_()


if __name__ == "__main__":
    main()
