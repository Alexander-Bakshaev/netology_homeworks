import psycopg2
from psycopg2 import sql


def create_db(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                surname VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_book(
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES client(client_id),
                phone CHAR(20)
            );
        """)
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Ошибка при создании таблиц:", e)


def add_client(conn, name, surname, email, phones=None):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO client(name, surname, email) VALUES (%s, %s, %s) RETURNING client_id;
        """, (name, surname, email))
        client_id = cur.fetchone()[0]
        if phones:
            for phone in phones:
                cur.execute("""
                    INSERT INTO phone_book(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Ошибка при добавлении клиента:", e)


def add_phone(conn, client_id, phone):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO phone_book(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Ошибка при добавлении телефона:", e)


def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    try:
        cur = conn.cursor()
        if name:
            cur.execute("""
                UPDATE client SET name = %s WHERE client_id = %s;
            """, (name, client_id))
            conn.commit()
        if surname:
            cur.execute("""
                UPDATE client SET surname = %s WHERE client_id = %s;
            """, (surname, client_id))
            conn.commit()
        if email:
            cur.execute("""
                UPDATE client SET email = %s WHERE client_id = %s;
            """, (email, client_id))
            conn.commit()
        if phones:
            for phone_id, phone_number in phones.items():
                cur.execute("""
                    UPDATE phone_book SET phone = %s WHERE phone_id = %s;
                """, (phone_number, phone_id))
                conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Ошибка при изменении клиента:", e)


def delete_phone(conn, client_id, phone):
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM phone_book WHERE client_id = %s AND phone = %s;
        """, (client_id, phone))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Ошибка при удалении телефона:", e)


def delete_client(conn, client_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM phone_book WHERE client_id = %s;
        """, (client_id,))
        conn.commit()
        cur.execute("""
            DELETE FROM client WHERE client_id = %s;
        """, (client_id,))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Ошибка при удалении клиента:", e)


def find_client(conn, **kwargs):
    try:
        cur = conn.cursor()
        conditions = []
        values = []
        for key, value in kwargs.items():
            if key == 'phone':
                conditions.append("EXISTS (SELECT 1 FROM phone_book WHERE client.client_id = phone_book.client_id AND phone_book.phone = %s)")
            else:
                conditions.append(sql.Identifier(key) + sql.SQL(" = %s"))
            values.append(value)
        if conditions:
            query = sql.SQL("SELECT * FROM client WHERE ") + sql.SQL(" OR ").join(conditions)
            cur.execute(query, values)
            rows = cur.fetchall()
            return rows
        else:
            return []
        cur.close()
    except psycopg2.Error as e:
        print("Ошибка при поиске клиента:", e)


try:
    with psycopg2.connect(database="netology_db", user="postgres", password="1220") as conn:
        create_db(conn)
        add_client(conn, 'Viktor', 'Vasilev', 'john@example.com', phones=None)
        add_phone(conn, 1, '8980003950')
        change_client(conn, 1, name='Peter', surname='Petrov', email='peter@peter.com')
        delete_phone(conn, 1, '8980003950')
        #print(find_client(conn, name='Peter', surname='Petrov'))
        #print(find_client(conn, phone='8980003950'))
except psycopg2.Error as e:
    print("Ошибка при подключении к базе данных:", e)
