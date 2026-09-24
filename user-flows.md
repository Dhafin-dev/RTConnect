# User Flows & Navigation Specification — RTConnect

This document details the discrete user flows, state decision logic, and end-to-end navigational paths across the RTConnect mobile application.

---

## Flow Inventory

| Flow ID | Flow Title | Primary Actor | Entry Screen | Terminal Outcome |
|---|---|---|---|---|
| **FLOW-001** | Account Registration & Onboarding | Guest / Citizen | `SCREEN-001` (Landing) | `SCREEN-003` (Login) with created account |
| **FLOW-002** | User Login & Role Routing | All Users | `SCREEN-003` (Login) | `SCREEN-004` (Warga Home) or `SCREEN-009` (RT Queue) |
| **FLOW-003** | Cover Letter Request & AI Draft | Citizen (*Warga*) | `SCREEN-004` (Warga Home) | `SCREEN-006` (Riwayat) with status `Diajukan` |
| **FLOW-004** | Letter Revision Resubmission | Citizen (*Warga*) | `SCREEN-006` (Riwayat) | `SCREEN-006` (Riwayat) with status `Diajukan` |
| **FLOW-005** | RT Letter Review & Decision | RT Head (*Ketua RT*)| `SCREEN-009` (RT Queue) | Decision committed (`Disetujui` / `Revisi` / `Ditolak`) |
| **FLOW-006** | Digital Signature & PDF Delivery| RT Head (*Ketua RT*)| `SCREEN-010` (Detail) | `SCREEN-012` (PDF Viewer) with QR verified |
| **FLOW-007** | Physical Signature Tracking | RT Head (*Ketua RT*)| `SCREEN-010` (Detail) | Physical letter ready for citizen pickup |
| **FLOW-008** | Tanya RT Chat & WA Escalation | Citizen (*Warga*) | `SCREEN-011` (Chatbot) | Answer displayed OR redirected to WhatsApp |

---

## Detailed Flow Specifications

### FLOW-001: Account Registration & Onboarding
- **Start:** `SCREEN-001` (Landing / Welcome Screen)
- **Action 01:** User taps "Registrasi" button.
- **Next:** `SCREEN-002` (Register Page)
- **Action 02:** User inputs NIK, Full Name, Address, Phone Number, Email, Password, and uploads signature image.
- **Action 03:** User taps "Daftar".
- **Decision:** Are all mandatory fields valid, NIK 16 digits, email/NIK unique, and signature attached?
  - *No:* Display inline validation errors. Return to `SCREEN-002`.
  - *Yes:* Dispatch registration API request, persist user, show success toast.
- **Next:** Navigate to `SCREEN-003` (Login Page).

```text
[START: Guest User]
      ↓
(SCREEN-001: Landing Page)
      ↓ [Tap 'Registrasi']
(SCREEN-002: Register Page)
      ↓ [Fill form & upload signature]
      ↓ [Tap 'Daftar']
{Is Form Valid & NIK Unique?}
      ├── [No]  ──► (Display validation error banners) ──► (Stay on SCREEN-002)
      └── [Yes] ──► (Create Account in Database)
                        ↓
                  (SCREEN-003: Login Page) [END]
```

---

### FLOW-002: User Login & Role Routing
- **Start:** `SCREEN-003` (Login Page)
- **Action 01:** User inputs Identifier (Email or NIK) and Password.
- **Action 02:** User taps "Masuk".
- **Decision 01:** Do credentials match a valid user record?
  - *No:* Display error "Email/NIK atau password salah". Return to `SCREEN-003`.
  - *Yes:* Store JWT session token securely. Check user role.
- **Decision 02:** What is `user.role`?
  - *If `role == 'warga'`:* Navigate to `SCREEN-004` (Warga Home).
  - *If `role == 'rt'`:* Navigate to `SCREEN-009` (RT Incoming Queue).

```text
[START: User on Login]
      ↓
(SCREEN-003: Login Page)
      ↓ [Enter Email/NIK & Password]
      ↓ [Tap 'Masuk']
{Credentials Valid?}
      ├── [No]  ──► (Display error message) ──► (Stay on SCREEN-003)
      └── [Yes] ──► [Store Session Token]
                        ↓
                 {Check user.role}
                        ├── ['warga'] ──► (SCREEN-004: Warga Home Page) [END]
                        └── ['rt']    ──► (SCREEN-009: RT Incoming Queue) [END]
```

---

### FLOW-003: Cover Letter Request Submission & AI Drafting
- **Start:** `SCREEN-004` (Warga Home Page)
- **Action 01:** User taps "Ajukan Surat" or "Buat Pengajuan Baru".
- **Next:** `SCREEN-007` (Application Form Page)
- **Action 02:** System pre-fills Applicant Name, NIK, and Address.
- **Action 03:** User selects `jenis_surat` from dropdown, types `keperluan`, selects `metode_tanda_tangan` (Digital / Basah), and optionally attaches supporting files.
- **Action 04:** User taps "Kirim Pengajuan".
- **Decision:** Is form valid and required purpose filled?
  - *No:* Display validation message on empty fields.
  - *Yes:* Send to backend API. Backend persists application with status `Diajukan` and triggers Generative AI draft formulation.
- **Next:** Show success confirmation dialog. Redirect to `SCREEN-006` (Application History).

```text
[START: Authenticated Warga]
      ↓
(SCREEN-004: Warga Home Page)
      ↓ [Tap 'Ajukan Surat']
(SCREEN-007: Application Form Page)
      ↓ [Auto-fills NIK, Name, Address]
      ↓ [Select Letter Type & Signature Method]
      ↓ [Input Purpose & Attach Docs]
      ↓ [Tap 'Kirim Pengajuan']
{Form Valid?}
      ├── [No]  ──► (Highlight missing fields) ──► (Stay on SCREEN-007)
      └── [Yes] ──► [Backend: Save Pengajuan (status='Diajukan')]
                        ↓
                  [Backend: AI Generates Letter Draft]
                        ↓
                  (SCREEN-006: Application History) [END]
```

---

### FLOW-005 & FLOW-006: RT Letter Review, Decision, & Digital Signing
- **Start:** `SCREEN-009` (RT Incoming Queue Screen)
- **Action 01:** RT Head taps on a pending application card.
- **Next:** `SCREEN-010` (RT Application Detail & Action Screen)
- **Action 02:** RT Head inspects citizen data, purpose, attachments, and the AI-generated letter draft.
- **Decision 01:** What action does the RT Head select?
  - *Option A (Tolak):* RT Head taps "Tolak" -> Enter rejection reason in dialog -> Status becomes `Ditolak` -> Notify Citizen -> Return to `SCREEN-009`.
  - *Option B (Revisi):* RT Head taps "Revisi" -> Enter specific revision notes in dialog -> Status becomes `Perlu Revisi` -> Notify Citizen -> Return to `SCREEN-009`.
  - *Option C (Setuju):* RT Head taps "Setuju" -> System assigns official letter number -> Status becomes `Disetujui`.
- **Decision 02 (If Setuju):** What is `metode_tanda_tangan`?
  - *Digital:* System prompts RT for security PIN confirmation -> System generates unique cryptographic QR verification token -> Embeds QR into final PDF -> Status becomes `Selesai` -> Citizen notified to download.
  - *Basah:* System generates printable PDF -> RT Head prints offline & physically signs -> RT Head taps "Konfirmasi Siap Diambil" -> Status becomes `Siap Diambil` -> Citizen notified to pick up at RT residence.

```text
[START: Authenticated Ketua RT]
      ↓
(SCREEN-009: RT Incoming Queue)
      ↓ [Tap application card]
(SCREEN-010: Application Detail Screen)
      ↓ [Review Citizen Info, Attachments & AI Draft]
{Select Evaluation Action}
      ├── [Tolak]  ──► [Enter Reason] ──► [Status: 'Ditolak'] ──► (Notify Citizen) ──► (SCREEN-009) [END]
      ├── [Revisi] ──► [Enter Notes]  ──► [Status: 'Perlu Revisi'] ──► (Notify Citizen) ──► (SCREEN-009) [END]
      └── [Setuju] ──► [Assign Official Letter Number]
                             ↓
                    {Signature Method?}
                             ├── [Digital] ──► [Input Security PIN]
                             │                      ↓
                             │                 [Embed QR Verification Token in PDF]
                             │                      ↓
                             │                 [Status: 'Selesai'] ──► (Notify Warga to Download) [END]
                             │
                             └── [Basah]   ──► [Print Physical Document Offline]
                                                    ↓
                                               [Sign physically with ink pen]
                                                    ↓
                                               [Tap 'Konfirmasi Siap Diambil']
                                                    ↓
                                               [Status: 'Siap Diambil'] ──► (Notify Warga to Pickup) [END]
```

---

### FLOW-008: Tanya RT Conversational Chatbot & Escalation
- **Start:** `SCREEN-011` (Tanya RT Chatbot Screen)
- **Action 01:** Citizen inputs inquiry text in chat field.
- **Action 02:** Citizen taps Send.
- **Action 03:** Chat bubble appears in user state. Backend triggers RAG vector search over `knowledge_chunks`.
- **Decision:** Is top chunk cosine similarity score >= 0.70?
  - *Yes (Knowledge Available):* LLM synthesizes concise answer strictly referencing the retrieved chunk. Chatbot displays reply bubble with source citation badge.
  - *No (Knowledge Unavailable / Out-of-Domain):* Chatbot displays fallback apology message and renders an action card: "Hubungi Ketua RT via WhatsApp".
- **Action 04 (If Escalated):** Citizen taps WhatsApp action card -> Application deep links to WhatsApp (`wa.me`) with pre-composed inquiry summary.

```text
[START: Citizen on Chatbot]
      ↓
(SCREEN-011: Tanya RT Chatbot Screen)
      ↓ [Type question & tap send]
[Display User Message Bubble]
      ↓
[Backend: Vector Search on Knowledge Base]
      ↓
{Similarity Score >= 0.70?}
      ├── [Yes] ──► [LLM Synthesizes Grounded Answer]
      │                   ↓
      │             [Display Bot Reply Bubble + Source Citation Badge] [END]
      │
      └── [No]  ──► [Display Fallback: "Informasi belum tersedia"]
                          ↓
                    [Render "Hubungi Ketua RT via WhatsApp" Action Button]
                          ↓ [Citizen taps button]
                    [Launch WhatsApp App via URL scheme with query text] [END]
```
