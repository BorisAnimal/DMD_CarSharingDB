import sqlite3
from db import init_db as db
from db import queries_from_task as ex

db_name = 'CarSharingDB.db'
conn = None


def exercise(number):
    exercises = [
        ex.ex_1,
        ex.ex_2,
        ex.ex_3,
        ex.ex_4,
        ex.ex_5,
        ex.ex_6,
        # ex.ex_7,
        # ex.ex_8,
    ]
    print("\nQuery #{} requested. Execution result:".format(number))
    if (number < 1 or number > 8):
        print("""Tricky input detected. There is no such exercise ({}) in our assignment :3 \nTry range [1..{}]"""
              .format(number,len(exercises)))
    else:
        try:
            if (number > len(exercises)):
                print("We do not this exercise :3 \nTry range [1..{}]".format(len(exercises)))
            else:
                print(exercises[number - 1](conn.cursor()))
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])


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


def fill_tables_with_random_data():
    try:
        __check_connector()
        db.fill_all_tables(conn.cursor())
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def execute(query):
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


def refresh_db():
    """
        drop database and create all from zero, also fill it with sample data
    """
    try:
        close()
        drop_database()
        __check_connector()
        create_tables()
        conn.commit()
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

        exercise(0)
        exercise(1)
        exercise(2)
        exercise(3)
        exercise(4)
        exercise(5)
        exercise(6)
        exercise(7)
        exercise(8)
        exercise(9)
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
