# `ex_01_conection_to_db.py`

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def add_customers(conn, customer):
    """
    Create a new customer account
    :param conn:
    :param customer:
    :return:
    """
    sql = """INSERT INTO customers(name, surname, email, phone, address) VALUES(?, ?, ?, ?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid


def add_orders(conn, order):
    """
    Create orders placed by customers
    :param conn:
    :param order:
    :return:
    """
    sql = """INSERT INTO orders(customer_id, amount) VALUES(?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, order)
    conn.commit()
    return cur.lastrowid


def display(conn, table):
    """
    Display all database rows for chosen table
    :param conn:
    :param table:
    :return:
    """
    sql = f"""SELECT * FROM {table}"""
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows


def update(conn, table, id_column, id, **kwargs):
    """
    Update the data
    :param conn:
    :param table:
    :param id:
    :param kwargs:
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )
    sql = f"""UPDATE {table} SET {parameters} WHERE {id_column} = ?"""
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()


def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")


def delete_all(conn, table):
    """
    Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")


if __name__ == '__main__':

    create_customers_sql = """
        CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL,
        surname VARCHAR(50) NOT NULL, 
        email VARCHAR(100) NOT NULL, 
        phone VARCHAR(15), 
        address TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

    create_orders_sql = """
        CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INT, 
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        amount DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        """

    db_file = "database.db"

    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_customers_sql)
        execute_sql(conn, create_orders_sql)
        customers = [("Jasek", "Pralka", "pjasek@pl", "0700700123", "Koniki Polne 2A, 58-666 Hell"),
                     ("Marian", "Kluska", "muska@pl", "+480700555000", "Slonika Wodnego 11m8, 52-111 Glazy"),
                     ("Johny", "Bravo", "jb@cn.com", "0800 CALL ME", "Cartoon Network")]
        for customer in customers:
            add_customers(conn, customer)

        order = (2, 15.55)
        order_id = add_orders(conn, order)
        # display(conn, "orders")
        # update(conn, "customers", "customer_id", 1, name="Jacek")
        # update(conn, "orders", "order_id", 2, amount=25.55)
        # delete_where(conn, "orders", order_id=3)
        # delete_all(conn, "orders")
        conn.close()

