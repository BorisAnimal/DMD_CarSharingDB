CREATE TABLE locations(
	location_id INTEGER,
	gpsX REAL,
	gpsY REAL,
	PRIMARY KEY (location_id)
);

CREATE TABLE addresses(
	descripts INTEGER,
	state TINYTEXT,
	city TINYTEXT,
	street TINYTEXT,
	house TINYTEXT,
	zip_code TEXT,
	FOREIGN KEY (descripts) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE TABLE customers(
	customer_id INTEGER,
	name TINYTEXT,
	date_of_birth TINYTEXT,
	phone_number TINYTEXT,
	last_name TINYTEXT,
	lives_in INTEGER,
	PRIMARY KEY (customer_id),
	FOREIGN KEY (lives_in) REFERENCES locations(location_id) ON DELETE SET NULL
);

CREATE TABLE employee(
	SSN INTEGER,
 	last_name TINYTEXT,
	name TINYTEXT,
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

INSERT INTO locations VALUES (0, 46.4277, 28.4294);
INSERT INTO locations VALUES (1, 55.8304, 49.0661);
INSERT INTO locations VALUES (2, 55.785663524, 49.119666188);
INSERT INTO locations VALUES (3, 55.7558, 37.6173);
INSERT INTO locations VALUES (4, 55.8314, 49.0601);
INSERT INTO locations VALUES (5, 55.785663524, 49.119666188);
INSERT INTO locations VALUES (6, 55.7558, 37.6173);
INSERT INTO locations VALUES (7, 55.785663524, 49.119666188);
INSERT INTO locations VALUES (8, 55.785663524, 49.119666188);
INSERT INTO locations VALUES (9, 55.785663524, 49.119666188);
INSERT INTO locations VALUES (10, 46.4277, 28.4294);

INSERT INTO addresses VALUES (0, "Republic of Moldova", "Iargara", "Stefan-Voda", "174/2", "6320");
INSERT INTO addresses VALUES (1, "Russia", "Innopolis", "Universitetscaya", "1/4-207", "420500");
INSERT INTO addresses VALUES (2, "Russia", "Kazan", "Baumana", "44", "420030");
INSERT INTO addresses VALUES (3, "Russia", "Moscow", "Lenin", "15/6", "105005");
INSERT INTO addresses VALUES (4, "Russia", "Innopolis", "Universitetscaya", "1/2-317", "420500");
INSERT INTO addresses VALUES (5, "Russia", "Innopolis", "Sportivnaya", "108", "420500");
INSERT INTO addresses VALUES (6, "Russia", "Innopolis", "Sportivnaya", "122", "420500");
INSERT INTO addresses VALUES (7, "Russia", "Kazan", "Baumana", "44", "420030");
INSERT INTO addresses VALUES (8, "Russia", "Kazan", "Baumana", "134", "420031");
INSERT INTO addresses VALUES (9, "Russia", "Kazan", "Tatarstan", "23", "420030");
INSERT INTO addresses VALUES (10, "Republic of Moldova", "Chisinau", "Bucuresti", "69", "5420");

INSERT INTO customers VALUES (0, "John", "1980-10-14 12:15:30", "89178516088", "Abramovich", 2);
INSERT INTO customers VALUES (1, "Marina", "1950-05-19 20:50:10", "89175516088", "Abramovich", 2);
INSERT INTO customers VALUES (2, "Constantin", "1995-06-24 10:55:18", "37369488834", "Condur", 0);
INSERT INTO customers VALUES (3, "Robert", "2001-03-03 05:45:23", "37362169587", "Popescu", 3);
INSERT INTO customers VALUES (4, "Timur", "1997-04-03 01:15:32", "89875156824", "Galkin", 1);
INSERT INTO customers VALUES (5, "Anastasia", "1992-09-15 09:19:29", "89879154822", "Skudarina", 4);
INSERT INTO customers VALUES (6, "Alex", "1980-10-14 12:15:30", "89145616088", "Pinchin", 6);
INSERT INTO customers VALUES (7, "Sabrina", "1987-01-11 20:50:10", "89735516088", "Smith", 5);
INSERT INTO customers VALUES (8, "Pasha", "1997-06-24 11:55:18", "37367648834", "Curinov", 8);
INSERT INTO customers VALUES (9, "Natalia", "2006-11-30 22:45:23", "37362163567", "Zubrina", 7);
INSERT INTO customers VALUES (10, "Boris", "1992-04-23 07:15:32", "89875156333", "Garin", 9);
INSERT INTO customers VALUES (11, "Ana", "1982-07-15 15:19:29", "89809158882", "Malikova", 10);

INSERT INTO cars VALUES (0, "free", 100, 1, "BMW", "pink", 1, "DE8Y2A", 4);
INSERT INTO cars VALUES (1, "free", 95, 1, "Opel", "red", 7, "AN8Y2A", 4);
INSERT INTO cars VALUES (2, "free", 50, 1, "Ford", "green", 6, "AN1111", 4);
INSERT INTO cars VALUES (3, "free", 75, 1, "Ferrari", "black", 10, "DE1010", 0);
INSERT INTO cars VALUES (4, "free", 100, 1, "Volvo", "blue", 0, "DE8Y2A", 10);
INSERT INTO cars VALUES (5, "free", 95, 1, "Mazda", "red", 3, "AN8Y2B", 9);
INSERT INTO cars VALUES (6, "free", 50, 1, "Lada", "blue", 7, "AN1T01", 9);
INSERT INTO cars VALUES (7, "free", 75, 1, "Mercedes-Benz", "yellow", 1, "DE30A0", 9);

INSERT INTO orders VALUES (0, "2017-11-10 07:02:40", "2017-11-13 15:00:00", 0, 2, 4, 2);
INSERT INTO orders VALUES (1, "2017-11-12 08:52:04", "2017-11-12 20:00:00", 1, 1, 5, 3);
INSERT INTO orders VALUES (2, "2017-11-14 11:42:02", "2017-11-14 18:00:00", 2, 0, 6, 1);
INSERT INTO orders VALUES (3, "2017-11-15 14:12:10", "2017-11-16 15:00:00", 3, 3, 7, 4);
INSERT INTO orders VALUES (4, "2017-11-16 16:47:40", "2017-11-18 16:00:00", 4, 5, 8, 5);
INSERT INTO orders VALUES (5, "2017-11-17 18:27:07", "2017-12-18 18:00:00", 5, 4, 9, 6);
INSERT INTO orders VALUES (6, "2017-11-18 19:28:42", "2017-11-18 23:00:00", 3, 7, 4, 7);
INSERT INTO orders VALUES (7, "2017-11-20 12:50:40", "2017-11-24 12:00:00", 6, 6, 5, 8);
INSERT INTO orders VALUES (8, "2017-11-21 01:09:53", "2017-12-25 15:00:00", 7, 6, 6, 9);
INSERT INTO orders VALUES (9, "2017-11-22 09:08:34", "2017-11-22 17:00:00", 8, 7, 10, 2);
INSERT INTO orders VALUES (10, "2017-11-22 10:25:16", "2017-11-26 15:00:00", 9, 3, 0, 3);
INSERT INTO orders VALUES (11, "2017-11-22 22:17:06", "2017-12-30 07:00:00", 11, 5, 3, 10);

INSERT INTO payments VALUES (0, 0, 134);
INSERT INTO payments VALUES (1, 1, 100);
INSERT INTO payments VALUES (2, 2, 645);
INSERT INTO payments VALUES (3, 3, 1000);
INSERT INTO payments VALUES (4, 4, 124);
INSERT INTO payments VALUES (5, 5, 524);
INSERT INTO payments VALUES (6, 6, 22);
INSERT INTO payments VALUES (7, 7, 7467);
INSERT INTO payments VALUES (8, 8, 44);
INSERT INTO payments VALUES (9, 9, 95);
INSERT INTO payments VALUES (10, 10, 100);
INSERT INTO payments VALUES (11, 11, 78);

INSERT INTO charging_stations VALUES (0, 5, 10, 8);
INSERT INTO charging_stations VALUES (1, 7, 20, 7);
INSERT INTO charging_stations VALUES (2, 6, 18, 5);

INSERT INTO history_of_travels VALUES (0, 0, "2017-11-15 15:00:00");
INSERT INTO history_of_travels VALUES (1, 5, "2017-11-17 16:00:00");
INSERT INTO history_of_travels VALUES (2, 6, "2017-11-18 12:00:00");
INSERT INTO history_of_travels VALUES (3, 7, "2017-11-20 07:00:00");
INSERT INTO history_of_travels VALUES (4, 3, "2017-11-22 11:00:00");
INSERT INTO history_of_travels VALUES (5, 7, "2017-12-15 14:00:00");
INSERT INTO history_of_travels VALUES (6, 1, "2017-12-17 16:00:00");

INSERT INTO car_parks VALUES (0, 6, 5);
INSERT INTO car_parks VALUES (1, 18, 7);
INSERT INTO car_parks VALUES (2, 14, 8);
INSERT INTO car_parks VALUES (3, 11, 10);

INSERT INTO employee VALUES (535405466, "Abragim", "Matvei", 7000, 89874651289, 4);
INSERT INTO employee VALUES (535156466, "Eugen", "Niculin", 2000, 89874651689, 2);
INSERT INTO employee VALUES (535402663, "Alina", "Bobrova", 3000, 89874463589, 3);
INSERT INTO employee VALUES (535888336, "Nadir", "Ahmantov", 8000, 89874637345, 1);
INSERT INTO employee VALUES (595827756, "Ecaterina", "Lubina", 5000, 85948473638, 0);

INSERT INTO feedbacks VALUES (0, "I liked the car", 5, 1, 0);
INSERT INTO feedbacks VALUES (1, "Good service", 6, 0, 1);
INSERT INTO feedbacks VALUES (2, "Thank you", 4, 2, 2);
INSERT INTO feedbacks VALUES (3, "Nice, I will always order your cars", 4, 1, 3);
INSERT INTO feedbacks VALUES (4, "Very nice programmers", 6, 0, 4);

INSERT INTO posts VALUE (0, "manager", 5000);
INSERT INTO posts VALUE (1, "director", 8000);
INSERT INTO posts VALUE (2, "banker", 2000);
INSERT INTO posts VALUE (3, "operator", 3000);
INSERT INTO posts VALUE (4, "programmer", 7000);

INSERT INTO repair_stations VALUE (0, 2, 5, 5);
INSERT INTO repair_stations VALUE (1, 1, 2, 7);
INSERT INTO repair_stations VALUE (2, 2, 3, 8);
