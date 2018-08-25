#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, subprocess
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QDialog)

class App(QDialog):
	def __init__(self):
		super(App, self).__init__()
		uic.loadUi("lh_gui.ui", self)
		self.run_lh.clicked.connect(self.runLatencyHisogram)

		self.show()

	def runLatencyHisogram(self):
		cmd = 'latency-histogram '
		if self.showBase.isChecked():
			cmd += '--base {} '.format(self.baseThreadInterval.value())
			cmd += '--bbinsize {} '.format(self.baseBinSize.value())
			cmd += '--bbins {} '.format(self.baseBins.value())
		else:
			cmd += '--nobase '
		cmd += '--servo {} '.format(self.servoThreadInterval.value())
		cmd += '--sbinsize {} '.format(self.servoBinSize.value())
		cmd += '--sbins {} '.format(self.servoBins.value())
		if self.logscaleX.isChecked():
			cmd += '--logscale 0 '
		if len(self.showText.displayText()) > 0:
			cmd += '--text "{}"'.format(self.showText.displayText())
		if self.showNotDisplayedBins.isChecked():
			cmd += '--show'
		self.hide()
		subprocess.call(cmd, shell=True)
		self.show()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
