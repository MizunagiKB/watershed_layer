# -*- coding: utf-8 -*-
"""
    @brief OpenCV3のラッパークラス
    @author MizunagiKB
"""
import cv2
import numpy


# ----------------------------------------------------------------------------
class CCVWatershed(object):
    """画像管理クラス
    """

    def __init__(self):
        """コンストラクタ
        """

        self.m_cvimage = None
        self.m_size = (0, 0)
        self.m_cvimage_maker = None
        self.m_narray_color = None


        self.m_narray_color = numpy.int32(
            list(numpy.ndindex(2, 2, 2)) * 2
        ) * 255

    def set_color_list(self, list_color):
        list_ndarray = [
            numpy.array([col.blue(), col.green(), col.red()]) for col in list_color
        ]
        self.m_narray_color = numpy.int32(list_ndarray)

    def load(self, image_pathname):
        """画像の読み込み

        Args:
            image_pathname (str):
                画像ファイルのフルパス

        Returns:
            None:
        """

        self.m_cvimage = cv2.imread(image_pathname)
        self.m_size = (
            self.m_cvimage.shape[1],
            self.m_cvimage.shape[0]
        )

        self.marker_clr()

    def save(self, image_pathname, cvimage):
        cv2.imwrite(image_pathname, cvimage)

    def marker_clr(self):
        """マーカー情報のリセット
        """

        if self.m_cvimage is not None:
            self.m_cvimage_maker = numpy.zeros(
                (self.m_size[1], self.m_size[0]),
                numpy.int32
            )

    def marker_set(self, nx, ny, marker_index):
        """Watershed用のマーカーをセット

        Args:
            nx (int):
            ny (int):
            maker_index (int):

        Returns:
            None:
        """

        cv2.rectangle(
            self.m_cvimage_maker,
            (int(nx) - 1, int(ny) - 1),
            (int(nx) + 1, int(ny) + 1),
            marker_index
        )

    def watershed(self, alpha):
        """Watershedアルゴリズムの適用

        Args:
        Returns:
            cv2::image
        """
        if self.m_cvimage is None:

            return None

        else:

            cvimage_maker = self.m_cvimage_maker.copy()
            cv2.watershed(self.m_cvimage, cvimage_maker)
            cvimage_overlay = self.m_narray_color[numpy.maximum(cvimage_maker, 0)]

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
def colororder_bgr_to_rgb(cvimage):

    tpl_cvimage = cv2.split(cvimage)
    result_cvimage = cv2.merge(
        (tpl_cvimage[2], tpl_cvimage[1], tpl_cvimage[0])
    )

    return result_cvimage


if __name__ == "__main__":
    pass



# [EOF]
