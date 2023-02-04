import psycopg2
import os

try:
    DATABASE_URL = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL)
    print("Connection to DB successfully established.")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls")
    all_users = cursor.fetchall()
    cursor.close()  # закрываем курсор
    conn.close()  # закрываем соединение
    print(f"All urls: {all_users}")
except Exception as e:
    print("Can't establish connection to database.")
    print(f"Exception '{e}' type: {type(e)}")
