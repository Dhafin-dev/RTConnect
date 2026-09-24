# Traceability Matrix Specification — RTConnect

This document establishes bidirectional traceability connecting source evidence from the reverse-engineered document (`Kelompok3_I1_TugasWeek4.pdf` & UML/PowerDesigner artifacts) down to software requirements, screens, components, development tasks, and test cases.

---

## Traceability Chain Schema

```text
SOURCE (Document Evidence)
      ↓
REQUIREMENT (Functional / Non-Functional Spec)
      ↓
SCREEN (UI Route & View)
      ↓
COMPONENT (Atomic / Molecular Widget)
      ↓
TASK (Atomic Executable Implementation Item)
      ↓
TEST (Automated Verification Test Case)
```

---

## End-to-End Traceability Matrix

| Source Evidence ID | Requirement ID | Screen ID | Component ID | Task ID | Test ID | Verification Status |
|---|---|---|---|---|---|---|
| **SRC-DOC-P01** (Cover & Latar Belakang) | `REQ-F-001` (Registration) | `SCREEN-002` (Register) | `COMP-CORE-003` (TextField), `COMP-CORE-001` (PrimaryBtn) | `TASK-008`, `TASK-010` | `TEST-UNIT-001`, `TEST-WGT-001` | VERIFIED |
| **SRC-DOC-P15** (Use Case Diagram UC-01/02) | `REQ-F-002` (Login) | `SCREEN-003` (Login) | `COMP-CORE-003` (TextField), `COMP-CORE-001` (PrimaryBtn) | `TASK-009`, `TASK-010` | `TEST-NAV-001`, `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P16** (Use Case Spec Mengajukan) | `REQ-F-005` (Submit Letter)| `SCREEN-007` (Form Buat)| `COMP-CORE-003`, `COMP-CORE-001` | `TASK-011`, `TASK-013` | `TEST-RESP-001`, `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P13** (TO-BE BPMN AI Drafting) | `REQ-F-006` (AI Draft) | `SCREEN-010` (RT Detail)| `COMP-FEAT-003` (AIDraftPreviewCard) | `TASK-011`, `TASK-015` | `TEST-UNIT-002`, `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P34** (Gambar 4.6 Page Pengajuan)| `REQ-F-007` (History) | `SCREEN-006` (Riwayat) | `COMP-FEAT-001` (ApplicationCard), `COMP-CORE-004` (StatusBadge)| `TASK-012` | `TEST-WGT-002`, `TEST-STATE-001`| VERIFIED |
| **SRC-DOC-P20** (Use Case Spec Revisi) | `REQ-F-008` (Revision) | `SCREEN-008` (Form Rev) | `COMP-CORE-003`, `COMP-CORE-001` | `TASK-013` | `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P36** (Gambar 4.8 Pengajuan RT) | `REQ-F-009` (RT Queue) | `SCREEN-009` (RT Inbox) | `COMP-FEAT-002` (QueueCard), `COMP-SHR-001` (BottomNav) | `TASK-014` | `TEST-NAV-002`, `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P23** (Use Case Spec Tindak Lanjut)|`REQ-F-010` (Decision) | `SCREEN-010` (RT Detail)| `COMP-FEAT-006` (DecisionDialog), `COMP-CORE-001` | `TASK-015` | `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P25** (Use Case Spec TTD Digital)| `REQ-F-011` (Digital Sign)| `SCREEN-010` (RT Detail)| `COMP-CORE-001`, `COMP-FEAT-006` | `TASK-016` | `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P24** (Use Case Spec TTD Basah) | `REQ-F-012` (Physical Sign)| `SCREEN-010` (RT Detail)| `COMP-CORE-001`, `COMP-CORE-002` | `TASK-016` | `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P21** (Use Case Spec Download) | `REQ-F-013` (PDF Viewer) | `SCREEN-012` (PDF View) | `SfPdfViewer`, `DownloadFAB` | `TASK-017` | `TEST-INT-001` | VERIFIED |
| **SRC-DOC-P18** (Use Case Spec Chatbot) | `REQ-F-014` (RAG Chat) | `SCREEN-011` (Chatbot) | `COMP-FEAT-004` (ChatBubble) | `TASK-018`, `TASK-019` | `TEST-UNIT-003`, `TEST-INT-002` | VERIFIED |
| **SRC-DOC-P19** (Use Case Spec Eskalasi WA)| `REQ-F-015` (WA Escalate)| `SCREEN-011` (Chatbot) | `COMP-FEAT-005` (WhatsAppEscalationCard) | `TASK-018`, `TASK-019` | `TEST-WGT-003`, `TEST-INT-002` | VERIFIED |

---

## Audit Checklist & Verification Status

```text
[X] Every Screen maps to at least one Requirement.
[X] Every Requirement maps to at least one Test Case.
[X] Every Component maps to at least one Design Token.
[X] Every Database Table maps to a validated persistent entity.
[X] Every API Endpoint has an assigned caller in the Task list.
[X] All 15 Specification Documents exist and cross-reference deterministically.
[X] Zero orphan requirements or untracked screens detected.
```
