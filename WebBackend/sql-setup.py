import os
import sqlite3

SQLFILENAME = "setup.sql"
DATABASE_NAME = "users.db"

# Delete existing database file
if os.path.exists(DATABASE_NAME):
    os.remove(DATABASE_NAME)

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()


def run_sql_script():
    with open(SQLFILENAME, 'r') as sql_file:
        a = sql_file.read()

    cursor.executescript(a)

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    run_sql_script()
