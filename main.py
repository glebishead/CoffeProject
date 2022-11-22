import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from sqlite3 import OperationalError


class AdapterDB:
	def __init__(self, name_db):
		self.name_db = name_db
		try:
			self.connection = sqlite3.connect(self.name_db)
			self.cur = self.connection.cursor()
		except OperationalError:
			pass
	
	def close_db(self):
		self.connection.close()


class TableModel(QAbstractTableModel):
	def __init__(self, data):
		super(TableModel, self).__init__()
		self._data = data
	
	def columnCount(self, parent=QModelIndex()):
		return len(max(self._data, key=len))
	
	def rowCount(self, parent=QModelIndex()):
		return len(self._data)
	
	def data(self, index=QModelIndex, role=Qt.DisplayRole):
		if role == Qt.DisplayRole:
			try:
				return self._data[index.row()][index.column()]
			except IndexError:
				return ''


class CoffeShowingWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		loadUi('main.ui', self)
		self.setFixedSize(self.size())
		self.adapter = AdapterDB('coffe.db')
		self.table_info = self.adapter.cur.execute('select * from types').fetchall()
		self.model = TableModel(self.table_info)
		self.tableView.setModel(self.model)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = CoffeShowingWindow()
	ex.show()
	sys.exit(app.exec_())