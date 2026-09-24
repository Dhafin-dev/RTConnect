# UI/UX Design Specification — RTConnect

This document defines the visual layout, component styling, interaction behaviors, and screen composition rules for the RTConnect mobile application. It is tailored for consumption by AI coding agents and is fully compatible as a prompt reference for **Google Stitch** and UI generation tools.

---

## 1. Design Direction
- **Archetype:** Clean, modern civic administration utility (Public Sector / Community Gov).
- **Tone:** Trustworthy, authoritative, accessible, minimal, high-contrast.
- **Form Factor:** Mobile portrait first (360dp - 428dp width).
- **Visual Feel:** Native Material 3 foundation customized with deep slate and crisp indigo accents. Clean cards, generous 8dp-grid whitespace, clear status signifiers, and zero decorative clutter.

---

## 2. Visual Principles
1. **Clarity First:** Citizens of varying technological literacy must understand their application status and action choices immediately without ambiguous terminology.
2. **Predictable Feedback:** Every button press, state change, and form submission presents deterministic visual feedback (snackbars, loading spinners, state chips).
3. **High Contrast:** High contrast ratio (>= 4.5:1) ensures legibility in daylight outdoor usage.
4. **Card-Based Hierarchy:** Content is grouped into clearly bounded surface cards with subtle borders and shadows to separate functional domains.

---

## 3. Design Tokens Summary
Design tokens are centralized in [`design-tokens.md`](design-tokens.md). Key mapping:
- Colors: Primary Brand (`#1E3A8A`), Primary Dark (`#0F172A`), Background (`#F8FAFC`), Surface (`#FFFFFF`).
- Spacing: 4dp (`2XS`), 8dp (`XS`), 12dp (`SM`), 16dp (`MD`), 24dp (`LG`), 32dp (`XL`).
- Radii: 4dp (`XS`), 8dp (`SM`), 12dp (`MD`), 16dp (`LG`).

---

## 4. Colors

```text
Surface & Background:
├── Background:       #F8FAFC (Slate 50)
├── Surface:          #FFFFFF (White)
├── Surface Alt:      #F1F5F9 (Slate 100)
└── Border:           #E2E8F0 (Slate 200)

Brand & Accents:
├── Primary Dark:     #0F172A (Slate 900)  - Dominant for primary CTAs and headings
├── Primary Blue:     #1E3A8A (Blue 900)   - Secondary brand anchor, active tab icons
├── Accent Blue:      #3B82F6 (Blue 500)   - Links, focus states, interactive indicators
└── Brand WhatsApp:   #25D366 (WhatsApp)   - Escalation CTA button

Status Colors:
├── Diajukan:         #F59E0B (Amber 500)
├── Perlu Revisi:     #EF4444 (Red 500)
├── Disetujui:        #10B981 (Emerald 500)
├── Selesai:          #059669 (Emerald 600)
└── Ditolak:          #6B7280 (Gray 500)
```

---

## 5. Typography

- **Font Family:** System Default (`Inter` on Android / `SF Pro` on iOS).
- **Scale:**
  - `Display Large`: 24sp / Bold 700 / Line Height 32sp.
  - `Title Large`: 18sp / Semi-Bold 600 / Line Height 24sp.
  - `Title Medium`: 16sp / Semi-Bold 600 / Line Height 22sp.
  - `Body Large`: 14sp / Regular 400 / Line Height 20sp.
  - `Body Medium`: 13sp / Regular 400 / Line Height 18sp.
  - `Label Small`: 11sp / Medium 500 / Line Height 14sp.

---

## 6. Spacing
All padding and margin intervals conform to the **8dp baseline grid**:
- Screen horizontal edge padding: `16dp` (`TOKEN-SPACE-004`).
- Card inner content padding: `16dp`.
- Gap between form input rows: `16dp`.
- Gap between stacked cards in list views: `12dp`.
- Gap between text header and subtitle: `4dp` or `8dp`.

---

## 7. Border Radius
- Buttons & Text inputs: `8dp` (`TOKEN-RADIUS-002`).
- Content cards & Lists: `12dp` (`TOKEN-RADIUS-003`).
- Dialogs & Bottom Sheet top headers: `16dp` (`TOKEN-RADIUS-004`).
- Status pills & Avatar icons: `999dp` (`TOKEN-RADIUS-005`).

---

## 8. Shadows
- List Cards: `0px 1px 3px rgba(0, 0, 0, 0.05)`.
- Bottom Navigation Bar: `0px -2px 10px rgba(0, 0, 0, 0.05)`.
- Floating Actions & Modals: `0px 8px 24px rgba(0, 0, 0, 0.12)`.

---

## 9. Icons
Standard Material Symbols Outlined (24dp default bounding box):
- Home / Beranda: `Icons.home_outlined` / `Icons.home`
- Letters / Pengajuan: `Icons.description_outlined` / `Icons.description`
- Chatbot / Tanya RT: `Icons.chat_bubble_outline` / `Icons.chat_bubble`
- User Profile: `Icons.person_outline` / `Icons.person`
- Drawer / Menu: `Icons.menu`
- Send Message: `Icons.send`
- Attach File: `Icons.attach_file`
- Download: `Icons.download`
- Chevron Forward: `Icons.chevron_right`

---

## 10. Buttons
1. **Primary Action Button:**
   - Background: `#0F172A` (Black / Dark Slate).
   - Text: `#FFFFFF`, Semi-Bold 14sp.
   - Height: `48dp`, Width: `double.infinity` (Full width inside form container).
   - Radius: `8dp`.
2. **Secondary / Outlined Button:**
   - Background: `#F1F5F9`, Border: `#E2E8F0`.
   - Text: `#0F172A`, Semi-Bold 14sp.
   - Height: `48dp`, Radius: `8dp`.
3. **Destructive Button (Tolak Pengajuan):**
   - Background: `#EF4444` (Red 500) or Outlined Red.
   - Text: `#FFFFFF`.
4. **WhatsApp Escalation Button:**
   - Background: `#25D366`, Text: `#FFFFFF`, Icon: WhatsApp/Chat.

---

## 11. Inputs
- Height: `48dp` container height.
- Border: `1.5dp` solid `#E2E8F0` resting; `2.0dp` solid `#3B82F6` focused; `1.5dp` solid `#EF4444` error.
- Background: `#FFFFFF`.
- Label: Placed outside/above field in Medium 13sp `#0F172A`, followed by an asterisk `*` for mandatory fields.
- Helper / Error Text: 12sp `#EF4444` rendered below field with `4dp` top margin.

---

## 12. Cards
- **Application Item Card:**
  - Background: `#FFFFFF`.
  - Border: `1dp` solid `#E2E8F0`.
  - Padding: `16dp`.
  - Content: Header with `Jenis Surat` (Title Medium) and Status Chip (Top Right); Body with `Nama Pemohon` (for RT) and `Tanggal Pengajuan` (Body Medium); Footer with trailing "Cek detail >" action link.

---

## 13. Navigation Structure
- **Root Router:** Declarative URL router (`go_router`).
- **Unauthenticated Stack:**
  - `/` (Landing Page)
  - `/register` (Registration Page)
  - `/login` (Login Page)
- **Warga Shell Stack:**
  - `/warga/home` (Home Screen)
  - `/warga/pengajuan` (Riwayat Pengajuan)
  - `/warga/pengajuan/baru` (Formulir Baru)
  - `/warga/pengajuan/revisi/:id` (Formulir Revisi)
  - `/chatbot` (Tanya RT Chatbot)
  - `/surat/preview/:id` (PDF Viewer)
- **RT Shell Stack:**
  - `/rt/pengajuan` (Antrean Masuk RT)
  - `/rt/pengajuan/:id` (Detail Pengajuan RT)

---

## 14. App Bar
- Background: `#FFFFFF`.
- Elevation: `0dp` with a bottom border `1dp solid #E2E8F0`.
- Leading: Left hamburger menu `Icons.menu` (opens profile drawer) or back button `Icons.arrow_back`.
- Center / Title: System brand logo or screen title in Semi-Bold 18sp.
- Actions: Optional notification bell with unread badge.

---

## 15. Bottom Navigation Bar
- Background: `#FFFFFF`.
- Border: `1dp` top border `#E2E8F0`.
- Height: `64dp`.
- 3 Tabs:
  1. **Pengajuan** (`Icons.description_outlined` / Label: "Pengajuan")
  2. **Beranda** (`Icons.home_outlined` / Label: "Beranda")
  3. **TanyaRT** (`Icons.chat_bubble_outline` / Label: "TanyaRT")
- Active Indicator: `#1E3A8A` icon and text color. Inactive: `#64748B`.

---

## 16. Dialogs
- Shape: Rounded rectangle (`16dp` radius).
- Actions: Dual button footer (Cancel [Secondary] + Confirm [Primary]).
- Use Cases: Confirm logout, Rejection reason modal input, Revision notes modal input, Security PIN confirmation modal for digital signatures.

---

## 17. Sheets (Bottom Sheets)
- Shape: Rounded top corners (`16dp` radius).
- Drag handle: Centered gray pill (`4dp` x `32dp`).
- Use Cases: Letter type selector, attachment picker (Camera vs Gallery).

---

## 18. Loading States
- Buttons: Replaces label with centered `20dp` circular progress indicator (White).
- Card lists: Shimmer placeholder skeleton (`Container` with animated gradient `#E2E8F0` -> `#F1F5F9`).
- PDF View: Full-screen centered spinner with label "Memuat Dokumen Surat...".

---

## 19. Empty States
- When a list contains 0 records:
  - Icon: Centered `Icons.inbox_outlined` (48dp, `#94A3B8`).
  - Title: "Belum Ada Pengajuan" (Title Medium).
  - Subtitle: "Pengajuan surat pengantar yang Anda buat akan muncul di sini." (Body Medium `#64748B`).
  - Action: "Buat Pengajuan Baru" button.

---

## 20. Error States
- Full-page error: Centered `Icons.cloud_off` with "Gagal Memuat Data" and a "Coba Lagi" retry button.
- Network banner: Top floating red snackbar displaying error description.

---

## 21. Component States
- **Resting:** Standard border `#E2E8F0`, surface `#FFFFFF`.
- **Hover / Pressed:** Light tint `#F1F5F9` overlay.
- **Disabled:** Background `#E2E8F0`, Text `#94A3B8`, click events ignored.

---

## 22. Responsive Rules
- Width constrained to maximum `480dp` centered on tablet/desktop viewports.
- All screen layouts are wrapped in `SafeArea` and `SingleChildScrollView` to prevent keyboard overflow exceptions (`RenderFlex overflowed`).

---

## 23. Accessibility (A11y)
- Minimum touch target: `48dp` x `48dp` for all clickable icons and chips.
- Semantic labels: Provided for all non-text icon buttons (`Semantics(label: "Buka menu drawer")`).
- Form inputs: Explicit `textInputAction` and `autofillHints` configured.

---

## 24. Screen Composition Hierarchy (Google Stitch Compatible)

```text
SCREEN: SCREEN-004 (Warga Home Page)
├── Scaffold
│   ├── AppBar
│   │   ├── Leading: IconButton (Icon: menu)
│   │   ├── Title: LogoImage ("RTConnect")
│   │   └── Actions: [NotificationBadgeIconButton]
│   ├── Drawer: ProfileDrawer (SCREEN-005)
│   ├── Body: SingleChildScrollView
│   │   └── Container (Padding: 16dp)
│   │       ├── HeroBannerCard
│   │       │   ├── Illustration / HeaderImage
│   │       │   ├── Text: "Tagline RTConnect" (Display Large)
│   │       │   └── Text: "deskripsi singkat..." (Body Medium)
│   │       ├── SizedBox (Height: 24dp)
│   │       ├── PrimaryActionButton ("Ajukan Surat")
│   │       ├── SizedBox (Height: 12dp)
│   │       └── SecondaryActionButton ("Tanya RT")
│   └── BottomNavigationBar (3 Tabs: Pengajuan, Beranda [Active], TanyaRT)
```
