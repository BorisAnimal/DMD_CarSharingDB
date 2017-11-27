import sqlite3
from db import init_db

db_name = 'CarSharingDB.db'
conn = None


def create_tables():
    __check_connector()
    init_db.create_tables(connector=conn)


def drop_database():
    cr_connector = sqlite3.connect(db_name)
    init_db.drop_database(db_name=db_name)
    cr_connector.close()


def close():
    if (conn != None):
        conn.close()


def __check_connector():
    global conn
    if (conn == None):
        conn = sqlite3.connect(database=db_name)


def main():
    drop_database()
    __check_connector()
    create_tables()
    init_db.fill_all(conn.cursor())
    conn.commit()

    close()
