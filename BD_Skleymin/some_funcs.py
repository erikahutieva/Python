import sys
import psycopg2
from PyQt5 import QtWidgets

def connect ():
    conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='1',
            host='localhost',
            port=5432
        )
    return conn


def get_id(id, name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT {name}_inf.{name}_num
        FROM contacts
        JOIN {name}_inf ON {name}_inf.{name}_num = contacts.{name}
        WHERE {name}_inf.{name} = %s
    """, (id,))
    fetched = cursor.fetchall()
    cursor.close()
    conn.close()  # Don't forget to close the connection

    if not fetched:  # Check if the list is empty
        return None  # Return None if no match is found

    return fetched[0][0]

def all_id(name, last_name, otch, street):
    columns = ["name", "last_name", "otch", "street"]
    values = [name, last_name, otch, street]
    result = []

    for col, val in zip(columns, values):
        id_value = get_id(val, col)
        if id_value is None:  # If no matching record is found
            id_value=0
        result.append(id_value)

    name, last_name, otch, street = map(int, result)
    return name, last_name, otch, street


