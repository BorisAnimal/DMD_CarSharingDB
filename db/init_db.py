import os
from db import __data_provider as provider

tables_file = "../setup.sql"
locations = None
customers = None


def create_db(connector, db_name):
    """
        :return: creates empty database
    """
    cursor = connector.cursor()
    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    cursor.commit()
    print("Database was successfully created")


def drop_database(db_name: str):
    """
        removes db_name file from disk
    """
    try:
        os.remove(db_name)
        print("Database file was successfully deleted")
    except os.error as e:
        print(e.args[0])


def create_tables(connector):
    """
        executes setup file which contains all commands to create tables and
        also some additional insert commands needed for tasks from assignment
    """
    cursor = connector.cursor()
    for i in __get_tables():
        cursor.execute(i)
    print("All tables was successfully created")


def __get_tables():
    """
        :return: list of commands from setup.sql file
    """
    r = []
    with open(tables_file) as f:
        r = f.read().split("\n\n")
    return r


def check_tables_existance(cursor):
    """
        checks user tables existence by checking tables number
        :return: true if more than one user table else otherwise
    """
    tbls = cursor.execute("""select * from sqlite_master""")
    # WARNING!!! do not execute fetchall() twice!!!
    if len(tbls.fetchall()) > 2:
        return True
    return False


def fill_all(cursor):
    """
        fill all tables with trash values
    """
    __fill_charging_stations(cursor)
    __fill_repair_stations(cursor)
    cars = __fill_cars(cursor)
    manager = __fill_employee(cursor)
    __fill_car_parks(cursor)
    __fill_customer_activity(cursor, cars, manager)
    print("All tables was successfully filled with data")
    cursor.close()


#############
#####   BLOCK OF QUERY COMMANDS TO DB
#############


def __generate_new_location(cursor):
    """
        :return: id of currently added location
    """
    global locations
    # Initialize locations tuples
    if (locations == None):
        locations = provider.get_locations()
    # Manage end of locations list
    if (len(locations) <= 0):
        locations = None
        print("\n\n\nWARNING!!!!HAVE NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        __generate_new_location(cursor)
    # If all good, add new location to the table locations
    else:
        cursor.execute("""INSERT INTO locations 
                                (state, city, street, house, zip_code, gpsX, gpsY)
                                  VALUES (?,?,?,?,?,?,?)""", locations.pop())
        return __get_last_id(cursor)


def __generate_new_customer(cursor):
    """
        :return: id of currently added customer
    """
    global customers
    if (customers == None):
        customers = provider.get_customers()
    if (len(customers) <= 0):
        customers = None
        print("\n\n\nWARNING!!!!HAVE NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        __generate_new_customer(cursor)
    else:
        __generate_new_location(cursor)
        cursor.execute("""INSERT INTO customers 
                                    (name, date_of_birth, phone_number, full_name, lives_in)
                                      VALUES (?,?,?,?,LAST_INSERT_ROWID())""", customers.pop())
        return __get_last_id(cursor)


def __fill_charging_stations(cursor):
    max = 6
    for i in range(max):
        __generate_new_location(cursor)
        cursor.execute("""insert into charging_stations (availible_sockets,max_availible_sockets, location) values
            (?,?,LAST_INSERT_ROWID())""", [str(i), str(max)])


def __fill_repair_stations(cursor):
    max = 6
    for i in range(max):
        __generate_new_location(cursor)
        cursor.execute("""insert into repair_stations (availible_sockets,max_availible_sockets,location) values
            (?,?,LAST_INSERT_ROWID())""", [str(i), str(max)])


def __fill_car_parks(cursor):
    for i in range(6):
        __generate_new_location(cursor)
        cursor.execute("""insert into car_parks (availible_sockets, location) values
            (?,LAST_INSERT_ROWID())""", [str(i)])


def __fill_cars(cursor):
    """
        :return: list of ids of currently added cars
    """
    tp = provider.get_cars()
    car_ids = []
    for i in tp:
        __generate_new_location(cursor)
        cursor.execute("""INSERT INTO  cars
                            (state, charge_level, tarif, model, color,plate, location)
                              VALUES (?,?,?,?,?,?,LAST_INSERT_ROWID())""", i)
        car_ids.append(__get_last_id(cursor))
    return car_ids


def __fill_employee(cursor):
    """
        :return: id of currently added employee
    """
    cursor.execute("""INSERT INTO posts (post_name, salary) VALUES (?,?)""", ("manager", 1400))
    man = __get_last_id(cursor)
    cursor.execute("""INSERT INTO posts (post_name, salary) VALUES (?,?)""", ("telephone operator", 1000))
    tel = __get_last_id(cursor)
    cursor.execute("""INSERT INTO employee (SSN, full_name,  phone_number, post_id) VALUES (?,?,?,?)""",
                   ("432101209", "Gager Nine", "88175522111", tel))
    cursor.execute("""INSERT INTO employee (SSN, full_name,  phone_number, post_id) VALUES (?,?,?,?)""",
                   ("902101234", "Cristofer Gag", "88005553535", man))
    # manager id in employee table
    return __get_last_id(cursor)


def __fill_customer_activity(cursor, car_ids: list, manager):
    """
        Fill tables:
            * order
            * feedback
            * payments
        with trash data of one exemplar
    """
    # ORDER
    begin = "2017-11-24 00:00:00"
    end = "2017-11-24 00:10:00"
    cust = __generate_new_customer(cursor)
    car_id = car_ids.pop()
    cust = __generate_new_customer(cursor)
    start = __generate_new_location(cursor)
    finish = __generate_new_location(cursor)
    cursor.execute(
        """insert into orders (start_time, end_time, made_by, included_car, start_location, destination) 
            VALUES (?,?,?,?,?,?)""", (start, end, cust, car_id, start, finish))
    ord = __get_last_id(cursor)
    # Feedback
    cursor.execute("""insert into feedbacks (content, grade, managed_by, leaved_by) VALUES (?,?,?,?)""",
                   ("All was good", 10, manager, cust))
    # Payments
    cursor.execute("""insert into payments (paid_for_order, paid_amount) VALUES (?,?)""", (ord, 120))


def __get_last_id(cursor):
    """
        :return: id of last added (sequentially, not use in multithreading) row in something table
        (not matter which table)
    """
    cursor.execute("select LAST_INSERT_ROWID()")
    for i in cursor:
        return i[0]
