# Design Tokens Specification — RTConnect

This document serves as the machine-readable design token registry for the RTConnect Flutter application. It defines the visual primitives, spacing scales, typography hierarchies, and component tokens.

---

## 1. Color Tokens

| Token ID | Token Name | Hex Value / Code | Semantic Usage | Source | Status |
|---|---|---|---|---|---|
| **TOKEN-COLOR-001** | Primary Brand | `#1E3A8A` (Blue 900) | Header backgrounds, primary action buttons, brand accents | Observed | CONFIRMED |
| **TOKEN-COLOR-002** | Primary Light | `#3B82F6` (Blue 500) | Active bottom navigation, links, focus borders | Observed | CONFIRMED |
| **TOKEN-COLOR-003** | Primary Container | `#EFF6FF` (Blue 50) | Selected card backgrounds, user chat bubble background | Proposed | PROPOSED |
| **TOKEN-COLOR-004** | Secondary Dark | `#0F172A` (Slate 900) | High-contrast headers, prominent card buttons | Observed | CONFIRMED |
| **TOKEN-COLOR-005** | Surface Neutral | `#FFFFFF` | Card surface, dialog background, app bar background | Observed | CONFIRMED |
| **TOKEN-COLOR-006** | Background App | `#F8FAFC` (Slate 50) | Scaffold body background | Observed | CONFIRMED |
| **TOKEN-COLOR-007** | Border Neutral | `#E2E8F0` (Slate 200) | Input field outlines, card borders, dividers | Observed | CONFIRMED |
| **TOKEN-COLOR-008** | Text Primary | `#0F172A` (Slate 900) | Primary titles, body text, form field labels | Observed | CONFIRMED |
| **TOKEN-COLOR-009** | Text Secondary | `#64748B` (Slate 500) | Subtitles, timestamps, helper text, placeholders | Observed | CONFIRMED |
| **TOKEN-COLOR-010** | Status Diajukan | `#F59E0B` (Amber 500) | Badge for newly submitted applications | Observed | CONFIRMED |
| **TOKEN-COLOR-011** | Status Revisi | `#EF4444` (Red 500) | Badge for applications requiring resident fixes | Observed | CONFIRMED |
| **TOKEN-COLOR-012** | Status Disetujui | `#10B981` (Emerald 500) | Badge for approved applications | Observed | CONFIRMED |
| **TOKEN-COLOR-013** | Status Selesai | `#059669` (Emerald 600) | Badge for final completed/signed letters | Observed | CONFIRMED |
| **TOKEN-COLOR-014** | Status Ditolak | `#6B7280` (Gray 500) | Badge for rejected letters | Observed | CONFIRMED |
| **TOKEN-COLOR-015** | Chat Bubble Bot | `#F1F5F9` (Slate 100) | Inbound AI assistant response bubble | Observed | CONFIRMED |
| **TOKEN-COLOR-016** | Chat Bubble User | `#1E3A8A` (Blue 900) | Outbound resident inquiry bubble | Observed | CONFIRMED |
| **TOKEN-COLOR-017** | WhatsApp Brand | `#25D366` | Escalation button background for WhatsApp | Proposed | PROPOSED |

---

## 2. Typography Tokens

All typography adopts the system font standard (Inter / Roboto) with explicit line heights and weights.

| Token ID | Token Name | Font Size | Weight | Line Height | Usage | Status |
|---|---|---|---|---|---|---|
| **TOKEN-TYPO-001** | Display Large | 24.0 sp | Bold (700) | 32.0 sp | Welcome header, Tagline RTConnect | CONFIRMED |
| **TOKEN-TYPO-002** | Title Large | 18.0 sp | Semi-Bold (600) | 24.0 sp | Screen app bar title, section headers | CONFIRMED |
| **TOKEN-TYPO-003** | Title Medium | 16.0 sp | Semi-Bold (600) | 22.0 sp | Card title (Jenis Pengajuan), Dialog title | CONFIRMED |
| **TOKEN-TYPO-004** | Body Large | 14.0 sp | Regular (400) | 20.0 sp | Main body text, input form text, chat messages | CONFIRMED |
| **TOKEN-TYPO-005** | Body Medium | 13.0 sp | Regular (400) | 18.0 sp | Secondary card info, application date | CONFIRMED |
| **TOKEN-TYPO-006** | Label Small | 11.0 sp | Medium (500) | 14.0 sp | Status badges, timestamps, helper text | CONFIRMED |
| **TOKEN-TYPO-007** | Button Label | 14.0 sp | Semi-Bold (600) | 20.0 sp | Primary and secondary button text | CONFIRMED |

---

## 3. Spacing & Metric Tokens

Adheres strictly to an **8dp baseline grid**.

| Token ID | Token Name | Value | Usage | Status |
|---|---|---|---|---|
| **TOKEN-SPACE-001** | Space 2XS | 4.0 dp | Minimal internal badge padding, icon gap | CONFIRMED |
| **TOKEN-SPACE-002** | Space XS | 8.0 dp | Dense component padding, chip gap | CONFIRMED |
| **TOKEN-SPACE-003** | Space SM | 12.0 dp | Form input vertical padding, card inner gap | CONFIRMED |
| **TOKEN-SPACE-004** | Space MD | 16.0 dp | Standard screen edge margin, card padding | CONFIRMED |
| **TOKEN-SPACE-005** | Space LG | 24.0 dp | Section vertical separator, modal padding | CONFIRMED |
| **TOKEN-SPACE-006** | Space XL | 32.0 dp | Header separation, auth screen hero gap | CONFIRMED |
| **TOKEN-SPACE-007** | Space 2XL | 48.0 dp | Top spacing on landing screen | CONFIRMED |

---

## 4. Border Radius Tokens

| Token ID | Token Name | Value | Usage | Status |
|---|---|---|---|---|
| **TOKEN-RADIUS-001**| Radius XS | 4.0 dp | Status tags, badge pills | CONFIRMED |
| **TOKEN-RADIUS-002**| Radius SM | 8.0 dp | Text field borders, small action buttons | CONFIRMED |
| **TOKEN-RADIUS-003**| Radius MD | 12.0 dp | Standard cards, application list items | CONFIRMED |
| **TOKEN-RADIUS-004**| Radius LG | 16.0 dp | Dialog containers, bottom sheet top corners | CONFIRMED |
| **TOKEN-RADIUS-005**| Radius Full | 999.0 dp | Pill buttons, avatar circle | CONFIRMED |

---

## 5. Elevation & Shadow Tokens

| Token ID | Token Name | Blur / Offset | Shadow Color | Usage | Status |
|---|---|---|---|---|---|
| **TOKEN-SHADOW-001**| Elevation Low | Blur 4dp, Offset (0, 1) | `rgba(0,0,0, 0.05)` | Application list cards | PROPOSED |
| **TOKEN-SHADOW-002**| Elevation Medium| Blur 12dp, Offset (0, 4) | `rgba(0,0,0, 0.08)` | Bottom navigation bar, floating CTA | PROPOSED |
| **TOKEN-SHADOW-003**| Elevation High | Blur 24dp, Offset (0, 8) | `rgba(0,0,0, 0.12)` | Modals, bottom sheets | PROPOSED |

---

## 6. Sizing Tokens

| Token ID | Token Name | Value | Usage | Status |
|---|---|---|---|---|
| **TOKEN-SIZE-001** | Min Touch Target | 48.0 dp | Minimum clickable area for accessibility | CONFIRMED |
| **TOKEN-SIZE-002** | Button Height Primary | 48.0 dp | Main action buttons (Submit, Login, Register) | CONFIRMED |
| **TOKEN-SIZE-003** | Input Height Standard | 48.0 dp | Text fields, dropdown triggers | CONFIRMED |
| **TOKEN-SIZE-004** | Bottom Nav Height | 64.0 dp | Standard bottom navigation bar | CONFIRMED |
| **TOKEN-SIZE-005** | Avatar Diameter | 56.0 dp | User profile picture in drawer | CONFIRMED |

---

## 7. Component-Specific Tokens

| Token ID | Target Component | Applied Tokens | Usage | Status |
|---|---|---|---|---|
| **TOKEN-COMP-001** | Primary Button | BG: `TOKEN-COLOR-004` (Black/Dark Slate), Radius: `TOKEN-RADIUS-SM`, Text: `TOKEN-TYPO-007` (White) | Form submissions, Login, Action CTA | CONFIRMED |
| **TOKEN-COMP-002** | Secondary Button | BG: `TOKEN-COLOR-007`, Radius: `TOKEN-RADIUS-SM`, Text: `TOKEN-TYPO-007` (Dark Slate) | Register button, secondary action | CONFIRMED |
| **TOKEN-COMP-003** | Input Field | Border: `TOKEN-COLOR-007`, Focus: `TOKEN-COLOR-002`, Radius: `TOKEN-RADIUS-SM`, Padding: `TOKEN-SPACE-SM` | Form controls | CONFIRMED |
| **TOKEN-COMP-004** | Application Card | BG: `TOKEN-COLOR-005`, Border: `TOKEN-COLOR-007`, Radius: `TOKEN-RADIUS-MD`, Shadow: `TOKEN-SHADOW-001` | List items in queue and history | CONFIRMED |
| **TOKEN-COMP-005** | Status Chip | Radius: `TOKEN-RADIUS-XS`, Text: `TOKEN-TYPO-006`, Padding: `TOKEN-SPACE-2XS` | Status indicators | CONFIRMED |
