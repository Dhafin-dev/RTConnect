# Atomic Development Tasks — RTConnect

This document contains the master task inventory for AI coding agents. Every task is atomic, executable, testable, strictly sequenced with dependencies, and bound to explicit acceptance criteria.

---

## Phase Summary

```text
PHASE 0: Project Setup & Linting (TASK-001 - TASK-002)
PHASE 1: Core Architecture & Design Tokens (TASK-003 - TASK-005)
PHASE 2: Shared Component Library (TASK-006 - TASK-008)
PHASE 3: Authentication & Identity Management (TASK-009 - TASK-011)
PHASE 4: Cover Letter Citizen Workflow (TASK-012 - TASK-015)
PHASE 5: RT Review & Decision Engine (TASK-016 - TASK-018)
PHASE 6: Digital Signature & PDF Delivery (TASK-019 - TASK-020)
PHASE 7: Tanya RT RAG Chatbot & Escalation (TASK-021 - TASK-023)
PHASE 8: End-to-End Verification & Release (TASK-024)
```

---

## Phase 0: Project Setup & Linting

### TASK ID: TASK-001
- **TITLE:** Initialize Flutter Project Structure & Pubspec Dependencies
- **PHASE:** Phase 0
- **OBJECTIVE:** Establish the base Flutter project with required packages and lint rules.
- **CONTEXT:** Prepares the environment so all subsequent feature modules can import standard libraries.
- **FILES TO CREATE:**
  - `pubspec.yaml`
  - `analysis_options.yaml`
  - `.gitignore`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** None.
- **IMPLEMENTATION STEPS:**
  1. Define dependencies in `pubspec.yaml`: `flutter_riverpod`, `go_router`, `dio`, `flutter_secure_storage`, `qr_flutter`, `syncfusion_flutter_pdfviewer`, `file_picker`, `url_launcher`, `intl`.
  2. Define dev_dependencies: `flutter_test`, `flutter_lints`, `mockito`, `build_runner`.
  3. Configure strict analysis options in `analysis_options.yaml` (pedantic lints, unused import warnings).
- **EXPECTED OUTPUT:** `flutter pub get` completes with exit code 0.
- **ACCEPTANCE CRITERIA:** Zero lint warnings on base project.
- **TESTS:** `flutter analyze`.
- **BLOCKERS:** None.
- **STATUS:** READY

---

### TASK ID: TASK-002
- **TITLE:** Configure Feature-First Directory Layout & Main Entrypoint
- **PHASE:** Phase 0
- **OBJECTIVE:** Create directory structure conforming to `architecture.md`.
- **CONTEXT:** Enforces layer separation across `core/`, `features/`, and `shared/`.
- **FILES TO CREATE:**
  - `lib/main.dart`
  - `lib/core/constants/app_constants.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-001.
- **IMPLEMENTATION STEPS:**
  1. Create directory trees: `lib/core/`, `lib/features/{auth,letters,chatbot,profile}/`, `lib/shared/`.
  2. In `lib/main.dart`, wrap root widget in `ProviderScope`.
  3. Set up `AppConstants` with default base URLs and storage keys.
- **EXPECTED OUTPUT:** `lib/main.dart` compiles and boots into a placeholder widget.
- **ACCEPTANCE CRITERIA:** `runApp` successfully executes with Riverpod `ProviderScope`.
- **TESTS:** `test/widget_test.dart` passes.
- **BLOCKERS:** TASK-001.
- **STATUS:** READY

---

## Phase 1: Core Architecture & Design Tokens

### TASK ID: TASK-003
- **TITLE:** Implement Design Tokens & ThemeData
- **PHASE:** Phase 1
- **OBJECTIVE:** Translate `design-tokens.md` into reusable Dart constants and a cohesive `ThemeData`.
- **CONTEXT:** Ensures all visual styling references single source of truth tokens.
- **FILES TO CREATE:**
  - `lib/core/theme/app_colors.dart`
  - `lib/core/theme/app_typography.dart`
  - `lib/core/theme/app_spacing.dart`
  - `lib/core/theme/app_theme.dart`
- **FILES TO MODIFY:** `lib/main.dart`.
- **DEPENDENCIES:** TASK-002.
- **IMPLEMENTATION STEPS:**
  1. Implement `AppColors` with all tokens (`TOKEN-COLOR-001` through `TOKEN-COLOR-017`).
  2. Implement `AppTypography` with text styles (`TOKEN-TYPO-001` through `TOKEN-TYPO-007`).
  3. Implement `AppSpacing` with 8dp grid constants (`TOKEN-SPACE-001` through `007`).
  4. Create `AppTheme.lightTheme` configuring Material 3 colorScheme, cardTheme, and inputDecorationTheme.
- **EXPECTED OUTPUT:** Theme is cleanly accessible via `Theme.of(context)`.
- **ACCEPTANCE CRITERIA:** All token values match `design-tokens.md` exactly.
- **TESTS:** `test/unit/theme_test.dart`.
- **BLOCKERS:** TASK-002.
- **STATUS:** READY

---

### TASK ID: TASK-004
- **TITLE:** Configure Network Client & Error Interceptors
- **PHASE:** Phase 1
- **OBJECTIVE:** Build the centralized `Dio` API client conforming to `api.md`.
- **CONTEXT:** Standardizes request execution, token injection, and response parsing.
- **FILES TO CREATE:**
  - `lib/core/network/api_client.dart`
  - `lib/core/network/api_endpoints.dart`
  - `lib/core/errors/app_exception.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-002.
- **IMPLEMENTATION STEPS:**
  1. Define `ApiEndpoints` with paths matching `API-001` through `API-015`.
  2. Create `ApiClient` wrapping `Dio` with base options (timeout: 10s).
  3. Implement `AuthInterceptor` retrieving token from secure storage.
  4. Map HTTP 400/401/403/500 errors into typed `AppException`.
- **EXPECTED OUTPUT:** `ApiClient` is injectable via a Riverpod `Provider`.
- **ACCEPTANCE CRITERIA:** Attaches `Bearer <token>` automatically when token is present.
- **TESTS:** `test/unit/network/api_client_test.dart`.
- **BLOCKERS:** TASK-002.
- **STATUS:** READY

---

### TASK ID: TASK-005
- **TITLE:** Set Up Declarative Routing & Role Guards
- **PHASE:** Phase 1
- **OBJECTIVE:** Configure `go_router` with route guards matching `user-flows.md`.
- **CONTEXT:** Handles navigation between auth, citizen dashboard, and RT queue.
- **FILES TO CREATE:**
  - `lib/core/router/app_router.dart`
  - `lib/core/router/route_names.dart`
- **FILES TO MODIFY:** `lib/main.dart`.
- **DEPENDENCIES:** TASK-003, TASK-004.
- **IMPLEMENTATION STEPS:**
  1. Define routes matching `SCREEN-001` through `SCREEN-012`.
  2. Implement redirect logic: if unauthenticated, redirect to `/login` (except on `/` or `/register`).
  3. Implement role guard: prevent warga from reaching `/rt/*` and vice versa.
- **EXPECTED OUTPUT:** Router handles push/pop with URL synchronization.
- **ACCEPTANCE CRITERIA:** Unauthorized deep links redirect to default home route.
- **TESTS:** `test/unit/router_test.dart`.
- **BLOCKERS:** TASK-003.
- **STATUS:** READY

---

## Phase 2: Shared Component Library

### TASK ID: TASK-006
- **TITLE:** Implement Core Button & Input Field Widgets
- **PHASE:** Phase 2
- **OBJECTIVE:** Build atomic core widgets conforming to `components.md`.
- **FILES TO CREATE:**
  - `lib/shared/widgets/rt_primary_button.dart`
  - `lib/shared/widgets/rt_secondary_button.dart`
  - `lib/shared/widgets/rt_text_field.dart`
  - `lib/shared/widgets/rt_status_badge.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-003.
- **IMPLEMENTATION STEPS:**
  1. Code `RTPrimaryButton` (`COMP-CORE-001`) with loading spinner state and 48dp height.
  2. Code `RTSecondaryButton` (`COMP-CORE-002`) with outlined border style.
  3. Code `RTTextField` (`COMP-CORE-003`) with password toggle and validation error rendering.
  4. Code `RTStatusBadge` (`COMP-CORE-004`) mapping status string to colors.
- **EXPECTED OUTPUT:** Atomic widgets ready for form construction.
- **ACCEPTANCE CRITERIA:** Matches design tokens; disables taps during loading.
- **TESTS:** `test/widget/shared/core_components_test.dart`.
- **BLOCKERS:** TASK-003.
- **STATUS:** READY

---

### TASK ID: TASK-007
- **TITLE:** Implement Shell Navigation Components (BottomNav & Drawer)
- **PHASE:** Phase 2
- **OBJECTIVE:** Build bottom navigation and user profile drawer.
- **FILES TO CREATE:**
  - `lib/shared/widgets/rt_bottom_nav_bar.dart`
  - `lib/shared/widgets/rt_app_bar.dart`
  - `lib/shared/widgets/rt_drawer_menu.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-006.
- **IMPLEMENTATION STEPS:**
  1. Implement `RTBottomNavBar` (`COMP-SHR-001`) with tabs: Pengajuan, Beranda, TanyaRT.
  2. Implement `RTAppBar` (`COMP-SHR-002`) with logo, drawer trigger, and notifications.
  3. Implement `RTDrawerMenu` (`COMP-SHR-003`) displaying avatar, role, and logout action.
- **EXPECTED OUTPUT:** Scaffold shell with sticky navigation.
- **ACCEPTANCE CRITERIA:** Active tab accurately reflects current route.
- **TESTS:** `test/widget/shared/navigation_components_test.dart`.
- **BLOCKERS:** TASK-006.
- **STATUS:** READY

---

## Phase 3: Authentication & Identity Management

### TASK ID: TASK-008
- **TITLE:** Implement Auth Domain Entities & Repository Contract
- **PHASE:** Phase 3
- **OBJECTIVE:** Define user models, repository interfaces, and validators.
- **FILES TO CREATE:**
  - `lib/features/auth/domain/user_entity.dart`
  - `lib/features/auth/domain/auth_repository.dart`
  - `lib/features/auth/domain/auth_validators.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-002.
- **IMPLEMENTATION STEPS:**
  1. Create `UserEntity` with fields: `userId`, `nik`, `name`, `email`, `role`, `signatureUrl`.
  2. Define `IAuthRepository` with `login()`, `register()`, `getMe()`, `logout()`.
  3. Implement `AuthValidators.validateNIK()` (16 digits) and `validatePassword()`.
- **ACCEPTANCE CRITERIA:** NIK validation fails on non-digit or length != 16.
- **TESTS:** `test/unit/auth/auth_validators_test.dart`.
- **BLOCKERS:** TASK-002.
- **STATUS:** READY

---

### TASK ID: TASK-009
- **TITLE:** Implement Auth Remote Data Source & Repository Implementation
- **PHASE:** Phase 3
- **OBJECTIVE:** Connect auth repository to backend endpoints `API-001` and `API-002`.
- **FILES TO CREATE:**
  - `lib/features/auth/data/auth_dto.dart`
  - `lib/features/auth/data/auth_remote_data_source.dart`
  - `lib/features/auth/data/auth_repository_impl.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-004, TASK-008.
- **IMPLEMENTATION STEPS:**
  1. Build `AuthDTO` with `fromJson` and `toDomain()` mapping.
  2. Implement `AuthRemoteDataSource` sending multipart/form-data for registration with signature file.
  3. Store returned JWT in `flutter_secure_storage`.
- **ACCEPTANCE CRITERIA:** Successfully caches token on login.
- **TESTS:** `test/unit/auth/auth_repository_test.dart`.
- **BLOCKERS:** TASK-008.
- **STATUS:** READY

---

### TASK ID: TASK-010
- **TITLE:** Build Landing, Login, and Registration Screens
- **PHASE:** Phase 3
- **OBJECTIVE:** Construct `SCREEN-001`, `SCREEN-002`, and `SCREEN-003`.
- **FILES TO CREATE:**
  - `lib/features/auth/presentation/landing_screen.dart`
  - `lib/features/auth/presentation/login_screen.dart`
  - `lib/features/auth/presentation/register_screen.dart`
  - `lib/features/auth/presentation/auth_controller.dart`
- **FILES TO MODIFY:** `lib/core/router/app_router.dart`.
- **DEPENDENCIES:** TASK-007, TASK-009.
- **IMPLEMENTATION STEPS:**
  1. Build `LandingScreen` with welcome banner and CTA buttons.
  2. Build `LoginScreen` with email/NIK input, password field, and submit controller.
  3. Build `RegisterScreen` with multi-field inputs and signature upload box.
  4. Wire `AuthController` using Riverpod `AsyncNotifier`.
- **ACCEPTANCE CRITERIA:** Submitting valid login directs to `/warga/home` or `/rt/pengajuan`.
- **TESTS:** `test/widget/auth/login_screen_test.dart`.
- **BLOCKERS:** TASK-009.
- **STATUS:** READY

---

## Phase 4: Cover Letter Citizen Workflow (Warga)

### TASK ID: TASK-011
- **TITLE:** Implement Cover Letter Domain & Data Layer
- **PHASE:** Phase 4
- **OBJECTIVE:** Model letter entities, types, and repository implementation.
- **FILES TO CREATE:**
  - `lib/features/letters/domain/letter_entity.dart`
  - `lib/features/letters/domain/letter_type_entity.dart`
  - `lib/features/letters/domain/letter_repository.dart`
  - `lib/features/letters/data/letter_dto.dart`
  - `lib/features/letters/data/letter_repository_impl.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-004.
- **IMPLEMENTATION STEPS:**
  1. Define `LetterEntity` with status enums and AI draft field.
  2. Implement `LetterRepositoryImpl` connecting to `API-004`, `API-005`, and `API-006`.
- **ACCEPTANCE CRITERIA:** Parses letter lists and drafts accurately from JSON.
- **TESTS:** `test/unit/letters/letter_repository_test.dart`.
- **BLOCKERS:** TASK-004.
- **STATUS:** READY

---

### TASK ID: TASK-012
- **TITLE:** Build Warga Home Screen & Application History Screen
- **PHASE:** Phase 4
- **OBJECTIVE:** Construct `SCREEN-004` (Home) and `SCREEN-006` (Riwayat Pengajuan).
- **FILES TO CREATE:**
  - `lib/features/letters/presentation/warga_home_screen.dart`
  - `lib/features/letters/presentation/letter_history_screen.dart`
  - `lib/features/letters/presentation/widgets/application_card.dart`
  - `lib/features/letters/presentation/letter_history_controller.dart`
- **FILES TO MODIFY:** `lib/core/router/app_router.dart`.
- **DEPENDENCIES:** TASK-010, TASK-011.
- **IMPLEMENTATION STEPS:**
  1. Build `WargaHomeScreen` with community banner and quick action cards.
  2. Build `LetterHistoryScreen` rendering chronological cards with status badges.
  3. Include pull-to-refresh and empty state placeholder.
- **ACCEPTANCE CRITERIA:** Displays citizen applications with status chips (`Diajukan`, etc.).
- **TESTS:** `test/widget/letters/history_screen_test.dart`.
- **BLOCKERS:** TASK-011.
- **STATUS:** READY

---

### TASK ID: TASK-013
- **TITLE:** Build Cover Letter Application Form Screen
- **PHASE:** Phase 4
- **OBJECTIVE:** Construct `SCREEN-007` for submitting new cover letters.
- **FILES TO CREATE:**
  - `lib/features/letters/presentation/letter_form_screen.dart`
  - `lib/features/letters/presentation/letter_form_controller.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-011, TASK-012.
- **IMPLEMENTATION STEPS:**
  1. Pre-fill citizen NIK, Name, and Address from user profile.
  2. Add dropdown for `jenis_surat` fetched from `API-004`.
  3. Add input for `keperluan` and radio selector for signature method (Digital vs Basah).
  4. On submit, trigger `API-005` and show loading indicator during AI draft synthesis.
- **ACCEPTANCE CRITERIA:** Disallows submission without purpose text; navigates to history on success.
- **TESTS:** `test/widget/letters/letter_form_screen_test.dart`.
- **BLOCKERS:** TASK-012.
- **STATUS:** READY

---

## Phase 5: RT Review & Decision Engine (Ketua RT)

### TASK ID: TASK-014
- **TITLE:** Build RT Incoming Review Queue Screen
- **PHASE:** Phase 5
- **OBJECTIVE:** Construct `SCREEN-009` displaying the administrative inbox for the RT Head.
- **FILES TO CREATE:**
  - `lib/features/letters/presentation/rt_queue_screen.dart`
  - `lib/features/letters/presentation/rt_queue_controller.dart`
  - `lib/features/letters/presentation/widgets/rt_queue_card.dart`
- **FILES TO MODIFY:** `lib/core/router/app_router.dart`.
- **DEPENDENCIES:** TASK-011.
- **IMPLEMENTATION STEPS:**
  1. Implement `RTQueueScreen` fetching applications from `API-007`.
  2. Implement filter tabs (`Perlu Tindakan`, `Selesai`, `Semua`).
  3. Card tap pushes route to `/rt/pengajuan/:id`.
- **ACCEPTANCE CRITERIA:** Lists pending applications chronologically with applicant names.
- **TESTS:** `test/widget/letters/rt_queue_screen_test.dart`.
- **BLOCKERS:** TASK-011.
- **STATUS:** READY

---

### TASK ID: TASK-015
- **TITLE:** Build RT Application Detail & AI Draft Review Screen
- **PHASE:** Phase 5
- **OBJECTIVE:** Construct `SCREEN-010` with AI draft inspector and decision buttons.
- **FILES TO CREATE:**
  - `lib/features/letters/presentation/rt_detail_screen.dart`
  - `lib/features/letters/presentation/widgets/ai_draft_card.dart`
  - `lib/features/letters/presentation/widgets/decision_modal_dialog.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-014.
- **IMPLEMENTATION STEPS:**
  1. Render applicant details, purpose, and attachment preview.
  2. Render `AIDraftCard` displaying the Generative AI-synthesized draf letter text.
  3. Implement action bar: "Setuju" (Green), "Revisi" (Amber), "Tolak" (Red).
  4. Open `DecisionModalDialog` on Revisi/Tolak to capture mandatory notes before dispatching `API-010`.
- **ACCEPTANCE CRITERIA:** Updates status in queue immediately upon decision submission.
- **TESTS:** `test/widget/letters/rt_detail_screen_test.dart`.
- **BLOCKERS:** TASK-014.
- **STATUS:** READY

---

## Phase 6: Digital Signature & PDF Delivery

### TASK ID: TASK-016
- **TITLE:** Implement Digital QR Signature Confirmation & Physical Dispatch Tracking
- **PHASE:** Phase 6
- **OBJECTIVE:** Build PIN confirmation modal for digital signing (`API-011`) and physical status tracker (`API-012`).
- **FILES TO CREATE:**
  - `lib/features/letters/presentation/widgets/pin_confirmation_dialog.dart`
  - `lib/features/letters/presentation/digital_signature_controller.dart`
- **FILES TO MODIFY:** `lib/features/letters/presentation/rt_detail_screen.dart`.
- **DEPENDENCIES:** TASK-015.
- **IMPLEMENTATION STEPS:**
  1. If method is Digital, prompt RT Head for 6-digit security PIN.
  2. Dispatch `API-011` to seal document and obtain `qr_verification_token`.
  3. If method is Basah, render "Cetak Dokumen" and "Konfirmasi Siap Diambil" button (`API-012`).
- **ACCEPTANCE CRITERIA:** Transitions status to `Selesai` (digital) or `Siap Diambil` (basah).
- **TESTS:** `test/unit/letters/signature_flow_test.dart`.
- **BLOCKERS:** TASK-015.
- **STATUS:** READY

---

### TASK ID: TASK-017
- **TITLE:** Build PDF Document Previewer & Downloader Screen
- **PHASE:** Phase 7
- **OBJECTIVE:** Construct `SCREEN-012` to view and download official finalized letters.
- **FILES TO CREATE:**
  - `lib/features/letters/presentation/pdf_viewer_screen.dart`
- **FILES TO MODIFY:** `lib/core/router/app_router.dart`.
- **DEPENDENCIES:** TASK-016.
- **IMPLEMENTATION STEPS:**
  1. Embed `SfPdfViewer.network` loading from `API-013`.
  2. Provide floating action button to trigger file download to local storage.
  3. Display verification banner indicating QR Code validity.
- **ACCEPTANCE CRITERIA:** Successfully streams and renders official signed PDF.
- **TESTS:** `test/widget/letters/pdf_viewer_screen_test.dart`.
- **BLOCKERS:** TASK-016.
- **STATUS:** READY

---

## Phase 7: Tanya RT RAG Chatbot & Escalation

### TASK ID: TASK-018
- **TITLE:** Implement Chatbot Domain & Data Layer
- **PHASE:** Phase 7
- **OBJECTIVE:** Model chat sessions, message entities, and RAG query repository.
- **FILES TO CREATE:**
  - `lib/features/chatbot/domain/chat_message_entity.dart`
  - `lib/features/chatbot/domain/chatbot_repository.dart`
  - `lib/features/chatbot/data/chat_message_dto.dart`
  - `lib/features/chatbot/data/chatbot_repository_impl.dart`
- **FILES TO MODIFY:** None.
- **DEPENDENCIES:** TASK-004.
- **IMPLEMENTATION STEPS:**
  1. Model `ChatMessageEntity` (`id`, `text`, `isUser`, `citation`, `isEscalated`, `waUrl`).
  2. Implement `ChatbotRepositoryImpl` calling `API-014`.
- **ACCEPTANCE CRITERIA:** Parses both grounded answers and escalation fallback payloads.
- **TESTS:** `test/unit/chatbot/chatbot_repository_test.dart`.
- **BLOCKERS:** TASK-004.
- **STATUS:** READY

---

### TASK ID: TASK-019
- **TITLE:** Build Tanya RT Conversational Chatbot Screen
- **PHASE:** Phase 7
- **OBJECTIVE:** Construct `SCREEN-011` with message bubbles and WhatsApp escalation button.
- **FILES TO CREATE:**
  - `lib/features/chatbot/presentation/chatbot_screen.dart`
  - `lib/features/chatbot/presentation/chatbot_controller.dart`
  - `lib/features/chatbot/presentation/widgets/chat_bubble.dart`
  - `lib/features/chatbot/presentation/widgets/whatsapp_escalation_card.dart`
- **FILES TO MODIFY:** `lib/core/router/app_router.dart`.
- **DEPENDENCIES:** TASK-018.
- **IMPLEMENTATION STEPS:**
  1. Build scrollable chat view with auto-scroll to bottom.
  2. Render `ChatBubble` with distinct colors for user vs bot and source citations.
  3. Render `WhatsAppEscalationCard` when `isEscalated == true`.
  4. Wire WhatsApp button with `url_launcher` to open `https://wa.me/...`.
- **ACCEPTANCE CRITERIA:** Displays bot answer within 3 seconds; launches WhatsApp on escalation click.
- **TESTS:** `test/widget/chatbot/chatbot_screen_test.dart`.
- **BLOCKERS:** TASK-018.
- **STATUS:** READY

---

## Phase 8: End-to-End Verification & Release

### TASK ID: TASK-020
- **TITLE:** End-to-End BDD Integration Testing & Quality Audit
- **PHASE:** Phase 8
- **OBJECTIVE:** Execute complete test suite matching `testing.md`.
- **FILES TO CREATE:**
  - `integration_test/app_flow_test.dart`
- **FILES TO MODIFY:** `traceability.md`.
- **DEPENDENCIES:** TASK-010, TASK-013, TASK-015, TASK-017, TASK-019.
- **IMPLEMENTATION STEPS:**
  1. Run automated integration test registering a user, submitting a letter, approving with digital signature, and downloading the PDF.
  2. Verify that Tanya RT chatbot correctly replies or displays the WhatsApp fallback card.
  3. Ensure `dart analyze` passes with zero errors and warnings.
  4. Mark all items complete in `traceability.md`.
- **EXPECTED OUTPUT:** 100% test pass rate.
- **ACCEPTANCE CRITERIA:** All BDD scenarios pass without regression.
- **TESTS:** `flutter test integration_test/app_flow_test.dart`.
- **BLOCKERS:** All prior tasks.
- **STATUS:** READY
