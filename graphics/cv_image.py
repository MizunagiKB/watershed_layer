# -*- coding: utf-8 -*-
"""
    @brief OpenCV3のラッパークラス
    @author MizunagiKB
"""
# ------------------------------------------------------------------ import(s)
import cv2
import numpy


# ------------------------------------------------------------------- class(s)
# ----------------------------------------------------------------------------
class CCVFilter(object):
    """OpenCV3のWatershed処理クラス
    """

    def __init__(self):
        """コンストラクタ
        """

        self.m_cvimage = None
        self.m_cvimage_mark = None
        self.m_ary_color = numpy.int32(
            list(numpy.ndindex(2, 2, 2))
        ) * 255

    # ------------------------------------------------------------------------
    def attach(self, cvimage):
        """画像の割り当て

        Args:
            cvimage (ndarray):
                ndarray形式で読み込まれた画像ファイル

        Returns:
            bool
        """

        if isinstance(cvimage, numpy.ndarray) is not True:
            self.m_cvimage = None
            self.m_cvimage_mark = None
            return False
        else:
            self.m_cvimage = cvimage
            self.m_cvimage_mark = None
            self.marker_clear()
            return True

    # ------------------------------------------------------------------------
    def marker_clear(self):
        """Watershedマーカーの初期化
        """

        if self.m_cvimage is not None:
            self.m_cvimage_mark = numpy.zeros(
                self.m_cvimage.shape[0:2],
                numpy.int32
            )

    # ------------------------------------------------------------------------
    def update_ary_color(self, list_color):
        """カラーリストの更新処理
        """

        list_ndarray = [
            numpy.array([col.blue(), col.green(), col.red()]) for col in list_color
        ]
        self.m_ary_color = numpy.int32(list_ndarray)

    # ------------------------------------------------------------------------
    def marker_set(self, xpos, ypos, marker_index):
        """Watershed用のマーカーをセット

        Args:
            nx (int):
            ny (int):
            maker_index (int):

        Returns:
            None:
        """

        cv2.rectangle(
            self.m_cvimage_mark,
            (int(xpos) - 1, int(ypos) - 1),
            (int(xpos) + 1, int(ypos) + 1),
            marker_index
        )

    # ------------------------------------------------------------------------
    def watershed(self, alpha):
        """Watershedアルゴリズムの適用

        Args:
        Returns:
            cv2::image
        """
        if self.m_cvimage is None:

            return None

        else:

            cvimage_mark = self.m_cvimage_mark.copy()
            cv2.watershed(self.m_cvimage, cvimage_mark)
            cvimage_overlay = self.m_ary_color[numpy.maximum(cvimage_mark, 0)]

            alpha_1 = alpha
            alpha_2 = 1.0 - alpha

            cvimage_result = cv2.addWeighted(
                self.m_cvimage,
                alpha_1,
                cvimage_overlay,
                alpha_2,
                0.0,
                dtype=cv2.CV_8UC3
            )

            return cvimage_result


# ============================================================================
def load(pathname):
    """画像の読み込み

    Args:
        pathname (str):
            画像ファイルのフルパス

    Returns:
        bool
    """

    cvimage = cv2.imread(pathname)

    return cvimage


# ============================================================================
def save(pathname, cvimage):
    return cv2.imwrite(pathname, cvimage)


# ============================================================================
def colororder_bgr_to_rgb(cvimage):

    tpl_cvimage = cv2.split(cvimage)
    result_cvimage = cv2.merge(
        (tpl_cvimage[2], tpl_cvimage[1], tpl_cvimage[0])
    )

    return result_cvimage


if __name__ == "__main__":
    pass



# [EOF]
