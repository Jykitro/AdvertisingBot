import logging
import os
import sqlite3
from datetime import datetime
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

# DEV t.me//ElonMuskSEO
def create_users_tables():
    with sqlite3.connect('database.db') as db:
        db.execute("""CREATE TABLE IF NOT EXISTS USERS (user_id INTEGER PRIMARY KEY NOT NULL,
                               username TEXT,
                               first_name TEXT,
                               last_name TEXT,
                               question_filled_out BOOLEAN DEFAULT False,
                               question_1 TEXT,
                               question_2 TEXT,
                               question_3 TEXT,
                               question_4 TEXT,
                               question_5 TEXT,
                               question_6 TEXT,
                               question_7 TEXT,
                               question_8 TEXT,
                               reg_date text
                               )"""
                   )
        print("Table created successfully")


def register_user(user_id, username, first_name, last_name):
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()
        current_date = datetime.now()
        user_check_query = cur.execute("SELECT * FROM USERS WHERE user_id = ?", (user_id,)).fetchall()
        if not user_check_query:
            logging.info(f"Registered * {username} * it to the database!")
            cur.execute(
                "INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, first_name, last_name, current_date))
            db.commit()


def check_filled_out(user_id):
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()
        profile_info_all = cur.execute('SELECT * FROM USERS WHERE user_id = ?', (user_id,)).fetchall()
        return profile_info_all[0][4]


def update_user(user_id, que1, que2, que3, que4, que5, que6, que7, que8):
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()
        cur.execute('''
            UPDATE USERS 
            SET question_1 = ?, question_2 = ?, question_3 = ?, question_4 = ?, question_5 = ?, question_6 = ?, 
            question_7 = ?, question_8 = ?, question_filled_out = TRUE
            WHERE user_id = ?
        ''', (que1, que2, que3, que4, que5, que6, que7, que8, user_id))


def all_user_id():
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()
        cur.execute("SELECT user_id FROM USERS")
        user_ids = cur.fetchall()
        # Вывод всех user_id
        # for user_id in user_ids:
        #     print(user_id[0])
        return user_ids


def get_amount_users():
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM Users")
        count = cur.fetchone()[0]
        return count


def get_today_user():
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()
        today = datetime.now().date()
        cur.execute("SELECT COUNT(*) FROM Users WHERE DATE(reg_date) = ?", (today,))
        count = cur.fetchone()[0]
        return count


def upload_dump():
    with sqlite3.connect(db_path) as db:
        query = "SELECT * FROM USERS"
        df = pd.read_sql_query(query, db)
        today = datetime.now().date()
        # Сохранение DataFrame в Excel файл
        df.to_excel(f"dump/{today}.xlsx", index=False, engine='openpyxl')
        logging.info("Данные успешно экспортированы в Excel.")
