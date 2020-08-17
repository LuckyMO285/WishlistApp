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

        self.action_Create.triggered.connect(self.create_new_wishlist_func)
        self.action_Load.triggered.connect(self.load_block)

        self.add_pushButton.clicked.connect(self.add_block)
        self.edit_pushButton.clicked.connect(self.edit_block)

    def create_new_wishlist_func(self):

        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter your wishlist name:')

        wishlist_name_unique_query = "SELECT EXISTS (SELECT 1 FROM wishapp.Wishlists WHERE wishlist_name = '%s');" % text
        self.cur.execute(wishlist_name_unique_query)
        wishlist_name_unique = self.cur.fetchone()[0] # 1 - if already in db, 0 - if not
        
        if wishlist_name_unique:
            self.error_dialog = QtWidgets.QMessageBox()
            self.error_dialog.setText("Wishlist already existing.")
            self.error_dialog.exec()
        else:       
            if ok:
                query = "INSERT INTO wishapp.Wishlists (wishlist_name) VALUES ('%s');" % text
                self.current_wishlist_ID = self.cur.execute(query)
                self.db.commit()

                self.current_wishlist_ID = (self.cur.lastrowid)
                self.db.commit()

                self.activateTable(self)
                self.setTextToWishlistTable(self, text)

    def wishlist_ok_func(self):
        self.wishlist_dialog.done(1)

    def add_block(self):
        self.dialog = AddDialog()
        self.dialog.clicked_ok.connect(self.add_block_ok_func)
        self.dialog.clicked_cancel.connect(self.cancel_func)
        self.dialog.exec()

    def add_block_ok_func(self):
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

            select_query = "SELECT wish_id, name, cost, link, notes FROM wishapp.wishes WHERE wishlists_id = %s;" % self.current_wishlist_ID
            self.cur.execute(select_query)
            result = self.cur.fetchall()
            self.printToTable(self, result)

            self.cancel_func()

    def load_block(self):

        select_query = "SELECT wishlist_name FROM wishapp.Wishlists;"
        self.cur.execute(select_query)
        result = list(self.cur.fetchall())
        flatten_result = [item for sublist in result for item in sublist]
        
        if not flatten_result:
            self.error_dialog = QtWidgets.QMessageBox()
            self.error_dialog.setText("No wishlists.")
            self.error_dialog.exec()
        else:
            self.dialog = LoadDialog(flatten_result)
            self.dialog.clicked_ok.connect(self.load_block_ok_func)
            self.dialog.clicked_cancel.connect(self.cancel_func)
            self.dialog.exec()

    def load_block_ok_func(self):
        wl_name = str(self.dialog.combo.currentText())

        id_query = "SELECT wishlist_id FROM wishapp.Wishlists WHERE wishlist_name='%s';" % wl_name
        self.cur.execute(id_query)
        self.current_wishlist_ID = self.cur.fetchone()[0]
        
        select_query = "SELECT wish_id, name, cost, link, notes FROM wishapp.Wishes WHERE wishlists_id=%s;" % self.current_wishlist_ID
        self.cur.execute(select_query)
        result = list(self.cur.fetchall())

        self.activateTable(self)
        self.printToTable(self, result)
        self.cancel_func()

    def edit_block(self):

        row = self.tableWidget.currentItem().row()

        self.row_id = self.tableWidget.item(row, 0).text()
        orig_name = self.tableWidget.item(row, 1).text()
        orig_cost = self.tableWidget.item(row, 2).text()
        orig_link = self.tableWidget.item(row, 3).text()
        orig_notes = self.tableWidget.item(row, 4).text()
        
        self.dialog = EditDialog(orig_name, orig_cost, orig_link, orig_notes)
        self.dialog.clicked_ok.connect(self.edit_block_ok_func)
        self.dialog.clicked_cancel.connect(self.cancel_func)
        self.dialog.exec()

    def edit_block_ok_func(self):
        
        cur_name = self.dialog.nameLineEdit.text()
        cur_cost = self.dialog.costLineEdit.text()
        cur_link = self.dialog.linkLineEdit.text()
        cur_notes = self.dialog.notesLineEdit.text()

        try:
            cur_cost = float(cur_cost)
        except ValueError:
            pass
        
        if cur_name and cur_link and cur_notes and isinstance(cur_cost, float) :
            query = "UPDATE wishapp.Wishes SET name='%s', cost=%s, link='%s', notes='%s' WHERE wish_id=%s;" % (cur_name, cur_cost, cur_link, cur_notes, self.row_id)
            print(query)
            self.cur.execute(query)
            self.db.commit()

            select_query = "SELECT wish_id, name, cost, link, notes FROM wishapp.wishes WHERE wishlists_id = %s;" % self.current_wishlist_ID
            self.cur.execute(select_query)
            result = self.cur.fetchall()
            self.printToTable(self, result)

            self.cancel_func()

        #query = "UPDATE wishapp.Wishes SET cost=11 WHERE wish_id=1;"
        

    def cancel_func(self):
        self.dialog.done(1)

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

class LoadDialog(QtWidgets.QDialog):
    clicked_ok = QtCore.pyqtSignal()
    clicked_cancel = QtCore.pyqtSignal()

    def __init__(self, wishlists_names, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 200)
        self.nameLabel = QtWidgets.QLabel("Wishlist_name")

        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItems(wishlists_names)

        self.load_buttonBox = QtWidgets.QDialogButtonBox()
        self.load_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        
        self.load_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.clicked_ok)
        self.load_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.clicked_cancel)

        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self.nameLabel, *(0, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.combo, *(0, 1), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        lay.addWidget(self.load_buttonBox, 1, 0, 1, 2, QtCore.Qt.AlignHCenter)

class EditDialog(QtWidgets.QDialog):
    clicked_ok = QtCore.pyqtSignal()
    clicked_cancel = QtCore.pyqtSignal()

    def __init__(self, c_name, c_cost, c_link, c_notes, parent=None):
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

        self.nameLineEdit.setText(c_name)
        self.costLineEdit.setText(c_cost)
        self.linkLineEdit.setText(c_link)
        self.notesLineEdit.setText(c_notes)

        self.edit_buttonBox = QtWidgets.QDialogButtonBox()
        self.edit_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        
        self.edit_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.clicked_ok)
        self.edit_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.clicked_cancel)

        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self.nameLabel, *(0, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.costLabel, *(1, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.linkLabel, *(2, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lay.addWidget(self.notesLabel, *(3, 0), QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        
        lay.addWidget(self.nameLineEdit, *(0, 1))
        lay.addWidget(self.costLineEdit, *(1, 1))
        lay.addWidget(self.linkLineEdit, *(2, 1))
        lay.addWidget(self.notesLineEdit, *(3, 1))

        lay.addWidget(self.edit_buttonBox, 4, 0, 1, 2, QtCore.Qt.AlignHCenter)


def main():
    
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
