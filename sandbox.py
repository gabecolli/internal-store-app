import sqlite3

userdb = sqlite3.connect("user.db")

user_cursor = userdb.cursor()

#comment added to confirm pull request is working