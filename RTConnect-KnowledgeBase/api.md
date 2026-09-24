# Technology-Agnostic API Specification — RTConnect

This document defines the RESTful API contract between the Flutter client and the server backend. It is completely technology-agnostic and does not mandate any specific backend framework (Node.js, Flask, Laravel, etc.).

---

## 1. API Overview
- **Protocol:** HTTP/1.1 or HTTP/2 over TLS (HTTPS).
- **Format:** JSON (`Content-Type: application/json`) for standard payloads; `multipart/form-data` for file uploads.
- **Envelope Standard:** All responses follow a consistent envelope:
  ```json
  {
    "success": true,
    "message": "Operation successful description",
    "data": {},
    "error": null
  }
  ```

---

## 2. Base URL
- **Development (Android Emulator):** `http://10.0.2.2:5000/api/v1` [PROPOSED]
- **Development (iOS Simulator):** `http://localhost:5000/api/v1` [PROPOSED]
- **Production:** `https://api.rtconnect.id/api/v1` [PROPOSED]

---

## 3. Authentication
- **Mechanism:** HTTP Bearer Token (`Authorization: Bearer <JWT_TOKEN>`).
- **Expiry:** Access token valid for 7 days (standard community app retention).

---

## 4. Endpoints Inventory

| Endpoint ID | Method | Path | Summary | Auth Required | Status |
|---|---|---|---|---|---|
| **API-001** | POST | `/auth/register` | Register new resident account with signature scan | No | CONFIRMED |
| **API-002** | POST | `/auth/login` | Authenticate using Email/NIK + Password | No | CONFIRMED |
| **API-003** | GET | `/auth/me` | Fetch authenticated user profile & role | Yes | CONFIRMED |
| **API-004** | GET | `/letters/types` | List available letter types & requirements | Yes | CONFIRMED |
| **API-005** | POST | `/letters/apply` | Submit new cover letter application | Yes (Warga) | CONFIRMED |
| **API-006** | GET | `/letters/my-applications` | Get resident's application history | Yes (Warga) | CONFIRMED |
| **API-007** | GET | `/letters/incoming-queue` | Get RT incoming review queue | Yes (RT) | CONFIRMED |
| **API-008** | GET | `/letters/:id` | Get detailed application with AI draft | Yes | CONFIRMED |
| **API-009** | PUT | `/letters/:id/resubmit` | Resubmit revised application | Yes (Warga) | CONFIRMED |
| **API-010** | POST | `/letters/:id/decision` | Submit RT decision (Approve/Revise/Reject) | Yes (RT) | CONFIRMED |
| **API-011** | POST | `/letters/:id/sign-digital` | Confirm digital signature & embed QR token | Yes (RT) | CONFIRMED |
| **API-012** | POST | `/letters/:id/confirm-physical` | Update physical ink signature status | Yes (RT) | CONFIRMED |
| **API-013** | GET | `/letters/:id/download` | Download finalized official PDF file | Yes | CONFIRMED |
| **API-014** | POST | `/chatbot/query` | Send resident inquiry to RAG engine | Yes (Warga) | CONFIRMED |
| **API-015** | GET | `/notifications` | Fetch user notification feed | Yes | CONFIRMED |

---

## 5. Endpoints Detail Specification

### API-001
- **Method:** `POST`
- **Path:** `/auth/register`
- **Purpose:** Registers a new resident in RT 032 with digital signature scan upload.
- **Authentication:** None (Public)
- **Request (multipart/form-data):**
  - `nik`: "3515082104990001" (String, 16 chars, mandatory)
  - `nama_lengkap`: "Budi Santoso" (String, mandatory)
  - `email`: "budi@gmail.com" (String, valid email, mandatory)
  - `password`: "Rahasia123!" (String, min 8 chars, mandatory)
  - `nomor_telepon`: "081234567890" (String, mandatory)
  - `alamat`: "Griya Taman Asri Blok D-14" (String, mandatory)
  - `tanda_tangan`: [Binary Image File] (PNG/JPG, mandatory)
- **Response (201 Created):**
  ```json
  {
    "success": true,
    "message": "Registrasi berhasil, akun telah dibuat",
    "data": {
      "user_id": 14,
      "nik": "3515082104990001",
      "nama_lengkap": "Budi Santoso",
      "role": "warga"
    }
  }
  ```
- **Errors:** 400 (Validation Error / NIK duplicated / Email duplicated).
- **Source:** Bab VII (7.1), Bab VIII (8.2)
- **Status:** CONFIRMED

---

### API-002
- **Method:** `POST`
- **Path:** `/auth/login`
- **Purpose:** Validates credentials and returns JWT bearer token and role.
- **Authentication:** None (Public)
- **Request (application/json):**
  ```json
  {
    "identity": "budi@gmail.com",
    "password": "Rahasia123!"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "message": "Login berhasil",
    "data": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "user_id": 14,
        "nama_lengkap": "Budi Santoso",
        "email": "budi@gmail.com",
        "role": "warga"
      }
    }
  }
  ```
- **Errors:** 401 Unauthorized ("Email/NIK atau password salah").
- **Source:** Bab VII (7.2), Bab VIII (8.1)
- **Status:** CONFIRMED

---

### API-005
- **Method:** `POST`
- **Path:** `/letters/apply`
- **Purpose:** Submits cover letter request and triggers Generative AI draft formulation.
- **Authentication:** Bearer Token (Role: Warga)
- **Request (multipart/form-data):**
  - `jenis_surat_id`: 1 (Integer, mandatory)
  - `keperluan`: "Persyaratan perpanjangan KTP elektronik di Disdukcapil" (String, mandatory)
  - `metode_tanda_tangan`: "digital" | "basah" (String, mandatory)
  - `lampiran`: [Binary File] (Optional PDF/JPG)
- **Response (201 Created):**
  ```json
  {
    "success": true,
    "message": "Pengajuan berhasil dikirim dan draf surat sedang disiapkan",
    "data": {
      "pengajuan_id": 101,
      "nomor_pengajuan": "SRT-2026-00101",
      "status": "diajukan",
      "draf_ai": "Yang bertanda tangan di bawah ini Ketua RT 032 RW 08 menerangkan bahwa...",
      "tanggal_pengajuan": "2026-09-24T07:00:00Z"
    }
  }
  ```
- **Errors:** 400 Bad Request, 401 Unauthorized.
- **Source:** Bab II (2.2.1), Bab III (UC-01), Bab VII (7.3)
- **Status:** CONFIRMED

---

### API-010
- **Method:** `POST`
- **Path:** `/letters/:id/decision`
- **Purpose:** Submits RT Head's evaluation on an application.
- **Authentication:** Bearer Token (Role: RT)
- **Request (application/json):**
  ```json
  {
    "action": "approve", // "approve" | "revise" | "reject"
    "catatan": "Berkas lengkap dan data warga terverifikasi"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "message": "Keputusan pengajuan berhasil disimpan",
    "data": {
      "pengajuan_id": 101,
      "status": "disetujui",
      "nomor_surat_resmi": "032/08/GTA/IX/2026"
    }
  }
  ```
- **Errors:** 400 Bad Request (Missing notes on reject/revise), 403 Forbidden.
- **Source:** Bab III (UC-08), Bab VIII (8.4)
- **Status:** CONFIRMED

---

### API-011
- **Method:** `POST`
- **Path:** `/letters/:id/sign-digital`
- **Purpose:** Authorizes RT digital signature via PIN and embeds verification QR token into PDF.
- **Authentication:** Bearer Token (Role: RT)
- **Request (application/json):**
  ```json
  {
    "pin": "123456"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "message": "Tanda tangan digital berhasil disematkan",
    "data": {
      "pengajuan_id": 101,
      "status": "selesai",
      "pdf_url": "/api/v1/letters/101/download",
      "signature_image_url": "QR-VERIFY-RT032-9F8D7E"
    }
  }
  ```
- **Source:** Bab VI (6.2.7), Bab VIII (8.4)
- **Status:** CONFIRMED

---

### API-014
- **Method:** `POST`
- **Path:** `/chatbot/query`
- **Purpose:** Queries neighborhood knowledge base using vector RAG.
- **Authentication:** Bearer Token (Role: Warga)
- **Request (application/json):**
  ```json
  {
    "session_id": 5,
    "query": "Berapa lama masa berlaku surat pengantar?"
  }
  ```
- **Response (200 OK - Grounded Knowledge Found):**
  ```json
  {
    "success": true,
    "message": "Jawaban berhasil ditemukan",
    "data": {
      "is_escalated": false,
      "answer": "Surat pengantar RT berlaku selama 30 hari kalender sejak tanggal diterbitkan.",
      "citation": "Pedoman Administrasi Warga RT 032 Pasal 4",
      "similarity_score": 0.8845
    }
  }
  ```
- **Response (200 OK - Fallback Escalated):**
  ```json
  {
    "success": true,
    "message": "Pertanyaan belum memiliki jawaban dalam basis pengetahuan",
    "data": {
      "is_escalated": true,
      "answer": "Maaf, informasi tersebut belum tercatat dalam basis data resmi RT 032. Silakan tanyakan langsung ke Ketua RT via WhatsApp.",
      "escalation_whatsapp_url": "https://wa.me/6281234567890?text=Halo%20Pak%20RT,%20saya%20ingin%20bertanya:%20...",
      "similarity_score": 0.4210
    }
  }
  ```
- **Source:** Bab II (2.2.2), Bab IV (Gambar 4.10), Bab VIII (8.3)
- **Status:** CONFIRMED

---

## 6. HTTP Status Codes
- `200 OK`: Request succeeded.
- `201 Created`: Resource created successfully.
- `400 Bad Request`: Payload validation failed.
- `401 Unauthorized`: Missing or invalid Bearer token.
- `403 Forbidden`: Insufficient role permissions (e.g. Warga accessing RT endpoints).
- `404 Not Found`: Target resource does not exist.
- `500 Internal Server Error`: Unexpected server exception.
