#! /usr/bin/env python

"""
LHGUI is Copyright (c) 2017  John Thornton <jt@gnipsel.com>

LHGUI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

Touchy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

to build the python file from the ui file
pyuic4 -i 0 -o lh_gui.py lh_gui.ui
"""

import sys, subprocess
from PyQt4 import QtGui
from lh_gui4 import Ui_lh_gui

class LHGUI(Ui_lh_gui):
	def __init__(self, dialog):
		Ui_lh_gui.__init__(self)
		self.setupUi(dialog)

		self.run_lh.clicked.connect(self.runLatencyHisogram)

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
		dialog.hide()
		subprocess.call(cmd, shell=True)
		dialog.show()
		#subprocess.call('latency-histogram --nobase --logscale 0', shell=True)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	dialog = QtGui.QDialog()

	prog = LHGUI(dialog)

	dialog.show()
	sys.exit(app.exec_())

"""
   latency-histogram [Options]

Options:
  --base      nS   (base  thread interval, default:   25000, min:  5000)
  --servo     nS   (servo thread interval, default: 1000000, min: 25000)
  --bbinsize  nS   (base  bin size,  default: 100
  --sbinsize  nS   (servo bin size, default: 100
  --bbins     n    (base  bins, default: 200
  --sbins     n    (servo bins, default: 200
  --logscale  0|1  (y axis log scale, default: 1)
  --text      note (additional note, default: "" )
  --show           (show count of undisplayed bins)
  --nobase         (servo thread only)
  --verbose        (progress and debug)

Notes:
  Linuxcnc and Hal should not be running, stop with halrun -U.
  Large number of bins and/or small binsizes will slow updates.
  For single thread, specify --nobase (and options for servo thread).
  Measured latencies outside of the +/- bin range are reported
  with special end bars.  Use --show to show count for
  the off-chart [pos|neg] bin
"""
