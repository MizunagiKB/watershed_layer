# -*- coding: utf-8 -*-
"""
    @brief Watershedによる領域分割画像の生成アプリ
    @author MizunagiKB
"""
# ------------------------------------------------------------------ import(s)
import sys

from PyQt5 import QtWidgets

import graphics.view
import ui_main_window


# ------------------------------------------------------------------- class(s)
class CMainWindow(QtWidgets.QMainWindow):
    """メインウインドウクラス"""

    def __init__(self):
        """コンストラクタ"""

        super(CMainWindow, self).__init__()

        self.m_uiface = ui_main_window.Ui_MainWindow()
        self.m_uiface.setupUi(self)

        self.m_gview = graphics.view.CGView(self)

        self.setCentralWidget(self.m_gview)


# -------------------------------------------------------------------- main(s)
def main():
    """Program Entry"""

    o_app = QtWidgets.QApplication(sys.argv)

    o_main_window = CMainWindow()
    o_main_window.show()

    return o_app.exec_()


if __name__ == "__main__":
    main()
