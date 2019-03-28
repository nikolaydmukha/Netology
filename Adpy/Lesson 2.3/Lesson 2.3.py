import psycopg2
import sys
from constants import list_of_students, course_list


# создает таблицы, если они ещё не созданы
def create_db():
    with psycopg2.connect("dbname=lesson2.3 user=postgres password=nd$6482") as conn:
        tables = {'course': "CREATE TABLE course(id integer NOT NULL, name varchar(100) NOT NULL);",
                  'student': "CREATE TABLE student(id integer NOT NULL, name varchar(100) NOT NULL, "
                             "gpa numeric(10, 2), birth timestamp with time zone);",
                  'student_course': "CREATE TABLE student_course(course_id integer NOT NULL, "
                                    "student_id integer NOT NULL);"
                  }
        with conn.cursor() as curs:
            for name, query in tables.items():
                curs.execute("select exists(select * from information_schema.tables where table_name='%s');" % name)
                result = curs.fetchone()[0]
                if not result:
                    curs.execute("%s" % query)


# добавить курс в таблицу курсов
def add_course(course_list):
    with psycopg2.connect("dbname=lesson2.3 user=postgres password=nd$6482") as conn:
        with conn.cursor() as curs:
            for item in course_list:
                for dict_key, value in item.items():
                    curs.execute("select id from course where id=%s" % dict_key)
                    result_query = curs.fetchone()
                    if result_query is None:
                        curs.execute('insert into course(id, name) values(%s, %s)', (dict_key, value))


# возвращает студентов определенного курса
def get_students(course_id):
    with psycopg2.connect("dbname=lesson2.3 user=postgres password=nd$6482") as conn:
        with conn.cursor() as curs:
            curs.execute("select student.name, course.name from student join student_course on "
                         "student.id = student_course.student_id join course on "
                         "course.id = student_course.course_id where course.id = %s" % course_id)
            data = curs.fetchall()
            if data:
                for row in data:
                    print(f"На курсе '{row[1]}' обучается {row[0]}")
            else:
                print(f"На данном курсе никто не обучается!")


# создает студентов и  записывает их на курс
def add_students(course_id, students):
    with psycopg2.connect("dbname=lesson2.3 user=postgres password=nd$6482") as conn:
        with conn.cursor() as curs:
            for item in students:
                for dict_key in item.keys():
                    curs.execute("select id from student where id=%s" % item[dict_key]['id'])
                    result_query = curs.fetchone()
                    if result_query is None:
                        curs.execute('insert into student(id, name, gpa, birth) values(%s, %s, %s, %s)',
                                     (item[dict_key]['id'], item[dict_key]['name'], item[dict_key]['gpa'],
                                      item[dict_key]['birth']))
                    else:
                        print(f"Студент {item[dict_key]['name']} уже есть в базе")
                    curs.execute('select * from student_course where course_id=%s and student_id=%s;',
                                 (course_id, item[dict_key]['id']))
                    if not curs.fetchone():
                        curs.execute('insert into student_course(course_id, student_id) values(%s, %s)',
                                    (course_id, item[dict_key]['id']))
                    else:
                        print(f"Студент {item[dict_key]['name']} уже записан на курс")


# просто создает студента
def add_student(student):
    with psycopg2.connect("dbname=lesson2.3 user=postgres password=nd$6482") as conn:
        with conn.cursor() as curs:
            for item in student:
                for dict_key in item.keys():
                    curs.execute("select id from student where id=%s" % item[dict_key]['id'])
                    result_query = curs.fetchone()
                    if result_query is None:
                        curs.execute('insert into student(id, name, gpa, birth) values(%s, %s, %s, %s)',
                                     (item[dict_key]['id'], item[dict_key]['name'], item[dict_key]['gpa'],
                                      item[dict_key]['birth']))
                    else:
                        print(f"Студент {item[dict_key]['name']} уже есть в базе")


# получить информацию о студенте
def get_student(student_id):
    with psycopg2.connect("dbname=lesson2.3 user=postgres password=nd$6482") as conn:
        with conn.cursor() as curs:
            curs.execute("select student.name, student.gpa, student.birth, course.name from student join "
                         "student_course on student.id=student_course.student_id join course on "
                         "course.id=student_course.course_id where student_course.student_id=%s"  % student_id)
            result_query = curs.fetchall()
            if len(result_query) == 1:
                    print('Имя:', result_query[0][0])
                    print('Средняя оценка:', result_query[0][1])
                    print('Дата рождения:', result_query[0][2])
                    print('Курсы студента:', result_query[0][3])
            elif len(result_query) > 1:
                print('Имя:', result_query[0][0])
                print('Средняя оценка:', result_query[0][1])
                print('Дата рождения:', result_query[0][2])
                courses = ""
                for data in result_query:
                    courses += data[3] + ","
                print("Курсы студента:", courses.rstrip(","))
            else:
                print("Такого студента нет!")

            return curs.fetchall()


if __name__ == "__main__":
    # создать таблицы, если они не созданы
    create_db()
    # создать студента в таблице студентов
    add_student(list_of_students)
    # записать студентов на курс
    add_students(2, list_of_students)
    # добавить курс
    add_course(course_list)
    # получить информаци о студенте(данные, какие курсы проходит)
    get_student(7)
    # получить список студентов конкретного курса
    get_students(2)
