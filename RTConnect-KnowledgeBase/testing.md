# Testing Specification & Test Cases — RTConnect

This document details the test matrix, test harnesses, and automated test cases covering Unit, Widget, Integration, BDD, Navigation, State, Visual, Responsive, and Regression Testing for the RTConnect Flutter application.

---

## Testing Matrix Overview

| Test Category | Target Layer / Scope | Framework / Tool | Coverage Target |
|---|---|---|---|
| **Unit Testing** | Domain entities, Validators, Repository mappers | `package:flutter_test`, `mockito` | >= 85% domain coverage |
| **Widget Testing** | Core components, Form fields, Chat bubbles | `package:flutter_test` (`WidgetTester`) | 100% core components |
| **Integration / BDD**| Complete citizen and RT workflows | `integration_test`, Gherkin runner | 100% acceptance criteria |
| **Navigation Testing**| Route guards, Deep linking, Role redirection | `go_router` test harness | All 12 routes tested |
| **State Testing** | Riverpod AsyncNotifiers, Mutation handlers | `ProviderContainer` unit harness | All state transitions |
| **API Contract Test** | DTO serialization, HTTP interceptor headers | MockWebServer / HttpMockAdapter | All 15 endpoints verified |
| **Responsive Test** | Viewport constraint tests (360dp vs 428dp) | `WidgetTester.binding.setSurfaceSize` | Zero overflow exceptions |

---

## 1. Unit Testing Specifications

### TEST ID: TEST-UNIT-001
- **TARGET:** `AuthValidators.validateNIK`
- **GIVEN:** An unauthenticated citizen filling the registration form.
- **WHEN:** The citizen inputs strings of varying formats ("12345", "351508210499000a", "3515082104990001").
- **THEN:** The validator returns an error string for non-16 digits and null for valid 16-digit strings.
- **EXPECTED RESULT:** PASS. Strings with non-digits or length != 16 are rejected.

---

### TEST ID: TEST-UNIT-002
- **TARGET:** `LetterDTO.fromJson`
- **GIVEN:** A valid JSON response representing a cover letter with an AI-generated draft.
- **WHEN:** `LetterDTO.fromJson` is invoked.
- **THEN:** It instantiates a strongly typed DTO matching all nested fields without null errors.
- **EXPECTED RESULT:** PASS. Fields `nomor_pengajuan`, `status`, and `draf_ai` are parsed accurately.

---

### TEST ID: TEST-UNIT-003
- **TARGET:** `ChatbotRepository.query`
- **GIVEN:** A mock network client returning a grounded knowledge answer with similarity score 0.88.
- **WHEN:** The repository executes `query("Syarat domisili")`.
- **THEN:** It maps the response into a `ChatMessageEntity` with `isEscalated == false` and non-null citation.
- **EXPECTED RESULT:** PASS. Accurate domain entity created.

---

## 2. Widget Testing Specifications

### TEST ID: TEST-WGT-001
- **TARGET:** `RTPrimaryButton` (`COMP-CORE-001`)
- **GIVEN:** `RTPrimaryButton` rendered with `isLoading: true`.
- **WHEN:** The widget tester taps the button.
- **THEN:** The click callback is not invoked, text label is hidden, and `CircularProgressIndicator` is visible.
- **EXPECTED RESULT:** PASS. Disables interactions during async loading.

---

### TEST ID: TEST-WGT-002
- **TARGET:** `RTStatusBadge` (`COMP-CORE-004`)
- **GIVEN:** `RTStatusBadge` rendered with `status: "perlu_revisi"`.
- **WHEN:** Widget is pumped into the test tree.
- **THEN:** It renders text "Perlu Revisi" with a red background matching `TOKEN-COLOR-011`.
- **EXPECTED RESULT:** PASS. Visual mapping matches status specifications.

---

### TEST ID: TEST-WGT-003
- **TARGET:** `RTWhatsAppEscalationCard` (`COMP-FEAT-005`)
- **GIVEN:** An escalated chat response rendered on `SCREEN-011`.
- **WHEN:** User views the chat screen.
- **THEN:** An action card is present with a green WhatsApp button and message "Hubungi Ketua RT via WhatsApp".
- **EXPECTED RESULT:** PASS. Escalation card is rendered exclusively when out-of-domain.

---

## 3. Navigation & Route Guard Testing

### TEST ID: TEST-NAV-001
- **TARGET:** `AppRouter` Auth Guard
- **GIVEN:** An unauthenticated user session (`auth_token == null`).
- **WHEN:** User attempts to navigate directly to `/warga/home`.
- **THEN:** The router intercepts the path and redirects the browser/app to `/login`.
- **EXPECTED RESULT:** PASS. Protected views inaccessible without token.

---

### TEST ID: TEST-NAV-002
- **TARGET:** `AppRouter` Role Guard
- **GIVEN:** An authenticated citizen session (`role == 'warga'`).
- **WHEN:** Citizen attempts to navigate to RT inbox `/rt/pengajuan`.
- **THEN:** The router intercepts the path and returns citizen to `/warga/home`.
- **EXPECTED RESULT:** PASS. Cross-role boundary violation strictly prevented.

---

## 4. State Management Testing (Riverpod)

### TEST ID: TEST-STATE-001
- **TARGET:** `LetterHistoryNotifier`
- **GIVEN:** A `ProviderContainer` initialized with mocked `LetterRepository`.
- **WHEN:** `letterHistoryNotifierProvider.future` completes.
- **THEN:** State transitions from `AsyncLoading` to `AsyncData` holding the letter list.
- **EXPECTED RESULT:** PASS. State container emits expected asynchronous lifecycle events.

---

## 5. Responsive & Overflow Testing

### TEST ID: TEST-RESP-001
- **TARGET:** `ApplicationFormScreen` (`SCREEN-007`) on Minimum Viewport (360x640dp)
- **GIVEN:** Virtual display size set to 360 width x 640 height with software keyboard active (insets 280dp).
- **WHEN:** Screen is pumped and text inputs are populated.
- **THEN:** No `RenderFlex overflowed` exception occurs.
- **EXPECTED RESULT:** PASS. Form scrolls freely without UI clipping.

---

## 6. End-to-End Integration & BDD Acceptance Testing

### TEST ID: TEST-INT-001 (Full Citizen Letter Application Flow)
- **TARGET:** End-to-end Cover Letter Submission & Approval
- **GIVEN:**
  - Citizen "Budi" is logged in on `SCREEN-004`.
  - Backend and database contain seed letter types.
- **WHEN:**
  1. Budi taps "Ajukan Surat" -> Lands on `SCREEN-007`.
  2. Budi selects "Surat Keterangan Domisili", types "Perpanjangan KTP", selects "Tanda Tangan Digital", and taps "Kirim Pengajuan".
  3. Budi is redirected to `SCREEN-006` and sees application with badge "Diajukan".
  4. RT Head logs in, opens `SCREEN-009`, sees Budi's application, and taps to open `SCREEN-010`.
  5. RT Head inspects AI draft, enters PIN "123456", and taps "Setuju & Bubuhkan TTD Digital".
  6. Budi opens application on `SCREEN-006`, status is updated to "Selesai", and taps "Unduh Surat".
- **THEN:**
  - PDF preview loads on `SCREEN-012` displaying verified tempelan gambar tanda tangan token.
- **EXPECTED RESULT:** PASS. End-to-end citizen to RT workflow completes with zero state divergence.

---

### TEST ID: TEST-INT-002 (Tanya RT RAG Knowledge Retrieval & Escalation)
- **TARGET:** Tanya RT Chatbot Semantic Verification
- **GIVEN:** Citizen opens `SCREEN-011` (`/chatbot`).
- **WHEN:**
  - Citizen asks: "Apa syarat mengurus surat domisili?"
- **THEN:**
  - Bot responds with grounded text mentioning KTP and community guidelines, displaying citation badge.
- **WHEN:**
  - Citizen asks: "Siapa juara piala dunia 2022?" (Out-of-domain).
- **THEN:**
  - Bot displays: "Maaf, informasi tersebut belum tercatat dalam basis data resmi RT 032."
  - Bot renders `RTWhatsAppEscalationCard` with active WhatsApp URL.
- **EXPECTED RESULT:** PASS. Demonstrates 100% compliance with RAG knowledge boundary rules.
