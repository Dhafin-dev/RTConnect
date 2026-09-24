import os
from dotenv import load_dotenv

# Muat variabel environment dari .env jika ada
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    BASE_DIR = BASE_DIR

    # Konfigurasi Database MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'rtconnect_db')

    # Keamanan JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'rtconnect_jwt_secret_key_rt032_gta_2026')
    JWT_EXPIRATION_DAYS = 7

    # Direktori Upload & File
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    SIGNATURES_FOLDER = os.path.join(UPLOAD_FOLDER, 'signatures')
    ATTACHMENTS_FOLDER = os.path.join(UPLOAD_FOLDER, 'attachments')
    LETTERS_FOLDER = os.path.join(UPLOAD_FOLDER, 'generated_letters')

    # Pengaturan RAG & Chatbot Tanya RT
    RAG_SIMILARITY_THRESHOLD = 0.70
    RT_WHATSAPP_NUMBER = '6281234567890'
    RT_NAME = 'Pak RT Indra'
    RT_AREA = 'RT 032 / RW 08 Griya Taman Asri'

    # PIN Otorisasi Digital Ketua RT
    DEFAULT_RT_PIN = '123456'
