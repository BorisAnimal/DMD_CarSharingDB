import sqlite3

from dream_team_db import init_db

usr = 'root'
pas = 'root'
db_name = 'CarSharingDB.db'
conn = None


# def create_database():
#     cr_connector = sqlite3.connect(user=usr, password=pas)
#     init_db.create_db(connector=cr_connector, db_name=db_name)
#     cr_connector.close()

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


drop_database()
# create_database()
# create_tables()
# __check_connector()
# data.fill_all(connector.cursor())
# connector.commit()

# data.test(conn.cursor())
__check_connector()
create_tables()
close()
