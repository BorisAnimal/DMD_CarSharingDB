import os
from db import __data_provider as provider

setup_file = "db/setup.sql"


def create_db(connector, db_name):
    """
        :return: creates empty databasez
    """
    cursor = connector.cursor()
    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    cursor.commit()
    print("Database was successfully created")


def drop_database(db_name):
    """
        removes db_name file from disk
    """
    try:
        os.remove(db_name)
        print("Database file was successfully deleted")
    except os.error as e:
        print(e.args[0])


def create_tables_with_data(connector):
    """
        executes setup file which contains all commands to create tables and
        also some additional insert commands needed for tasks from assignment
    """
    cursor = connector.cursor()
    for i in __get_querries():
        cursor.execute(i)
    print("All tables was successfully created")


def __get_querries():
    """
        :return: list of commands from setup.sql file
    """
    r = []
    with open(setup_file) as f:
        r = f.read().split(";")
    return r


def check_tables_existance(cursor):
    """
        checks user tables existence by checking tables number
        :return: true if more than one user table else otherwise
    """
    tbls = cursor.execute("""SELECT count(*) FROM sqlite_master""")
    if tbls.fetchall()[0][0] > 2:
        return True
    return False


def fill_all_tables(cursor):
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
#####   BLOCK OF INSERT QUERY COMMANDS TO DB
#############


locations = None
customers = None
addresses = None


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
        return __generate_new_location(cursor)
    # If all good, add new location to the table locations
    else:
        cursor.execute("""INSERT INTO locations 
                                (gpsX, gpsY)
                                  VALUES (?,?)""", locations.pop())
    id = __get_last_id(cursor)

    global addresses
    if (addresses == None):
        addresses = provider.get_addresses()
    if (len(addresses) <= 0):
        addresses = None
        print("\n\n\nWARNING!!!!HAVE NO MORE ADDRESSES!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
    else:
        cursor.execute("""INSERT INTO addresses
                                      (descripts, state, city, street, house, zip_code) 
                                      VALUES (LAST_INSERT_ROWID(), ?,?,?,?,?)""", addresses.pop())

    return id


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
                                    (name, date_of_birth, phone_number, name, last_name, lives_in)
                                      VALUES (?,?,?,?,?,LAST_INSERT_ROWID())""", customers.pop())
        return __get_last_id(cursor)


def __fill_charging_stations(cursor):
    max = 6
    for i in range(max):
        __generate_new_location(cursor)
        cursor.execute("""INSERT INTO charging_stations (availible_sockets,max_availible_sockets, location) VALUES
            (?,?,LAST_INSERT_ROWID())""", [str(i), str(max)])


def __fill_repair_stations(cursor):
    max = 6
    for i in range(max):
        __generate_new_location(cursor)
        cursor.execute("""INSERT INTO repair_stations (availible_sockets,max_availible_sockets,location) VALUES
            (?,?,LAST_INSERT_ROWID())""", [str(i), str(max)])


def __fill_car_parks(cursor):
    for i in range(6):
        __generate_new_location(cursor)
        cursor.execute("""INSERT INTO car_parks (availible_sockets, location) VALUES
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
    cursor.execute("""INSERT INTO employee (SSN, name, last_name,  phone_number, post_id) VALUES (?,?,?,?,?)""",
                   ("432101209", "Gager", "Nine", "88175522111", tel))
    cursor.execute("""INSERT INTO employee (SSN, name, last_name,  phone_number, post_id) VALUES (?,?,?,?,?)""",
                   ("902101234", "Cristofer", "Gag", "88005553535", man))
    # manager id in employee table
    return __get_last_id(cursor)


def __fill_customer_activity(cursor, car_ids, manager):
    """
        Fill tables:
            * order
            * feedback
            * payments
            * history_of_travels
        with trash data of one exemplar
    """
    # ORDER
    begin = "2017-11-24 00:00:00"
    end = "2017-11-24 00:10:00"
    car_id = car_ids.pop()
    cust = __generate_new_customer(cursor)
    start = __generate_new_location(cursor)
    finish = __generate_new_location(cursor)
    cursor.execute(
        """INSERT INTO orders (start_time, end_time, made_by, included_car, start_location, destination) 
            VALUES (?,?,?,?,?,?)""", (begin, end, cust, car_id, start, finish))
    ord = __get_last_id(cursor)
    # Feedback
    cursor.execute("""INSERT INTO feedbacks (content, grade, managed_by, leaved_by) VALUES (?,?,?,?)""",
                   ("All was good", 10, manager, cust))
    # Payments
    cursor.execute("""INSERT INTO payments (paid_for_order, paid_amount) VALUES (?,?)""", (ord, 120))
    # History of travels
    cursor.execute("""INSERT INTO history_of_travels (car_id, location_id, time) VALUES (?,?,?)""",
                   (car_id, start, begin))
    cursor.execute("""INSERT INTO history_of_travels (car_id, location_id, time) VALUES (?,?,?)""",
                   (car_id, finish, end))


def __get_last_id(cursor):
    """
        :return: id of last added (sequentially, not use in multithreading) row in something table
        (not matter which table)
    """
    cursor.execute("select LAST_INSERT_ROWID()")
    for i in cursor:
        return i[0]


if __name__ == "__main__":
    setup_file = "setup.sql"
