import os

tables_file = "setup.sql"

def create_db(connector, db_name):
    cursor = connector.cursor()
    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))


def get_tables():
    r = []
    with open(tables_file) as f:
        r = f.read().split("\n\n")
    return r


def create_tables(connector):
    cursor = connector.cursor()
    for i in get_tables():
        cursor.execute(i)
        print(i)


def drop_database( db_name: str):
    os.remove(db_name)
