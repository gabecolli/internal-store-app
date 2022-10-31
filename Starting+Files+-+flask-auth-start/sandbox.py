import sqlite3

userdb = sqlite3.connect("user.db")

user_cursor = userdb.cursor()