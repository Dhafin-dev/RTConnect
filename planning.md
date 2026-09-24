# Master Development Plan — RTConnect

## 01. Project Context
- **Project Name:** RTConnect (Citizen & RT Administrative Service Platform) [CONFIRMED]
- **Target Institution:** RT 032 RW 08 Griya Taman Asri, Tawangsari, Taman, Sidoarjo, East Java [CONFIRMED]
- **Academic Environment:** S1 Information Systems, Faculty of Science and Technology, Universitas Airlangga (Practical Software Engineering Course - Class I1, 2026) [CONFIRMED]
- **Problem Statement:** Administrative operations at the neighborhood level (RT/RW) suffer from heavy reliance on physical presence, manual paper drafting of cover letters, frequent typographical errors, and repetitive procedural inquiries sent via personal WhatsApp messages to the RT Head. [CONFIRMED]
- **Solution:** A centralized mobile client with two primary pillars:
  1. *Automated Administrative Letter Service:* Generative AI-assisted letter drafting with dual-mode verification (Verifiable Digital QR Code vs. Physical Pen Signature). [CONFIRMED]
  2. *24/7 Citizen AI Assistant ("Tanya RT"):* NLP Chatbot powered by Retrieval-Augmented Generation (RAG) over verified neighborhood bylaws with a direct escalation fallback to the RT Head's WhatsApp. [CONFIRMED]

---

## 02. Development Objective
Deliver an enterprise-grade, high-fidelity Flutter mobile application backed by a MySQL database that:
1. Allows residents (*Warga*) to register, log in, request administrative cover letters, track status in real-time, download approved digital letters, and query neighborhood rules via a RAG chatbot.
2. Equips the RT Head (*Ketua RT*) with an administrative portal to review incoming applications, request revisions, reject with logged reasons, approve, embed digital QR signatures, or coordinate physical ink signing.
3. Adheres strictly to clean software engineering practices, verifiable BDD testing specifications, and Google Stitch-compatible design token standards.

---

## 03. Scope
1. **User Authentication & Role Handling:**
   - Resident (*Warga*) self-registration with digital signature/signature scan upload. [CONFIRMED]
   - Unified credentials login (Email or NIK + Password) with role-based routing (Warga vs Ketua RT). [CONFIRMED]
2. **Cover Letter Administration (*Surat Pengantar*):**
   - Letter types: Domisili, Pengantar KTP/KK, Pengantar SKCK, Surat Keterangan Usaha. [CONFIRMED]
   - Form submission with auto-filled resident profile attributes, purpose, signature method choice, and optional attachments. [CONFIRMED]
   - Generative AI auto-drafting integration for formal bureaucratical letter body generation. [CONFIRMED]
   - Multi-status lifecycle: `Diajukan` -> `Perlu Revisi` | `Ditolak` | `Disetujui` -> `Siap Diambil` (if physical) | `Selesai` (if digital). [CONFIRMED]
   - Verification via verifiable QR token for digital signatures. [CONFIRMED]
   - PDF document preview and download. [CONFIRMED]
3. **Citizen AI Support ("Tanya RT"):**
   - RAG Chatbot interactive conversation screen. [CONFIRMED]
   - Knowledge base retrieval over local community guidelines. [CONFIRMED]
   - Out-of-domain query detection with dynamic escalation to WhatsApp. [CONFIRMED]
4. **Notifications & Tracking:**
   - In-app status update feeds and activity tracking for both actors. [CONFIRMED]

---

## 04. Non-Scope
1. Financial payment gateway or RT monthly fee collections (Iuran RT) [NOT OBSERVED in source; excluded from MVP].
2. Sub-district (Kelurahan) or District (Kecamatan) level approval routing [CONFIRMED limited strictly to RT level].
3. Native offline vector embedding generator running on-device (client relies on backend REST embedding endpoint) [PROPOSED].
4. Multi-tenant SaaS orchestration across multiple different RT/RW communities [CONFIRMED focused on RT 032 RW 08 pilot].

---

## 05. Functional Requirements Summary

| Requirement ID | Module | Title | Actor | Priority | Status |
|---|---|---|---|---|---|
| **REQ-F-001** | Auth | Resident Account Self-Registration | Warga | MUST | CONFIRMED |
| **REQ-F-002** | Auth | Unified User Login (Email/NIK + Password) | All | MUST | CONFIRMED |
| **REQ-F-003** | Auth | Role-based Dashboard Redirection | All | MUST | CONFIRMED |
| **REQ-F-004** | Profile | View and Update User Profile & Signature | All | SHOULD | CONFIRMED |
| **REQ-F-005** | Letters | Submit Cover Letter Application | Warga | MUST | CONFIRMED |
| **REQ-F-006** | Letters | AI-Assisted Automated Draft Generation | System | MUST | CONFIRMED |
| **REQ-F-007** | Letters | View Application History and Real-Time Status | Warga | MUST | CONFIRMED |
| **REQ-F-008** | Letters | Resubmit Application Form Upon Revision Request | Warga | MUST | CONFIRMED |
| **REQ-F-009** | Letters | Review Application Queue & Attachment Validation | Ketua RT | MUST | CONFIRMED |
| **REQ-F-010** | Letters | Process Letter Decision (Approve / Revise / Reject) | Ketua RT | MUST | CONFIRMED |
| **REQ-F-011** | Letters | Confirm Digital Signature (QR Code Embedding) | Ketua RT | MUST | CONFIRMED |
| **REQ-F-012** | Letters | Confirm Physical Ink Signature Readiness | Ketua RT | MUST | CONFIRMED |
| **REQ-F-013** | Letters | Download Final Letter PDF | Warga | MUST | CONFIRMED |
| **REQ-F-014** | Chatbot | Ask Procedural Questions via RAG Chatbot | Warga | MUST | CONFIRMED |
| **REQ-F-015** | Chatbot | Escalate Unanswered Inquiries to RT WhatsApp | Warga | MUST | CONFIRMED |
| **REQ-F-016** | Notice | In-App Notification Feed for Status Updates | All | SHOULD | CONFIRMED |

---

## 06. Non-Functional Requirements Summary

| Requirement ID | Category | Target Metric / Constraint | Priority | Status |
|---|---|---|---|---|
| **REQ-NF-001** | Performance | Screen initial render under 1.5 seconds on 4G networks | MUST | PROPOSED |
| **REQ-NF-002** | Performance | Chatbot response roundtrip under 3.0 seconds | SHOULD | PROPOSED |
| **REQ-NF-003** | Usability | System Usability Scale (SUS) benchmark score >= 70.0 | MUST | CONFIRMED |
| **REQ-NF-004** | Reliability | Black-box test case pass rate = 100% on primary flows | MUST | CONFIRMED |
| **REQ-NF-005** | Security | Cryptographic hashing of passwords (bcrypt / Argon2) | MUST | CONFIRMED |
| **REQ-NF-006** | Security | JWT/Bearer session token authentication with expiry | MUST | PROPOSED |
| **REQ-NF-007** | Responsive | Support Android & iOS viewport widths: 360px - 428px | MUST | PROPOSED |
| **REQ-NF-008** | Accessibility | Minimum touch target size 48x48 dp; WCAG 2.1 AA contrast | MUST | PROPOSED |

---

## 07. User Roles

```text
+-------------------+-----------------------------------------------------------------+
| Role ID           | Description & Access Boundary                                   |
+-------------------+-----------------------------------------------------------------+
| ROLE-WARGA        | Citizen / Resident. Can submit applications, revise forms,      |
|                   | download final approved PDFs, and chat with AI assistant.       |
| ROLE-RT           | RT Head. Can review incoming queues, inspect documents,        |
|                   | approve/reject/revise, sign digitally, or update physical status|
| ROLE-ADMIN        | System Administrator (Superuser/Dev). Manages knowledge bases   |
|                   | and system configurations. [INFERRED/PROPOSED]                  |
+-------------------+-----------------------------------------------------------------+
```

---

## 08. Feature Inventory

```text
FEAT-01: Authentication & Identity Management
  ├── Sub-feat 01.1: Registration with NIK and Signature Upload
  ├── Sub-feat 01.2: Dual-Identifier Login (Email or NIK)
  └── Sub-feat 01.3: Secure Session Persistence & Logout

FEAT-02: Cover Letter Management (Warga Portal)
  ├── Sub-feat 02.1: Multi-Type Application Form with Dynamic Requirements
  ├── Sub-feat 02.2: Application History Dashboard with Status Badges
  ├── Sub-feat 02.3: Form Revision Resubmission
  └── Sub-feat 02.4: PDF Viewer and File Downloader

FEAT-03: Letter Review & Approval Engine (RT Portal)
  ├── Sub-feat 03.1: Incoming Application Queue & Filter
  ├── Sub-feat 03.2: Application Detail & AI Draft Inspector
  ├── Sub-feat 03.3: Tri-State Action Handler (Approve / Revision / Reject)
  ├── Sub-feat 03.4: Digital Signature (PIN Auth + QR Code Generation)
  └── Sub-feat 03.5: Physical Signature Dispatch Tracker

FEAT-04: Tanya RT Conversational Assistant
  ├── Sub-feat 04.1: Real-Time Chat Interface (Message Bubbles & Timestamps)
  ├── Sub-feat 04.2: Semantic Knowledge Search & Citation Badging
  └── Sub-feat 04.3: Out-of-Domain WhatsApp Escalation Generator

FEAT-05: Notifications & Alerts
  ├── Sub-feat 05.1: In-App Activity Feed
  └── Sub-feat 05.2: Unread Indicator Badges
```

---

## 09. Screen Inventory

| Screen ID | Screen Name | Route Path | Authorized Roles | Source Evidence |
|---|---|---|---|---|
| **SCREEN-001** | Landing / Welcome Screen | `/` | Guest | Gambar 4.1 [CONFIRMED] |
| **SCREEN-002** | Registration Screen | `/register` | Guest | Gambar 4.2 [CONFIRMED] |
| **SCREEN-003** | Login Screen | `/login` | Guest | Gambar 4.3 (Hal 31) [CONFIRMED] |
| **SCREEN-004** | Citizen Home / Dashboard | `/warga/home` | ROLE-WARGA | Gambar 4.4 (Hal 32) [CONFIRMED] |
| **SCREEN-005** | User Profile & Drawer | `/drawer-menu` | All Authenticated | Gambar 4.5 [CONFIRMED] |
| **SCREEN-006** | Citizen Application History | `/warga/pengajuan` | ROLE-WARGA | Gambar 4.6 [CONFIRMED] |
| **SCREEN-007** | Application Form Screen | `/warga/pengajuan/baru`| ROLE-WARGA | Gambar 4.7 [CONFIRMED] |
| **SCREEN-008** | Application Revision Form | `/warga/pengajuan/revisi/:id`| ROLE-WARGA | Hal 20, 44 [CONFIRMED] |
| **SCREEN-009** | RT Incoming Queue Screen | `/rt/pengajuan` | ROLE-RT | Gambar 4.8 [CONFIRMED] |
| **SCREEN-010** | RT Application Detail & Action| `/rt/pengajuan/:id` | ROLE-RT | Gambar 4.9 [CONFIRMED] |
| **SCREEN-011** | Tanya RT Chatbot Screen | `/chatbot` | ROLE-WARGA | Gambar 4.10 [CONFIRMED] |
| **SCREEN-012** | PDF Document Previewer | `/surat/preview/:id` | All Authenticated | Hal 21, 44 [CONFIRMED] |

---

## 10. User Flow (Summary)

```text
[ Guest User ]
      │
      ├─► (SCREEN-001: Landing) ──► (SCREEN-002: Register) ──► [ Save User & TTD ] ──► (SCREEN-003: Login)
      │                                                                                        │
      └────────────────────────────────────────────────────────────────────────────────────────┘
                                                                                               │
                                                   ┌───────────────────────────────────────────┴───────────────────────────────────────────┐
                                                   ▼ [Role = Warga]                                                                        ▼ [Role = RT]
                                        (SCREEN-004: Warga Home)                                                                (SCREEN-009: RT Queue)
                                                   │                                                                                       │
                      ┌────────────────────────────┼────────────────────────────┐                                                          ▼
                      ▼                            ▼                            ▼                                              (SCREEN-010: Review Detail)
          (SCREEN-007: Form Buat)       (SCREEN-006: Riwayat)         (SCREEN-011: Tanya RT)                                               │
                      │                            │                            │                                           ┌──────────────┼──────────────┐
                      ▼                            │                            ▼                                           ▼              ▼              ▼
              [ Submit + AI Draft ]                │                 [ RAG Search Query ]                                [ Approve ]   [ Request Rev ] [ Reject ]
                      │                            │                            │                                           │              │              │
                      ▼                            │                 ┌──────────┴──────────┐                                │              ▼              ▼
              [ Status = Diajukan ]                │                 ▼                     ▼                                │         [ Notif Warga ] [ Terminate ]
                      │                            │           [ Score >= 0.7 ]      [ Score < 0.7 ]                        │              │
                      │                            │                 │                     │                                │              ▼
                      │                            │                 ▼                     ▼                                │     (SCREEN-008: Form Revisi)
                      │                            │           [ Bot Reply ]         [ WA Escalate ]                        │
                      │                            │                                                                        ▼
                      │                            │                                                            ┌───────────────────────┐
                      │                            │                                                            ▼                       ▼
                      │                            │                                                   [ Method: Digital ]      [ Method: Basah ]
                      │                            │                                                            │                       │
                      │                            │                                                            ▼                       ▼
                      │                            │                                                    [ Embed QR Token ]       [ Print & Ink Sign ]
                      │                            │                                                            │                       │
                      │                            │                                                            ▼                       ▼
                      │                            │                                                    [ Status: Selesai ]     [ Status: Siap Diambil ]
                      │                            │                                                            │                       │
                      └────────────────────────────┴────────────────────────────────────────────────────────────┴───────────────────────┘
                                                   │
                                                   ▼
                                        (SCREEN-012: PDF Preview & Download)
```

---

## 11. Technology Stack Selection

```text
Component                    Observed / Confirmed            Proposed Development Choice        Rationale
-----------------------------------------------------------------------------------------------------------------------------------
Client Framework             Flutter                         Flutter 3.x+ (Dart 3.x+)           Cross-platform native compilation
State Management             NOT OBSERVED                    flutter_riverpod (v2.x)            Compile-time safety & testability
Client Routing               NOT OBSERVED                    go_router                          Declarative URL-driven navigation
HTTP Client                  NOT OBSERVED                    dio                                Interceptors, FormData, timeouts
Local Secure Storage         NOT OBSERVED                    flutter_secure_storage             Encrypted key-value store for JWT
Target Persistence           MySQL                           MySQL 8.0+ / 8.4 LTS               Relational schema & JSON support
AI Letter Formulation        OpenAI API [CONFIRMED]          Technology-Agnostic LLM REST Call  Formalized Indonesian text draft
Chatbot Retrieval (RAG)      Embedding Search [CONFIRMED]    Vector Cosine Similarity           Knowledge grounding over bylaws
```

---

## 12. Architecture (High-Level)
Adheres to **Feature-First Clean Architecture**:
- `lib/core/`: Network clients, token storage, router, global design tokens, error handlers.
- `lib/features/{auth, letters, chatbot, profile}/`:
  - `data/`: Data sources (remote/local), DTO models, repository implementations.
  - `domain/`: Pure business entities, repository interfaces, validation logic.
  - `presentation/`: Riverpod state notifiers/controllers, screens, feature-specific widgets.
- `lib/shared/`: Universal atomic components (buttons, input fields, badges, dialogs).

*(See [`architecture.md`](architecture.md) for complete structural blueprint).*

---

## 13. Database Summary
Single centralized `users` table to maintain relational integrity, linked to `jenis_surat`, `pengajuan_surat`, `surat_final`, `knowledge_base`, `knowledge_chunks`, and `chat_sessions`.  
*(See [`database.md`](database.md) for complete DDL, constraints, and foreign key definitions).*

---

## 14. API Contract Summary
Technology-agnostic REST endpoints with standardized JSON envelopes (`success`, `data`, `message`, `error_code`).  
*(See [`api.md`](api.md) for full endpoint specifications, request payloads, and status codes).*

---

## 15. Design System Summary
High-contrast, mobile-first design system utilizing an Indigo/Slate palette with clean typography, explicit 8dp grid spacing, and Google Stitch-compatible component tokens.  
*(See [`design.md`](design.md) and [`design-tokens.md`](design-tokens.md)).*

---

## 16. Development Phases

```text
Phase 0: Project Setup & Linting
Phase 1: Architecture & Core Infrastructure
Phase 2: Design Tokens & Shared Component Library
Phase 3: Authentication & Identity Management
Phase 4: Citizen Letter Application Flow (Warga)
Phase 5: RT Review & Decision Engine (Ketua RT)
Phase 6: Digital QR Signature & PDF Handling
Phase 7: Tanya RT RAG Chatbot & WA Escalation
Phase 8: End-to-End Integration, BDD Testing, and Verification
```

---

## 17. Task Breakdown Summary
Total Atomic Tasks: 24 Executable Tasks across 9 Phases (`TASK-001` through `TASK-024`).  
*(See [`tasks.md`](tasks.md) for implementation steps, dependencies, and expected outputs).*

---

## 18. Dependencies (Flutter Packages)

```yaml
# PROPOSED PACKAGES (Evaluated for production stability)
dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.5.1      # State management
  go_router: ^14.0.0             # Declarative routing & guards
  dio: ^5.4.1                    # REST client with interceptors
  flutter_secure_storage: ^9.0.0 # Encrypted token storage
  intl: ^0.19.0                  # Date and currency formatting
  qr_flutter: ^4.1.0             # QR Code rendering for verification
  syncfusion_flutter_pdfviewer: ^25.1.39 # In-app PDF previewer
  file_picker: ^8.0.0            # File upload selection
  url_launcher: ^6.2.5           # WhatsApp escalation deep linking

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  mockito: ^5.4.4
  build_runner: ^2.4.8
```

---

## 19. Testing Strategy
- **Unit Testing:** Domain entities, validation rules, repository data parsing.
- **Widget Testing:** Atomic components, error banners, input validation states.
- **Integration / BDD Testing:** Full scenario flows using Gherkin criteria defined in `testing.md`.
- **Target:** 100% pass on core BDD acceptance criteria.

---

## 20. Acceptance Criteria (Global Master Criteria)
1. Resident can register, upload signature, and immediately log in.
2. User is redirected to the appropriate dashboard based on assigned role.
3. Cover letter submission triggers AI draft creation and updates RT queue.
4. RT can approve, request revision, or reject with mandatory rationale.
5. Digital signature workflow embeds verifiable QR code in the generated PDF.
6. Tanya RT Chatbot accurately returns answers from indexed knowledge chunks and defaults to WhatsApp escalation when confidence is low.

---

## 21. Risks and Mitigations

| Risk ID | Risk Description | Severity | Mitigation Strategy |
|---|---|---|---|
| **RISK-001** | LLM Hallucination in letter draft or chatbot answers | HIGH | Use strict system prompt templates for letters; enforce semantic similarity threshold (>= 0.70) with direct RT WhatsApp fallback for chatbot. |
| **RISK-002** | Large PDF / Attachment memory leaks on low-end devices | MEDIUM | Use streaming file downloads and native OS viewer delegation when possible. |
| **RISK-003** | Network latency in citizen mobile environments | MEDIUM | Implement optimistic UI updates, local caching, and exponential backoff retry policies in Dio client. |

---

## 22. Knowledge Gaps
- Exact production server domain hosting the MySQL database (`api_base_url` configurable via environment variables).
- WhatsApp business API vs direct `wa.me` URL schema (Direct `https://wa.me/{phone}?text={query}` is confirmed as lightweight and zero-cost).

---

## 23. Assumptions
- Mobile devices have internet connectivity during submission and chat interactions.
- Residents have a valid NIK (16-digit Indonesian national identity number).
- Ketua RT possesses authority to approve or reject letters on behalf of RT 032 RW 08.

---

## 24. Definition of Done (DoD)
A task or feature is considered **DONE** if and only if:
1. All assigned files are implemented with zero compilation errors (`dart analyze` clean).
2. Code follows design tokens and clean architecture rules without hardcoded styles.
3. Associated automated unit/widget tests in `testing.md` pass successfully.
4. Feature behavior matches the corresponding Acceptance Criteria.
5. Traceability matrix entry in `traceability.md` is updated and marked complete.
