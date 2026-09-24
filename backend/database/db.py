import os
import pymysql
from pymysql.cursors import DictCursor

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', os.getenv('DB_HOST', '127.0.0.1')),
        port=int(os.getenv('MYSQL_PORT', os.getenv('DB_PORT', 3306))),
        user=os.getenv('MYSQL_USER', os.getenv('DB_USER', 'root')),
        password=os.getenv('MYSQL_PASSWORD', os.getenv('DB_PASSWORD', '')),
        database=os.getenv('MYSQL_DB', os.getenv('DB_NAME', 'rtconnect_db')),
        charset='utf8mb4',
        cursorclass=DictCursor,
        autocommit=True
    )

def query_all(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
    finally:
        conn.close()

def query_one(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchone()
    finally:
        conn.close()

def execute(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            last_id = cursor.lastrowid
            return last_id
    finally:
        conn.close()
