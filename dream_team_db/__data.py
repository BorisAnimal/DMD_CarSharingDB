# def add_location(cursor, state, city, street, house, zip_code, gps):
#     cursor.execute("""INSERT INTO locations
#                     (state, city, street, house, zip_code, gps)
#                       VALUES (%s,%s,%s,%d,%d,%f)""",
#                    (state, city, street, house, zip_code, gps))


def add_customer(cursor, name, date_of_birth, phone_number, full_name, lives_in):
    cursor.execute("""INSERT INTO customers 
                    (name, date_of_birth, phone_number, full_name, lives_in)
                      VALUES (?,?,?,?,?,?)""",
                   (name, date_of_birth, phone_number,
                    full_name, lives_in))


# def add_manager(cursor, SSN, full_name, salary, phone_number):
#     cursor.execute("""INSERT INTO managers
#                     (SSN, full_name, salary, phone_number)
#                       VALUES (?,?,?,?)""",
#                    (SSN, full_name, salary, phone_number))
#

# def add_telephone_operator(cursor, SSN, full_name, salary, phone_number):
#     cursor.execute("""INSERT INTO telephone_operators
#                     (SSN, full_name, salary, phone_number)
#                       VALUES (?,?,?,?)""",
#                    (SSN, full_name, salary, phone_number))

#
# def add_repair_station(cursor, availible_sockets, location):
#     cursor.execute("""INSERT INTO  repair_station
#                     (availible_sockets, location)
#                       VALUES (?,?)""",
#                    (availible_sockets, location))


# def add_charging_station(cursor, availible_sockets, location):
#     cursor.execute("""INSERT INTO  repair_station
#                     (availible_sockets, location)
#                       VALUES (?,?)""",
#                    (availible_sockets, location))


# def add_car_park(cursor, availible_sockets, location):
#     cursor.execute("""INSERT INTO  repair_station
#                     (availible_sockets, location)
#                       VALUES (?,?)""",
#                    (availible_sockets, location))


# def add_car(cursor, state, charge_level, tarif, model, destination, location):
#     cursor.execute("""INSERT INTO  cars
#                     (state, charge_level, tarif, model, destination, location)
#                       VALUES (?,?,?,?,?,?)""",
#                    (state, charge_level, tarif, model, destination, location))


# def add_feedback(cursor, content, grade, managed_by, leaved_by):
#     cursor.execute("""INSERT INTO feedbacks
#                     (content, grade, managed_by, leaved_by)
#                       VALUES (?,?,?,?)""",
#                    (content, grade, managed_by, leaved_by))


# def add_payment(cursor, customer_id, total_amount):
#     cursor.execute("""INSERT INTO payments
#                     (customer_id, total_amount)
#                       VALUES (?,?)""",
#                    (customer_id, total_amount))
#
#
# def add_order(cursor, start_time, end_time, payment_id, made_by, included_car):
#     cursor.execute("""INSERT INTO orders
#                     (start_time, end_time, payment_id, made_by, included_car)
#                       VALUES (?,?,?,?,?)""",
#                    (start_time, end_time, payment_id, made_by, included_car))


# if __name__ == "__main__":
#     connection = sqlite3.connect('database.db')
#     cursor = connection.cursor()
#     add_location(cursor, "some_state53", "some_city1", "some_street", "some_house", "some_zip_code", "some_gps")
#     connection.commit()
#     cursor.execute("""SELECT * FROM locations;""")
#     response = "locations: \n"
#     for row in cursor.fetchall():
#         response += str(row[0]) + '|' + str(row[1]) + '\n'
#     print(response)
#     connection.close()
