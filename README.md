# RTConnect — Aplikasi Administrasi RT/RW Terintegrasi Generative AI & NLP Chatbot

Aplikasi mobile layanan administrasi publik di tingkat rukun tetangga (**RT 032 RW 08 Griya Taman Asri, Sidoarjo**) berbasis **Flutter & Dart** dengan persistensi data **MySQL**, memadukan:
1. **Otomatisasi Surat Pengantar Digital:** Perumusan draf narasi birokrasi baku secara otomatis dengan bantuan *Generative AI*.
2. **Dual-Mode Verification:** Fleksibilitas pengesahan dokumen melalui **Tanda Tangan Digital (Tempelan Gambar Resmi)** dan **Tanda Tangan Basah Fisik**.
3. **Tanya RT (24/7 Citizen AI Assistant):** *Chatbot* interaktif berbasis *Retrieval-Augmented Generation* (RAG) untuk menjawab syarat dan tata tertib RT secara *grounded*, serta fitur eskalasi langsung ke WhatsApp Ketua RT.

---

## 👥 Pengembang (Kelompok 3 — Praktikum PPL I1 UNAIR 2026)
- **Dosen Pengampu:** Dr. Indra Kharisma Raharjana, S.Kom., M.T. (NIP. 198110282006041003)
- **Program Studi:** S1 Sistem Informasi, Fakultas Sains dan Teknologi, Universitas Airlangga

### Anggota Tim:
1. **Muhammad Nafidz Arradhin** (187241027)
2. **Mirza Diwa Luscakson** (187241042)
3. **Febrian Muhammad Yudhistira** (187241051)
4. **Ahmad Dhafin Al Farisy** (187241057)

---

## 🏗️ Arsitektur & Teknologi

```text
Frontend Mobile : Flutter 3.x+ (Dart 3.x+)
Architecture    : Feature-First Clean Architecture
State Management: Riverpod (v2.x)
Navigation      : GoRouter (v14.x)
Networking      : Dio HTTP Client (REST API)
Database        : MySQL 8.x
AI / RAG Engine : Vector Cosine Similarity & LLM Formulator
```

---

## 📊 Diagram Pemodelan Sistem (UML)

Diagram arsitektur sistem resolusi tinggi tersimpan pada folder [`assets/diagrams/`](assets/diagrams/):
- **Use Case Diagram:** `assets/diagrams/RTConnect_UseCase_Diagram.png`
- **Sequence Diagram Login:** `assets/diagrams/RTConnect_Sequence_Login.png`
- **Sequence Diagram Register:** `assets/diagrams/RTConnect_Sequence_Register.png`
- **Sequence Diagram Pengajuan Surat:** `assets/diagrams/RTConnect_Sequence_Pengajuan_Surat.png`
- **Sequence Diagram Chatbot RAG:** `assets/diagrams/RTConnect_Sequence_Chatbot_RAG.png`
- **Activity Diagram Surat Pengantar:** `assets/diagrams/RTConnect_Activity_Pengajuan_Surat.png`
- **Activity Diagram Chatbot Tanya RT:** `assets/diagrams/RTConnect_Activity_Chatbot.png`

---

## 📝 Catatan Proyek & Knowledge Base
Perencanaan rinci (*master planning*, *design tokens*, *user flows*, *test cases*, dan spesifikasi teknis) dikelola secara lokal pada *Obsidian Knowledge Base* (`RTConnect-KnowledgeBase/`).
