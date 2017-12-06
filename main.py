# coding=utf-8
import sqlite3
from db import init_db as db
from db import queries_from_task as ex

db_name = 'CarSharingDB.db'
conn = None


def execute_select(number):
    """
        Executes exercise from prepared list by its number from assignment list

    :param number: number of execute selection
    """
    selections = [
        ex.ex_1,
        ex.ex_2,
        ex.ex_3,
        ex.ex_4,
        ex.ex_5,
        ex.ex_6,
        ex.ex_7,
        ex.ex_8,
    ]
    __check_connector()
    print("\nQuery #{} requested. Execution result:".format(number))
    if (number < 1 or number > 8):
        print("""Tricky input detected. There is no such select ({}) in our assignment :3 \nTry range [1..{}]"""
              .format(number, len(selections)))
    else:
        try:
            if (number > len(selections)):
                print("We not implemented this selection :3 \nTry range [1..{}]".format(len(selections)))
            else:
                print(selections[number - 1](conn.cursor()))
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])


def create_tables_with_data():
    """
        creates schema of all tables with empty rows
    """
    try:
        __check_connector()
        db.create_tables_with_data(connector=conn)
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
        initiate connection if it is None
    """
    global conn
    if (conn == None):
        try:
            conn = sqlite3.connect(database=db_name)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])


def custom_query(query):
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
        create_tables_with_data()
        conn.commit()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


def base_test():
    try:
        refresh_db()
        # create connection
        __check_connector()
        # check tables existence
        if not db.check_tables_existance(conn.cursor()):
            create_tables_with_data()
            conn.commit()

        print("\nUser defined input execution test>>")
        custom_query("SELECT * FROM customers LIMIT 5")

        execute_select(0)
        execute_select(1)
        execute_select(2)
        execute_select(3)
        execute_select(4)
        execute_select(5)
        execute_select(6)
        execute_select(7)
        execute_select(8)
        execute_select(9)

        db.fill_all_tables(conn.cursor())

        close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


if __name__ == "__main__":
    __check_connector()
    # check tables existence
    if not db.check_tables_existance(conn.cursor()):
        create_tables_with_data()
        conn.commit()
    base_test()
