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
        order_id INT PRIMARY KEY, 
        customer_id INT, 
        order_date TIMESTAMP, 
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
        conn.close()

