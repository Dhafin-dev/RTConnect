# Rencana Perbaikan & Pengembangan RTConnect (`planning.md`)

Dokumen ini berisi rencana tindak lanjut berdasarkan hasil **audit langsung menggunakan ChromeDevToolsMCP** (uji peran Warga, Ketua RT, akses anonim, Lighthouse, serta inspeksi jaringan & penyimpanan browser) yang dikombinasikan dengan **pemeriksaan kode sumber** backend dan frontend pada **26 November 2026**.

Tujuannya agar tim dapat melihat masalah secara utuh dalam bahasa yang ringkas, jelas prioritasnya, serta punya langkah eksekusi dan kriteria selesai (*Definition of Done*) yang terukur.

---

## Ringkasan Kondisi Saat Ini

### Yang Sudah Berjalan Baik
- **Autentikasi & Perlindungan Rute**: Pengunjung tanpa login yang mengakses rute privat (mis. `/#/warga/home`) otomatis diarahkan ke `/#/login`.
- **Kontrol Akses API (RBAC & IDOR Utama)**:
  - Endpoint terproteksi menolak akses tanpa token (`401 Unauthorized`).
  - Akun `warga` ditolak (`403 Forbidden`) pada endpoint khusus Ketua RT (`/letters/incoming-queue`, `/letters/ai-stats`, `/chatbot/knowledge`, `/decision`, `/sign-digital`, `/confirm-physical`).
  - Akun `warga` ditolak (`403 Forbidden`) saat mencoba membuka detail/PDF pengajuan milik warga lain maupun berkas `generated_letters/` via `/auth/files/`.
- **Alur Inti Persuratan**: Landing page, validasi form login kosong, prefill biodata pengajuan terakhir (`/letters/my-last-data`), pratinjau blangko resmi, PDF Viewer (`SfPdfViewer` + tautan unduhan bertanda tangan), antrean tinjauan RT, serta dialog otorisasi PIN Ketua RT (`PinAuthDialog`) sudah berfungsi.

### Masalah Utama yang Perlu Ditangani
Ditemukan **13 item temuan** di sisi keamanan, fungsionalitas, stabilitas jaringan, dan aksesibilitas. Masalah dikelompokkan menjadi **4 fase** dari yang paling mendesak (`P0`) hingga penyempurnaan (`P3`).

---

## Peta Prioritas Cepat

| ID | Prioritas | Kategori | Ringkasan Masalah | Lokasi Utama |
|---|---|---|---|---|
| **SEC-01** | `P0` | Keamanan | Celah IDOR / baca file arbitrer pada `POST`/`GET /api/v1/auth/signature` | `backend/routes/auth_routes.py` |
| **SEC-02** | `P0` | Keamanan | JWT masih diterima lewat URL query (`?token=`) | `backend/middleware/auth_middleware.py` |
| **FIX-01** | `P0` | Fungsional | Nama pemohon di Beranda RT selalu tampil `"Warga RT 04"` (`nama_warga` vs `nama_lengkap`) | `frontend/lib/features/home/presentation/rt_home_screen.dart` |
| **FIX-02** | `P0` | Fungsional | Menu "TanyaRT" untuk Ketua RT selalu gagal `403 Forbidden` | `frontend/lib/features/home/presentation/rt_home_screen.dart`, `frontend/lib/core/router/app_router.dart` |
| **SEC-03** | `P1` | Keamanan | Endpoint `PUT/PATCH /api/v1/auth/me` tanpa validasi & rawan HTTP 500 saat `null` / email duplikat | `backend/routes/auth_routes.py` |
| **FIX-03** | `P1` | Fungsional | TanyaRT tetap memicu eskalasi WhatsApp & notifikasi RT saat LLM timeout meski jawaban leksikal cocok (`1.0`) | `backend/services/rag_service.py` |
| **SEC-04** | `P1` | Keamanan | Belum ada rate limit `/auth/login` & `/auth/register`, serta header keamanan HTTP belum dipasang | `backend/app.py`, `backend/routes/auth_routes.py` |
| **SEC-05** | `P1` | Keamanan | Token JWT & NIK tersimpan di `localStorage` pada Web (bersama kunci enkripsinya) | `frontend/lib/features/auth/data/auth_repository.dart`, `frontend/web/index.html` |
| **UX-01** | `P2` | UX / Jaringan | Pesan error mentah (`DioException`, `FormatAplikasi`) bocor ke UI & `connectTimeout: 10s` terlalu singkat | `frontend/lib/core/network/api_client.dart`, `auth_controller.dart`, `pin_auth_dialog.dart`, dll. |
| **FIX-04** | `P2` | Fungsional | Unggah pindaian TTD saat registrasi tidak jalan di Flutter Web (`path` null) | `frontend/lib/features/auth/presentation/register_screen.dart`, `auth_repository.dart` |
| **UX-02** | `P2` | Konsistensi | Batas upload di UI tertulis `5 MB` (backend `8 MB`) & log error Firebase Web muncul saat startup | `letter_application_screen.dart`, `push_notification_service.dart` |
| **A11Y-01** | `P3` | Aksesibilitas | Skor Lighthouse Accessibility 89 & Agentic Browsing 0 karena input tanpa label & tombol ikon tanpa `tooltip` | `frontend/lib/shared/widgets/rt_text_field.dart`, `warga_home_screen.dart`, `rt_home_screen.dart` |
| **UX-03** | `P3` | Kelengkapan | Elemen statis/stub (`Iuran RT: Lunas` hardcoded, menu `Pengaturan Akun` kosong, feedback chatbot `👍/👎` lokal saja) | `letter_detail_screen.dart`, `rt_drawer_menu.dart`, `chatbot_screen.dart` |

---

## Rencana Pelaksanaan Bertahap

### Fase 1 (`P0`) — Keamanan Kritis & Bug Pemblokir Alur Utama
*Target: menutup celah akses data tidak sah dan memperbaiki alur utama Ketua RT yang rusak.*

1. **[SEC-01] Tutup celah IDOR pada `POST /api/v1/auth/signature` & `GET /api/v1/auth/signature`**
   - **Masalah**: `POST /api/v1/auth/signature` mengizinkan input JSON `tanda_tangan_url` / `signature_key` tanpa memeriksa apakah kunci file tersebut milik user yang sedang login atau berasal dari kategori `signatures/`. Lalu `GET /api/v1/auth/signature` langsung mengembalikan isi file berdasarkan kunci tersebut tanpa pengecekan kepemilikan.
   - **Solusi**:
     - Hapus dukungan pengisian kunci file bebas lewat JSON di `POST /api/v1/auth/signature` (wajibkan upload multipart file melalui `store_upload(sig_file, 'signatures')`), **atau** jika masih diperlukan secara internal, wajibkan prefix `signatures/` serta validasi bahwa kunci tersebut memang milik `user_id` terkait.
     - Pada `GET /api/v1/auth/signature`, pastikan `sig_key` diawali `signatures/` sebelum memanggil `read_bytes()`.
   - **Selesai jika**: Pengiriman JSON berisi path file milik user lain (mis. `attachments/...` atau `generated_letters/...`) ditolak dengan `400`/`403`.

2. **[SEC-02] Nonaktifkan autentikasi JWT via URL Query Parameter (`?token=`)**
   - **Masalah**: `jwt_required` menerima token dari `request.args.get('token')`. Ini memudahkan token bocor di log server, riwayat browser, dan header `Referer`.
   - **Solusi**:
     - Hapus cabang `elif request.args.get('token'):` di `backend/middleware/auth_middleware.py` dan gunakan hanya header `Authorization: Bearer <token>`.
     - Pastikan seluruh pemanggil di frontend (termasuk unduhan PDF) sudah memakai header `Authorization` atau tautan bertanda tangan berumur pendek (`/letters/download/<token>`).
   - **Selesai jika**: `GET /api/v1/auth/me?token=<jwt>` mengembalikan `401 UNAUTHORIZED`.

3. **[FIX-01] Perbaiki tampilan nama pemohon di Beranda Ketua RT**
   - **Masalah**: `RTHomeScreen` membaca `item['nama_warga']`, sedangkan API `/letters/incoming-queue` mengembalikan `nama_lengkap`. Akibatnya semua kartu antrean di Beranda RT menampilkan `"Warga RT 04"`.
   - **Solusi**: Ubah pembacaan di `rt_home_screen.dart` menjadi `item['nama_lengkap'] ?? item['nama_warga'] ?? 'Warga RT 04'`.
   - **Selesai jika**: Kartu antrean di Beranda RT menampilkan nama asli pemohon (sama seperti di halaman `Antrean Pengajuan Warga`).

4. **[FIX-02] Selesaikan konflik peran "TanyaRT" untuk Ketua RT**
   - **Masalah**: Ketua RT melihat tombol "TanyaRT" di Beranda dan Bottom Navigation Bar yang mengarah ke layar chat warga (`/chatbot`). Saat mengirim pertanyaan, backend membalas `403 FORBIDDEN`. Di sisi lain, endpoint CRUD basis pengetahuan (`/api/v1/chatbot/knowledge`) khusus RT sudah ada di backend tetapi belum punya halaman di frontend.
   - **Solusi (pilih salah satu atau gabungkan)**:
     - **Opsi A (Direkomendasikan)**: Buatkan halaman **Kelola Basis Pengetahuan TanyaRT** khusus peran `rt` yang memanggil `GET/POST/PUT/DELETE /api/v1/chatbot/knowledge`, dan arahkan tab/kartu "TanyaRT" milik RT ke halaman tersebut.
     - **Opsi B (Minimal)**: Izinkan peran `rt` mengakses `/chatbot/query` untuk simulasi uji coba **atau** sembunyikan/ganti tombol "TanyaRT" di tampilan RT agar tidak menemui error `403`.
   - **Selesai jika**: Tidak ada alur navigasi di akun Ketua RT yang memicu error `403` saat digunakan secara normal.

---

### Fase 2 (`P1`) — Penguatan Keamanan API & Keandalan Layanan
*Target: mencegah crash/error 500, serangan brute-force, eskalasi palsu, dan memperketat proteksi browser.*

5. **[SEC-03] Tambahkan validasi & error handling pada `PUT/PATCH /api/v1/auth/me`**
   - **Masalah**: Input `nama_lengkap`, `nomor_telepon`, `alamat`, `email` tidak divalidasi panjang/formatnya; payload JSON bernilai `null` menyebabkan `AttributeError` (`500`); mengubah email ke email yang sudah terdaftar memicu `UniqueViolation` tak tertangani (`500`).
   - **Solusi**:
     - Terapkan validasi tipe string, non-kosong, batas panjang, serta format email/telepon yang konsisten dengan `/register`.
     - Tangkap `UniqueViolation` dan kembalikan `409 DUPLICATE_ENTRY` (atau `400`) dengan pesan Bahasa Indonesia yang jelas.
     - Untuk peran `rt` yang tidak punya kolom `alamat` di tabel `rt`, pastikan perilaku penyimpanan tetap konsisten.
   - **Selesai jika**: Input `null`, string kosong, format email salah, dan email duplikat ditolak dengan `400`/`409` (bukan `500`).

6. **[FIX-03] Perbaiki logika eskalasi WhatsApp di TanyaRT saat LLM timeout**
   - **Masalah**: Di `backend/services/rag_service.py` (baris 879–890), ketika pencarian leksikal sudah menemukan sumber resmi (`status == 'SUMBER_DITEMUKAN'`, skor `0.83`–`1.0`), kegagalan/timeout sintesis LLM (`used_llm == False`) justru memaksa `is_escalated = True`. Dampaknya, setiap pertanyaan warga memunculkan kartu WhatsApp dan mengirim notifikasi eskalasi ke RT.
   - **Solusi**:
     - Jika pencarian leksikal/semantik sudah menemukan rujukan valid (`SUMBER_DITEMUKAN`) dan jawaban fallback deterministik tersedia (`format_grounded_chunk_result`), pertahankan `is_escalated = False` meskipun LLM timeout.
     - Eskalasi (`is_escalated = True`) hanya dipicu jika rujukan memang tidak ditemukan / skor di bawah ambang batas / topik memang mewajibkan verifikasi RT.
   - **Selesai jika**: Pertanyaan seperti `"Syarat Surat SKCK"` dan `"Jadwal Kerja Bakti"` tidak lagi menandai sesi sebagai `dieskalasi` atau mengirim notifikasi eskalasi ke RT saat Ollama/Gemini timeout.

7. **[SEC-04] Pasang Rate Limiting Auth & HTTP Security Headers**
   - **Masalah**: Belum ada batas percobaan pada `/auth/login` dan `/auth/register`, serta API belum mengirim header keamanan standar.
   - **Solusi**:
     - Tambahkan rate limiter (mis. `Flask-Limiter` per IP + identitas untuk `/auth/login` dan per IP untuk `/auth/register`).
     - Tambahkan `@app.after_request` di `backend/app.py` untuk menyertakan `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, serta `Cache-Control: no-store` untuk endpoint `/api/v1/auth/*` (selain avatar/signature jika ingin di-cache privat).
     - Pastikan konfigurasi produksi (reverse proxy/Gunicorn) menyembunyikan header `Server` versi Python/Werkzeug.
   - **Selesai jika**: Percobaan login berulang di atas ambang batas membalas `429 Too Many Requests`, dan header keamanan tampil di respons Chrome DevTools Network.

8. **[SEC-05] Perketat keamanan sesi pada Flutter Web**
   - **Masalah**: `flutter_secure_storage` di web menyimpan token JWT dan NIK di `localStorage` beserta kuncinya, sehingga rentan jika ada XSS.
   - **Solusi**:
     - **Jangka pendek (mitigasi cepat)**: Tambahkan `Content-Security-Policy` (CSP) ketat pada `frontend/web/index.html` / web server (batasi `script-src`, blokir inline script tak dikenal) untuk menekan risiko XSS, dan hindari menyimpan data PII tambahan (`keyUserNik`) di `localStorage` bila tidak dibutuhkan (cukup ambil dari `/auth/me` di memori state Riverpod).
     - **Jangka menengah (ideal untuk web produksi)**: Pertimbangkan autentikasi berbasis `HttpOnly; Secure; SameSite=Lax` cookie untuk klien Web agar JWT tidak pernah dapat dibaca JavaScript.
   - **Selesai jika**: `user_nik` tidak lagi tersimpan di `localStorage` web dan CSP aktif tanpa memblokir aset Flutter/CanvasKit yang sah.

---

### Fase 3 (`P2`) — Penanganan Error, Timeout Jaringan, & Kompatibilitas Web
*Target: memastikan pengguna tidak pernah melihat stack/exception teknis dan fitur registrasi/upload berjalan lancar di Web maupun Mobile.*

9. **[UX-01] Standarisasi ekstraksi pesan error API & penyesuaian timeout**
   - **Masalah**:
     - `AuthController.login()`, `AuthController.register()`, `RTHomeScreen`, `RTReviewScreen`, `LetterApplicationScreen`, `PinAuthDialog`, dan `LetterSubmitController.submitDecision/confirmPhysical` masih memakai `e.toString()`, sehingga pesan seperti `"DioException [unknown]: ..."` atau `"FormatAplikasi ..."` tampil langsung ke pengguna.
     - `connectTimeout: Duration(seconds: 10)` di `ApiClient` terlalu ketat saat koneksi awal Supabase WAN / cold start (> 10 detik), sehingga request batal (`net::ERR_ABORTED`) lalu layar gagal memuat.
   - **Solusi**:
     - Buat helper tunggal (mis. `formatErrorMessage(Object error)`) di `frontend/lib/core/errors/` yang mengekstrak `AppException.message` dari `DioException.error` dan menghilangkan prefix `Exception:`/`FormatException:` dengan benar.
     - Terapkan helper tersebut secara seragam di seluruh controller dan dialog (`AuthController`, `ProfileController`, `LetterSubmitController`, `PinAuthDialog`, serta `error:` builder di screen).
     - Naikkan `connectTimeout` / `receiveTimeout` di `ApiClient` ke angka yang aman untuk koneksi WAN (mis. `20–30 detik`) dan pastikan tombol **"Muat Ulang"** di `RTHomeScreen` juga tersedia saat gagal memuat (saat ini hanya ada teks `Error: ...`, tidak ada tombol retry seperti di `RTReviewScreen`).
   - **Selesai jika**: Tidak ada string `DioException` atau `FormatAplikasi` muncul di UI pada skenario password salah, URL non-HTTPS di mode release, PIN salah, maupun gangguan jaringan.

10. **[FIX-04] Perbaiki unggah pindaian TTD saat Registrasi di Flutter Web**
    - **Masalah**: `RegisterScreen._pickSignatureFile()` tidak menyertakan `withData: true` dan `AuthRepository.register()` memanggil `MultipartFile.fromFile()`, sehingga di browser `path` bernilai `null` dan file tidak bisa diunggah.
    - **Solusi**: Samakan pola dengan `LetterRepository.applyLetter()` — gunakan `FilePicker.platform.pickFiles(..., withData: true)`, simpan `PlatformFile`, dan kirim `MultipartFile.fromBytes()` bila `bytes != null` (fallback ke `fromFile` di mobile/desktop).
    - **Selesai jika**: Pengguna dapat memilih dan mengunggah file PNG/JPG tanda tangan pada halaman Registrasi baik di browser maupun Android.

11. **[UX-02] Sinkronkan batas ukuran file & rapikan log Firebase Web**
    - **Masalah**: UI `LetterApplicationScreen` menyebut batas lampiran `"Maks. 5 MB"`, sedangkan backend `Config.MAX_UPLOAD_BYTES` adalah `8 MB`. Selain itu, `PushNotificationService.initialize()` mencoba memanggil `Firebase.initializeApp()` di Web tanpa `FirebaseOptions`, sehingga memicu log error di Console.
    - **Solusi**:
      - Seragamkan batas ukuran berkas (ubah teks UI menjadi `Maks. 8 MB` dan tambahkan validasi ukuran di sisi klien sebelum upload).
      - Pada `PushNotificationService.initialize()`, lewati inisialisasi FCM Web bila konfigurasi Firebase Web belum disediakan (cek `kIsWeb` secara eksplisit).
    - **Selesai jika**: Teks batas unggahan dan validasi klien cocok dengan backend (`8 MB`), dan Console browser bebas dari assertion error Firebase saat halaman web dimuat.

---

### Fase 4 (`P3`) — Aksesibilitas (WCAG / Lighthouse) & Penyelesaian Fitur Stub
*Target: meningkatkan kualitas antarmuka, dukungan screen reader/automasi, dan menghilangkan elemen palsu/non-fungsional.*

12. **[A11Y-01] Perbaiki aksesibilitas form & tombol ikon**
    - **Masalah**: Audit Lighthouse pada halaman Login memberi skor **Accessibility 89** dan **Agentic Browsing 0** karena:
      - `RTTextField` merender label sebagai widget `RichText` terpisah di atas `TextFormField`, sehingga elemen `<input>` HTML tidak memiliki label aksesibel (`aria-label` / `<label>`).
      - Tombol toggle visibilitas password di `RTTextField` dan tombol lonceng notifikasi di `WargaHomeScreen` / `RTHomeScreen` adalah `IconButton` tanpa `tooltip`.
    - **Solusi**:
      - Bungkus `TextFormField` di `RTTextField` dengan `Semantics(label: widget.label, textField: true)` atau sediakan `hintText`/`labelText` yang terbaca oleh pohon aksesibilitas.
      - Tambahkan `tooltip` yang deskriptif pada `IconButton` toggle password (`'Tampilkan kata sandi'` / `'Sembunyikan kata sandi'`) dan `IconButton` notifikasi (`'Notifikasi'`), serta cek layar form lain (`LetterApplicationScreen`, `PinAuthDialog`).
    - **Selesai jika**: Audit Lighthouse pada halaman Login & Beranda meraih skor **Accessibility ≥ 95** dan lulus audit `label` serta `aria-command-name`.

13. **[UX-03] Bereskan elemen hardcoded/stub di UI**
    - **Masalah**:
      - Badge `'Iuran RT: Lunas'` di `LetterDetailScreen` bersifat statis/hardcoded (berpotensi menyesatkan jika warga belum membayar iuran).
      - Menu `'Pengaturan Akun'` di `RTDrawerMenu` hanya menutup drawer tanpa membuka halaman.
      - Tombol `'👍 Membantu'` dan `'👎 Belum Sesuai'` di `ChatbotScreen` hanya menampilkan SnackBar lokal tanpa menyimpan data ke server.
    - **Solusi**:
      - Hapus badge `'Iuran RT: Lunas'` atau hubungkan ke field status iuran nyata di database.
      - Arahkan `'Pengaturan Akun'` ke halaman profil/pengaturan atau hapus jika belum masuk cakupan rilis.
      - Sediakan endpoint pencatatan feedback chatbot (atau hapus tombol feedback sementara agar tidak memberi kesan tersimpan).
    - **Selesai jika**: Tidak ada lagi tombol atau badge status yang bersifat dummy/menyesatkan di UI produksi.

---

## Checklist Verifikasi (Definition of Done)

Setelah seluruh fase (atau per fase) selesai dikerjakan, lakukan verifikasi berikut:

1. **Pengujian Backend**:
   - `cd backend && python test_api.py` → seluruh skenario lulus.
   - `cd backend && python run_bdd.py` → seluruh skenario BDD lulus.
   - Uji manual/otomatis khusus untuk celah baru: `?token=` ditolak (`401`), JSON injection di `/auth/signature` ditolak (`400`/`403`), `PUT /auth/me` dengan `null`/email duplikat mengembalikan `400`/`409`, rate limit mengembalikan `429`.
2. **Pengujian Frontend**:
   - `cd frontend && flutter analyze` → 0 error/warning baru.
   - `cd frontend && flutter test` → seluruh unit & widget test lulus.
3. **Verifikasi Ulang Live via ChromeDevToolsMCP**:
   - Login Warga & Ketua RT (termasuk uji password salah: pastikan tidak ada teks `DioException` mentah).
   - Cek Beranda RT (nama pemohon tampil sesuai database, bukan `"Warga RT 04"`).
   - Cek TanyaRT (baik dari Warga tanpa eskalasi palsu maupun dari akun RT tanpa error `403`).
   - Cek `localStorage` (tidak ada PII `user_nik`), Network response headers (header keamanan terpasang), dan Console (tidak ada uncaught error).
   - Jalankan ulang `lighthouse_audit` pada Login & Beranda untuk memastikan skor Accessibility ≥ 95.
