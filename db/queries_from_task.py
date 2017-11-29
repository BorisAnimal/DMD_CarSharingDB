import sqlite3


def ex_1(cursor):
    """
    We assumed that name of forgetful customer is "Marina"
    To solve this task we join tables "customers", "orders", "cars"
    We find all Marina's orders,
    and then we find all cars' (this cars included in Marina's orders) plates,
    that has red color and plate that starts with "AN"
    :param cursor:
    :return: String with plates of cars
    """
    name_of_forgetful_customer = "Marina"
    plate_start = "AN"
    cursor.execute("""SELECT DISTINCT plate
                      FROM 
                      ((SELECT * FROM customers WHERE name = ?) cust
                      INNER JOIN 
                      orders
                      ON customer_id = made_by ) a
                      INNER JOIN
                      (SELECT * FROM cars WHERE plate LIKE ? || '%') b
                      ON included_car = car_id;
    """, (name_of_forgetful_customer, plate_start))
    result = "possible car's plate(s): "
    for row in cursor.fetchall():
        result += row[0] + " "
    result += "\n"
    return result


def ex_2(cursor):
    """
    To find if car used charging station we check if car has same location as charging stations in some hour
    For this we use tables history_of_travels and charging_stations
    :param cursor:
    :return: String with amount of visits to charging stations for each hour at 2017-12-14
    """
    date = "2017-12-14 00:00:00"
    result = ""
    for i in range(0, 23, 1):
        h1 = str(i) + " hours"
        h2 = str(i + 1) + " hours"
        cursor.execute("""SELECT COUNT(*) FROM history_of_travels 
                          WHERE history_of_travels."time" >= datetime(?,?) 
                          AND history_of_travels."time" < datetime(?,?)
                          AND location_id IN (SELECT location FROM charging_stations);
        """, (date, h1, date, h2))
        result += h1 + "-" + h2 + " " + str(cursor.fetchone()[0]) + " visit(s)\n"
    return result


def ex_3(cursor):
    """
    To find how many cars was busy in some period of time
    We check how many orders satisfies condition
    start_of_order <= end_range AND start_range <= end_of_order
    We use python to iterate through days and hours
    :param cursor:
    :return: string that conatins how many % of cars are busy at morning, afternoon, evening
    """
    start_date = "2017-11-14 00:00:00"
    result = "Morning, Afternoon, Evening \n"
    cursor.execute("""SELECT COUNT(*) FROM cars;""")
    cars_number = cursor.fetchone()[0]
    for j in range(7, 18, 5):  # iterate through days periods
        counter = 0
        for i in range(0, 7, 1):  # iterate through days
            h = "+" + str(j + 24 * i) + " hours"
            h2 = "+" + str(j + 24 * i + 2) + " hours"
            cursor.execute("""SELECT COUNT(*) FROM 
                              (SELECT DISTINCT included_car 
                              FROM orders 
                              WHERE start_time<=datetime(?, ?)
                              AND end_time>=datetime(?, ?));""",
                           (start_date, h2, start_date, h))
            # count all cars that was busy all needed time range
            # that means: start_of_order <= start_range <= end_range <= end_of_order
            counter += cursor.fetchone()[0]
        result += str(counter / cars_number / 7 * 100) + " "
    return result


def ex_4(cursor):
    """
    We assume that name of lazy customer is John
    To check if john paid more than needed We use tables orders, cars and payments
    customer must pay for order (order.start_time-order.end_time)*included_car.tarif
    if this amount is smaller than payments.paid_amount
    we return how many times he paid more than needed
    :param cursor:
    :return:
    """
    name_of_lazy_customer = "John"
    cursor.execute("""SELECT customer_id FROM customers WHERE customers.name=?;""", (name_of_lazy_customer,))
    id = cursor.fetchone()[0]
    cursor.execute("""SELECT COUNT(*) FROM
                        (
                          ((SELECT paid_amount, paid_for_order FROM payments)
                            JOIN
                          (SELECT (julianday(end_time)-julianday(start_time)) AS order_time, included_car, order_id FROM orders
                              WHERE made_by=? AND end_time>datetime('now', '-1 months'))
                            ON paid_for_order = order_id) a
                            JOIN
                          (SELECT car_id, tarif FROM cars)
                            ON car_id = included_car
                        ) WHERE paid_amount>tarif*order_time;
                    """, (id,))
    result = "John paid more than nedeed " + str(cursor.fetchone()[0]) + " times in last month\n"
    return result


def ex_5(cursor, date = "2017-11-14 00:00:00"):
    d_date = "2017-11-14 00:00:00"
    cursor.execute("""
        SELECT (x_c-x_2) AS x, (y_c-y_2) AS y FROM (
          (SELECT included_car, gpsX AS x_c, gpsY AS y_c, location_id, start_time AS time_c, order_id FROM
            (orders
              JOIN
            locations
              ON start_location = locations.location_id
          ) WHERE start_time >= ?
          ) AS S1
            JOIN
          (SELECT car_id, locations.location_id, time, gpsX AS x_2, gpsY AS y_2 FROM
            (history_of_travels
              JOIN
            locations
              ON history_of_travels.location_id = locations.location_id
            )
          ) AS S2
            ON S2.car_id = S1.included_car
        )
        WHERE time < time_c
        GROUP BY order_id
    """, (date,))
    result = "Average distance: "
    sum_of_distances = 0
    count = 0
    for row in cursor.fetchall():
        sum_of_distances += (row[0] * row[0] + row[1] * row[1]) ** 0.5
        count += 1
    result += str(sum_of_distances / count)
    cursor.execute(
        """SELECT datetime(AVG(julianday(end_time) - julianday(start_time))) AS time FROM orders WHERE orders.start_time >= ?""",
        (date,))
    result += " Average duration: "
    for row in cursor.fetchall():
        result += str(row[0]).split(' ')[1] + '\n'
    return result


def ex_6(cursor):
    time = [(7, 10), (12, 14), (17, 19)]
    result = ""
    for (i, j) in time:
        cursor.execute("""SELECT locations.state || ', ' || locations.city || ', ' || locations.street || ', ' || locations.house AS name_s  FROM (
                        SELECT orders.start_location loc_id
                        FROM orders
                        WHERE CAST(COALESCE(strftime("%H", orders.start_time), 0) AS INTEGER) >= ?
                          AND CAST(COALESCE(strftime("%H", orders.start_time), 0) AS INTEGER) < ?
                        GROUP BY orders.start_location
                        ORDER BY COUNT(*) DESC
                        LIMIT 3
                    ) AS S1
                    JOIN locations ON locations.location_id = S1.loc_id
            """, (i, j))
        result += "from " + str(i) + "h to " + str(j) + "h:\n"
        result += "top start locations: \n"
        for row in cursor.fetchall():
            result += str(row[0]) + '\n'
        cursor.execute("""SELECT locations.state || ', ' || locations.city || ', ' || locations.street || ', ' || locations.house AS name_d  FROM(
                        SELECT orders.destination
                        FROM orders
                        WHERE CAST(COALESCE(strftime("%H", orders.end_time), 0) AS INTEGER) >= ?
                          AND CAST(COALESCE(strftime("%H", orders.end_time), 0) AS INTEGER) < ?
                        GROUP BY orders.destination
                        ORDER BY  COUNT(*) DESC
                        LIMIT 3
                    ) AS S2
                    JOIN locations ON locations.location_id = S2.destination
                    """, (i, j))
        result += "top destinations: \n"
        for row in cursor.fetchall():
            result += str(row[0]) + '\n'
    return result
