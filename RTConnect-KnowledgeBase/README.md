# RTConnect Mobile Application — AI Agent Implementation Specification

## Project Type
Mobile Application (Civic Tech / Community Governance / Administrative Automation)

## Technology Stack

```text
Frontend:
Flutter (3.x+)
Dart (3.x+)

Backend:
Technology-Agnostic RESTful API Contract
(STATUS: Source specifies Python Flask for research prototype backend; API specification in this repository is strictly technology-agnostic)

Database:
MySQL (8.0+ / 8.4 LTS)
```

---

## Documentation Map

This repository contains the complete specification suite required for AI coding agents to autonomously build, test, and verify the **RTConnect** mobile application without referring to raw legacy artifacts.

| Order | Document File | Primary Focus | When AI Agents Must Read |
|---|---|---|---|
| **00** | [`ai-rules.md`](ai-rules.md) | Non-Negotiable AI Rules | **First step** before touching any file or generating code |
| **01** | [`README.md`](README.md) | Entry point & Project overview | At project initialization |
| **02** | [`planning.md`](planning.md) | Master development plan & phases | Prior to planning sprints, phases, or work sessions |
| **03** | [`requirements.md`](requirements.md) | Functional & Non-Functional Requirements | Prior to feature modeling and architecture validation |
| **04** | [`user-flows.md`](user-flows.md) | User journeys & decision trees | Prior to screen navigation and state wiring |
| **05** | [`design-tokens.md`](design-tokens.md) | Machine-readable design tokens | When configuring theme, typography, colors, and layout metrics |
| **06** | [`design.md`](design.md) | UI/UX specifications (Google Stitch compatible) | Prior to generating UI screens and visual components |
| **07** | [`screens.md`](screens.md) | Screen-by-screen implementation details | When constructing UI screen widgets |
| **08** | [`components.md`](components.md) | Component registry & widget hierarchy | When building reusable atomic/molecular widgets |
| **09** | [`architecture.md`](architecture.md) | Flutter application architecture | When building layers, providers/blocs, repositories, and models |
| **10** | [`database.md`](database.md) | MySQL schema, constraints, ERD, seed | When preparing database tables, migrations, or local sqlite mirror |
| **11** | [`api.md`](api.md) | Technology-agnostic REST API contract | When writing API service clients and mock handlers |
| **12** | [`tasks.md`](tasks.md) | Atomic executable development tasks | When picking up implementation items sequentially |
| **13** | [`testing.md`](testing.md) | Unit, widget, BDD, and integration tests | During TDD cycles and verification phases |
| **14** | [`traceability.md`](traceability.md) | End-to-end traceability matrix | During quality audits and acceptance sign-offs |

---

## Implementation Status

- **Specification State:** COMPLETE & FROZEN (Ready for AI Autonomous Execution)
- **Target Application:** RTConnect (Citizen & RT Administrative Service Application)
- **Current Phase:** Ready for Phase 0 (Project Setup & Foundation)

---

## Important Constraints

1. **Language & Environment:**
   - Client Application: Flutter with Dart null-safety enabled.
   - Target Platforms: Android & iOS (Responsive mobile phone form factor, 360dp - 428dp viewport width).
2. **Database:**
   - MySQL 8.x target persistence.
   - Centralized authentication table (`users`) to resolve role inheritance between Warga and Ketua RT.
3. **AI & NLP Module Constraints:**
   - Generative AI is strictly used for drafting official letter text from structured user inputs.
   - Chatbot relies on Retrieval-Augmented Generation (RAG) using semantic embeddings against verified community knowledge documents.
   - Out-of-domain inquiries (< 0.70 similarity threshold) MUST fallback to an escalation link targeting the RT Head's WhatsApp number.
4. **Signature Methods:**
   - Digital: Verifiable cryptographic tempelan gambar tanda tangan token embedded in the PDF document.
   - Physical ("Basah"): Dual-mode hybrid flow allowing offline printing, manual pen ink signature, and status update confirmation.

---

## Known Unknowns & Decision Gates

| Item ID | Unknown Topic | Impact Area | Proposed Resolution / Decision Gate | Status |
|---|---|---|---|---|
| **UNK-001** | Exact Cloud Storage Provider for uploaded files (KTP/signature scans) | File Upload / Storage | Store relative file paths in MySQL; use multipart upload endpoint abstraction. | PROPOSED |
| **UNK-002** | Exact Vector Search DB Engine for MySQL | RAG Knowledge Base | Store embedding vectors as JSON arrays in MySQL; perform cosine similarity calculation in service layer or MySQL 8.4 vector indexing. | PROPOSED |
| **UNK-003** | Push Notification Service Gateway | Real-time alerts | Abstract via NotificationService interface; fallback to in-app polling/REST fetching. | PROPOSED |

---

## How AI Coding Agents Should Read and Execute This Repository

Follow this deterministic execution pipeline:

```text
               +-----------------------------+
               |        ai-rules.md          |  (Step 0: Read Non-Negotiables)
               +--------------+--------------+
                              |
               +--------------v--------------+
               |          README.md          |  (Step 1: Understand Map & Status)
               +--------------+--------------+
                              |
               +--------------v--------------+
               |         planning.md         |  (Step 2: Master Scope & Phases)
               +--------------+--------------+
                              |
       +----------------------+----------------------+
       |                                             |
+------v---------------------+        +--------------v--------------+
|      requirements.md       |        |       architecture.md       |  (Step 3: Specs & Architecture)
|      user-flows.md         |        |       database.md / api.md  |
+------+---------------------+        +--------------+--------------+
       |                                             |
       +----------------------+----------------------+
                              |
               +--------------v--------------+
               | design.md / design-tokens.md|  (Step 4: Design Tokens & UI Specs)
               | screens.md / components.md  |
               +--------------+--------------+
                              |
               +--------------v--------------+
               |          tasks.md           |  (Step 5: Pick Atomic Task by ID)
               +--------------+--------------+
                              |
               +--------------v--------------+
               |         testing.md          |  (Step 6: Write Test -> Implement -> Pass)
               +--------------+--------------+
                              |
               +--------------v--------------+
               |       traceability.md       |  (Step 7: Audit Traceability & Complete)
               +-----------------------------+
```
