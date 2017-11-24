import mysql.connector

from dream_team_db import init_db
from dream_team_db import data

usr = 'root'
pas = 'root'
host = '127.0.0.1'
db_name = 'CarSharingDB'
connector = None

def create_database():
    cr_connector = mysql.connector.connect(user=usr, password=pas, host=host)
    init_db.create_db(connector=cr_connector, db_name=db_name)
    cr_connector.close()

def create_tables():
    __check_connector()
    init_db.create_tables(connector=connector)

def drop_database():
    cr_connector = mysql.connector.connect(user=usr, password=pas, host=host)
    init_db.drop_database(cr_connector, db_name=db_name)
    cr_connector.close()

def close():
    __check_connector()
    connector.close()

def __check_connector():
    global connector
    if (connector == None):
        connector = mysql.connector.connect(user=usr, password=pas, host=host, database=db_name)


# drop_database()
# create_database()
# create_tables()
# __check_connector()
# data.fill_all(connector.cursor())
# connector.commit()

data.test(connector.cursor())

close()