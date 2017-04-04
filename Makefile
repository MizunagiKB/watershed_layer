#
#	Makefile for PyQt5
#	@Author: @MizunagiKB
#
PYTHON = python
PYUIC = pyuic5
PYRCC = pyrcc5

.PHONY: all
all: PYUIC PYRCC

PYUIC: ui_main_window.py
PYRCC: resource_rc.py

ui_main_window.py: ui_main_window.ui
	$(PYUIC) $< -o $@

resource_rc.py: resource.qrc
	$(PYRCC) $< -o $@

.PHONY: run
run: PYUIC PYRCC
	$(PYTHON) watershed_layer.py
