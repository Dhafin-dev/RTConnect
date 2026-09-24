# MySQL Database Specification — RTConnect

This document details the persistent relational database architecture for the RTConnect system using MySQL 8.0+ / 8.4 LTS. It resolves historical schema separation discrepancies and establishes a unified, normalized, and performant data store.

---

## 1. Database Overview
- **RDBMS Engine:** MySQL 8.0+ / 8.4 LTS (InnoDB Storage Engine). [CONFIRMED]
- **Character Set / Collation:** `utf8mb4` / `utf8mb4_unicode_ci` (Full Unicode support for emojis, special characters, and Indonesian text).
- **Architecture Strategy:** Centralized Unified User model (`users`) to resolve role inheritance between Warga and RT, linked to application tracking, document management, and RAG knowledge indexing.

---

## 2. Entity Inventory

| Entity ID | Table Name | Business Domain | Record Volume Estimate | Source | Status |
|---|---|---|---|---|---|
| **TABLE-001** | `users` | Identity & Authentication | 500 - 2,000 rows (RT scale) | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-002** | `jenis_surat` | Administrative Master Data | 5 - 20 rows | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-003** | `pengajuan_surat` | Letter Applications & AI Drafts | 1,000 - 10,000 rows | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-004** | `surat_final` | Official Signed PDFs & QR Tokens| 1,000 - 10,000 rows | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-005** | `knowledge_base` | Community Bylaws & Guidelines | 50 - 200 documents | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-006** | `knowledge_chunks`| Text Chunks & Vector Embeddings | 500 - 2,000 chunks | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-007** | `chat_sessions` | Chatbot Conversations | 2,000 - 20,000 sessions | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-008** | `chat_messages` | Chat Transcripts & Top Chunks | 10,000 - 100,000 rows | Bab V (Gambar 5.1/5.2) | CONFIRMED |
| **TABLE-009** | `notifikasi` | In-App Alerts & Activity Feed | 5,000 - 50,000 rows | Bab V (Gambar 5.1/5.2) | CONFIRMED |

---

## 3. Entity Relationship Diagram (ERD)

```text
       +---------------------------------------------+
       |                    users                    |
       |---------------------------------------------|
       | PK: user_id                                 |
       | UQ: nik, email                              |
       +----------------------+----------------------+
                              | 1
                              |
                              | N (as warga_id)
                              v
+------------------+ 1     N +-----------------------+ 1     1 +---------------------+
|   jenis_surat    |<--------+    pengajuan_surat    +<--------+     surat_final     |
|------------------|         |-----------------------|         |---------------------|
| PK: jenis_id     |         | PK: pengajuan_id      |         | PK: surat_final_id  |
+------------------+         | FK: warga_id, rt_id   |         | FK: pengajuan_id    |
                             | FK: jenis_surat_id    |         | UQ: signature_image_url        |
                             +-----------------------+         +---------------------+
                                      | 1
                                      | N (via user_id)
                                      v
                             +-----------------------+
                             |       notifikasi      |
                             |-----------------------|
                             | PK: notifikasi_id     |
                             | FK: penerima_id       |
                             +-----------------------+

       +---------------------------------------------+
       |               knowledge_base                |
       |---------------------------------------------|
       | PK: knowledge_id                            |
       | FK: diunggah_oleh_rt -> users(user_id)      |
       +----------------------+----------------------+
                              | 1
                              | N
                              v
       +---------------------------------------------+
       |              knowledge_chunks               |
       |---------------------------------------------|
       | PK: chunk_id                                |
       | FK: knowledge_id -> knowledge_base          |
       | DATA: embedding_vector (JSON / Vector)      |
       +----------------------+----------------------+
                              | 1 (referenced as top_chunk_id)
                              | N
                              v
+------------------+ 1     N +-----------------------+
|  chat_sessions   |<--------+     chat_messages     |
|------------------|         |-----------------------|
| PK: session_id   |         | PK: message_id        |
| FK: warga_id     |         | FK: session_id        |
+------------------+         | FK: top_chunk_id      |
                             +-----------------------+
```

---

## 4. Tables Detail Specification

### TABLE ID: TABLE-001
- **TABLE NAME:** `users`
- **PURPOSE:** Centralized storage of user credentials, profile information, role definitions, and registered digital signature scans.
- **COLUMNS:**
  - `user_id` INT AUTO_INCREMENT
  - `nik` VARCHAR(16) NOT NULL
  - `nama_lengkap` VARCHAR(100) NOT NULL
  - `email` VARCHAR(100) NOT NULL
  - `password_hash` VARCHAR(255) NOT NULL
  - `nomor_telepon` VARCHAR(20) NOT NULL
  - `alamat` VARCHAR(255) NOT NULL
  - `nomor_rt` VARCHAR(5) DEFAULT '032'
  - `nomor_rw` VARCHAR(5) DEFAULT '08'
  - `role` ENUM('warga', 'rt', 'admin') NOT NULL DEFAULT 'warga'
  - `tanda_tangan_digital` VARCHAR(255) NULL
  - `is_active` BOOLEAN DEFAULT TRUE
  - `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
  - `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
- **PRIMARY KEY:** `user_id`
- **FOREIGN KEYS:** None.
- **INDEXES:** `idx_users_nik` (`nik` UNIQUE), `idx_users_email` (`email` UNIQUE).
- **RELATIONSHIPS:** 1:N with `pengajuan_surat` (as warga and RT reviewer), 1:N with `chat_sessions`, 1:N with `notifikasi`.
- **CONSTRAINTS:** NIK must be exactly 16 characters.
- **SOURCE:** Bab V (Gambar 5.1/5.2)
- **STATUS:** CONFIRMED

---

### TABLE ID: TABLE-002
- **TABLE NAME:** `jenis_surat`
- **PURPOSE:** Reference catalog of available administrative cover letter templates and requirements.
- **COLUMNS:**
  - `jenis_surat_id` INT AUTO_INCREMENT
  - `kode_surat` VARCHAR(20) NOT NULL
  - `nama_surat` VARCHAR(100) NOT NULL
  - `template_dokumen` TEXT NOT NULL
  - `persyaratan_dokumen` TEXT NULL
  - `is_aktif` BOOLEAN DEFAULT TRUE
  - `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
- **PRIMARY KEY:** `jenis_surat_id`
- **FOREIGN KEYS:** None.
- **INDEXES:** `idx_jenis_kode` (`kode_surat` UNIQUE).
- **RELATIONSHIPS:** 1:N with `pengajuan_surat`.
- **CONSTRAINTS:** `kode_surat` must be unique.
- **SOURCE:** Bab V (Gambar 5.1/5.2)
- **STATUS:** CONFIRMED

---

### TABLE ID: TABLE-003
- **TABLE NAME:** `pengajuan_surat`
- **PURPOSE:** Core transactional records tracking cover letter applications from submission through review and completion.
- **COLUMNS:**
  - `pengajuan_id` INT AUTO_INCREMENT
  - `nomor_pengajuan` VARCHAR(50) NOT NULL
  - `warga_id` INT NOT NULL
  - `rt_id` INT NULL
  - `jenis_surat_id` INT NOT NULL
  - `keperluan` TEXT NOT NULL
  - `metode_tanda_tangan` ENUM('digital', 'basah') NOT NULL DEFAULT 'digital'
  - `berkas_lampiran_url` VARCHAR(255) NULL
  - `draf_ai_konten` TEXT NULL
  - `status` ENUM('diajukan', 'perlu_revisi', 'disetujui', 'ditolak', 'siap_diambil', 'selesai') NOT NULL DEFAULT 'diajukan'
  - `catatan_revisi` VARCHAR(255) NULL
  - `alasan_penolakan` VARCHAR(255) NULL
  - `tanggal_pengajuan` DATETIME DEFAULT CURRENT_TIMESTAMP
  - `tanggal_diverifikasi` DATETIME NULL
  - `tanggal_selesai` DATETIME NULL
- **PRIMARY KEY:** `pengajuan_id`
- **FOREIGN KEYS:**
  - `warga_id` REFERENCES `users`(`user_id`) ON DELETE CASCADE
  - `rt_id` REFERENCES `users`(`user_id`) ON DELETE SET NULL
  - `jenis_surat_id` REFERENCES `jenis_surat`(`jenis_surat_id`)
- **INDEXES:** `idx_pengajuan_warga` (`warga_id`), `idx_pengajuan_status` (`status`).
- **RELATIONSHIPS:** N:1 with `users` (Warga), N:1 with `users` (RT), 1:1 with `surat_final`.
- **CONSTRAINTS:** If status is `ditolak`, `alasan_penolakan` must not be null.
- **SOURCE:** Bab V (Gambar 5.1/5.2)
- **STATUS:** CONFIRMED

---

### TABLE ID: TABLE-004
- **TABLE NAME:** `surat_final`
- **PURPOSE:** Stores official issued documents, PDF file paths, and registered digital signature image overlays.
- **COLUMNS:**
  - `surat_final_id` INT AUTO_INCREMENT
  - `pengajuan_id` INT NOT NULL
  - `nomor_surat_resmi` VARCHAR(100) NOT NULL
  - `file_pdf_path` VARCHAR(255) NOT NULL
  - `signature_image_path` VARCHAR(128) NOT NULL
  - `status_pengesahan` ENUM('digital_sah', 'basah_selesai') NOT NULL
  - `tanggal_terbit` DATETIME DEFAULT CURRENT_TIMESTAMP
  - `tanggal_diambil` DATETIME NULL
- **PRIMARY KEY:** `surat_final_id`
- **FOREIGN KEYS:** `pengajuan_id` REFERENCES `pengajuan_surat`(`pengajuan_id`) ON DELETE CASCADE
- **INDEXES:** `idx_final_qr` (`signature_image_path` UNIQUE), `idx_final_nomor` (`nomor_surat_resmi` UNIQUE).
- **RELATIONSHIPS:** 1:1 with `pengajuan_surat`.
- **CONSTRAINTS:** `pengajuan_id` must be unique.
- **SOURCE:** Bab V (Gambar 5.1/5.2)
- **STATUS:** CONFIRMED

---

### TABLE ID: TABLE-005 & TABLE-006 (Knowledge Base & Chunks)
- **TABLE NAME:** `knowledge_base` & `knowledge_chunks`
- **PURPOSE:** Ingests neighborhood bylaws, procedural guidelines, chunking them into semantic sections with embedding vectors for RAG.
- **COLUMNS (`knowledge_chunks`):**
  - `chunk_id` INT AUTO_INCREMENT PRIMARY KEY
  - `knowledge_id` INT NOT NULL (FK -> `knowledge_base`)
  - `urutan_chunk` INT NOT NULL
  - `isi_chunk` TEXT NOT NULL
  - `embedding_vector` JSON NOT NULL (1536-dimensional float array)
  - `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
- **SOURCE:** Bab V (Gambar 5.1/5.2), Bab VIII (8.3)
- **STATUS:** CONFIRMED

---

## 5. Seed Data (Initial Bootstrap)

```sql
INSERT INTO `jenis_surat` (`kode_surat`, `nama_surat`, `template_dokumen`, `persyaratan_dokumen`) VALUES
('DOM', 'Surat Keterangan Domisili', 'Surat Keterangan Domisili Warga RT 032 RW 08', 'KTP dan Bukti Tempat Tinggal'),
('KTP', 'Surat Pengantar Pembuatan KTP', 'Surat Pengantar Pembuatan/Perpanjangan KTP', 'Fotokopi Kartu Keluarga'),
('SKCK', 'Surat Pengantar SKCK', 'Surat Pengantar Pembuatan Catatan Kepolisian', 'KTP dan KK Asli'),
('SKU', 'Surat Keterangan Usaha', 'Surat Keterangan Domisili Usaha Mikro Warga', 'Foto Tempat Usaha');

INSERT INTO `users` (`nik`, `nama_lengkap`, `email`, `password_hash`, `nomor_telepon`, `alamat`, `role`) VALUES
('3515080101800001', 'Pak RT Indra', 'rt032@rtconnect.id', '$2b$12$e80yVj2y57Vd...[hash]', '081234567890', 'Griya Taman Asri Blok B-01', 'rt'),
('3515082405020002', 'Ahmad Dhafin', 'dhafin@gmail.com', '$2b$12$uY7k62e9...[hash]', '089876543210', 'Griya Taman Asri Blok D-14', 'warga');
```

---

## 6. Migration & Lifecycle Strategy
- Changes versioned sequentially via SQL migration files (`V1__init_schema.sql`, `V2__seed_master_data.sql`).
- Purge policy: Chat session records older than 180 days can be archived. Application audit history is retained permanently.
