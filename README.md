# RTConnect — Aplikasi Administrasi Warga RT/RW

RTConnect adalah aplikasi Flutter dengan REST API Flask dan database MySQL untuk membantu warga mengajukan surat, memeriksa status permohonan, dan mencari informasi tata tertib RT.

Fitur utama:

1. **Pengajuan surat digital:** Draf narasi dibuat dari template deterministik yang dapat ditinjau Ketua RT.
2. **Verifikasi surat:** Alur tanda tangan digital berbasis gambar dan tanda tangan basah.
3. **Tanya RT:** Pencarian leksikal dalam knowledge base dengan eskalasi ke WhatsApp jika jawaban tidak ditemukan.

Draf surat tidak menggunakan model generatif. Tanya RT memakai cosine similarity atas kata dan stemming sederhana; skornya heuristik, bukan confidence model. Bucket file production harus privat. PDF saat ini menampilkan gambar tanda tangan dan belum memiliki tanda tangan kriptografis pada byte PDF.

## Arsitektur

```text
Client       : Flutter / Dart
State        : Riverpod
Navigation   : GoRouter
Networking   : Dio REST client
Backend      : Flask / Gunicorn
Database     : MySQL 8.4+
File storage : Local for development; private S3-compatible bucket for production
Draft/search : Deterministic template and lexical retrieval
```

Production builds use an HTTPS API URL injected with `--dart-define=API_BASE_URL=...`. Release clients reject non-HTTPS API addresses. Development Android emulators default to `10.0.2.2`; physical devices need a reachable development API URL.

## Menjalankan Secara Lokal

1. Salin `.env.example` menjadi `.env` dan ganti password lokal.
2. Jalankan `docker compose up --build`.
3. Buat akun Ketua RT melalui `docker compose exec api python -m database.create_rt_user`.
4. Jalankan aplikasi Flutter dan daftarkan akun warga.

## Deployment Publik

Panduan untuk container host, MySQL terkelola dengan TLS, bucket objek privat, domain HTTPS, CORS Flutter Web, dan build Android ada di [DEPLOYMENT.md](DEPLOYMENT.md).

Satu deployment saat ini melayani satu komunitas RT/RW. Deployment publik bisa diakses pengguna di berbagai lokasi, tetapi aplikasi belum mendukung banyak komunitas dalam satu database.

## Diagram UML

Diagram tersedia pada folder [`assets/diagrams/`](assets/diagrams/):

- Use Case Diagram
- Sequence Diagram Login dan Register
- Sequence Diagram Pengajuan Surat
- Sequence Diagram Chatbot Tanya RT
- Activity Diagram Surat Pengantar
- Activity Diagram Chatbot Tanya RT

## Pengembang

Kelompok 3 — Praktikum PPL I1 UNAIR 2026, Program Studi Sistem Informasi, Fakultas Sains dan Teknologi, Universitas Airlangga.

- Muhammad Nafidz Arradhin
- Mirza Diwa Luscakson
- Febrian Muhammad Yudhistira
- Ahmad Dhafin Al Farisy

Perencanaan dan spesifikasi proyek tersimpan di `RTConnect-KnowledgeBase/`.
