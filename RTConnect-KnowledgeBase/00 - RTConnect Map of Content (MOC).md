# 🌐 RTConnect — Master Map of Content (MOC)
#project/rtconnect #architecture #flutter #mysql #systems-analyst

Selamat datang di **Obsidian Knowledge Base RTConnect**! Vault ini merupakan *Single Source of Truth* (SSOT) yang memetakan seluruh arsitektur, kebutuhan fungsional, spesifikasi layar, skema basis data, kontrak API, dan rencana pengujian aplikasi mobile **RTConnect**.

```
                           [[00 - RTConnect Map of Content (MOC)]]
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
              [[ai-rules]] (Aturan AI)                        [[README]] (Overview)
                      │                                               │
                      ▼                                               ▼
             [[planning]] (Master Plan)                       [[requirements]] (Spesifikasi)
                      │                                               │
         ┌────────────┼────────────┐                     ┌────────────┼────────────┐
         ▼            ▼            ▼                     ▼            ▼            ▼
   [[architecture]] [[database]] [[api]]            [[design]]  [[screens]] [[components]]
         │            │            │                     │            │            │
         └────────────┬────────────┘                     └────────────┬────────────┘
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              ▼
                                       [[user-flows]]
                                              │
                                       [[design-tokens]]
                                              │
                                        [[tasks]] (Pelaksanaan)
                                              │
                                       [[testing]] (Uji Kualitas)
                                              │
                                     [[traceability]] (Audit Trail)
```

---

## 📌 Indeks Utama Dokumen (Wikilinks)

### 1. Fondasi & Tata Kelola Proyek
- [[ai-rules]] — **Non-Negotiable AI Rules**: 24 aturan mutlak bagi agen AI dan pengembang, termasuk pengikatan remote repo GitHub `https://github.com/Dhafin-dev/RTConnect.git` dan protokol komit otomatis.
- [[README]] — **Dokumentasi Utama**: Peta pembacaan berkas, batasan teknologi, dan panduan eksekusi agentic.
- [[planning]] — **Master Development Plan**: Latar belakang, 24 seksi perencanaan, inventaris fitur, jadwal rilis, analisis risiko, dan definisi selesai (*Definition of Done*).
- [[requirements]] — **Software Requirements**: Spesifikasi kebutuhan fungsional (`REQ-F-001` s.d. `REQ-F-016`) dan non-fungsional dengan tingkat prioritas (MUST/SHOULD/MAY).

---

### 2. Antarmuka Pengguna & Desain Visual
- [[design]] — **Spesifikasi UI/UX (Google Stitch Compatible)**: Prinsip visual, komponen kartu, app bar, navigasi bawah, dialog alasan penolakan, dan hirarki komposisi layar.
- [[design-tokens]] — **Katalog Token Desain**: Definisi nilai hex warna, tipografi, grid kelipatan 8dp, radius sudut, elevasi, dan dimensi target sentuh.
- [[screens]] — **Spesifikasi Layar Lengkap**: Rincian 12 layar (`SCREEN-001` s.d. `SCREEN-012`) mencakup state loading, error, empty, dan kriteria penerimaan.
- [[components]] — **Registry Widget Flutter**: Inventaris widget Core (`COMP-CORE`), Shared (`COMP-SHR`), dan Feature (`COMP-FEAT`) lengkap dengan kontrak properti dan aksesibilitas.
- [[user-flows]] — **Alur Pengguna & Navigasi**: Visualisasi diagram alur registrasi, login multi-peran, pengajuan draf surat AI, approval RT, dan eskalasi chat WhatsApp.

---

### 3. Arsitektur Teknis, Basis Data & API
- [[architecture]] — **Arsitektur Flutter**: Feature-First Clean Architecture, Riverpod 2.x, GoRouter, Dio Client, dan manajemen sesi lokal terenkripsi.
- [[database]] — **Spesifikasi MySQL 8.x**: 9 entitas ternormalisasi (`users`, `jenis_surat`, `pengajuan_surat`, `surat_final`, `knowledge_chunks`, `chat_sessions`, dll.), DDL, indeks, dan data seed.
- [[api]] — **Kontrak REST API Technology-Agnostic**: Spesifikasi 15 endpoint (`API-001` s.d. `API-015`), format JSON request/response envelope, dan kode status HTTP.

---

### 4. Eksekusi, Pengujian & Audit
- [[tasks]] — **Rencana Kerja Atomik**: 24 tugas terurut (`TASK-001` s.d. `TASK-024`) dari Fase 0 (Setup) hingga Fase 8 (Verifikasi Akhir).
- [[testing]] — **Spesifikasi Pengujian**: Matriks pengujian Unit, Widget, Navigasi, State, Anti-overflow responsif, dan skenario BDD End-to-End.
- [[traceability]] — **Matriks Ketertelusuran**: Pemetaan terverifikasi dari sumber dokumen -> kebutuhan -> layar -> komponen -> tugas -> tes.
- [[docs/REVISI_DOKUMEN_RTCONNECT]] — **Naskah Perbaikan Laporan Kuliah**: Analisis inkonsistensi bab per bab, koreksi penomoran, perbaikan narasi, dan 15 referensi terindeks (APA 7th).

---

## 🏷️ Tag Navigasi Cepat
#flutter #dart #mysql #ui-ux #bdd #behat #rag-chatbot #generative-ai #clean-architecture
