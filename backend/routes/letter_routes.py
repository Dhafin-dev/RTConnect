import os
import random
import datetime
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from config import Config
from database.db import query_all, query_one, execute
from middleware.auth_middleware import jwt_required, roles_accepted
from services.ai_draft_service import generate_letter_draft
from services.pdf_service import generate_official_letter_pdf

letter_bp = Blueprint('letters', __name__, url_prefix='/api/v1/letters')

def generate_nomor_pengajuan() -> str:
    year = datetime.datetime.now().year
    rand_id = random.randint(10000, 99999)
    return f"SRT-{year}-{rand_id}"

def generate_nomor_surat_resmi(jenis_kode: str) -> str:
    now = datetime.datetime.now()
    roman_months = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
    month_roman = roman_months[now.month - 1]
    rand_seq = random.randint(100, 999)
    return f"032/08/GTA/{jenis_kode}/{rand_seq}/{month_roman}/{now.year}"

@letter_bp.route('/types', methods=['GET'])
@jwt_required
def get_letter_types():
    """API-004: Mengambil daftar jenis surat yang tersedia"""
    types = query_all("SELECT jenis_surat_id, kode_surat, nama_surat, template_dokumen, persyaratan_dokumen FROM jenis_surat WHERE is_aktif = 1")
    return jsonify({
        'success': True,
        'message': 'Daftar jenis surat berhasil diambil',
        'data': types,
        'error': None
    }), 200

@letter_bp.route('/apply', methods=['POST'])
@jwt_required
@roles_accepted('warga')
def apply_letter():
    """API-005: Warga mengajukan permohonan surat pengantar baru"""
    user = request.current_user
    
    if request.is_json:
        data = request.get_json() or {}
        lampiran_file = None
    else:
        data = request.form.to_dict()
        lampiran_file = request.files.get('lampiran')

    jenis_surat_id = data.get('jenis_surat_id')
    keperluan = (data.get('keperluan') or '').strip()
    metode_tanda_tangan = data.get('metode_tanda_tangan', 'digital')

    if not jenis_surat_id or not keperluan:
        return jsonify({
            'success': False,
            'message': 'Jenis surat dan rincian keperluan permohonan wajib diisi',
            'data': None,
            'error': 'VALIDATION_ERROR'
        }), 400

    jenis = query_one("SELECT * FROM jenis_surat WHERE jenis_surat_id = %s", (jenis_surat_id,))
    if not jenis:
        return jsonify({
            'success': False,
            'message': 'Jenis surat tidak valid atau tidak ditemukan',
            'data': None,
            'error': 'NOT_FOUND'
        }), 404

    # Simpan lampiran jika ada
    lampiran_url = None
    if lampiran_file and lampiran_file.filename:
        filename = f"att_{user['nik']}_{secure_filename(lampiran_file.filename)}"
        save_path = os.path.join(Config.ATTACHMENTS_FOLDER, filename)
        lampiran_file.save(save_path)
        lampiran_url = f"uploads/attachments/{filename}"

    # Formulasi Draf AI Otomatis
    draf_ai = generate_letter_draft(user, jenis, keperluan)
    nomor_pengajuan = generate_nomor_pengajuan()

    pengajuan_id = execute(
        """INSERT INTO pengajuan_surat 
           (nomor_pengajuan, warga_id, jenis_surat_id, keperluan, metode_tanda_tangan, berkas_lampiran_url, draf_ai_konten, status)
           VALUES (%s, %s, %s, %s, %s, %s, %s, 'diajukan')""",
        (nomor_pengajuan, user['user_id'], jenis_surat_id, keperluan, metode_tanda_tangan, lampiran_url, draf_ai)
    )

    # Tambah Notifikasi untuk Ketua RT
    rt_user = query_one("SELECT user_id FROM users WHERE role = 'rt' LIMIT 1")
    if rt_user:
        execute(
            """INSERT INTO notifikasi (penerima_id, tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan)
               VALUES (%s, 'pengajuan_baru', %s, %s, %s)""",
            (
                rt_user['user_id'],
                'Pengajuan Surat Baru',
                f"Pengajuan {jenis['nama_surat']} baru dari {user['nama_lengkap']}",
                f"/letters/{pengajuan_id}"
            )
        )

    return jsonify({
        'success': True,
        'message': 'Pengajuan berhasil dikirim dan draf surat sedang disiapkan',
        'data': {
            'pengajuan_id': pengajuan_id,
            'nomor_pengajuan': nomor_pengajuan,
            'status': 'diajukan',
            'draf_ai': draf_ai,
            'tanggal_pengajuan': datetime.datetime.now().isoformat()
        },
        'error': None
    }), 201

@letter_bp.route('/my-applications', methods=['GET'])
@jwt_required
@roles_accepted('warga')
def get_my_applications():
    """API-006: Mengambil riwayat pengajuan surat milik warga yang login"""
    user_id = request.current_user['user_id']
    applications = query_all(
        """SELECT p.pengajuan_id, p.nomor_pengajuan, p.keperluan, p.metode_tanda_tangan, 
                  p.status, p.catatan_revisi, p.alasan_penolakan, p.tanggal_pengajuan, p.tanggal_selesai,
                  j.nama_surat, j.kode_surat,
                  sf.nomor_surat_resmi, sf.surat_final_id
           FROM pengajuan_surat p
           JOIN jenis_surat j ON p.jenis_surat_id = j.jenis_surat_id
           LEFT JOIN surat_final sf ON p.pengajuan_id = sf.pengajuan_id
           WHERE p.warga_id = %s
           ORDER BY p.tanggal_pengajuan DESC""",
        (user_id,)
    )

    return jsonify({
        'success': True,
        'message': 'Riwayat pengajuan berhasil diambil',
        'data': applications,
        'error': None
    }), 200

@letter_bp.route('/incoming-queue', methods=['GET'])
@jwt_required
@roles_accepted('rt', 'admin')
def get_incoming_queue():
    """API-007: Mengambil antrean surat masuk untuk verifikasi Ketua RT"""
    queue = query_all(
        """SELECT p.pengajuan_id, p.nomor_pengajuan, p.keperluan, p.metode_tanda_tangan, 
                  p.status, p.tanggal_pengajuan, p.catatan_revisi,
                  u.user_id as warga_id, u.nama_lengkap, u.nik, u.alamat, u.nomor_telepon,
                  j.nama_surat, j.kode_surat
           FROM pengajuan_surat p
           JOIN users u ON p.warga_id = u.user_id
           JOIN jenis_surat j ON p.jenis_surat_id = j.jenis_surat_id
           ORDER BY 
             CASE p.status
               WHEN 'diajukan' THEN 1
               WHEN 'perlu_revisi' THEN 2
               WHEN 'disetujui' THEN 3
               ELSE 4
             END,
             p.tanggal_pengajuan DESC"""
    )

    return jsonify({
        'success': True,
        'message': 'Antrean surat masuk berhasil diambil',
        'data': queue,
        'error': None
    }), 200

@letter_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_application_detail(id: int):
    """API-008: Mengambil detail permohonan surat dan draf AI"""
    user = request.current_user

    app_data = query_one(
        """SELECT p.*, 
                  u.nama_lengkap, u.nik, u.alamat, u.nomor_telepon, u.nomor_rt, u.nomor_rw,
                  j.nama_surat, j.kode_surat, j.template_dokumen,
                  sf.nomor_surat_resmi, sf.status_pengesahan, sf.tanggal_terbit, sf.file_pdf_path
           FROM pengajuan_surat p
           JOIN users u ON p.warga_id = u.user_id
           JOIN jenis_surat j ON p.jenis_surat_id = j.jenis_surat_id
           LEFT JOIN surat_final sf ON p.pengajuan_id = sf.pengajuan_id
           WHERE p.pengajuan_id = %s""",
        (id,)
    )

    if not app_data:
        return jsonify({
            'success': False,
            'message': 'Pengajuan surat tidak ditemukan',
            'data': None,
            'error': 'NOT_FOUND'
        }), 404

    # Warga hanya dapat melihat pengajuan miliknya sendiri
    if user['role'] == 'warga' and app_data['warga_id'] != user['user_id']:
        return jsonify({
            'success': False,
            'message': 'Akses ditolak: Anda tidak memiliki akses ke pengajuan ini',
            'data': None,
            'error': 'FORBIDDEN'
        }), 403

    return jsonify({
        'success': True,
        'message': 'Detail pengajuan berhasil diambil',
        'data': app_data,
        'error': None
    }), 200

@letter_bp.route('/<int:id>/resubmit', methods=['PUT'])
@jwt_required
@roles_accepted('warga')
def resubmit_application(id: int):
    """API-009: Warga mengajukan ulang revisi dokumen surat"""
    user = request.current_user
    app_data = query_one("SELECT * FROM pengajuan_surat WHERE pengajuan_id = %s", (id,))

    if not app_data:
        return jsonify({'success': False, 'message': 'Pengajuan tidak ditemukan', 'data': None, 'error': 'NOT_FOUND'}), 404

    if app_data['warga_id'] != user['user_id']:
        return jsonify({'success': False, 'message': 'Akses ditolak', 'data': None, 'error': 'FORBIDDEN'}), 403

    data = request.form.to_dict() if not request.is_json else (request.get_json() or {})
    keperluan = data.get('keperluan', app_data['keperluan'])

    jenis = query_one("SELECT * FROM jenis_surat WHERE jenis_surat_id = %s", (app_data['jenis_surat_id'],))
    new_draft = generate_letter_draft(user, jenis, keperluan)

    execute(
        """UPDATE pengajuan_surat 
           SET keperluan = %s, draf_ai_konten = %s, status = 'diajukan', catatan_revisi = NULL 
           WHERE pengajuan_id = %s""",
        (keperluan, new_draft, id)
    )

    return jsonify({
        'success': True,
        'message': 'Pengajuan telah berhasil diperbarui dan diajukan kembali ke RT',
        'data': {'pengajuan_id': id, 'status': 'diajukan', 'draf_ai': new_draft},
        'error': None
    }), 200

@letter_bp.route('/<int:id>/decision', methods=['POST'])
@jwt_required
@roles_accepted('rt', 'admin')
def submit_decision(id: int):
    """API-010: Keputusan evaluasi Ketua RT (approve / revise / reject)"""
    data = request.get_json() or {}
    action = data.get('action') # 'approve', 'revise', 'reject'
    catatan = (data.get('catatan') or data.get('alasan') or '').strip()

    if action not in ['approve', 'revise', 'reject']:
        return jsonify({
            'success': False,
            'message': "Action harus salah satu dari: 'approve', 'revise', atau 'reject'",
            'data': None,
            'error': 'INVALID_ACTION'
        }), 400

    app_data = query_one(
        "SELECT p.*, j.kode_surat FROM pengajuan_surat p JOIN jenis_surat j ON p.jenis_surat_id = j.jenis_surat_id WHERE p.pengajuan_id = %s",
        (id,)
    )
    if not app_data:
        return jsonify({'success': False, 'message': 'Pengajuan surat tidak ditemukan', 'data': None, 'error': 'NOT_FOUND'}), 404

    now = datetime.datetime.now()
    rt_user = request.current_user

    if action == 'approve':
        status = 'disetujui'
        nomor_resmi = generate_nomor_surat_resmi(app_data['kode_surat'])
        execute(
            "UPDATE pengajuan_surat SET status = %s, rt_id = %s, tanggal_diverifikasi = %s WHERE pengajuan_id = %s",
            (status, rt_user['user_id'], now, id)
        )
        # Notifikasi Warga
        execute(
            """INSERT INTO notifikasi (penerima_id, tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan)
               VALUES (%s, 'surat_disetujui', 'Surat Pengantar Disetujui', %s, %s)""",
            (app_data['warga_id'], f"Surat Anda {app_data['nomor_pengajuan']} telah disetujui oleh Ketua RT", f"/letters/{id}")
        )
        return jsonify({
            'success': True,
            'message': 'Pengajuan berhasil disetujui',
            'data': {'pengajuan_id': id, 'status': status, 'nomor_surat_resmi': nomor_resmi},
            'error': None
        }), 200

    elif action == 'revise':
        if not catatan:
            return jsonify({'success': False, 'message': 'Catatan perbaikan wajib diisi jika meminta revisi', 'data': None, 'error': 'NOTE_REQUIRED'}), 400
        status = 'perlu_revisi'
        execute(
            "UPDATE pengajuan_surat SET status = %s, catatan_revisi = %s, rt_id = %s WHERE pengajuan_id = %s",
            (status, catatan, rt_user['user_id'], id)
        )
        # Notifikasi Warga
        execute(
            """INSERT INTO notifikasi (penerima_id, tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan)
               VALUES (%s, 'perlu_revisi', 'Pengajuan Perlu Revisi', %s, %s)""",
            (app_data['warga_id'], f"Catatan Pak RT: {catatan}", f"/letters/{id}")
        )
        return jsonify({
            'success': True,
            'message': 'Permintaan revisi berhasil dikirim ke warga',
            'data': {'pengajuan_id': id, 'status': status, 'catatan_revisi': catatan},
            'error': None
        }), 200

    else: # reject
        if not catatan:
            return jsonify({'success': False, 'message': 'Alasan penolakan wajib diisi', 'data': None, 'error': 'REASON_REQUIRED'}), 400
        status = 'ditolak'
        execute(
            "UPDATE pengajuan_surat SET status = %s, alasan_penolakan = %s, rt_id = %s, tanggal_diverifikasi = %s WHERE pengajuan_id = %s",
            (status, catatan, rt_user['user_id'], now, id)
        )
        # Notifikasi Warga
        execute(
            """INSERT INTO notifikasi (penerima_id, tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan)
               VALUES (%s, 'surat_ditolak', 'Pengajuan Surat Ditolak', %s, %s)""",
            (app_data['warga_id'], f"Alasan: {catatan}", f"/letters/{id}")
        )
        return jsonify({
            'success': True,
            'message': 'Pengajuan surat telah ditolak',
            'data': {'pengajuan_id': id, 'status': status, 'alasan_penolakan': catatan},
            'error': None
        }), 200

@letter_bp.route('/<int:id>/sign-digital', methods=['POST'])
@jwt_required
@roles_accepted('rt', 'admin')
def sign_digital(id: int):
    """
    API-011: Otorisasi digital PIN Ketua RT & pembuatan dokumen PDF resmi 
    dengan tempelan gambar tanda tangan digital (UC-09).
    """
    data = request.get_json() or {}
    pin = str(data.get('pin', '')).strip()

    if pin != Config.DEFAULT_RT_PIN:
        return jsonify({
            'success': False,
            'message': 'PIN Otorisasi Ketua RT salah',
            'data': None,
            'error': 'INVALID_PIN'
        }), 401

    app_data = query_one(
        """SELECT p.*, j.kode_surat, j.nama_surat,
                  u.nama_lengkap, u.nik, u.nomor_telepon, u.alamat, u.nomor_rt, u.nomor_rw
           FROM pengajuan_surat p
           JOIN jenis_surat j ON p.jenis_surat_id = j.jenis_surat_id
           JOIN users u ON p.warga_id = u.user_id
           WHERE p.pengajuan_id = %s""",
        (id,)
    )

    if not app_data:
        return jsonify({'success': False, 'message': 'Pengajuan surat tidak ditemukan', 'data': None, 'error': 'NOT_FOUND'}), 404

    rt_user = request.current_user
    nomor_resmi = generate_nomor_surat_resmi(app_data['kode_surat'])

    # Buat PDF resmi dengan tempelan gambar tanda tangan digital
    pdf_filename = f"Surat_{app_data['nomor_pengajuan']}_{id}.pdf"
    pdf_path = generate_official_letter_pdf(
        application=app_data,
        resident=app_data,
        letter_type={'nama_surat': app_data['nama_surat'], 'kode_surat': app_data['kode_surat']},
        official_letter_number=nomor_resmi,
        rt_user=rt_user,
        output_filename=pdf_filename
    )

    rel_pdf_path = f"uploads/generated_letters/{pdf_filename}"
    token_verif = f"SIGN-RT032-{app_data['nomor_pengajuan']}-{random.randint(1000, 9999)}"

    # Simpan atau update ke tabel surat_final
    existing_sf = query_one("SELECT surat_final_id FROM surat_final WHERE pengajuan_id = %s", (id,))
    if existing_sf:
        execute(
            """UPDATE surat_final 
               SET nomor_surat_resmi = %s, file_pdf_path = %s, qr_verification_token = %s, status_pengesahan = 'digital_sah' 
               WHERE pengajuan_id = %s""",
            (nomor_resmi, rel_pdf_path, token_verif, id)
        )
    else:
        execute(
            """INSERT INTO surat_final (pengajuan_id, nomor_surat_resmi, file_pdf_path, qr_verification_token, status_pengesahan)
               VALUES (%s, %s, %s, %s, 'digital_sah')""",
            (id, nomor_resmi, rel_pdf_path, token_verif)
        )

    # Perbarui status pengajuan menjadi selesai
    now = datetime.datetime.now()
    execute(
        "UPDATE pengajuan_surat SET status = 'selesai', tanggal_selesai = %s, rt_id = %s WHERE pengajuan_id = %s",
        (now, rt_user['user_id'], id)
    )

    # Kirim notifikasi warga
    execute(
        """INSERT INTO notifikasi (penerima_id, tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan)
           VALUES (%s, 'surat_disetujui', 'Surat Selesai Ditandatangani', %s, %s)""",
        (app_data['warga_id'], f"Surat {app_data['nama_surat']} Anda telah selesai dan siap diunduh.", f"/letters/{id}/download")
    )

    return jsonify({
        'success': True,
        'message': 'Tanda tangan digital berhasil disematkan',
        'data': {
            'pengajuan_id': id,
            'status': 'selesai',
            'nomor_surat_resmi': nomor_resmi,
            'pdf_url': f"/api/v1/letters/{id}/download",
            'signature_type': 'tempelan_gambar_tanda_tangan_digital'
        },
        'error': None
    }), 200

@letter_bp.route('/<int:id>/confirm-physical', methods=['POST'])
@jwt_required
@roles_accepted('rt', 'admin')
def confirm_physical(id: int):
    """API-012: Otorisasi status tanda tangan basah & siap diambil di kediaman RT"""
    app_data = query_one("SELECT * FROM pengajuan_surat WHERE pengajuan_id = %s", (id,))
    if not app_data:
        return jsonify({'success': False, 'message': 'Pengajuan tidak ditemukan', 'data': None, 'error': 'NOT_FOUND'}), 404

    rt_user = request.current_user
    execute("UPDATE pengajuan_surat SET status = 'siap_diambil', rt_id = %s WHERE pengajuan_id = %s", (rt_user['user_id'], id))

    # Notifikasi Warga
    execute(
        """INSERT INTO notifikasi (penerima_id, tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan)
           VALUES (%s, 'surat_siap_diambil', 'Surat Siap Diambil', %s, %s)""",
        (app_data['warga_id'], "Surat fisik bertanda tangan basah telah selesai dan siap diambil di kediaman Pak RT.", f"/letters/{id}")
    )

    return jsonify({
        'success': True,
        'message': 'Status surat fisik berhasil diubah menjadi siap diambil',
        'data': {'pengajuan_id': id, 'status': 'siap_diambil'},
        'error': None
    }), 200

@letter_bp.route('/<int:id>/download', methods=['GET'])
@jwt_required
def download_letter_pdf(id: int):
    """API-013: Mengunduh file PDF resmi yang telah disahkan"""
    user = request.current_user
    app_data = query_one("SELECT * FROM pengajuan_surat WHERE pengajuan_id = %s", (id,))
    if not app_data:
        return jsonify({'success': False, 'message': 'Pengajuan surat tidak ditemukan', 'data': None, 'error': 'NOT_FOUND'}), 404

    if user['role'] == 'warga' and app_data['warga_id'] != user['user_id']:
        return jsonify({'success': False, 'message': 'Akses ditolak', 'data': None, 'error': 'FORBIDDEN'}), 403

    sf = query_one("SELECT * FROM surat_final WHERE pengajuan_id = %s", (id,))
    if not sf or not sf['file_pdf_path']:
        return jsonify({'success': False, 'message': 'Dokumen PDF surat belum disahkan atau belum tersedia', 'data': None, 'error': 'NOT_FOUND'}), 404

    rel_path = sf['file_pdf_path']
    full_path = os.path.join(Config.BASE_DIR, rel_path) if not os.path.isabs(rel_path) else rel_path

    if not os.path.exists(full_path):
        return jsonify({'success': False, 'message': 'File fisik PDF tidak ditemukan di server', 'data': None, 'error': 'FILE_NOT_FOUND'}), 404

    filename = os.path.basename(full_path)
    return send_file(full_path, mimetype='application/pdf', as_attachment=True, download_name=filename)
