# Software Requirements Specification — RTConnect

This document details the functional and non-functional requirements for the RTConnect mobile application. Each requirement is assigned a deterministic ID, an actor, priority, traceability source, and confidence score.

---

## 1. Functional Requirements

### REQ-001
- **Title:** Resident Account Self-Registration
- **Description:** Unregistered citizens living in RT 032 RW 08 must be able to register an account by supplying their national identity data, credentials, and digital signature scan.
- **Actor:** Citizen (*Warga*)
- **Precondition:** User is unauthenticated and opens the application.
- **Trigger:** User taps "Registrasi" on the Welcome screen and submits the registration form.
- **Expected Behavior:** System validates 16-digit numeric NIK format, uniqueness of email and NIK, password strength, and signature file. Upon successful validation, the account is created with status "Terdaftar" and the user is redirected to the login screen.
- **Priority:** MUST
- **Source:** Bab III (UC-01), Bab IV (Gambar 4.2), Bab VII (7.1), Bab VIII (8.2)
- **Confidence:** CONFIRMED

---

### REQ-002
- **Title:** Unified User Authentication (Login)
- **Description:** Registered users (both Warga and Ketua RT) must be able to securely authenticate into the system using either their Email or NIK along with their password.
- **Actor:** All Users (*Warga*, *Ketua RT*)
- **Precondition:** User is registered and on the Login screen.
- **Trigger:** User inputs identifier (Email/NIK) and password, then taps "Masuk".
- **Expected Behavior:** System validates input, searches user record, verifies cryptographic hash, issues a session token, logs the login timestamp, and redirects the user to their role-specific dashboard.
- **Priority:** MUST
- **Source:** Bab IV (Gambar 4.3), Bab VII (7.2), Bab VIII (8.1)
- **Confidence:** CONFIRMED

---

### REQ-003
- **Title:** Role-Based Screen Redirection & Navigation
- **Description:** System must evaluate the authenticated user's role and restrict access to unauthorized views.
- **Actor:** System / All Users
- **Precondition:** User successfully authenticates.
- **Trigger:** Authentication completion event.
- **Expected Behavior:** If `role == 'warga'`, navigate to `/warga/home`. If `role == 'rt'`, navigate to `/rt/pengajuan`. Unauthorized route access attempts redirect to the user's home screen.
- **Priority:** MUST
- **Source:** Bab VII (7.2), Bab VIII (8.1)
- **Confidence:** CONFIRMED

---

### REQ-004
- **Title:** Cover Letter Request Submission
- **Description:** Residents can submit a new administrative cover letter request with auto-filled resident data.
- **Actor:** Citizen (*Warga*)
- **Precondition:** Resident is authenticated and has an active account.
- **Trigger:** Resident taps "Buat Pengajuan Baru" from the home screen or history screen.
- **Expected Behavior:** System renders form with auto-filled Name, NIK, and Address. Resident selects letter type (Domisili, KTP, SKCK, Usaha), enters purpose, chooses signature method (Digital vs Basah), and optionally uploads attachments. On submission, the application is stored with status `Diajukan` and triggers AI drafting.
- **Priority:** MUST
- **Source:** Bab III (UC-01, UC-02), Bab IV (Gambar 4.7), Bab VII (7.3), Bab VIII (8.4)
- **Confidence:** CONFIRMED

---

### REQ-005
- **Title:** Generative AI Letter Draft Synthesis
- **Description:** System utilizes Generative AI to formulate an official Indonesian administrative letter draft based on the resident's submitted details and purpose.
- **Actor:** System (AI Module)
- **Precondition:** Application is successfully validated and stored.
- **Trigger:** Creation of a new cover letter record.
- **Expected Behavior:** System invokes LLM endpoint with a pre-configured prompt template, generating a formal draft (`draf_ai_konten`) stored alongside the application for the RT Head to review.
- **Priority:** MUST
- **Source:** Bab I (1.1), Bab II (2.2.1), Bab V (Gambar 5.1/5.2)
- **Confidence:** CONFIRMED

---

### REQ-006
- **Title:** Resident Application Tracking & Status History
- **Description:** Residents must be able to view a real-time list of all their historical and active letter submissions along with their current status.
- **Actor:** Citizen (*Warga*)
- **Precondition:** Resident is authenticated.
- **Trigger:** Resident opens the "Pengajuan" tab or taps "Riwayat Pengajuan".
- **Expected Behavior:** System queries all applications for `warga_id` and renders cards indicating Letter Type, Submission Date, and a color-coded status badge (`Diajukan`, `Perlu Revisi`, `Disetujui`, `Ditolak`, `Siap Diambil`, `Selesai`).
- **Priority:** MUST
- **Source:** Bab IV (Gambar 4.6), Bab VII (7.3)
- **Confidence:** CONFIRMED

---

### REQ-007
- **Title:** Form Revision Resubmission
- **Description:** When an application status is set to `Perlu Revisi`, the resident must be able to edit the flagged information and resubmit.
- **Actor:** Citizen (*Warga*)
- **Precondition:** Application has status `Perlu Revisi` and contains RT review notes.
- **Trigger:** Resident opens the detail of a flagged application and taps "Perbaiki Pengajuan".
- **Expected Behavior:** Form opens populated with previous values and displays the RT revision notes. Resident updates the fields or attachments and taps "Kirim Ulang Revisi". Status transitions back to `Diajukan`.
- **Priority:** MUST
- **Source:** Bab III (UC-03), Bab VI (6.2.3), Bab VII (7.3)
- **Confidence:** CONFIRMED

---

### REQ-008
- **Title:** RT Head Incoming Application Review Queue
- **Description:** The RT Head must have an administrative inbox displaying all pending citizen requests requiring action.
- **Actor:** RT Head (*Ketua RT*)
- **Precondition:** User is authenticated with `role == 'rt'`.
- **Trigger:** RT Head navigates to the incoming queue screen.
- **Expected Behavior:** System renders list of applications displaying Applicant Name, Letter Type, Date, and Signature Method, with filters for active statuses. Tapping a card opens the detailed review screen.
- **Priority:** MUST
- **Source:** Bab IV (Gambar 4.8), Bab VII (7.3)
- **Confidence:** CONFIRMED

---

### REQ-009
- **Title:** Application Evaluation (Approve, Revise, Reject)
- **Description:** The RT Head can take one of three official actions on a pending application: Approve, Request Revision, or Reject.
- **Actor:** RT Head (*Ketua RT*)
- **Precondition:** RT Head is viewing the application detail screen.
- **Trigger:** RT Head taps "Setuju", "Revisi", or "Tolak".
- **Expected Behavior:**
  - If "Setuju": System marks application as `Disetujui`, assigns an official letter number, and routes to signature workflow.
  - If "Revisi": System prompts for revision notes, updates status to `Perlu Revisi`, and notifies the citizen.
  - If "Tolak": System prompts for mandatory rejection reason, updates status to `Ditolak`, and terminates workflow.
- **Priority:** MUST
- **Source:** Bab III (UC-08), Bab IV (Gambar 4.9), Bab VII (7.3), Bab VIII (8.4)
- **Confidence:** CONFIRMED

---

### REQ-010
- **Title:** Digital Signature Verification (Tempelan Gambar Tanda Tangan Embedding)
- **Description:** For applications requesting digital signatures, the RT Head confirms authorization to embed a registered digital signature image overlay into the official PDF.
- **Actor:** RT Head (*Ketua RT*)
- **Precondition:** Application is `Disetujui` and `metode_tanda_tangan == 'digital'`.
- **Trigger:** RT Head enters security PIN / confirmation on the signing screen.
- **Expected Behavior:** System verifies PIN, generates a unique signature image overlay, binds it to the generated PDF document, marks status as `Selesai`, and notifies the resident that the document is ready for download.
- **Priority:** MUST
- **Source:** Bab III (UC-07/UC-09), Bab VI (6.2.7), Bab VII (7.3), Bab VIII (8.4)
- **Confidence:** CONFIRMED

---

### REQ-011
- **Title:** Physical Signature Workflow Confirmation
- **Description:** For applications requiring physical ink signatures, the RT Head prints the document offline and confirms in the system when it is ready for in-person pickup.
- **Actor:** RT Head (*Ketua RT*)
- **Precondition:** Application is `Disetujui` and `metode_tanda_tangan == 'basah'`.
- **Trigger:** RT Head prints the document and taps "Konfirmasi Siap Diambil".
- **Expected Behavior:** System updates status to `Siap Diambil` and dispatches notification to the resident detailing pickup hours and RT residence location.
- **Priority:** MUST
- **Source:** Bab III (UC-06/UC-10), Bab VI (6.2.6), Bab VII (7.3), Bab VIII (8.4)
- **Confidence:** CONFIRMED

---

### REQ-012
- **Title:** Final PDF Preview and Download
- **Description:** Citizens can preview and download the finalized, digitally signed official cover letter PDF.
- **Actor:** Citizen (*Warga*)
- **Precondition:** Application status is `Selesai`.
- **Trigger:** Citizen taps "Unduh Surat" or opens document preview.
- **Expected Behavior:** Application fetches the PDF file stream and displays it via the integrated PDF viewer, with an option to save to local device storage.
- **Priority:** MUST
- **Source:** Bab III (UC-04/UC-06), Bab VI (6.2.4), Bab VII (7.3)
- **Confidence:** CONFIRMED

---

### REQ-013
- **Title:** Tanya RT Conversational Knowledge Assistant (RAG Chatbot)
- **Description:** Residents can converse with an AI chatbot to inquire about neighborhood rules, administrative prerequisites, and community procedures.
- **Actor:** Citizen (*Warga*)
- **Precondition:** Resident is authenticated and opens the "Tanya RT" screen.
- **Trigger:** Resident types a query in the chat input and taps send.
- **Expected Behavior:** System performs semantic embedding vector search over neighborhood bylaws (`knowledge_chunks`). If similarity score >= 0.70, it synthesizes an accurate answer grounded strictly on local rules with citations.
- **Priority:** MUST
- **Source:** Bab II (2.2.2), Bab IV (Gambar 4.10), Bab V (5.1/5.2), Bab VII (7.4), Bab VIII (8.3)
- **Confidence:** CONFIRMED

---

### REQ-014
- **Title:** Unanswered Query Escalation to RT WhatsApp
- **Description:** If the chatbot cannot find relevant community knowledge (similarity score < 0.70), it offers an immediate fallback to contact the RT Head directly via WhatsApp.
- **Actor:** Citizen (*Warga*)
- **Precondition:** Chatbot returns no high-confidence matching knowledge.
- **Trigger:** Resident taps the "Hubungi Ketua RT via WhatsApp" action button.
- **Expected Behavior:** System launches the WhatsApp application via URL scheme (`https://wa.me/{rt_phone}?text={encoded_summary}`), pre-populating the chat with the resident's inquiry summary.
- **Priority:** MUST
- **Source:** Bab II (2.2.2), Bab IV (Gambar 4.10), Bab VII (7.4), Bab VIII (8.3)
- **Confidence:** CONFIRMED

---

## 2. Non-Functional Requirements

### REQ-NF-001
- **Title:** UI Responsiveness & Frame Rate
- **Description:** Flutter views must maintain 60 FPS transitions without perceptible jank or blocking on the main UI thread during network or file operations.
- **Priority:** MUST
- **Confidence:** PROPOSED

### REQ-NF-002
- **Title:** Data Privacy & Secure Storage
- **Description:** User authentication tokens must be stored using platform-encrypted keychain/keystore (`flutter_secure_storage`). Passwords must never be transmitted or stored in plain text.
- **Priority:** MUST
- **Confidence:** CONFIRMED

### REQ-NF-003
- **Title:** Accessibility Compliance
- **Description:** All touch targets must adhere to a minimum size of 48x48 dp. Color contrast ratios must meet WCAG 2.1 AA standards (minimum 4.5:1 for normal text).
- **Priority:** SHOULD
- **Confidence:** PROPOSED
