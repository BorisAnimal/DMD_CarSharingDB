import os
from db import __data_provider as provider

tables_file = "setup.sql"
locations = None
customers = None


def create_db(connector, db_name):
    cursor = connector.cursor()
    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))


def drop_database(db_name: str):
    os.remove(db_name)


def create_tables(connector):
    cursor = connector.cursor()
    for i in __get_tables():
        cursor.execute(i)
        print(i)


def __get_tables():
    r = []
    with open(tables_file) as f:
        r = f.read().split("\n\n")
    return r


def fill_all(cursor):
    __fill_charging_stations(cursor)
    __fill_repair_stations(cursor)
    cars = __fill_cars(cursor)
    manager = __fill_employee(cursor)
    __fill_car_parks(cursor)
    __fill_customer_activity(cursor, cars, manager)

    cursor.close()


def __generate_new_location(cursor):
    global locations
    if (locations == None):
        locations = provider.get_locations()
    if (len(locations) <= 0):
        locations = None
        print("\n\n\nWARNING!!!!HAVE NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        __generate_new_location(cursor)
    else:
        cursor.execute("""INSERT INTO locations 
                                (state, city, street, house, zip_code, gpsX, gpsY)
                                  VALUES (?,?,?,?,?,?,?)""", locations.pop())
        cursor.execute("select LAST_INSERT_ROWID()")
        for i in cursor:
            return i[0]


def __generate_new_customer(cursor):
    global customers
    if (customers == None):
        cursor = provider.get_customers()
    if (len(customers) <= 0):
        customers = None
        print("\n\n\nWARNING!!!!HAVE NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        __generate_new_customer(cursor)
    else:
        __generate_new_location(cursor)
        cursor.execute("""INSERT INTO customers 
                                    (name, date_of_birth, phone_number, full_name, lives_in)
                                      VALUES (?,?,?,?,LAST_INSERT_ROWID())""", customers.pop())
        cursor.execute("select LAST_INSERT_ROWID()")
        for i in cursor:
            return i[0]


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
    tp = provider.get_cars()
    car_ids = []
    for i in tp:
        __generate_new_location(cursor)
        cursor.execute("""INSERT INTO  cars
                            (state, charge_level, tarif, model, color,plate, location)
                              VALUES (?,?,?,?,?,?,LAST_INSERT_ROWID())""", i)
        cursor.execute("select LAST_INSERT_ROWID()")
        for i in cursor:
            car_ids.append(i[0])
    return car_ids


def __fill_employee(cursor):
    cursor.execute("""INSERT INTO posts (post_name, salary) VALUES (?,?)""", ("manager", 1400))
    cursor.execute("select LAST_INSERT_ROWID()")
    man = -1
    for i in cursor:
        man = i[0]
    cursor.execute("""INSERT INTO posts (post_name, salary) VALUES (?,?)""", ("telephone operator", 1000))
    cursor.execute("select LAST_INSERT_ROWID()")
    tel = -1
    for i in cursor:
        tel = i[0]
    cursor.execute("""INSERT INTO employee (SSN, full_name,  phone_number, post_id) VALUES (?,?,?,?)""",
                   ("432101209", "Gager Nine", "88175522111", tel))
    cursor.execute("""INSERT INTO employee (SSN, full_name,  phone_number, post_id) VALUES (?,?,?,?)""",
                   ("902101234", "Cristofer Gag", "88005553535", man))
    # manager id in employee table
    cursor.execute("select LAST_INSERT_ROWID()")
    for i in cursor:
        return i[0]


def __fill_customer_activity(cursor, car_ids: list, manager):
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
    ord = ''
    cursor.execute("select LAST_INSERT_ROWID()")
    for i in cursor:
        ord = i[0]
    # Feedback
    cursor.execute("""insert into feedbacks (content, grade, managed_by, leaved_by) VALUES (?,?,?,?)""",
                   ("All was good", 10, manager, cust))
    # Payments
    cursor.execute("""insert into payments (paid_for_order, paid_amount) VALUES (?,?)""", (ord, 120))
