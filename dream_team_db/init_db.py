def create_db(connector, db_name):
    cursor = connector.cursor()
    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))


tables = {
    "locations": """CREATE TABLE locations(
            location_id INTEGER AUTO_INCREMENT,
            state TINYTEXT,
            city TINYTEXT,
            street TINYTEXT,
            house TINYTEXT,
            zip_code TEXT,
            gps TEXT,
            PRIMARY KEY (location_id));""",

    "customers": """CREATE TABLE customers(
	customer_id INTEGER AUTO_INCREMENT,
	name TINYTEXT,
	date_of_birth TINYTEXT,
	phone_number TINYTEXT,
	full_name TINYTEXT,
	lives_in INTEGER,
	PRIMARY KEY (customer_id),
	FOREIGN KEY (lives_in) REFERENCES locations(location_id) ON DELETE SET NULL
);""",
    "managers": """CREATE TABLE managers(
	SSN INTEGER,
	full_name TINYTEXT,
	salary INTEGER,
	phone_number TINYTEXT,
	PRIMARY KEY (SSN)
);""",
    "telephone_operators": """CREATE TABLE telephone_operators(
	SSN INTEGER,
	work_phone INTEGER,
	full_name TINYTEXT,
	salary INTEGER,
	phone_number TINYTEXT,
	PRIMARY KEY (SSN)
);""",
    "repair_stations": """CREATE TABLE repair_stations(
	r_station_id INTEGER AUTO_INCREMENT,
	availible_sockets INTEGER,
	location INTEGER,
	PRIMARY KEY (r_station_id),
	FOREIGN KEY (location) REFERENCES locations(location_id) ON DELETE CASCADE
);""",

    "charging_stations": """CREATE TABLE charging_stations(
	c_station_id INTEGER AUTO_INCREMENT,
	availible_sockets INTEGER,
	location INTEGER,
	PRIMARY KEY (c_station_id),
	FOREIGN KEY (location) REFERENCES locations(location_id) ON DELETE CASCADE
);""",

    "car_parks": """CREATE TABLE car_parks(
	car_park_id INTEGER AUTO_INCREMENT,
	availible_sockets INTEGER,
	location INTEGER,
	PRIMARY KEY (car_park_id),
	FOREIGN KEY (location) REFERENCES locations(location_id) ON DELETE CASCADE
);""",

    "cars": """CREATE TABLE cars(
	car_id INTEGER AUTO_INCREMENT,
	state TINYTEXT,
	charge_level INTEGER,
	tarif INTEGER,
	model TINYTEXT,
	destination INTEGER,
	location INTEGER,
	PRIMARY KEY (car_id),
	FOREIGN KEY (location) REFERENCES locations(location_id)  ON DELETE SET NULL
);""",

    "feedbacks": """CREATE TABLE feedbacks(
	feedback_id INTEGER AUTO_INCREMENT,
	content TEXT,
	grade INTEGER,
	managed_by INTEGER,
	leaved_by INTEGER,
	PRIMARY KEY (feedback_id),
	FOREIGN KEY (managed_by) REFERENCES managers(SSN) ON DELETE SET NULL,
	FOREIGN KEY (leaved_by) REFERENCES customers(customer_id) ON DELETE SET NULL
);""",

    "payments": """CREATE TABLE payments (
	payment_id INTEGER AUTO_INCREMENT,
	customer_id INTEGER,
	total_amount INTEGER,
    PRIMARY KEY (payment_id),
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);""",

    "orders": """CREATE TABLE orders(
	order_id INTEGER AUTO_INCREMENT,
	start_time TINYTEXT,
	end_time TINYTEXT,
	payment_id INTEGER,
	made_by INTEGER,
	included_car INTEGER,
	PRIMARY KEY (order_id),
	FOREIGN KEY (included_car) REFERENCES cars(car_id),
	FOREIGN KEY (made_by) REFERENCES customers(customer_id),
	FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
)"""
}


def create_tables(connector):
    cursor = connector.cursor()
    for i in tables:
        cursor.execute(tables[i])
        # print(tables[i])


def drop_database(connector, db_name: str):
    cursor = connector.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {}".format(db_name))
