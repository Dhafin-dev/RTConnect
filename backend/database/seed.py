import os
import bcrypt
from db import execute, query_one

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_database():
    print("=== Memulai seeding data RTConnect ke MySQL ===")

    # 1. Master Jenis Surat
    surat_types = [
        ('DOM', 'Surat Keterangan Domisili', 'Surat Keterangan Domisili Warga RT 032 RW 08 Griya Taman Asri', 'KTP dan Bukti Tempat Tinggal (PBB/Sewa)'),
        ('KTP', 'Surat Pengantar KTP Baru / Perpanjangan', 'Surat Pengantar Pengurusan KTP-el ke Kelurahan/Kecamatan', 'Fotokopi Kartu Keluarga dan KTP Lama'),
        ('SKCK', 'Surat Pengantar SKCK', 'Surat Pengantar Pembuatan Catatan Kepolisian', 'KTP Asli dan Kartu Keluarga'),
        ('SKU', 'Surat Keterangan Usaha', 'Surat Keterangan Domisili Usaha Mikro Warga', 'Foto Tempat Usaha dan KTP Pemilik')
    ]

    for kode, nama, template, syarat in surat_types:
        existing = query_one("SELECT jenis_surat_id FROM jenis_surat WHERE kode_surat = %s", (kode,))
        if not existing:
            execute(
                "INSERT INTO jenis_surat (kode_surat, nama_surat, template_dokumen, persyaratan_dokumen) VALUES (%s, %s, %s, %s)",
                (kode, nama, template, syarat)
            )
            print(f"  [+] Jenis Surat: {nama}")

    # 2. Akun Pengguna Default (Ketua RT & Warga)
    default_users = [
        (
            '3515080101800001',
            'Pak RT Indra',
            'rt032@rtconnect.id',
            hash_password('123456'),
            '081234567890',
            'Griya Taman Asri Blok B-01',
            'rt',
            'uploads/signatures/rt_indra_signature.png'
        ),
        (
            '3515082405020002',
            'Ahmad Dhafin Al Farisy',
            'dafin@gmail.com',
            hash_password('123456'),
            '089876543210',
            'Griya Taman Asri Blok D-14',
            'warga',
            'uploads/signatures/warga_dafin_signature.png'
        )
    ]

    for nik, nama, email, pw_hash, phone, alamat, role, ttd in default_users:
        existing = query_one("SELECT user_id FROM users WHERE email = %s OR nik = %s", (email, nik))
        if not existing:
            execute(
                """INSERT INTO users 
                   (nik, nama_lengkap, email, password_hash, nomor_telepon, alamat, role, tanda_tangan_digital) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (nik, nama, email, pw_hash, phone, alamat, role, ttd)
            )
            print(f"  [+] User: {nama} ({role.upper()})")

    # 3. Knowledge Base untuk RAG Chatbot Tanya RT
    rt_user = query_one("SELECT user_id FROM users WHERE role = 'rt' LIMIT 1")
    rt_id = rt_user['user_id'] if rt_user else None

    bylaws = [
        (
            'Pedoman Tata Tertib & Layanan Surat RT 032',
            'administrasi',
            '1. Surat pengantar RT 032 berlaku selama 30 hari kalender sejak tanggal pengesahan.\n'
            '2. Untuk pembuatan surat domisili, warga wajib menyiapkan KTP asli dan bukti tempat tinggal.\n'
            '3. Warga yang mengurus surat keterangan usaha (SKU) wajib melampirkan foto tempat usaha fisik.\n'
            '4. Pelayanan surat tanda tangan basah dapat diambil di rumah Ketua RT pada jam 18.30 - 21.00 WIB setiap hari kerja.'
        ),
        (
            'Ketentuan Iuran Lingkungan & Fasilitas Umum',
            'fasum',
            '1. Iuran kas kebersihan dan keamanan RT 032 dibayarkan paling lambat tanggal 10 setiap bulannya.\n'
            '2. Penggunaan Balai Warga RT untuk hajatan atau acara warga wajib melapor kepada Ketua RT minimal 7 hari sebelumnya.\n'
            '3. Kerja bakti saluran air dan kebersihan lingkungan dilaksanakan setiap hari Minggu pertama awal bulan.'
        )
    ]

    for judul, kategori, isi in bylaws:
        existing = query_one("SELECT knowledge_id FROM knowledge_base WHERE judul_dokumen = %s", (judul,))
        if not existing:
            kb_id = execute(
                "INSERT INTO knowledge_base (judul_dokumen, kategori, isi_dokumen, diunggah_oleh_rt) VALUES (%s, %s, %s, %s)",
                (judul, kategori, isi, rt_id)
            )
            print(f"  [+] Knowledge Base: {judul}")

            # Chunking Dokumen
            lines = [line.strip() for line in isi.split('\n') if line.strip()]
            for idx, chunk in enumerate(lines):
                execute(
                    "INSERT INTO knowledge_chunks (knowledge_id, urutan_chunk, isi_chunk, kata_kunci) VALUES (%s, %s, %s, %s)",
                    (kb_id, idx + 1, chunk, judul)
                )

    print("[SUCCESS] Seeding basis data RTConnect berhasil!")

if __name__ == '__main__':
    seed_database()
