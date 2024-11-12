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

def main(query, params=None):
    try:
        conn=connect()
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
        else:
            conn.commit()  
            results = []

        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

def add_record(name, last_name, otch, street, stroenie, korp, room, phone):
    conn = connect()
    cursor = conn.cursor()
    result = []

    # Выполняем запросы и добавляем результаты в result
    cursor.execute("""
        SELECT name_inf.name_num
        FROM contacts
        JOIN name_inf ON name_inf.name_num = contacts.name
        WHERE name_inf.name = %s
    """, (name,))
    fetched = cursor.fetchall()
    result.append(fetched[0][0] if fetched else None)

    cursor.execute("""
        SELECT last_name_inf.fam_num
        FROM contacts
        JOIN last_name_inf ON last_name_inf.fam_num = contacts.last_name
        WHERE last_name_inf.last_name = %s
    """, (last_name,))
    fetched = cursor.fetchall()
    result.append(fetched[0][0] if fetched else None)

    cursor.execute("""
        SELECT otch_inf.otch_num
        FROM contacts
        JOIN otch_inf ON otch_inf.otch_num = contacts.otch
        WHERE otch_inf.otch = %s
    """, (otch,))
    fetched = cursor.fetchall()
    result.append(fetched[0][0] if fetched else None)

    cursor.execute("""
        SELECT street_inf.street_num
        FROM contacts
        JOIN street_inf ON street_inf.street_num = contacts.street
        WHERE street_inf.street = %s
    """, (street,))
    fetched = cursor.fetchall()
    result.append(fetched[0][0] if fetched else None)

    # Проверяем, что все элементы в result не None
    if all(result):
        name, last_name, otch, street = int(result[0]), int(result[1]), int(result[2]), int(result[3])
    else:
        print("Не найдено совпадений")
        cursor.close()
        return

    insert_query = """
    INSERT INTO contacts (name, last_name, otch, street, stroenie, korp, room, phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (name, last_name, otch, street, stroenie, korp, room, phone)
    main(insert_query, params)

    print("Record added successfully")



def delete_record(record_id):
    delete_query = f"DELETE FROM contacts WHERE id = {record_id}"
    main(delete_query, (record_id,))
    print("Record deleted successfully")


def filter_table(table, name_filter, last_name_filter, otch_filter, street_filter, str_filter, korp_filter, room_filter, phone_filter):
    ask = """SELECT contacts.id, name_inf.name, last_name_inf.last_name, otch_inf.otch, street_inf.street, 
                contacts.stroenie, contacts.korp, contacts.room, contacts.phone 
                FROM contacts
                JOIN last_name_inf ON last_name_inf.fam_num = contacts.last_name
                JOIN name_inf ON name_num = contacts.name
                JOIN otch_inf ON otch_num = contacts.otch
                JOIN street_inf ON street_num = contacts.street"""

    filters = []
    if name_filter.text():
        filters.append(f"name_inf.name ILIKE '%{name_filter.text()}%'")
    if last_name_filter.text():
        filters.append(f"last_name_inf.last_name ILIKE '%{last_name_filter.text()}%'")
    if otch_filter.text():
        filters.append(f"otch_inf.otch ILIKE '%{otch_filter.text()}%'")
    if street_filter.text():
        filters.append(f"street_inf.street ILIKE '%{street_filter.text()}%'")
    if str_filter.text():
        filters.append(f"contacts.stroenie ILIKE '%{str_filter.text()}%'")
    if korp_filter.text():
        filters.append(f"contacts.korp LIKE '%{korp_filter.text()}%'")
    if room_filter.text():
        filters.append(f"contacts.room = {int(room_filter.text())}")
    if phone_filter.text():
        filters.append(f"contacts.phone LIKE '%{phone_filter.text()}%'")

    filter_query = " AND ".join(filters) if filters else None

    # Load new data
    data = main(ask,filter_query)

    # Clear the table
    table.setRowCount(0)

    # Populate the table with new data
    for row_data in data:
        row_number = table.rowCount()
        table.insertRow(row_number)
        for column_number, value in enumerate(row_data):
            table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(value)))


def interface():
    window = QtWidgets.QWidget()
    window.setWindowTitle('Телефонный справочник')
    window.setGeometry(100, 100, 800, 400)

    layout = QtWidgets.QVBoxLayout(window)
    filter_layout = QtWidgets.QHBoxLayout()

    # Create input fields for filters
    name_filter = QtWidgets.QLineEdit()
    name_filter.setPlaceholderText("Имя")
    filter_layout.addWidget(name_filter)

    last_name_filter = QtWidgets.QLineEdit()
    last_name_filter.setPlaceholderText("Фамилия")
    filter_layout.addWidget(last_name_filter)

    otch_filter = QtWidgets.QLineEdit()
    otch_filter.setPlaceholderText("Отчество")
    filter_layout.addWidget(otch_filter)

    street_filter = QtWidgets.QLineEdit()
    street_filter.setPlaceholderText("Улица")
    filter_layout.addWidget(street_filter)

    str_filter = QtWidgets.QLineEdit()
    str_filter.setPlaceholderText("Строение")
    filter_layout.addWidget(str_filter)

    korp_filter = QtWidgets.QLineEdit()
    korp_filter.setPlaceholderText("Корпус")
    filter_layout.addWidget(korp_filter)

    room_filter = QtWidgets.QLineEdit()
    room_filter.setPlaceholderText("Квартира")
    filter_layout.addWidget(room_filter)

    phone_filter = QtWidgets.QLineEdit()
    phone_filter.setPlaceholderText("Телефон")
    filter_layout.addWidget(phone_filter)

    filter_button = QtWidgets.QPushButton("Применить фильтр")
    filter_button.clicked.connect(lambda: filter_table(table, name_filter, last_name_filter, otch_filter, street_filter, str_filter, korp_filter, room_filter, phone_filter))
    filter_layout.addWidget(filter_button)

    # Button to add a new record
    add_button = QtWidgets.QPushButton("Добавить запись")


    add_button.clicked.connect(lambda: add_record(
        name_filter.text(),
        last_name_filter.text(),
        otch_filter.text(),
        street_filter.text(),
        str_filter.text(),
        korp_filter.text(),
        room_filter.text(),
        phone_filter.text()
    ))
    filter_layout.addWidget(add_button)

    # Button to delete a selected record
    delete_button = QtWidgets.QPushButton("Удалить запись")
    delete_button.clicked.connect(lambda: delete_record(int(table.currentItem().text()) if table.currentItem() else None))
    filter_layout.addWidget(delete_button)

    layout.addLayout(filter_layout)

    # Table to display data
    table = QtWidgets.QTableWidget()
    table.setColumnCount(9)
    table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Отчество", "Улица", "Строение", "Корпус", "Квартира", "Телефон"])
    layout.addWidget(table)

    # Populate the table on startup
    filter_table(table, name_filter, last_name_filter, otch_filter, street_filter, str_filter, korp_filter, room_filter, phone_filter)

    return window


app = QtWidgets.QApplication(sys.argv)
window = interface()
window.show()
sys.exit(app.exec_())