import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database.db import query_one, init_database_if_needed

# Import Route Blueprints
from routes.auth_routes import auth_bp
from routes.letter_routes import letter_bp
from routes.chatbot_routes import chatbot_bp
from routes.notification_routes import notification_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Izinkan CORS untuk koneksi Flutter mobile (Android/iOS) dan Web
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Pastikan folder penyimpanan tersedia
    for folder in [Config.UPLOAD_FOLDER, Config.SIGNATURES_FOLDER, Config.ATTACHMENTS_FOLDER, Config.LETTERS_FOLDER]:
        os.makedirs(folder, exist_ok=True)

    # Otomatis inisialisasi tabel basis data jika belum ada
    init_database_if_needed()

    # Registrasi Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(letter_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(notification_bp)

    @app.route('/')
    def root():
        return jsonify({
            'success': True,
            'message': 'Selamat datang di RTConnect Backend REST API',
            'version': '1.0.0',
            'rt_community': Config.RT_AREA,
            'endpoints': {
                'auth': '/api/v1/auth',
                'letters': '/api/v1/letters',
                'chatbot': '/api/v1/chatbot',
                'notifications': '/api/v1/notifications',
                'health': '/api/v1/health'
            }
        }), 200

    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        db_status = 'ok'
        try:
            query_one("SELECT 1")
        except Exception as e:
            db_status = f'error: {str(e)}'

        return jsonify({
            'success': db_status == 'ok',
            'message': 'RTConnect API Server Status',
            'data': {
                'status': 'healthy' if db_status == 'ok' else 'degraded',
                'database': db_status,
                'rt_unit': Config.RT_AREA
            },
            'error': None if db_status == 'ok' else 'DATABASE_ERROR'
        }), 200 if db_status == 'ok' else 503

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            'success': False,
            'message': 'Endpoint atau sumber daya yang diminta tidak ditemukan',
            'data': None,
            'error': 'NOT_FOUND'
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            'success': False,
            'message': 'Metode HTTP tidak diizinkan untuk endpoint ini',
            'data': None,
            'error': 'METHOD_NOT_ALLOWED'
        }), 405

    @app.errorhandler(500)
    def handle_server_error(e):
        return jsonify({
            'success': False,
            'message': 'Terjadi kesalahan internal pada server',
            'data': None,
            'error': 'INTERNAL_SERVER_ERROR'
        }), 500

    return app

# Expose app instance untuk WSGI / Gunicorn (Railway, Render, dll)
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"[*] Menjalankan RTConnect Backend di http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
