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
	FOREIGN KEY (managed_by) REFERENCES employess(SSN) ON DELETE SET NULL,
	FOREIGN KEY (leaved_by) REFERENCES customers(customer_id) ON DELETE SET NULL
);

CREATE TABLE payments (
	payment_id INTEGER,
	paid_customer_id INTEGER,
	paid_amount INTEGER,
    PRIMARY KEY (payment_id),
	FOREIGN KEY (paid_customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE orders(
	order_id INTEGER,
	start_time DATETIME,
	end_time DATETIME,
	payment_id INTEGER,
	made_by INTEGER,
	included_car INTEGER,
	start_location INTEGER,
	destination INTEGER,
	PRIMARY KEY (order_id),
	FOREIGN KEY (included_car) REFERENCES cars(car_id),
	FOREIGN KEY (made_by) REFERENCES customers(customer_id),
	FOREIGN KEY (payment_id) REFERENCES payments(payment_id),
	FOREIGN KEY (start_location) REFERENCES locations(location_id),
	FOREIGN KEY (destination) REFERENCES locations(location_id)
);

CREATE TABLE history_of_travels(
	car_id INTEGER,
	location_id INTEGER,
	time DATETIME,
	FOREIGN KEY (car_id) REFERENCES cars(car_id),
	FOREIGN KEY (location_id) REFERENCES locations(location_id)
)