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
        gps = ["10.210", "21.80", "17.21", "15.1561", "213.112"]
        locations = list(itertools.product(stt, ct, str, hs, zp, gps))
    if (len(locations) <= 0):
        locations = None
        print("\n\n\nWARNING!!!!NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        generate_new_location()
    else:
        cursor.execute("""INSERT INTO locations 
                                (state, city, street, house, zip_code, gps)
                                  VALUES (%s,%s,%s,%s,%s,%s)""", locations.pop())


def fill_charging_stations(cursor):
    for i in range(6):
        generate_new_location(cursor)
        cursor.execute("""insert into charging_stations (availible_sockets, location) values
            (%s,LAST_INSERT_ID())""", [str(i)])


def fill_repair_stations(cursor):
    for i in range(6):
        generate_new_location(cursor)
        cursor.execute("""insert into repair_stations (availible_sockets, location) values
            (%s,LAST_INSERT_ID())""", [str(i)])


def fill_car_parks(cursor):
    for i in range(6):
        generate_new_location(cursor)
        cursor.execute("""insert into car_parks (availible_sockets, location) values
            (%s,LAST_INSERT_ID())""", [str(i)])


def fill_cars(cursor):
    st = ["good", "bad"]
    cl = [10, 90]
    tf = [70, 80]
    ml = ["Volvo", "lada"]
    tp = list(itertools.product(st, cl, tf, ml))
    # (cursor, state, charge_level, tarif, model, destination, location)
    for i in tp:
        generate_new_location(cursor)
        cursor.execute("""INSERT INTO  cars
                            (state, charge_level, tarif, model, location)
                              VALUES (%s,%s,%s,%s, LAST_INSERT_ID())""", i)


def fill_manager(cursor):
    SSN = "902101234"
    name = "Cristofer Gag"
    salary = "1400"
    phone = "88005553535"
    cursor.execute("""INSERT INTO managers
                    (SSN, full_name, salary, phone_number)
                      VALUES (%s,%s,%s,%s)""", (SSN, name, salary, phone))


def fill_telephone_operator(cursor):
    SSN = "432101209"
    name = "Gager Nine"
    salary = "1000"
    phone = "88175522111"
    cursor.execute("""INSERT INTO telephone_operators
                    (SSN, full_name, salary, phone_number)
                      VALUES (%s,%s,%s,%s)""", (SSN, name, salary, phone))


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
        print("\n\n\nWARNING!!!!NO MORE LOCATIONS!!! HARDCODE ANYMORE VALUES IN LISTS!!!!!!ACHTUNG!!!!\n\n\n")
        generate_new_customer(cursor)
    else:
        generate_new_location(cursor)
        cursor.execute("""INSERT INTO customers 
                                    (name, date_of_birth, phone_number, full_name, lives_in)
                                      VALUES (%s,%s,%s,%s, LAST_INSERT_ID())""", customers.pop())
        cursor.execute("select LAST_INSERT_ID()")
        for i in cursor:
            return i[0]


def fill_customer_activity(cursor):
    pass #TODO: создать customer, затем order и feedback, затем к ниму ещё и manager приписать


def fill_all(cursor):
    fill_charging_stations(cursor)
    fill_repair_stations(cursor)
    fill_cars(cursor)
    fill_manager(cursor)
    fill_telephone_operator(cursor)
    fill_car_parks(cursor)

    fill_customer_activity(cursor)

    cursor.close()


