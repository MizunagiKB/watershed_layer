# -*- coding: utf-8 -*-
"""
"""
# ------------------------------------------------------------------ import(s)
import sys
import os
import unittest
import tempfile


# ------------------------------------------------------------------- class(s)
class CTest(unittest.TestCase):
    """
    """
    VALID_IMAGE = "utest/test_ffffff.png"
    INVALID_IMAGE = "utest/test_ffffff.err"

    # ------------------------------------------------------------------------
    def test_class(self):
        import graphics.cv_image

        o_cv = graphics.cv_image.CCVFilter()

        self.assertTrue(isinstance(o_cv, graphics.cv_image.CCVFilter))

    # ------------------------------------------------------------------------
    def test_load(self):
        import graphics.cv_image

        self.assertIsNotNone(
            graphics.cv_image.load(os.path.join(os.getcwd(), VALID_IMAGE))
        )

        self.assertIsNone(
            graphics.cv_image.load(os.path.join(os.getcwd(), INVALID_IMAGE))
        )

    # ------------------------------------------------------------------------
    def test_save(self):
        import graphics.cv_image

        cvimage = graphics.cv_image.load(os.path.join(os.getcwd(), VALID_IMAGE))

        self.assertTrue(
            graphics.cv_image.save(os.path.join(os.getcwd(), "utest/save.png"), cvimage)
        )

        self.assertFalse(
            graphics.cv_image.save(os.path.join(os.getcwd(), "utest/save.png"), None)
        )

    # ------------------------------------------------------------------------
    def test_attach(self):
        import graphics.cv_image

        o_cv = graphics.cv_image.CCVFilter()

        cvimage = graphics.cv_image.load(os.path.join(os.getcwd(), VALID_IMAGE))

        self.assertTrue(o_cv.attach(cvimage))


if __name__ == "__main__":

    dirpath = os.path.abspath(os.getcwd())

    if dirpath not in sys.path:
        sys.path.append(dirpath)

    unittest.main()



# [EOF]
