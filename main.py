import sqlite3
from db import init_db as db

db_name = 'CarSharingDB.db'
conn = None


def create_tables():
    """
        creates schema of all tables with empty rows
    """
    try:
        __check_connector()
        db.create_tables(connector=conn)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def drop_database():
    """
        deletes database file from disk
    """
    try:
        cr_connector = sqlite3.connect(db_name)
        db.drop_database(db_name=db_name)
        cr_connector.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def close():
    """
        commits connection results and closes it
    """
    global conn
    if (conn != None):
        conn.commit()
        conn.close()
        conn = None


def __check_connector():
    """
        initiate connection if it None
    """
    global conn
    if (conn == None):
        try:
            conn = sqlite3.connect(database=db_name)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])


def refresh_db():
    """
        drop database and create all from zero, also fill it with sample data
    """
    try:
        drop_database()
        __check_connector()
        create_tables()
        db.fill_all(conn.cursor())
        conn.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def execute(query: str):
    """
        execute user defined command
    """
    __check_connector()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        for i in cursor:
            print(i)
        print("Execution succeed")
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


if __name__ == "__main__":
    try:
        refresh_db()  # TODO: remove this command
        # create connection
        __check_connector()
        # check tables existence
        if not db.check_tables_existance(conn.cursor()):
            create_tables()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
