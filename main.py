import sys  # sys нужен для передачи argv в QApplication
import MySQLdb as mdb
from PyQt5 import QtWidgets, QtGui, QtCore

import design

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
    
        self.db = mdb.connect('localhost', user, password)
        self.cur = self.db.cursor()
        self.cur.execute("CREATE DATABASE IF NOT EXISTS wishapp;")
        self.cur.execute("USE wishapp;")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Wishlists (wishlist_id INT PRIMARY KEY AUTO_INCREMENT, wishlist_name TEXT);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Wishes (wish_id INT PRIMARY KEY AUTO_INCREMENT, wishlists_id INT, name TEXT, cost FLOAT, link TEXT, notes TEXT, FOREIGN KEY (wishlists_id) REFERENCES wishlists (wishlist_id));")
        self.cur.execute("USE wishapp;")

        self.current_wishlist_ID = -1
        
        self.setupUi(self)
        self.menubar.triggered[QtWidgets.QAction].connect(self.create_new_wishlist_func)

        self.add_pushButton.clicked.connect(self.add_values)

    def create_new_wishlist_func(self):

        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter your wishlist name:')

        wishlist_name_unique_query = "SELECT EXISTS (SELECT 1 FROM wishapp.Wishlists WHERE wishlist_name = '%s');" % text
        self.cur.execute(wishlist_name_unique_query)
        wishlist_name_unique = self.cur.fetchone()[0] # 1 - if already in db, 0 - if not
        
        if wishlist_name_unique:
            self.wishlist_dialog = AlreadyExistingWishlistDialog()
            self.wishlist_dialog.clicked.connect(self.wishlist_ok_func)
            self.wishlist_dialog.exec()
        else:       
            if ok:
                query = "INSERT INTO wishapp.Wishlists (wishlist_name) VALUES ('%s');" % text
                self.current_wishlist_ID = self.cur.execute(query)
                self.db.commit()

                self.current_wishlist_ID = (self.cur.lastrowid)
                self.db.commit()

                self.activateTable(self)
                self.setTextToWishlistTable(self, text)

    def add_values(self):
        self.dialog = AddDialog()
        self.dialog.clicked_ok.connect(self.ok_func)
        self.dialog.clicked_cancel.connect(self.cancel_func)
        self.dialog.exec()

    def ok_func(self):
        cur_name = self.dialog.nameLineEdit.text()
        cur_cost = self.dialog.costLineEdit.text()
        cur_link = self.dialog.linkLineEdit.text()
        cur_notes = self.dialog.notesLineEdit.text()

        try:
            cur_cost = float(cur_cost)
        except ValueError:
            pass
        
        if cur_name and cur_link and cur_notes and isinstance(cur_cost, float) :
            query = "INSERT INTO wishapp.Wishes (wishlists_id, name, cost, link, notes) VALUES (%s, '%s', %s, '%s', '%s');" % (self.current_wishlist_ID, cur_name, cur_cost, cur_link, cur_notes)
            self.cur.execute(query)
            self.db.commit()

            select_query = "SELECT name, cost, link, notes FROM wishapp.wishes WHERE wishlists_id = %s;" % self.current_wishlist_ID
            self.cur.execute(select_query)
            result = self.cur.fetchall()
            self.printToTable(self, result)

            self.cancel_func()

    def wishlist_ok_func(self):
        self.wishlist_dialog.done(1)

    def cancel_func(self):
        self.dialog.done(1)

class AlreadyExistingWishlistDialog(QtWidgets.QDialog):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 200)
        self.messageLabel = QtWidgets.QLabel("Wishlist already existing")
        
        self.okButton = QtWidgets.QPushButton("OK")
        self.okButton.clicked.connect(self.clicked)

        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self.messageLabel, *(0, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.okButton, *(1, 0), QtCore.Qt.AlignHCenter)

class AddDialog(QtWidgets.QDialog):
    clicked_ok = QtCore.pyqtSignal()
    clicked_cancel = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 200)
        self.nameLabel = QtWidgets.QLabel("Name")
        self.costLabel = QtWidgets.QLabel("Cost")
        self.linkLabel = QtWidgets.QLabel("Link")
        self.notesLabel = QtWidgets.QLabel("Notes")

        self.nameLineEdit = QtWidgets.QLineEdit()
        self.costLineEdit = QtWidgets.QLineEdit()
        self.linkLineEdit = QtWidgets.QLineEdit()
        self.notesLineEdit = QtWidgets.QLineEdit()

        self.add_buttonBox = QtWidgets.QDialogButtonBox()
        self.add_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        
        self.add_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.clicked_ok)
        self.add_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.clicked_cancel)

        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self.nameLabel, *(0, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.costLabel, *(1, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.linkLabel, *(2, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.notesLabel, *(3, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        lay.addWidget(self.nameLineEdit, *(0, 1))
        lay.addWidget(self.costLineEdit, *(1, 1))
        lay.addWidget(self.linkLineEdit, *(2, 1))
        lay.addWidget(self.notesLineEdit, *(3, 1))

        lay.addWidget(self.add_buttonBox, 4, 0, 1, 2, QtCore.Qt.AlignHCenter)

def main():
    
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
