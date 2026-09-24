# AI Coding Agent Non-Negotiable Rules

These rules are strictly enforced and mandatory for any AI coding agent, subagent, or autonomous executor operating on the RTConnect codebase.

---

## Core Non-Negotiable Directives

| Rule ID | Directive | Enforcement Level |
|---|---|---|
| **RULE-001** | **Read `README.md` before implementation.** Every agent must first parse the map of documents to understand context and constraints. | STRICT |
| **RULE-002** | **Read `planning.md` before creating architecture or structuring folders.** Never begin coding without knowing the active development phase and master objective. | STRICT |
| **RULE-003** | **Read `architecture.md` before modifying Flutter structure.** Adhere strictly to the defined Feature-First layer architecture. Do not cross layer boundaries arbitrarily. | STRICT |
| **RULE-004** | **Read `design.md` and `design-tokens.md` before implementing UI.** All widgets, colors, typography, paddings, and corner radii must use standardized design tokens. Hardcoding arbitrary hex colors or pixel dimensions is forbidden. | STRICT |
| **RULE-005** | **Read `screens.md` before implementing screens.** Each screen must conform to its assigned layout hierarchy, state transitions (Loading, Empty, Error, Success), and route parameters. | STRICT |
| **RULE-006** | **Read `database.md` before altering persistence models.** Every entity and field must trace back to the documented MySQL schema. Do not invent columns without an explicit revision request. | STRICT |
| **RULE-007** | **Read `api.md` before implementing API integration.** Service clients must strictly reflect documented endpoints, request payloads, response bodies, and error formats. | STRICT |
| **RULE-008** | **Read `tasks.md` before starting implementation.** Development must proceed strictly by atomic `TASK-xxx` order and dependencies. Do not jump ahead across blocked phases. | STRICT |
| **RULE-009** | **Do not invent requirements.** If an observed behavior or requirement is absent from `requirements.md` or `planning.md`, mark it as `UNKNOWN` or file a decision gate proposal. | STRICT |
| **RULE-010** | **Do not introduce dependencies without justification.** Only use packages listed and justified in `architecture.md`. Any new package must be flagged as `PROPOSED` with rationale and alternatives. | STRICT |
| **RULE-011** | **Do not modify architecture without documenting the decision.** Architectural drift is strictly prevented. Never mix BLoC, Riverpod, and Provider within the same codebase without architectural mandate. | STRICT |
| **RULE-012** | **Do not create undocumented screens.** Every route and widget view must correspond to a registered `SCREEN-xxx` in `screens.md`. | STRICT |
| **RULE-013** | **Do not create undocumented API endpoints.** All networking calls must map directly to an `API-xxx` contract in `api.md`. | STRICT |
| **RULE-014** | **Do not create undocumented database tables or columns.** Persistence must strictly mirror `database.md`. | STRICT |
| **RULE-015** | **Preserve the documented design system.** Follow Google Stitch compatibility standards and component specifications in `components.md`. | STRICT |
| **RULE-016** | **Reuse existing components.** Before building a new widget, inspect `components.md` to reuse established atoms, molecules, or shared widgets. | STRICT |
| **RULE-017** | **Do not duplicate business logic.** Validation logic, state transitions, and utility functions must reside in their designated domain or core layers. | STRICT |
| **RULE-018** | **Do not use mock data in production implementation.** Mocks are permissible only within isolated test files (`test/`) or mock repositories when backend endpoints are marked as `NOT OBSERVED`. Never leave hardcoded strings in release builds. | STRICT |
| **RULE-019** | **Do not silently change API contracts.** If an endpoint payload or status code differs from `api.md`, halt and report a contract discrepancy. | STRICT |
| **RULE-020** | **If documentation conflicts, stop and identify the conflict.** Immediately pause execution, isolate the conflicting document IDs, and present the contradiction for resolution. | STRICT |

---

## AI Agent Operational Protocols

### Protocol A: Classification Discipline
Whenever an AI agent generates, refactors, or reviews specifications or code, it must explicitly tag the evidentiary status of any critical assertion:
- `[CONFIRMED]`: Directly backed by source evidence in the 59-page document, PowerDesigner models, or user requirements.
- `[INFERRED]`: Derived through deduction from multiple confirmed facts.
- `[PROPOSED]`: Recommended development enhancement (e.g. state management selection, routing package).
- `[UNKNOWN]`: Explicitly unresolvable with current data.
- `[NOT OBSERVED]`: Feature or component not present in input material.

### Protocol B: Code Quality Verification
Before declaring any task as `DONE`:
1. Run `dart analyze` to ensure zero compilation errors and zero warnings.
2. Run automated tests corresponding to the `TASK-xxx` via `flutter test`.
3. Verify that all Acceptance Criteria assigned to the task are met.
4. Ensure all newly created files are tracked and documented in `traceability.md`.
