import os
import bcrypt
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
from database.db import query_one, execute
from middleware.auth_middleware import generate_token, jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

@auth_bp.route('/register', methods=['POST'])
def register():
    """API-001: Pendaftaran akun warga baru"""
    # Dukung baik multipart/form-data maupun application/json
    if request.is_json:
        data = request.get_json() or {}
        sig_file = None
    else:
        data = request.form.to_dict()
        sig_file = request.files.get('tanda_tangan')

    nik = (data.get('nik') or '').strip()
    nama_lengkap = (data.get('nama_lengkap') or '').strip()
    email = (data.get('email') or '').strip()
    password = (data.get('password') or '').strip()
    nomor_telepon = (data.get('nomor_telepon') or '').strip()
    alamat = (data.get('alamat') or '').strip()

    # Validasi input
    if not (nik and nama_lengkap and email and password and nomor_telepon and alamat):
        return jsonify({
            'success': False,
            'message': 'Semua kolom data (NIK, Nama, Email, Password, No HP, Alamat) wajib diisi',
            'data': None,
            'error': 'VALIDATION_ERROR'
        }), 400

    if len(nik) != 16 or not nik.isdigit():
        return jsonify({
            'success': False,
            'message': 'NIK harus terdiri dari tepat 16 digit angka',
            'data': None,
            'error': 'INVALID_NIK'
        }), 400

    # Cek duplikasi NIK atau Email
    existing = query_one("SELECT user_id, nik, email FROM users WHERE nik = %s OR email = %s", (nik, email))
    if existing:
        field = "NIK" if existing['nik'] == nik else "Email"
        return jsonify({
            'success': False,
            'message': f'{field} tersebut sudah terdaftar dalam sistem RTConnect',
            'data': None,
            'error': 'DUPLICATE_ENTRY'
        }), 400

    # Simpan tanda tangan digital jika diunggah
    sig_path_rel = None
    if sig_file and sig_file.filename:
        filename = f"sig_{nik}_{secure_filename(sig_file.filename)}"
        save_path = os.path.join(Config.SIGNATURES_FOLDER, filename)
        sig_file.save(save_path)
        sig_path_rel = f"uploads/signatures/{filename}"
    else:
        sig_path_rel = 'uploads/signatures/warga_dafin_signature.png'

    pw_hash = hash_password(password)
    user_id = execute(
        """INSERT INTO users 
           (nik, nama_lengkap, email, password_hash, nomor_telepon, alamat, nomor_rt, nomor_rw, role, tanda_tangan_digital) 
           VALUES (%s, %s, %s, %s, %s, %s, '032', '08', 'warga', %s)""",
        (nik, nama_lengkap, email, pw_hash, nomor_telepon, alamat, sig_path_rel)
    )

    return jsonify({
        'success': True,
        'message': 'Registrasi berhasil, akun warga telah dibuat',
        'data': {
            'user_id': user_id,
            'nik': nik,
            'nama_lengkap': nama_lengkap,
            'role': 'warga'
        },
        'error': None
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """API-002: Login dengan Email/NIK dan Password"""
    data = request.get_json() or {}
    identity = (data.get('identity') or data.get('email') or '').strip()
    password = (data.get('password') or '').strip()

    if not identity or not password:
        return jsonify({
            'success': False,
            'message': 'Email/NIK dan Password wajib diisi',
            'data': None,
            'error': 'MISSING_CREDENTIALS'
        }), 400

    user = query_one(
        "SELECT user_id, nik, nama_lengkap, email, password_hash, nomor_telepon, alamat, nomor_rt, nomor_rw, role, is_active FROM users WHERE email = %s OR nik = %s",
        (identity, identity)
    )

    if not user or not check_password(password, user['password_hash']):
        return jsonify({
            'success': False,
            'message': 'Email/NIK atau password salah',
            'data': None,
            'error': 'UNAUTHORIZED'
        }), 401

    if not user['is_active']:
        return jsonify({
            'success': False,
            'message': 'Akun Anda telah dinonaktifkan oleh administrator',
            'data': None,
            'error': 'ACCOUNT_INACTIVE'
        }), 403

    token = generate_token(user['user_id'], user['role'], user['email'])

    return jsonify({
        'success': True,
        'message': 'Login berhasil',
        'data': {
            'token': token,
            'user': {
                'user_id': user['user_id'],
                'nama_lengkap': user['nama_lengkap'],
                'email': user['email'],
                'nik': user['nik'],
                'nomor_telepon': user['nomor_telepon'],
                'alamat': user['alamat'],
                'nomor_rt': user['nomor_rt'],
                'nomor_rw': user['nomor_rw'],
                'role': user['role']
            }
        },
        'error': None
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_current_user_profile():
    """API-003: Mendapatkan profil pengguna yang sedang login"""
    user = request.current_user
    return jsonify({
        'success': True,
        'message': 'Data profil berhasil diambil',
        'data': {
            'user_id': user['user_id'],
            'nik': user['nik'],
            'nama_lengkap': user['nama_lengkap'],
            'email': user['email'],
            'nomor_telepon': user['nomor_telepon'],
            'alamat': user['alamat'],
            'nomor_rt': user['nomor_rt'],
            'nomor_rw': user['nomor_rw'],
            'role': user['role'],
            'tanda_tangan_digital': user['tanda_tangan_digital']
        },
        'error': None
    }), 200
