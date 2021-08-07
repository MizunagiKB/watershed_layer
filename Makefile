#
#	Makefile for PyQt5
#	@Author: @MizunagiKB
#
PYTHON		= python
PYINSTALLER	= pyinstaller
PYUIC		= pyuic5
PYRCC		= pyrcc5

.PHONY: all
all: PYUIC PYRCC

PYUIC: ui_main_window.py
PYRCC: resource_rc.py

ui_main_window.py: ui_main_window.ui
	$(PYUIC) $< -o $@

resource_rc.py: resource.qrc
	$(PYRCC) $< -o $@

test:
	$(PYTHON) utest/test_cv_image.py

.PHONY: run build
build:
	$(PYINSTALLER) --noconsole --onefile watershed_layer.py

run: PYUIC PYRCC
	$(PYTHON) watershed_layer.py
