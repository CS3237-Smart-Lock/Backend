import os
import sqlite3

DB_PATH = os.path.join('.', 'db', 'database')
DB_INIT_SCRIPT_PATH = os.path.join('db', 'init_db.sql')

if os.path.exists(DB_PATH):
    ans = input("Database already exists, remove? [y/n] ")
    if ans.lower() == 'y':
        os.remove(DB_PATH)
    else:
        exit(0)

with open(DB_PATH, 'w') as f:
    pass

connection = sqlite3.connect(DB_PATH)

with open(DB_INIT_SCRIPT_PATH) as f:
    query = f.read()

cursor = connection.cursor()
try:
    cursor.execute(query)
    connection.commit()
finally:
    if cursor:
        cursor.close()
