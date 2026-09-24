# RTConnect — Backend REST API & Database Service

Service backend resmi untuk sistem pelayanan administrasi rukun tetangga **RTConnect** (RT 032 / RW 08 Perumahan Griya Taman Asri). Dibangun menggunakan **Python Flask** dan terintegrasi langsung dengan database **MySQL 8.4 LTS**.

---

## 1. Arsitektur & Teknologi

- **Bahasa & Framework:** Python 3.14+, Flask, Flask-CORS
- **Database:** MySQL 8.4.3 LTS (Database `rtconnect_db`)
- **Konektor Basis Data:** PyMySQL dengan pooling koneksi otomatis
- **Autentikasi & Keamanan:** JSON Web Token (PyJWT, RS256/HS256, masa aktif 7 hari) & Bcrypt Password Hashing
- **Mesin Dokumen & TTD Digital (UC-09):** ReportLab PDF Builder dengan **tempelan gambar tanda tangan digital** (signature image scan overlay) resmi Ketua RT
- **Mesin AI Draf & RAG Chatbot (UC-05):** Formulasi draf otomatis surat pengantar + RAG retrieval berbasis Cosine Similarity & Indonesian Stemming dengan ambang batas kecocokan $\ge 0.70$ serta fallback eskalasi WhatsApp Ketua RT

---

## 2. Struktur Direktori

```text
backend/
├── app.py                     # Entry point server Flask & blueprint registration
├── config.py                  # Konfigurasi database, JWT, path direktori upload
├── requirements.txt           # Dependensi pustaka Python
├── test_api.py                # Suite pengujian otomatis mencakup seluruh 15 endpoint
├── database/
│   ├── db.py                  # Helper koneksi & query wrapper PyMySQL
│   ├── schema.sql             # Skema DDL 9 tabel MySQL
│   └── seed.py                # Seeder data awal (akun RT/warga, jenis surat, RAG knowledge)
├── middleware/
│   └── auth_middleware.py     # Decorator @jwt_required dan @roles_accepted
├── routes/
│   ├── auth_routes.py         # API-001 (Register), API-002 (Login), API-003 (Me)
│   ├── letter_routes.py       # API-004 s.d API-013 (Siklus lengkap pengajuan & PDF)
│   ├── chatbot_routes.py      # API-014 (RAG Tanya RT, sesi percakapan, riwayat pesan)
│   └── notification_routes.py # API-015 (Feed notifikasi & status baca)
├── services/
│   ├── ai_draft_service.py    # Formulasi draf surat resmi oleh sistem AI
│   ├── rag_service.py         # Retrieval Augmented Generation & WhatsApp escalation
│   └── pdf_service.py         # Generator PDF surat resmi dengan tempelan gambar TTD digital
└── uploads/
    ├── signatures/            # Tempat penyimpanan gambar tanda tangan digital (.png)
    ├── attachments/           # Berkas pendukung pengajuan warga
    └── generated_letters/     # Dokumen PDF surat resmi yang telah disahkan
```

---

## 3. Langkah Instalasi & Menjalankan

### A. Persiapan Lingkungan Virtual (Virtualenv)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### B. Inisialisasi Database MySQL
Pastikan MySQL service aktif pada port 3306, kemudian jalankan:
```powershell
$env:PYTHONPATH="database"
.\.venv\Scripts\python.exe database/seed.py
```

### C. Menjalankan Server REST API
```powershell
$env:PYTHONPATH=".;database"
.\.venv\Scripts\python.exe app.py
```
Server akan aktif di: `http://127.0.0.1:5000` (atau `http://10.0.2.2:5000` dari Android Emulator).

### D. Menjalankan Uji Coba Otomatis (Test Suite)
Untuk memverifikasi seluruh 15 endpoint dan alur bisnis end-to-end:
```powershell
$env:PYTHONPATH=".;database"
.\.venv\Scripts\python.exe test_api.py
```

---

## 4. Daftar Endpoint API (Sesuai `api.md`)

| Endpoint ID | Metode | Path | Hak Akses | Deskripsi |
|---|---|---|---|---|
| **API-001** | POST | `/api/v1/auth/register` | Publik | Pendaftaran akun warga + scan tanda tangan |
| **API-002** | POST | `/api/v1/auth/login` | Publik | Otentikasi Email/NIK & Password (JWT) |
| **API-003** | GET | `/api/v1/auth/me` | Auth | Ambil profil pengguna login & role |
| **API-004** | GET | `/api/v1/letters/types` | Auth | Daftar jenis surat & persyaratan |
| **API-005** | POST | `/api/v1/letters/apply` | Warga | Pengajuan surat baru & formulasi draf AI |
| **API-006** | GET | `/api/v1/letters/my-applications` | Warga | Riwayat permohonan surat warga |
| **API-007** | GET | `/api/v1/letters/incoming-queue` | RT | Antrean surat masuk untuk verifikasi RT |
| **API-008** | GET | `/api/v1/letters/:id` | Auth | Detail pengajuan surat & draf isi |
| **API-009** | PUT | `/api/v1/letters/:id/resubmit` | Warga | Pengajuan ulang setelah perbaikan revisi |
| **API-010** | POST | `/api/v1/letters/:id/decision` | RT | Keputusan RT: Setujui, Minta Revisi, Tolak |
| **API-011** | POST | `/api/v1/letters/:id/sign-digital` | RT | Otorisasi PIN RT & terbit PDF + TTD digital |
| **API-012** | POST | `/api/v1/letters/:id/confirm-physical` | RT | Otorisasi surat fisik siap diambil |
| **API-013** | GET | `/api/v1/letters/:id/download` | Auth | Unduh dokumen PDF resmi |
| **API-014** | POST | `/api/v1/chatbot/query` | Warga | Tanya RAG RT (similarity threshold 0.70) |
| **API-015** | GET | `/api/v1/notifications` | Auth | Feed notifikasi status pengajuan & eskalasi |

---

## 5. Kredensial Default Uji Coba

- **Ketua RT 032:**
  - Email: `rt032@rtconnect.id`
  - Password: `123456`
  - PIN Otorisasi TTD: `123456`
- **Warga RT 032:**
  - Email: `dafin@gmail.com`
  - Password: `123456`
