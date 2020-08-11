import sys  # sys нужен для передачи argv в QApplication
import MySQLdb as mdb
from PyQt5 import QtWidgets, QtGui, QtCore

import design

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
    
        self.db = mdb.connect('localhost', 'login', 'password')
        self.cur = self.db.cursor()
        self.cur.execute("CREATE DATABASE IF NOT EXISTS wishapp;")
        self.cur.execute("USE wishapp;")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Wishlists (wishlist_id INT PRIMARY KEY AUTO_INCREMENT, wishlist_name TEXT);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Wishes (wish_id INT PRIMARY KEY AUTO_INCREMENT, wishlists_id INT, name TEXT, cost INT, link TEXT, notes TEXT, FOREIGN KEY (wishlists_id) REFERENCES wishlists (wishlist_id));")
        self.cur.execute("USE wishapp;")
        
        self.setupUi(self)
        self.menubar.triggered[QtWidgets.QAction].connect(self.create_new_wishlist_func)
        

    def create_new_wishlist_func(self, q):

        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter your wishlist name:')

        if ok:
            query = "INSERT INTO wishapp.Wishlists (wishlist_name) VALUES ('%s');" % text
            self.cur.execute(query)
            self.db.commit()

            self.activateTable(self)
            self.setTextToWishlistTable(self, text)

def main():
    
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
