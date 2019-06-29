from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class DnD_GUI(QtWidgets.QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
	
		self.parent = parent
