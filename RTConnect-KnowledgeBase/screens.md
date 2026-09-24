# Screen Specifications — RTConnect

This document details the screen-level implementation specifications for all Flutter views in the RTConnect application.

---

## Screen Inventory

| ID | Screen Name | Route | Role | Entry Point | Exit Point | Key Components | State |
|---|---|---|---|---|---|---|---|
| **SCREEN-001** | Landing / Welcome Screen | `/` | Guest | App Launch | Login / Register | Hero Brand, Dual Action Buttons, Bottom Nav | Static |
| **SCREEN-002** | Registration Screen | `/register` | Guest | Landing Screen | Login Screen | Registration Form, Signature Canvas/Upload | Form State |
| **SCREEN-003** | Login Screen | `/login` | Guest | Landing Screen | Role Dashboard | Identifier & Password Form, Submit Button | Async Auth State |
| **SCREEN-004** | Warga Home Screen | `/warga/home` | Warga | Login / Nav | Form / Chatbot | Hero Banner, Quick CTA Cards, Bottom Nav | Cached Profile |
| **SCREEN-005** | Profile & Drawer Menu | `/drawer` | Authenticated | Hamburger Icon | Any Root Screen | Avatar, User Meta, Nav List, Logout Button | User State |
| **SCREEN-006** | Warga Application History | `/warga/pengajuan` | Warga | Bottom Nav | Detail / New Form | Filter Chips, Card List, Floating Action Button | Async List State |
| **SCREEN-007** | Application Form Screen | `/warga/pengajuan/baru`| Warga | Home / History | History Screen | Auto-fill Meta, Dropdown, Radio, File Picker | Form Async State|
| **SCREEN-008** | Application Revision Form | `/warga/pengajuan/revisi/:id`| Warga| History Detail | History Screen | Form with Prior Data, Revision Notice Banner| Form Async State|
| **SCREEN-009** | RT Incoming Queue Screen | `/rt/pengajuan` | RT | Login | Application Detail| Status Filter Tabs, Incoming Cards, Bottom Nav | Async List State |
| **SCREEN-010** | RT Application Detail | `/rt/pengajuan/:id`| RT | Queue Screen | Queue Screen | Citizen Meta, AI Draft Card, Action Bar | Async Detail State|
| **SCREEN-011** | Tanya RT Chatbot Screen | `/chatbot` | Warga | Bottom Nav | Home / WA App | Message Bubble List, Input Field, WA Fallback | Stream/List State|
| **SCREEN-012** | PDF Document Viewer | `/surat/preview/:id`| All | History / Queue | Prior Screen | PDF Render View, Download FAB, Share Button | Async File State |

---

## Screen Detail Specifications

### SCREEN ID: SCREEN-001
- **NAME:** Landing / Welcome Screen
- **ROUTE:** `/`
- **ROLE:** Guest / Unauthenticated
- **PURPOSE:** Welcome landing page introducing RTConnect and serving as the gateway to authentication.
- **ENTRY CONDITIONS:** User is unauthenticated.
- **LAYOUT:** Vertical column centered within `SafeArea`, topped by the logo, centered title, primary action buttons, and pinned bottom navigation.
- **COMPONENTS:** `BrandLogo`, `DisplayHeading` ("Selamat Datang RTConnect"), `PrimaryButton` ("Masuk"), `SecondaryButton` ("Registrasi"), `BottomNavBar`.
- **DATA REQUIRED:** None.
- **STATE REQUIRED:** None.
- **USER ACTIONS:** Tap "Masuk" -> Navigates to `/login`; Tap "Registrasi" -> Navigates to `/register`.
- **NAVIGATION:** Push to `/login` or `/register`.
- **LOADING STATE:** Not applicable.
- **EMPTY STATE:** Not applicable.
- **ERROR STATE:** Not applicable.
- **SUCCESS STATE:** Not applicable.
- **RESPONSIVE BEHAVIOR:** Padded uniformly with max width 420dp.
- **ACCESSIBILITY:** Semantics configured for primary brand buttons.
- **ACCEPTANCE CRITERIA:** Renders title, subtitle, and both buttons; clicking either redirects accurately.

---

### SCREEN ID: SCREEN-002
- **NAME:** Registration Screen
- **ROUTE:** `/register`
- **ROLE:** Guest / Citizen
- **PURPOSE:** Enables new residents to create an account by filling credentials and providing an official digital signature image.
- **ENTRY CONDITIONS:** Guest user taps "Registrasi".
- **LAYOUT:** SingleChildScrollView containing a stepped form card.
- **COMPONENTS:** Form fields (NIK, Full Name, Address, Phone, Email, Password, Password Confirm), `SignatureUploadBox`, `SubmitButton` ("Daftar Akun").
- **DATA REQUIRED:** None initially.
- **STATE REQUIRED:** `RegisterFormState` (field controllers, validation state, uploaded signature file path, isSubmitting boolean).
- **USER ACTIONS:** Fill fields, attach PNG/JPG signature, tap "Daftar".
- **NAVIGATION:** On success, redirect to `/login` with success snackbar.
- **LOADING STATE:** Submit button disabled and shows progress spinner.
- **EMPTY STATE:** Empty form with placeholders.
- **ERROR STATE:** Inline field errors (e.g. "NIK harus 16 digit angka").
- **SUCCESS STATE:** SnackBar "Pendaftaran berhasil, silakan masuk".
- **RESPONSIVE BEHAVIOR:** Keyboard-aware scroll view (`keyboardDismissBehavior: onDrag`).
- **ACCESSIBILITY:** All fields have associated descriptive text labels.
- **ACCEPTANCE CRITERIA:** Disallows submission if NIK length != 16 or signature is missing; creates record on valid input.

---

### SCREEN ID: SCREEN-003
- **NAME:** Login Screen
- **ROUTE:** `/login`
- **ROLE:** Guest / All Users
- **PURPOSE:** Authenticates residents and RT Heads into their respective dashboards.
- **ENTRY CONDITIONS:** User is on `/login`.
- **LAYOUT:** Centered card with email/NIK input, password input with show/hide toggle, and "Masuk" button.
- **COMPONENTS:** `CustomTextField` (Identifier), `CustomTextField` (Password), `PrimaryButton` ("Masuk"), `TextButton` ("Belum punya akun? Daftar").
- **DATA REQUIRED:** None.
- **STATE REQUIRED:** `LoginFormState` (identifier, password, isSubmitting, errorMessage).
- **USER ACTIONS:** Input credentials, tap "Masuk".
- **NAVIGATION:** If `role == 'warga'`, navigate to `/warga/home`; if `role == 'rt'`, navigate to `/rt/pengajuan`.
- **LOADING STATE:** Submit button displays circular spinner.
- **ERROR STATE:** Floating red error banner on HTTP 401.
- **SUCCESS STATE:** Transitions immediately into target dashboard.
- **ACCEPTANCE CRITERIA:** Successfully parses role and routes appropriately; blocks invalid passwords.

---

### SCREEN ID: SCREEN-004
- **NAME:** Warga Home Screen
- **ROUTE:** `/warga/home`
- **ROLE:** Citizen (`warga`)
- **PURPOSE:** Primary hub for citizens to access services, check news, and launch letter requests or AI inquiries.
- **ENTRY CONDITIONS:** User is authenticated as Warga.
- **LAYOUT:** Top AppBar with hamburger icon, hero card with community branding, quick-action buttons, bottom navigation.
- **COMPONENTS:** `AppBarWithDrawer`, `HeroBanner`, `PrimaryButton` ("Ajukan Surat"), `SecondaryButton` ("Tanya RT"), `BottomNavBar`.
- **DATA REQUIRED:** Authenticated user profile (`nama_lengkap`, `alamat`).
- **STATE REQUIRED:** `AsyncValue<UserProfile>`.
- **USER ACTIONS:** Tap "Ajukan Surat" -> Navigates to `/warga/pengajuan/baru`; Tap "Tanya RT" -> Navigates to `/chatbot`.
- **NAVIGATION:** Push to application form or switch tab to Tanya RT.
- **ACCEPTANCE CRITERIA:** Displays user's name accurately and routes to child features.

---

### SCREEN ID: SCREEN-006
- **NAME:** Citizen Application History Screen
- **ROUTE:** `/warga/pengajuan`
- **ROLE:** Citizen (`warga`)
- **PURPOSE:** Displays chronological tracking of all letter requests made by the resident.
- **ENTRY CONDITIONS:** Citizen selects "Pengajuan" tab or taps history.
- **LAYOUT:** Scaffold with pull-to-refresh `ListView` of application cards, topped by filter chips, with a floating action button "Buat Pengajuan Baru".
- **COMPONENTS:** `FilterChipRow`, `ApplicationCard`, `StatusBadge`, `FloatingActionButton`, `EmptyStateWidget`.
- **DATA REQUIRED:** List of `LetterEntity` records for authenticated user.
- **STATE REQUIRED:** `AsyncValue<List<LetterEntity>>`, selected status filter.
- **USER ACTIONS:** Tap card -> Opens `/surat/preview/:id` if finished or detail if revising; Pull down to refresh.
- **LOADING STATE:** Shimmer cards placeholder.
- **EMPTY STATE:** Illustrated container with "Belum ada pengajuan" and button to create new.
- **ERROR STATE:** Error container with "Gagal memuat riwayat" and "Coba Lagi" button.
- **ACCEPTANCE CRITERIA:** Shows accurate status badges (`Diajukan`, `Perlu Revisi`, `Disetujui`, `Siap Diambil`, `Selesai`).

---

### SCREEN ID: SCREEN-007
- **NAME:** Application Form Screen
- **ROUTE:** `/warga/pengajuan/baru`
- **ROLE:** Citizen (`warga`)
- **PURPOSE:** Allows citizens to choose a letter type, input details, select signature method, and submit.
- **ENTRY CONDITIONS:** Citizen taps "Ajukan Surat".
- **LAYOUT:** Scrollable form card.
- **COMPONENTS:** Read-only auto-filled user summary, `DropdownButtonFormField` (Jenis Surat), `TextFormField` (Keperluan), `RadioListTile` (Tanda Tangan Digital vs Basah), `FileUploadBox`, `PrimaryButton` ("Kirim Pengajuan").
- **DATA REQUIRED:** Available letter types list (`/letters/types`).
- **STATE REQUIRED:** Selected letter type, purpose text, signature method enum, attached file.
- **USER ACTIONS:** Select options, write purpose, tap "Kirim Pengajuan".
- **LOADING STATE:** Progress indicator while AI generates draft on backend.
- **SUCCESS STATE:** Confirmation dialog: "Pengajuan berhasil dikirim!" -> Redirects to `/warga/pengajuan`.
- **ACCEPTANCE CRITERIA:** Enforces purpose input; disallows submission with invalid parameters.

---

### SCREEN ID: SCREEN-009
- **NAME:** RT Incoming Queue Screen
- **ROUTE:** `/rt/pengajuan`
- **ROLE:** RT Head (`rt`)
- **PURPOSE:** Inbox for the RT Head to monitor and process citizen requests.
- **ENTRY CONDITIONS:** User is authenticated as RT Head.
- **LAYOUT:** Segmented tab bar (`Perlu Ditinjau`, `Disetujui`, `Selesai`), list of cards displaying applicant name, letter type, and submission date.
- **COMPONENTS:** `TabBar`, `RTApplicationCard`, `BottomNavBar`.
- **DATA REQUIRED:** Stream/List of all neighborhood applications.
- **STATE REQUIRED:** Filter state, search query.
- **USER ACTIONS:** Tap application card -> Opens `SCREEN-010`.
- **ACCEPTANCE CRITERIA:** Displays pending applications chronologically with applicant names.

---

### SCREEN ID: SCREEN-010
- **NAME:** RT Application Detail & Action Screen
- **ROUTE:** `/rt/pengajuan/:id`
- **ROLE:** RT Head (`rt`)
- **PURPOSE:** Review citizen data, attached documents, and the Generative AI letter draft, followed by issuing an approval, revision, or rejection decision.
- **ENTRY CONDITIONS:** RT Head selects a card from the queue.
- **LAYOUT:** Scrollable sectioned card view:
  1. Section A: Citizen Information (NIK, Name, Address, Phone).
  2. Section B: Application Parameters (Type, Purpose, Signature Method).
  3. Section C: AI Letter Draft Preview Container.
  4. Section D: Attachments thumbnail viewer.
  5. Action Bar: Tri-button footer (Setuju, Revisi, Tolak).
- **COMPONENTS:** `AIDraftCard`, `ActionButtons` (`Setuju` [Green], `Revisi` [Amber], `Tolak` [Red]), `ReasonModalDialog`.
- **DATA REQUIRED:** Full `LetterEntity` record including `draf_ai_konten`.
- **STATE REQUIRED:** Active decision loading state.
- **USER ACTIONS:**
  - Tap "Setuju": If Digital, prompt PIN modal; if Basah, prompt print confirmation.
  - Tap "Revisi": Opens modal for revision notes -> Updates status to `Perlu Revisi`.
  - Tap "Tolak": Opens modal for rejection reason -> Updates status to `Ditolak`.
- **ACCEPTANCE CRITERIA:** Disallows empty notes on revision or rejection; updates status instantly.

---

### SCREEN ID: SCREEN-011
- **NAME:** Tanya RT Chatbot Screen
- **ROUTE:** `/chatbot`
- **ROLE:** Citizen (`warga`)
- **PURPOSE:** Conversational interface for citizens to ask questions regarding community procedures.
- **ENTRY CONDITIONS:** Citizen taps "TanyaRT" tab.
- **LAYOUT:** App bar ("Tanya RT"), scrollable message list with auto-scroll to bottom, bottom input bar with send button.
- **COMPONENTS:** `ChatMessageList`, `UserMessageBubble`, `BotMessageBubble`, `SourceCitationChip`, `WhatsAppEscalationCard`, `ChatInputField`.
- **DATA REQUIRED:** Active `chat_messages` for current session.
- **STATE REQUIRED:** `ChatControllerState` (message list, isTyping boolean, text controller).
- **USER ACTIONS:** Type text and tap Send; if escalation appears, tap "Hubungi Ketua RT via WhatsApp".
- **ACCEPTANCE CRITERIA:** Displays typing indicator while RAG search executes; renders WhatsApp escalation button if query cannot be answered.

---

### SCREEN ID: SCREEN-012
- **NAME:** PDF Document Previewer Screen
- **ROUTE:** `/surat/preview/:id`
- **ROLE:** All Authenticated Users
- **PURPOSE:** Full-screen in-app rendering of the official letter PDF with option to download or verify tempelan gambar tanda tangan.
- **ENTRY CONDITIONS:** Tapping "Unduh Surat" or "Lihat Surat" on a completed application.
- **LAYOUT:** Full-height PDF viewer with floating action buttons to download or share.
- **COMPONENTS:** `SfPdfViewer`, `DownloadFAB`, `VerificationBadge`.
- **DATA REQUIRED:** Letter PDF stream URL and `signature_image_path`.
- **STATE REQUIRED:** PDF loading percentage.
- **USER ACTIONS:** Zoom, pan, tap Download to save file locally.
- **ACCEPTANCE CRITERIA:** Loads valid PDF stream and saves to device downloads folder.
