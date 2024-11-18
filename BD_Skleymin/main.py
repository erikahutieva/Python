
from some_funcs import *


def sql_record(query, params=None):
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
            conn.commit() #фиксируем изменения в бд
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
    if len(phone)!=11: 
        print("Введите номер 11-значный номер телефона")
        return
    name, last_name, otch, street = all_id(name, last_name, otch, street)
    insert_query = """
INSERT INTO contacts (id, name, last_name, otch, street, stroenie, korp, room, phone)
VALUES ((SELECT COALESCE(MAX(id), 0) + 1 FROM contacts), %s, %s, %s, %s, %s, %s, %s, %s)
"""

    params = (name, last_name, otch, street, stroenie, korp, room, phone)
    sql_record(insert_query, params)


def delete_record(name, last_name, otch, street, stroenie, korp, room, phone):
    ids = all_id(name, last_name, otch, street)
    if ids is None:
        print("Нечего удалять")
        return

    name, last_name, otch, street = ids

    params = []
    filters = []

    if name:
        filters.append("name = %s")
        params.append(name)
    if last_name:
        filters.append("last_name = %s")
        params.append(last_name)
    if otch:
        filters.append("otch = %s")
        params.append(otch)
    if street:
        filters.append("street = %s")
        params.append(street)
    if stroenie:
        filters.append("stroenie = %s")
        params.append(stroenie)
    if korp:
        filters.append("korp = %s")
        params.append(korp)
    if room:
        filters.append("room = %s")
        params.append(room)
    if phone:
        filters.append("phone = %s")
        params.append(phone)


    filter_clause = " AND ".join(filters)

    if not filter_clause:
        print("Нет фильтров")
        return


    delete_query = f"DELETE FROM contacts WHERE {filter_clause}"
    

def filter_table(table, name_filter, last_name_filter, otch_filter, street_filter, str_filter, korp_filter, room_filter, phone_filter):
    ask = """SELECT contacts.id, name_inf.name, last_name_inf.last_name, otch_inf.otch, street_inf.street, 
                contacts.stroenie, contacts.korp, contacts.room, contacts.phone 
                FROM contacts
                JOIN last_name_inf ON last_name_inf.last_name_num = contacts.last_name
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

    filter_query = " AND ".join(filters) 

    data = sql_record(ask,filter_query)


    table.setRowCount(0)


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


    delete_button = QtWidgets.QPushButton("Удалить запись")
    delete_button.clicked.connect(lambda: delete_record(
        name_filter.text(),
        last_name_filter.text(),
        otch_filter.text(),
        street_filter.text(),
        str_filter.text(),
        korp_filter.text(),
        room_filter.text(),
        phone_filter.text()  
))
    filter_layout.addWidget(delete_button)

    layout.addLayout(filter_layout)


    table = QtWidgets.QTableWidget()
    table.setColumnCount(9)
    table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Отчество", "Улица", "Строение", "Корпус", "Квартира", "Телефон"])
    layout.addWidget(table)

    filter_table(table, name_filter, last_name_filter, otch_filter, street_filter, str_filter, korp_filter, room_filter, phone_filter)

    return window


app = QtWidgets.QApplication(sys.argv)
window = interface()
window.show()
sys.exit(app.exec_())