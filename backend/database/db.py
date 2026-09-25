import os
import pymysql
from pymysql.cursors import DictCursor
from urllib.parse import urlparse

def get_connection():
    # Support Railway / Cloud MYSQL_URL or DATABASE_URL
    database_url = os.getenv('MYSQL_URL') or os.getenv('DATABASE_URL')
    if database_url and (database_url.startswith('mysql://') or database_url.startswith('mysql+pymysql://')):
        parsed = urlparse(database_url)
        return pymysql.connect(
            host=parsed.hostname or '127.0.0.1',
            port=parsed.port or 3306,
            user=parsed.username or 'root',
            password=parsed.password or '',
            database=parsed.path.lstrip('/') or 'railway',
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )

    # Support Railway variables (MYSQLHOST, MYSQLPORT, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE)
    # as well as standard MYSQL_HOST and DB_HOST
    host = os.getenv('MYSQLHOST') or os.getenv('MYSQL_HOST') or os.getenv('DB_HOST', '127.0.0.1')
    port = int(os.getenv('MYSQLPORT') or os.getenv('MYSQL_PORT') or os.getenv('DB_PORT', 3306))
    user = os.getenv('MYSQLUSER') or os.getenv('MYSQL_USER') or os.getenv('DB_USER', 'root')
    password = os.getenv('MYSQLPASSWORD') or os.getenv('MYSQL_PASSWORD') or os.getenv('DB_PASSWORD', '')
    database = os.getenv('MYSQLDATABASE') or os.getenv('MYSQL_DB') or os.getenv('DB_NAME', 'rtconnect_db')

    try:
        return pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )
    except pymysql.err.OperationalError as e:
        # Error 1049: Unknown database. Try creating it if user has privileges (e.g., local dev)
        if len(e.args) > 0 and e.args[0] == 1049:
            temp_conn = pymysql.connect(
                host=host, port=port, user=user, password=password,
                charset='utf8mb4', autocommit=True
            )
            with temp_conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            temp_conn.close()
            return pymysql.connect(
                host=host, port=port, user=user, password=password,
                database=database, charset='utf8mb4', cursorclass=DictCursor, autocommit=True
            )
        raise

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

def init_database_if_needed():
    """Otomatis membuat tabel dan data awal jika basis data masih kosong"""
    try:
        query_one("SELECT 1 FROM users LIMIT 1")
        return
    except Exception as e:
        print(f"[*] Basis data belum diinisialisasi atau tabel users belum ada ({e}). Memulai inisialisasi...")

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(base_dir, 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    statements = schema_sql.split(';')
                    for stmt in statements:
                        clean_stmt = stmt.strip()
                        if not clean_stmt:
                            continue
                        upper = clean_stmt.upper()
                        # Lewati statement CREATE DATABASE dan USE agar kompatibel dengan Railway DB
                        if upper.startswith('CREATE DATABASE') or upper.startswith('USE '):
                            continue
                        try:
                            cursor.execute(clean_stmt)
                        except Exception as stmt_err:
                            print(f"[!] Warning executing statement: {stmt_err}")
                print("[+] Tabel basis data berhasil dibuat!")
            finally:
                conn.close()

            # Jalankan seeding data awal
            try:
                try:
                    from database.seed import seed_database
                except ImportError:
                    from seed import seed_database
                seed_database()
            except Exception as seed_err:
                print(f"[!] Seeding warning: {seed_err}")
    except Exception as init_err:
        print(f"[!] Gagal menginisialisasi skema basis data: {init_err}")
