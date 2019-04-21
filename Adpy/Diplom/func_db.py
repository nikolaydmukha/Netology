import os
import psycopg2
from configparser import ConfigParser


# Функция получает данные для коннекта к БД
def config_db(filename='database.ini', section='postgresql'):
    path = os.path.abspath("files")
    pathfile = path + "\\" + filename
    parser = ConfigParser()
    parser.read(os.path.abspath(filename))
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    print(db)
    return db


# Коннект к БД
def connect():
    conn = None
    try:
        params = config_db()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# Создание таблиц
def create_tables():
    commands = [
        """
        DROP TABLE users
        """,
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            lovefinder_name VARCHAR(255) NOT NULL,
            lovefinder_vk_id INTEGER NOT NULL,
            vk_id INTEGER NOT NULL,
            fullname VARCHAR(255) NOT NULL,
            age_from INTEGER NOT NULL,
            age_to INTEGER NOT NULL,
            city_id INTEGER NOT NULL,
            country_id INTEGER NOT NULL
            )
        """]
    conn = None
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# Втставка данных в БД
def insert_users(lovefinder_data, finded_users, result_data):
    sql = "INSERT INTO users(lovefinder_name, lovefinder_vk_id, vk_id, fullname, age_from, age_to, city_id, country_id)" \
          " VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = None
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print(type(result_data))
        for key in result_data[:10]:
            print(key)
            print(finded_users)
            print("2222222", finded_users[0][key]['age_from'])
            cur.execute(sql, (lovefinder_data['fullname'], lovefinder_data['id'], finded_users[0][key]['id'], key,
                              finded_users[0][key]['age_from'], finded_users[0][key]['age_to'], finded_users[0][key]['city_id'],
                              finded_users[0][key]['country_id']))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# Получение информации из табдицы
def get_users():
    conn = None
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT id, vk_id, fullname, lovefinder_name, lovefinder_vk_id, age_from, age_to,"
                    "city_id, country_id FROM users")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()