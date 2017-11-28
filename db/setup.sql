CREATE TABLE locations(
	location_id INTEGER,
	state TINYTEXT,
	city TINYTEXT,
	street TINYTEXT,
	house TINYTEXT,
	zip_code TEXT,
	gpsX REAL,
	gpsY REAL,
	PRIMARY KEY (location_id)
);

CREATE TABLE customers(
	customer_id INTEGER,
	name TINYTEXT,
	date_of_birth TINYTEXT,
	phone_number TINYTEXT,
	full_name TINYTEXT,
	lives_in INTEGER,
	PRIMARY KEY (customer_id),
	FOREIGN KEY (lives_in) REFERENCES locations(location_id) ON DELETE SET NULL
);

CREATE TABLE employee(
	SSN INTEGER,
	full_name TINYTEXT,
	salary INTEGER,
	phone_number TINYTEXT,
	post_id INTEGER,
	PRIMARY KEY (SSN),
	FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);

CREATE TABLE posts(
	post_id INTEGER,
	post_name TINYTEXT,
	salary INTEGER,
	PRIMARY KEY (post_id)
);

CREATE TABLE repair_stations(
	r_station_id INTEGER,
	availible_sockets INTEGER,
	max_availible_sockets INTEGER,
	location INTEGER,
	PRIMARY KEY (r_station_id),
	FOREIGN KEY (location) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE TABLE charging_stations(
	c_station_id INTEGER,
	availible_sockets INTEGER,
	max_availible_sockets INTEGER,
	location INTEGER,
	PRIMARY KEY (c_station_id),
	FOREIGN KEY (location) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE TABLE car_parks(
	car_park_id INTEGER,
	availible_sockets INTEGER,
	location INTEGER,
	PRIMARY KEY (car_park_id),
	FOREIGN KEY (location) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE TABLE cars(
	car_id INTEGER,
	state TINYTEXT,
	charge_level INTEGER,
	tarif INTEGER,
	model TINYTEXT,
	color TINYTEXT,
	destination INTEGER,
	plate TINYTEXT,
	location INTEGER,
	PRIMARY KEY (car_id),
	FOREIGN KEY (location) REFERENCES locations(location_id)  ON DELETE SET NULL,
	FOREIGN KEY (destination) REFERENCES locations(location_id)  ON DELETE SET NULL
);

CREATE TABLE feedbacks(
	feedback_id INTEGER,
	content TEXT,
	grade INTEGER,
	managed_by INTEGER,
	leaved_by INTEGER,
	PRIMARY KEY (feedback_id),
	FOREIGN KEY (managed_by) REFERENCES employee(SSN) ON DELETE SET NULL,
	FOREIGN KEY (leaved_by) REFERENCES customers(customer_id) ON DELETE SET NULL
);

CREATE TABLE payments (
	payment_id INTEGER,
	paid_for_order INTEGER,
	paid_amount INTEGER,
  PRIMARY KEY (payment_id),
	FOREIGN KEY (paid_for_order) REFERENCES orders(order_id) ON DELETE CASCADE
);

CREATE TABLE orders(
	order_id INTEGER,
	start_time DATETIME,
	end_time DATETIME,
	made_by INTEGER,
	included_car INTEGER,
	start_location INTEGER,
	destination INTEGER,
	PRIMARY KEY (order_id),
	FOREIGN KEY (included_car) REFERENCES cars(car_id),
	FOREIGN KEY (made_by) REFERENCES customers(customer_id),
	FOREIGN KEY (start_location) REFERENCES locations(location_id),
	FOREIGN KEY (destination) REFERENCES locations(location_id)
);

CREATE TABLE history_of_travels(
	car_id INTEGER,
	location_id INTEGER,
	time DATETIME,
	FOREIGN KEY (car_id) REFERENCES cars(car_id),
	FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

INSERT INTO locations VALUES (0, "default state", "default city", "default street", "default house", "start zip code", 0,0);

INSERT INTO locations VALUES (1, "default state", "default city", "default street", "default house", "destination zip code", 1,1);

INSERT INTO locations VALUES (2, "default state", "default city", "default street", "default house", "charge station zip code1", 2,2);

INSERT INTO customers VALUES (0, "John", "19980-10-14 00:00:00", "89178516088", "John Abramovich", 0);

INSERT INTO customers VALUES (1, "Marina", "19980-10-14 00:00:00", "89178516088", "Marina Abramovich", 0);

INSERT INTO cars VALUES (0, "free", 100, 1, "BMW", "pink", 1, "DE8Y2A", 0);

INSERT INTO cars VALUES (1, "free", 100, 1, "BMW", "red", 1, "AN8Y2A", 0);

INSERT INTO cars VALUES (2, "free", 100, 1, "BMW", "red", 1, "AN1111", 0);

INSERT INTO orders VALUES (0, "2017-11-14 12:00:00", "2017-11-14 15:00:00", 0, 0, 0, 1);

INSERT INTO orders VALUES (1, "2017-11-14 12:00:00", "2017-11-14 15:00:00", 1, 1, 0, 1);

INSERT INTO orders VALUES (2, "2017-12-14 12:00:00", "2017-12-14 15:00:00", 1, 2, 0, 1);

INSERT INTO payments VALUES (0, 0, 100000000);

INSERT INTO payments VALUES (1, 1, 100);

INSERT INTO payments VALUES (2, 2, 100);

INSERT INTO charging_stations VALUES (0, 5, 5, 2);

INSERT INTO history_of_travels VALUES (0, 0, "2017-10-0 00:00:00");

INSERT INTO history_of_travels VALUES (1, 0, "2017-10-0 00:00:00");

INSERT INTO history_of_travels VALUES (2, 0, "2017-10-0 00:00:00");

INSERT INTO history_of_travels VALUES (0, 1, "2017-11-14 15:00:00");

INSERT INTO history_of_travels VALUES (1, 1, "2017-11-14 15:00:00");

INSERT INTO history_of_travels VALUES (2, 1, "2017-12-14 15:00:00");

INSERT INTO history_of_travels VALUES (2, 2, "2017-12-14 16:00:00");
