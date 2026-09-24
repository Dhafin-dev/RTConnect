# Flutter Component Registry — RTConnect

This document details the component hierarchy, props, internal state, events, design tokens, and accessibility contracts for all reusable widgets in the RTConnect application.

---

## Component Registry Map

```text
Core Components:
├── COMP-CORE-001: RTPrimaryButton
├── COMP-CORE-002: RTSecondaryButton
├── COMP-CORE-003: RTTextField
└── COMP-CORE-004: RTStatusBadge

Shared Components:
├── COMP-SHR-001: RTBottomNavBar
├── COMP-SHR-002: RTAppBar
├── COMP-SHR-003: RTDrawerMenu
├── COMP-SHR-004: RTEmptyStateView
└── COMP-SHR-005: RTErrorBanner

Feature Components:
├── COMP-FEAT-001: RTApplicationCard (Warga History)
├── COMP-FEAT-002: RTQueueCard (RT Inbox)
├── COMP-FEAT-003: RTAIDraftPreviewCard
├── COMP-FEAT-004: RTChatBubble
├── COMP-FEAT-005: RTWhatsAppEscalationCard
└── COMP-FEAT-006: RTDecisionDialog
```

---

## 1. Core Components

### COMPONENT ID: COMP-CORE-001
- **NAME:** `RTPrimaryButton`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Primary action button for forms, modal confirmations, and high-priority CTAs.
- **INPUTS / PROPS:**
  - `String text`: Button label text.
  - `VoidCallback? onPressed`: Click callback; if null, button is rendered disabled.
  - `bool isLoading`: When true, displays centered spinner instead of text.
  - `IconData? icon`: Optional prefix icon.
- **STATE:** None (Purely controlled).
- **VARIANTS:** Enabled, Disabled, Loading.
- **CHILDREN:** `Text`, `CircularProgressIndicator`, optional `Icon`.
- **EVENTS:** `onPressed` on tap.
- **DEPENDENCIES:** Material Flutter.
- **USED BY:** `SCREEN-001`, `SCREEN-002`, `SCREEN-003`, `SCREEN-007`, `SCREEN-010`.
- **DESIGN TOKENS:** `TOKEN-COMP-001`, `TOKEN-COLOR-004`, `TOKEN-RADIUS-SM`, `TOKEN-SIZE-002`.
- **ACCESSIBILITY:** Semantics button label; minimum height 48dp (`TOKEN-SIZE-001`).
- **ACCEPTANCE CRITERIA:** Suppresses multiple taps while `isLoading == true`.

---

### COMPONENT ID: COMP-CORE-002
- **NAME:** `RTSecondaryButton`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Secondary or cancel button.
- **INPUTS / PROPS:**
  - `String text`: Button label text.
  - `VoidCallback? onPressed`: Click callback.
  - `Color? borderColor`: Optional custom outline color.
- **STATE:** None.
- **VARIANTS:** Standard Outlined, Ghost.
- **USED BY:** `SCREEN-001`, `SCREEN-004`, `SCREEN-010`.
- **DESIGN TOKENS:** `TOKEN-COMP-002`, `TOKEN-COLOR-007`.
- **ACCEPTANCE CRITERIA:** Renders crisp border without elevation.

---

### COMPONENT ID: COMP-CORE-003
- **NAME:** `RTTextField`
- **TYPE:** `StatefulWidget`
- **PURPOSE:** Universal text entry widget with validation, password visibility toggling, and prefix/suffix support.
- **INPUTS / PROPS:**
  - `String label`: Text displayed above input field.
  - `String? hint`: Placeholder text.
  - `TextEditingController controller`: Text controller.
  - `String? Function(String?)? validator`: Validation callback.
  - `bool isPassword`: If true, renders visibility toggle icon.
  - `TextInputType keyboardType`: Configures keyboard (e.g. number for NIK).
  - `int maxLines`: Number of lines (default 1; >1 for Keperluan).
- **STATE:** `bool _obscureText` (local to widget).
- **USED BY:** `SCREEN-002`, `SCREEN-003`, `SCREEN-007`, `SCREEN-008`.
- **DESIGN TOKENS:** `TOKEN-COMP-003`, `TOKEN-RADIUS-SM`, `TOKEN-TYPO-004`.
- **ACCEPTANCE CRITERIA:** Correctly renders error message below field when validator returns error string.

---

### COMPONENT ID: COMP-CORE-004
- **NAME:** `RTStatusBadge`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Displays a color-coded status chip indicating the current application state.
- **INPUTS / PROPS:**
  - `String status`: One of `diajukan`, `perlu_revisi`, `disetujui`, `ditolak`, `siap_diambil`, `selesai`.
- **STATE:** None.
- **VARIANTS:** Amber (`Diajukan`), Red (`Perlu Revisi`, `Ditolak`), Emerald (`Disetujui`, `Selesai`, `Siap Diambil`).
- **USED BY:** `SCREEN-006`, `SCREEN-009`, `SCREEN-010`.
- **DESIGN TOKENS:** `TOKEN-COMP-005`, `TOKEN-RADIUS-XS`, `TOKEN-TYPO-006`.
- **ACCEPTANCE CRITERIA:** Maps string status deterministically to Indonesian label and corresponding background/text colors.

---

## 2. Shared Components

### COMPONENT ID: COMP-SHR-001
- **NAME:** `RTBottomNavBar`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Pinned 3-tab navigation bar adhering to prototype wireframe.
- **INPUTS / PROPS:**
  - `int currentIndex`: Active tab index (0 = Pengajuan, 1 = Beranda, 2 = TanyaRT).
  - `ValueChanged<int> onTap`: Callback fired when tab is tapped.
- **STATE:** Controlled externally by `go_router` or shell provider.
- **DESIGN TOKENS:** `TOKEN-COLOR-001`, `TOKEN-COLOR-009`, `TOKEN-SIZE-004`.
- **USED BY:** `SCREEN-001`, `SCREEN-004`, `SCREEN-006`, `SCREEN-009`, `SCREEN-011`.
- **ACCEPTANCE CRITERIA:** Highlights active icon and label in `#1E3A8A`; switches route seamlessly.

---

### COMPONENT ID: COMP-SHR-003
- **NAME:** `RTDrawerMenu`
- **TYPE:** `ConsumerWidget`
- **PURPOSE:** Side drawer profile menu accessible via hamburger button on app bar.
- **INPUTS / PROPS:** None (Reads authenticated user provider).
- **CHILDREN:** User avatar (`TOKEN-SIZE-005`), Name, Email, Role badge, Navigation tiles (Profil, Riwayat / Antrean, Pengaturan), Logout button (`COMP-CORE-001`).
- **EVENTS:** Logout action invalidates session and navigates to `SCREEN-001`.
- **DESIGN TOKENS:** `TOKEN-COLOR-005`, `TOKEN-SPACE-MD`.
- **USED BY:** Global Shell Scaffold (`SCREEN-004`, `SCREEN-009`).
- **ACCEPTANCE CRITERIA:** Closes drawer prior to route push; triggers session clear on logout.

---

## 3. Feature Components

### COMPONENT ID: COMP-FEAT-001
- **NAME:** `RTApplicationCard`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Renders individual cover letter records in the Citizen history list.
- **INPUTS / PROPS:**
  - `LetterEntity letter`: Letter domain model.
  - `VoidCallback onTap`: Callback to inspect details or download PDF.
- **CHILDREN:** Letter title, date string, `RTStatusBadge`, trailing chevron "cek detail >".
- **DESIGN TOKENS:** `TOKEN-COMP-004`, `TOKEN-SPACE-MD`, `TOKEN-RADIUS-MD`.
- **USED BY:** `SCREEN-006` (Application History).
- **ACCEPTANCE CRITERIA:** Renders application number, formatted submission date, and correct status badge.

---

### COMPONENT ID: COMP-FEAT-003
- **NAME:** `RTAIDraftPreviewCard`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Container highlighting the Generative AI-formulated letter draft for RT review.
- **INPUTS / PROPS:**
  - `String draftText`: Text synthesized by LLM.
- **CHILDREN:** AI badge ("Draf Surat Otomatis AI"), stylized quotation container, text content.
- **DESIGN TOKENS:** `TOKEN-COLOR-003`, `TOKEN-COLOR-001`, `TOKEN-RADIUS-SM`.
- **USED BY:** `SCREEN-010` (RT Application Detail).
- **ACCEPTANCE CRITERIA:** Renders full draft text in readable typography with visual signifier indicating AI synthesis.

---

### COMPONENT ID: COMP-FEAT-004
- **NAME:** `RTChatBubble`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Renders conversation messages in Tanya RT chat view.
- **INPUTS / PROPS:**
  - `String message`: Message body text.
  - `bool isUser`: True for citizen inquiry, false for AI response.
  - `String? citation`: Optional knowledge base citation title.
  - `String timestamp`: Formatted time string.
- **VARIANTS:** User (Right-aligned, `#1E3A8A` background, white text) vs. Bot (Left-aligned, `#F1F5F9` background, slate text).
- **DESIGN TOKENS:** `TOKEN-COLOR-015`, `TOKEN-COLOR-016`, `TOKEN-RADIUS-MD`.
- **USED BY:** `SCREEN-011` (Chatbot Screen).
- **ACCEPTANCE CRITERIA:** Displays citation badge underneath text if citation string is provided.

---

### COMPONENT ID: COMP-FEAT-005
- **NAME:** `RTWhatsAppEscalationCard`
- **TYPE:** `StatelessWidget`
- **PURPOSE:** Callout card rendered in the chat view when an inquiry is out-of-domain.
- **INPUTS / PROPS:**
  - `String whatsappUrl`: Formatted `https://wa.me/...` URL string.
- **CHILDREN:** Info icon, explanation text, and WhatsApp green CTA button.
- **EVENTS:** Tapping CTA invokes `url_launcher` to open WhatsApp.
- **DESIGN TOKENS:** `TOKEN-COLOR-017`, `TOKEN-RADIUS-SM`.
- **USED BY:** `SCREEN-011` (Chatbot Screen).
- **ACCEPTANCE CRITERIA:** Launches WhatsApp directly with the pre-filled inquiry text.
