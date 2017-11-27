import itertools

locations = None
customers = None


def generate_new_location(cursor):
    global locations
    if (locations == None):
        stt = ["Chuvashia", "Tatarstan", "Kalmikia", "Bashkiria"]
        ct = ["Kazan", "Innopolis", "Cheboksary"]
        str = ["Sportivnaya", "Baumana", "Lenina", "Gogolya"]
        hs = ["19", "1", "15", "12", "10", "2"]
        zp = ["420500", "452250", "124525", "151521", "422188"]
        gpsx = ["10.210", "21.80", "17.21", "15.1561", "213.112"]
        gpsy = ["10.210", "21.80", "17.21", "15.1561", "213.112"]
        locations = list(itertools.product(stt, ct, str, hs, zp, gpsx, gpsy))
    if (len(locations) <= 0):
        locations = None
        print("\n\n\nWARNING!!!!HAVE NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        generate_new_location(cursor)
    else:
        cursor.execute("""INSERT INTO locations 
                                (state, city, street, house, zip_code, gpsX, gpsY)
                                  VALUES (?,?,?,?,?,?,?)""", locations.pop())
        cursor.execute("select LAST_INSERT_ROWID()")
        for i in cursor:
            return i[0]


def generate_new_customer(cursor):
    global customers
    if (customers == None):
        nm = ["John", "Snowy", "Snoop"]
        dt = ["29.01.1992", "30.01.2000", "31.01.1987", "01.02.1991", "02.02.2002"]
        pn = ["5445555455", "646465465", "6465446464", "66651515", "46566515"]
        fn = ["Lock Dogg", "Matt Daymon", "Kate Gogo", "Lina Tiger"]
        customers = list(itertools.product(nm, dt, pn, fn))
    if (len(customers) <= 0):
        customers = None
        print("\n\n\nWARNING!!!!HAVE NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        generate_new_customer(cursor)
    else:
        generate_new_location(cursor)
        cursor.execute("""INSERT INTO customers 
                                    (name, date_of_birth, phone_number, full_name, lives_in)
                                      VALUES (?,?,?,?,LAST_INSERT_ROWID())""", customers.pop())
        cursor.execute("select LAST_INSERT_ROWID()")
        for i in cursor:
            return i[0]


def fill_charging_stations(cursor):
    max = 6
    for i in range(max):
        generate_new_location(cursor)
        cursor.execute("""insert into charging_stations (availible_sockets,max_availible_sockets, location) values
            (?,?,LAST_INSERT_ROWID())""", [str(i), str(max)])


def fill_repair_stations(cursor):
    max = 6
    for i in range(max):
        generate_new_location(cursor)
        cursor.execute("""insert into repair_stations (availible_sockets,max_availible_sockets,location) values
            (?,?,LAST_INSERT_ROWID())""", [str(i), str(max)])


def fill_car_parks(cursor):
    for i in range(6):
        generate_new_location(cursor)
        cursor.execute("""insert into car_parks (availible_sockets, location) values
            (?,LAST_INSERT_ROWID())""", [str(i)])


def fill_cars(cursor):
    st = ["good", "bad"]
    cl = [10, 90]
    tf = [70, 80]
    ml = ["Volvo", "lada"]
    col = ["red", "green", "Brown"]
    pl = ["e777kx", "h123bm"]
    tp = list(itertools.product(st, cl, tf, ml, col, pl))
    car_ids = []
    # (cursor, state, charge_level, tarif, model, destination, location)
    for i in tp:
        generate_new_location(cursor)
        cursor.execute("""INSERT INTO  cars
                            (state, charge_level, tarif, model, color,plate, location)
                              VALUES (?,?,?,?,?,?,LAST_INSERT_ROWID())""", i)
        cursor.execute("select LAST_INSERT_ROWID()")
        for i in cursor:
            car_ids.append(i[0])
    return car_ids


def fill_employee(cursor):
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





def fill_customer_activity(cursor, car_ids: list, manager):
    # ORDER
    begin = "2017-11-24 00:00:00"
    end = "2017-11-24 00:10:00"
    cust = generate_new_customer(cursor)
    car_id = car_ids.pop()
    cust = generate_new_customer(cursor)
    start = generate_new_location(cursor)
    finish = generate_new_location(cursor)
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

def fill_all(cursor):
    fill_charging_stations(cursor)
    fill_repair_stations(cursor)
    cars = fill_cars(cursor)
    manager = fill_employee(cursor)
    fill_car_parks(cursor)
    fill_customer_activity(cursor, cars, manager)

    cursor.close()


    # car_parks
    # cars
    # charging_stations
    # customers
    # employees
    # feedbacks
    # orders
    # payments
    # history_of_travels
    # locations

    # posts
    # repair_stations
