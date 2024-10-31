import psycopg2
from decouple import config

db_url = config('DB_URL')
host = config('HOST')
port = config('PORT')
user = config('USER')
password = config('PASSWORD')
database = config('DB_NAME')

conn = psycopg2.connect(dbname=database, user=user, password=password, host=host, port=port)
conn.autocommit = True

def create_table():
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INT8 NOT NULL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        age INT8 NOT NULL,
                        gender VARCHAR(255) NOT NULL,
                        aim VARCHAR(255));""")

def insert(id, test_dict):
    if check_primary(id):
        with conn.cursor() as cursor:
            cursor.execute(f"""INSERT INTO users(id, name, age, gender, aim)
                        VALUES ({id},'{test_dict["name"]}',
                        {test_dict["age"]},
                        '{test_dict["gender"]}',
                        '{test_dict["aim"]}');""")
    else:
        with conn.cursor() as cursor:
            cursor.execute(f"""UPDATE users SET id = {id}, name = '{test_dict["name"]}', age = {test_dict["age"]},
                        gender = '{test_dict["gender"]}', aim = '{test_dict["aim"]}'
                        WHERE id = {id};""")

def check_primary(id):
    with conn.cursor() as cursor:
        cursor.execute(f"""SELECT id FROM users;""")
        p = cursor.fetchall()
        if p == None:
            return True
        lst = [int(i[0]) for i in p]
    return True if id not in lst else False

def delete_user(id):
    with conn.cursor() as cursor:
        cursor.execute(f"""DELETE FROM users WHERE id = {id}""")

def print_data(id):
    with conn.cursor() as cursor:
        cursor.execute(f"""SELECT name, age, gender, aim FROM users WHERE id = {id};""")
        return cursor.fetchone()

def age_procent(num):
    with conn.cursor() as cursor:
        cursor.execute(f"""SELECT ROUND(COUNT(CASE WHEN age = {num} THEN 1 END) * 100.0 / count(*), 2) AS fraction FROM users;""")
        procent_age = cursor.fetchone()[0]
        return int(procent_age)

def gender_procent(st):
    with conn.cursor() as cursor:
        cursor.execute(f"""SELECT ROUND(COUNT(CASE WHEN gender = '{st}' THEN 1 END) * 100.0 / COUNT(*), 2) AS fraction FROM users;""")
        procent_gender = cursor.fetchone()[0]
        return int(procent_gender)