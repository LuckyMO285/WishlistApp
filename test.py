import MySQLdb as mdb
import sys

try:
    db = mdb.connect('localhost', 'root', 'MySQLPassword1')

    with db:
        cur = db.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS wishapp;")
        cur.execute("USE wishapp;")
        cur.execute("CREATE TABLE Wishlists (wishlist_id INT PRIMARY KEY AUTO_INCREMENT, wishlist_name TEXT);")
        print('here')
        cur.execute("CREATE TABLE Wishes (wish_id INT PRIMARY KEY AUTO_INCREMENT, wishlists_id INT, name TEXT, cost INT, link TEXT, notes TEXT, FOREIGN KEY (wishlists_id) REFERENCES wishlists (wishlist_id));")
    print('Success')
except mdb.Error as e:
    print('Failed')
    sys.exit(1)
