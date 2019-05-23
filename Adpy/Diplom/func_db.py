import os
import psycopg2
from configparser import ConfigParser
from vk_user import get_photos


# Функция получает данные для коннекта к БД
def config_db(filename='database.ini', section='postgresql'):
    path = os.path.abspath("files")
    pathfile = os.path.join(path, filename)
    parser = ConfigParser()
    parser.read(os.path.abspath(filename))
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


# Создание таблиц
def create_tables():
    commands = [
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
        pass
        #print(error)
    finally:
        if conn is not None:
            conn.close()


# Втставка данных в БД
def insert_users(lovefinder_data, finded_users, result_data):
    sql = "INSERT INTO users(lovefinder_name, lovefinder_vk_id, vk_id, fullname, age_from, age_to, city_id, " \
          "country_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = None
    # Получим ТОП фото только подходящих под поиск людей
    print("Получаем фотографии пользователей...")
    for i in result_data:
        finded_users[0][i]['photos_url'] = get_photos(finded_users[0][i]['id'])
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print("Найденные люди: ")
        for key in enumerate(result_data[:10], start=1):
            formated_name = key[1][-len(key[1]):key[1].rfind("_")]
            cur.execute(sql, (lovefinder_data['fullname'], lovefinder_data['id'], finded_users[0][key[1]]['id'],
                              formated_name, finded_users[0][key[1]]['age_from'], finded_users[0][key[1]]['age_to'],
                              finded_users[0][key[1]]['city_id'], finded_users[0][key[1]]['country_id']))

            if finded_users[0][key[1]]['photos_url']:
                links = ', '.join(finded_users[0][key[1]]['photos_url'])
            else:
                links = "У пользователя нет фотографий"
            print(f"{key[0]}. Имя: {formated_name} Аккаунт ВК: http://vk.com/id{finded_users[0][key[1]]['id']} "
                  f"ТОП-3 фото: {links}")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# Получение информации из табдицы
def get_users(lovefinder_data, age_from, age_to, ids):
    conn = None
    sql = "SELECT vk_id FROM users WHERE lovefinder_vk_id=%s AND age_from=%s AND age_to=%s AND vk_id in %s"
    try:
        params = config_db()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (lovefinder_data['id'], age_from, age_to, tuple(ids)))
        result_query = cur.fetchall()
        old_finded = []
        for data in result_query:
            old_finded.append(data[0])
        cur.close()
        return old_finded
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
