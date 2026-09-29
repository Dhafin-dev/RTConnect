# -*- coding: utf-8 -*-
"""
Spesifikasi Teknis Lengkap SRS RTConnect
Memuat Use Case, BDD Gherkin, FR, NFR, Database Data Dictionary, GUI, BPMN, dan RTM
"""

FR_LIST = [
    {
        "id": "FR-01",
        "title": "Registrasi Akun Warga Mandiri",
        "desc": "Sistem harus menyediakan fasilitas pendaftaran akun baru bagi warga dengan memvalidasi format NIK (16 digit angka), nama lengkap, alamat domisili, nomor telepon, email unik, password terenkripsi bcrypt, serta unggahan berkas spesimen stempel tanda tangan warga.",
        "actor": "Warga",
        "input": "NIK, Nama Lengkap, Alamat, No. Telp, Email, Password, File Stempel TTD",
        "output": "Akun warga baru tersimpan (role: 'warga', is_active: TRUE), pesan sukses, pengalihan ke Halaman Login",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-02",
        "title": "Autentikasi Pengguna Terpadu (Login)",
        "desc": "Sistem harus memvalidasi kredensial pengguna (Email atau NIK serta Password) melalui verifikasi hash kriptografis, menerbitkan token sesi (JWT), mencatat riwayat login, dan mengarahkan pengguna ke dashboard sesuai perannya (Warga atau Ketua RT).",
        "actor": "Pengguna (Warga & Ketua RT)",
        "input": "Identitas Akun (Email / NIK) dan Password",
        "output": "Sesi terotentikasi, JWT Token, pengalihan ke Dashboard Warga atau Dashboard RT",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-03",
        "title": "Pengajuan Permohonan Surat Pengantar Mandiri",
        "desc": "Sistem harus menyediakan formulir permohonan surat pengantar dengan biodata pemohon terisi otomatis dari profil, memungkinkan pemilihan jenis surat (Domisili, KTP, SKCK, Usaha), pengisian keperluan, pemilihan opsi metode tanda tangan (Digital vs Basah), serta pengunggahan berkas lampiran pendukung opsional.",
        "actor": "Warga",
        "input": "Jenis Surat, Keperluan/Tujuan, Pilihan TTD, File Lampiran Opsional",
        "output": "Rekor pengajuan_surat baru tersimpan dengan status 'diajukan'",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-04",
        "title": "Formulasi Draf Narasi Surat Otomatis Berbasis Generative AI",
        "desc": "Sistem harus secara otomatis memanfaatkan model Generative AI untuk menyusun draf narasi surat formal berbahasa Indonesia baku segera setelah pengajuan berhasil disubmit, dan menyimpannya pada atribut draf_ai_konten.",
        "actor": "Sistem (AI Engine)",
        "input": "Data Pemohon, Keperluan Surat, Template Standar Jenis Surat",
        "output": "Teks draf formal surat pengantar tersimpan dan siap ditinjau Ketua RT",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-05",
        "title": "Peninjauan Berkas Pengajuan Masuk oleh Ketua RT",
        "desc": "Sistem harus menampilkan antrean permohonan surat masuk pada dashboard Ketua RT, menyediakan tampilan rincian data pemohon, dokumen lampiran pendukung, serta pratinjau draf narasi surat hasil rumusan AI.",
        "actor": "Ketua RT",
        "input": "Pemilihan ID Pengajuan pada daftar antrean",
        "output": "Halaman detail verifikasi permohonan dengan pratinjau berkas dan tombol aksi",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-06",
        "title": "Tindak Lanjut Keputusan Pengajuan (Setuju, Revisi, Tolak)",
        "desc": "Sistem harus memungkinkan Ketua RT mengambil salah satu dari 3 tindakan: (1) Menyetujui pengajuan (menerbitkan nomor surat resmi), (2) Meminta revisi berkas dengan menyertakan catatan kekurangan spesifik, atau (3) Menolak pengajuan dengan alasan tertulis wajib.",
        "actor": "Ketua RT",
        "input": "Pilihan Keputusan (Setuju / Revisi / Tolak), Catatan Revisi / Alasan Tolak",
        "output": "Pembaruan status pengajuan ('disetujui' / 'perlu_revisi' / 'ditolak') dan pengiriman notifikasi ke warga",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-07",
        "title": "Pengesahan Tanda Tangan Digital Resmi (Tempelan Gambar)",
        "desc": "Untuk pengajuan berstatus 'disetujui' dengan metode digital, sistem harus memvalidasi konfirmasi PIN Ketua RT, menyematkan gambar stempel tanda tangan resmi Ketua RT ke dalam dokumen PDF, menerbitkan kode verifikasi keaslian, dan mengubah status pengajuan menjadi 'selesai'.",
        "actor": "Ketua RT & Sistem",
        "input": "PIN Otorisasi TTD Digital Ketua RT",
        "output": "Dokumen PDF resmi (surat_final) tersimpan di server dengan stempel digital, status 'selesai'",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-08",
        "title": "Alur Pengesahan Tanda Tangan Basah (Fisik)",
        "desc": "Untuk pengajuan berstatus 'disetujui' dengan metode basah, sistem harus menyediakan lembar cetak draf siap tanda tangan, dan memungkinkan Ketua RT memperbarui status menjadi 'siap_diambil' setelah dokumen fisik selesai ditandatangani dan dicap stempel basah.",
        "actor": "Ketua RT & Sistem",
        "input": "Aksi tombol konfirmasi 'Siap Diambil' di dashboard RT",
        "output": "Pembaruan status menjadi 'siap_diambil' dan notifikasi jadwal pengambilan fisik ke warga",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-09",
        "title": "Pengunduhan Dokumen Surat Pengantar PDF Resmi",
        "desc": "Sistem harus memungkinkan warga melihat dan mengunduh berkas PDF surat pengantar resmi yang telah disahkan secara digital langsung dari menu riwayat permohonan akun warga.",
        "actor": "Warga",
        "input": "Penekanan tombol 'Unduh Surat' pada pengajuan berstatus 'selesai'",
        "output": "Aliran berkas (stream) PDF resmi tersimpan ke penyimpanan lokal perangkat warga",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-10",
        "title": "Pelacakan Status & Pengiriman Ulang Form Revisi Warga",
        "desc": "Sistem harus menyajikan linimasa status pengajuan secara real-time. Jika pengajuan berstatus 'perlu_revisi', sistem harus membuka kembali formulir isian dengan data lama untuk diperbaiki warga dan disubmit ulang (mengubah status kembali menjadi 'diajukan').",
        "actor": "Warga",
        "input": "Perbaikan data isian / pengunggahan berkas lampiran baru",
        "output": "Rekor pengajuan diperbarui dengan status kembali 'diajukan' dan notifikasi ke Ketua RT",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-11",
        "title": "Layanan Tanya Jawab Cerdas via Chatbot (NLP & RAG)",
        "desc": "Sistem harus menyediakan asisten percakapan cerdas yang memproses pertanyaan warga seputar informasi dan prosedur administrasi RT, melakukan pencarian semantik (vector similarity) pada basis pengetahuan dokumen regulasi RT, dan memberikan jawaban akurat dengan kutipan sumber jika skor relevansi >= 0.70.",
        "actor": "Warga & Sistem (NLP)",
        "input": "Teks pertanyaan warga pada antarmuka chat",
        "output": "Respons jawaban faktual terverifikasi beserta badge referensi aturan RT resmi",
        "priority": "Tinggi (High)"
    },
    {
        "id": "FR-12",
        "title": "Eskalasi Otomatis Pertanyaan Tidak Terjawab ke WhatsApp Ketua RT",
        "desc": "Jika skor kemiripan semantik pertanyaan warga berada di bawah ambang batas (< 0.70), sistem harus secara otomatis menghasilkan ringkasan pertanyaan, menampilkan pesan fallback, dan menyediakan tautan URL langsung ke WhatsApp Ketua RT (wa.me) dengan pesan pertanyaan yang terisi otomatis.",
        "actor": "Sistem & Warga",
        "input": "Penekanan tombol 'Hubungi Ketua RT via WhatsApp' pada gelembung chat",
        "output": "Aplikasi WhatsApp terbuka dengan pesan terformat siap kirim ke nomor Ketua RT",
        "priority": "Sedang (Medium)"
    }
]

NFR_LIST = [
    {
        "id": "NFR-01",
        "category": "Performance (Kinerja)",
        "desc": "Waktu tanggap (response time) antarmuka sistem untuk pemuatan data pengajuan dan autentikasi tidak boleh melebihi 2.0 detik pada koneksi internet normal (minimal 5 Mbps). Waktu formulasi draf AI oleh LLM tidak boleh melebihi 5.0 detik.",
        "metric": "Latency < 2.0s (UI/API), Latency < 5.0s (LLM Generation)"
    },
    {
        "id": "NFR-02",
        "category": "Security (Keamanan Data)",
        "desc": "Seluruh kata sandi pengguna wajib dienkripsi searah menggunakan algoritma bcrypt sebelum disimpan ke basis data. Komunikasi data antarmuka dan backend wajib menggunakan protokol terenkripsi HTTPS/TLS 1.3.",
        "metric": "Enkripsi bcrypt (work factor >= 10), Token JWT bertanda tangan digital HS256, HTTPS aktif"
    },
    {
        "id": "NFR-03",
        "category": "Usability (Kebergunaan)",
        "desc": "Antarmuka sistem dirancang dengan prinsip konsistensi desain, kontras warna memenuhi standar WCAG 2.1 AA (minimal rasio kontras 4.5:1 untuk teks normal), dan target sentuh minimal 48x48 dp. Target skor System Usability Scale (SUS) minimal 70 (kategori Acceptable / Good).",
        "metric": "Skor SUS >= 70, Rasio Kontras WCAG AA >= 4.5:1, Target Sentuh >= 48dp"
    },
    {
        "id": "NFR-04",
        "category": "Availability (Ketersediaan)",
        "desc": "Sistem RTConnect harus memiliki tingkat ketersediaan layanan minimal 99.0% waktu operasional per bulan di luar jadwal pemeliharaan terencana.",
        "metric": "Uptime >= 99.0%"
    },
    {
        "id": "NFR-05",
        "category": "Maintainability (Pemeliharaan)",
        "desc": "Kode sumber backend harus mematuhi standar penulisan PEP-8 Python dan prinsip Clean Architecture / MVC. Struktur database harus ternormalisasi minimal 3NF untuk mencegah anomali data.",
        "metric": "Kepatuhan PEP-8, Normalisasi Skema 3NF, Dokumentasi API OpenAPI/Swagger"
    },
    {
        "id": "NFR-06",
        "category": "Interoperability (Interoperabilitas)",
        "desc": "Sistem harus menyediakan RESTful API berbasis format JSON untuk pertukaran data antar-komponen serta mendukung integrasi eksternal dengan OpenAI API dan WhatsApp URL Gateway.",
        "metric": "Standard JSON REST API, Skema Response HTTP 200/400/401/404/500 Terstandarisasi"
    },
    {
        "id": "NFR-07",
        "category": "Legal Compliance (Kepatuhan Hukum)",
        "desc": "Pengesahan tanda tangan elektronik wajib memenuhi ketentuan Undang-Undang Republik Indonesia Nomor 1 Tahun 2024 tentang Perubahan Kedua atas UU ITE, dengan memastikan integritas dokumen tidak dapat diubah setelah ditandatangani.",
        "metric": "Kepatuhan UU ITE No. 1/2024, Validasi Keaslian Hash Dokumen"
    },
    {
        "id": "NFR-08",
        "category": "Accuracy & Anti-Hallucination",
        "desc": "Chatbot RAG wajib memberikan jawaban yang strictly grounded pada dokumen pengetahuan resmi RT. Tingkat akurasi pencocokan semantik diukur dengan cosine similarity dengan threshold pasti 0.70 untuk mencegah halusinasi model AI.",
        "metric": "Threshold Cosine Similarity = 0.70, Zero Hallucination Policy (Fallback ke WA RT)"
    }
]

USE_CASE_SPECS = [
    {
        "id": "UC-01",
        "name": "Registrasi Akun Warga Mandiri",
        "actor": "Warga",
        "desc": "Memfasilitasi pendaftaran akun baru bagi warga RT 032 yang belum terdaftar di sistem RTConnect.",
        "precondition": "Pengguna berada pada Halaman Welcome / Landing Page dan belum memiliki akun.",
        "postcondition": "Akun warga baru terdaftar di basis data dengan role 'warga' dan status aktif; pengguna dialihkan ke Halaman Login.",
        "main_flow": [
            ("1. Warga", "Membuka halaman registrasi dengan menekan tombol 'Registrasi'."),
            ("2. Sistem", "Menampilkan formulir pendaftaran akun warga."),
            ("3. Warga", "Mengisi NIK (16 digit), Nama Lengkap, Alamat, No. HP, Email, Password, serta mengunggah berkas spesimen tanda tangan."),
            ("4. Warga", "Menekan tombol 'Daftar Akun'."),
            ("5. Sistem", "Memvalidasi kelengkapan data, format NIK, keunikan email dan NIK di database."),
            ("6. Sistem", "Mengenkripsi password dengan bcrypt dan menyimpan file spesimen tanda tangan."),
            ("7. Sistem", "Menyimpan data pengguna baru ke tabel 'users' dan menampilkan pesan konfirmasi sukses."),
            ("8. Sistem", "Mengarahkan warga ke Halaman Login.")
        ],
        "alt_flow": [
            ("A1. Format NIK Tidak Valid", "Pada langkah 5, jika NIK tidak berjumlah 16 digit angka, sistem menampilkan pesan error dan meminta perbaikan."),
            ("A2. Duplikasi Akun", "Pada langkah 5, jika email atau NIK telah terdaftar sebelumnya, sistem memberi peringatan bahwa akun sudah ada.")
        ],
        "exc_flow": [
            ("E1. Berkas TTD Rusak/Melebihi Ukuran", "Jika berkas tanda tangan bukan format gambar atau melebihi 2MB, sistem menolak unggahan dan meminta berkas yang valid.")
        ]
    },
    {
        "id": "UC-02",
        "name": "Login ke Sistem",
        "actor": "Pengguna (Warga & Ketua RT)",
        "desc": "Mengautentikasi pengguna untuk dapat mengakses dashboard dan fitur layanan sesuai hak akses masing-masing peran.",
        "precondition": "Pengguna telah memiliki akun terdaftar dan berada pada Halaman Login.",
        "postcondition": "Sistem menerbitkan token sesi otorisasi aktif dan membuka dashboard sesuai peran pengguna.",
        "main_flow": [
            ("1. Pengguna", "Membuka halaman login."),
            ("2. Sistem", "Menampilkan form input Email/NIK dan Password."),
            ("3. Pengguna", "Memasukkan kredensial dan menekan tombol 'Masuk'."),
            ("4. Sistem", "Memeriksa kelengkapan input dan mencari data akun di database."),
            ("5. Sistem", "Mencocokkan password dengan hash yang tersimpan."),
            ("6. Sistem", "Membuat token sesi aktif dan memperbarui waktu login terakhir."),
            ("7. Sistem", "Mengarahkan Warga ke Dashboard Warga (/warga/home) atau Ketua RT ke Dashboard RT (/rt/pengajuan).")
        ],
        "alt_flow": [
            ("A1. Pengguna Berperan Warga", "Pada langkah 7, sistem mengarahkan antarmuka ke menu pengajuan dan chatbot warga."),
            ("A2. Pengguna Berperan Ketua RT", "Pada langkah 7, sistem mengarahkan antarmuka ke antrean pengajuan dan manajemen permohonan.")
        ],
        "exc_flow": [
            ("E1. Akun Tidak Terdaftar", "Jika identitas tidak ditemukan, sistem menampilkan pesan error 'Akun tidak terdaftar'."),
            ("E2. Password Salah", "Jika password tidak cocok, sistem menampilkan pesan peringatan 'Password salah'.")
        ]
    },
    {
        "id": "UC-03",
        "name": "Mengajukan Surat Pengantar",
        "actor": "Warga",
        "desc": "Memfasilitasi warga mengajukan permohonan surat pengantar RT secara digital, formulasi draf oleh Generative AI, serta perbaikan data bila ada permintaan revisi.",
        "precondition": "Warga telah berhasil login dan berada pada Dashboard Warga.",
        "postcondition": "Pengajuan tersimpan di database dengan status 'diajukan', draf AI terformulasi, dan notifikasi terkirim ke Ketua RT.",
        "main_flow": [
            ("1. Warga", "Membuka menu 'Ajukan Surat Pengantar'."),
            ("2. Sistem", "Menampilkan formulir pengajuan dengan identitas warga terisi otomatis dari profil akun."),
            ("3. Warga", "Memilih jenis surat pengantar (Domisili, KTP, SKCK, Usaha)."),
            ("4. Warga", "Mengisi tujuan/keperluan surat dan memilih metode tanda tangan (Digital Tempelan / Basah Fisik)."),
            ("5. Warga", "Mengunggah berkas pendukung opsional dan menekan tombol 'Kirim Pengajuan'."),
            ("6. Sistem", "Memvalidasi isian formulir dan menyimpan data pengajuan dengan status 'diajukan'."),
            ("7. Sistem", "Secara otomatis merumuskan draf narasi surat melalui Generative AI dan menyimpannya pada draf_ai_konten."),
            ("8. Sistem", "Mengirimkan notifikasi pengajuan baru ke Ketua RT dan menampilkan pesan sukses ke warga.")
        ],
        "alt_flow": [
            ("A1. Pengisian Ulang Form Akibat Revisi (Feedback Dosen #1)", "Jika pengajuan berstatus 'Perlu Revisi', warga membuka form perbaikan pada riwayat pengajuan, memperbarui isian/lampiran sesuai catatan RT, lalu menekan 'Kirim Ulang Revisi'. Sistem memperbarui data dan mengembalikan status menjadi 'diajukan'.")
        ],
        "exc_flow": [
            ("E1. Keperluan Kosong / Format Lampiran Salah", "Sistem memvalidasi isian dan menampilkan pesan error merah jika ada field wajib yang belum diisi.")
        ]
    },
    {
        "id": "UC-04",
        "name": "Mendownload Surat Pengantar",
        "actor": "Warga",
        "desc": "Memungkinkan warga mengunduh dan menyimpan berkas PDF surat pengantar resmi yang telah disahkan oleh Ketua RT.",
        "precondition": "Pengajuan surat telah selesai diproses oleh Ketua RT dengan status 'selesai' (Metode Digital).",
        "postcondition": "File PDF surat pengantar resmi bertanda tangan digital tersimpan di perangkat warga.",
        "main_flow": [
            ("1. Warga", "Membuka menu riwayat permohonan surat."),
            ("2. Sistem", "Menampilkan daftar pengajuan beserta badge status."),
            ("3. Warga", "Memilih permohonan yang berstatus 'Selesai' dan menekan tombol 'Unduh Surat'."),
            ("4. Sistem", "Menyiapkan aliran berkas PDF resmi dari tabel surat_final."),
            ("5. Sistem", "Menampilkan pratinjau dokumen PDF pada PDF Viewer dan mengunduh berkas ke perangkat warga.")
        ],
        "alt_flow": [
            ("A1. Pengambilan Fisik (TTD Basah)", "Jika permohonan berstatus 'Siap Diambil', tombol unduh digantikan dengan informasi petunjuk pengambilan fisik surat di kediaman RT.")
        ],
        "exc_flow": [
            ("E1. Berkas Rusak / Gagal Unduh", "Sistem menampilkan pesan galat jika koneksi terputus saat streaming berkas PDF dan menyediakan opsi unduh ulang.")
        ]
    },
    {
        "id": "UC-05",
        "name": "Meninjau dan Menindaklanjuti Pengajuan Surat",
        "actor": "Ketua RT",
        "desc": "Memfasilitasi Ketua RT meninjau berkas pemohon, draf rumusan AI, menentukan keputusan (Setuju, Revisi, Tolak), serta membubuhkan tanda tangan (digital tempelan gambar atau basah fisik).",
        "precondition": "Ketua RT telah login dan terdapat permohonan masuk dengan status 'diajukan'.",
        "postcondition": "Status pengajuan diperbarui ('selesai', 'siap_diambil', 'perlu_revisi', atau 'ditolak'), nomor surat diterbitkan jika disetujui, dan warga ternotifikasi.",
        "main_flow": [
            ("1. Ketua RT", "Membuka menu antrean pengajuan pada dashboard RT."),
            ("2. Sistem", "Menampilkan daftar kartu permohonan warga yang menunggu tindak lanjut."),
            ("3. Ketua RT", "Memilih salah satu permohonan untuk membuka halaman detail."),
            ("4. Sistem", "Menampilkan data lengkap pemohon, berkas lampiran, dan pratinjau draf narasi surat rumusan AI."),
            ("5. Ketua RT", "Memilih keputusan tindak lanjut: 'Setujui Pengajuan'."),
            ("6. Sistem", "Menerbitkan nomor surat resmi RT 032 dan menetapkan status 'disetujui'."),
            ("7. Ketua RT", "Memproses pengesahan: Jika metode Digital, memasukkan PIN otorisasi TTD digital. Sistem menyematkan stempel tanda tangan resmi RT pada PDF final dan memperbarui status menjadi 'selesai'."),
            ("8. Sistem", "Mengirimkan notifikasi otomatis ke warga bahwa surat pengantar telah selesai dan siap diunduh.")
        ],
        "alt_flow": [
            ("A1. Keputusan Meminta Revisi (Feedback Dosen #1)", "Pada langkah 5, Ketua RT menekan tombol 'Revisi', mengisi catatan kekurangan berkas, lalu menekan konfirmasi. Sistem memperbarui status menjadi 'perlu_revisi' dan mengirim notifikasi instruksi revisi ke warga."),
            ("A2. Keputusan Menolak Pengajuan", "Pada langkah 5, Ketua RT menekan tombol 'Tolak', mengisi alasan penolakan wajib, lalu menekan konfirmasi. Sistem memperbarui status menjadi 'ditolak' dan mengirimkan notifikasi penolakan ke warga."),
            ("A3. Pengesahan Jalur Tanda Tangan Basah (Feedback Dosen #1)", "Pada langkah 7, jika metode pengajuan adalah 'basah', Ketua RT mencetak surat fisik, menandatangani dengan pulpen, lalu menekan tombol 'Konfirmasi Siap Diambil'. Sistem memperbarui status menjadi 'siap_diambil' dan mengirim notifikasi pengambilan fisik ke warga.")
        ],
        "exc_flow": [
            ("E1. Alasan Penolakan Kosong", "Sistem memvalidasi bahwa kolom alasan penolakan wajib diisi sebelum perubahan status dapat disimpan."),
            ("E2. PIN TTD Digital Salah", "Jika PIN keamanan tidak cocok, sistem menolak penyematan stempel tanda tangan dan meminta input PIN yang benar.")
        ]
    },
    {
        "id": "UC-06",
        "name": "Bertanya kepada RT via Chatbot",
        "actor": "Warga",
        "desc": "Menyediakan layanan konsultasi mandiri seputar informasi dan regulasi RT melalui chatbot NLP berbasis RAG, serta menyediakan fasilitas eskalasi otomatis ke WhatsApp Ketua RT jika informasi tidak ditemukan.",
        "precondition": "Warga telah login dan membuka tab layanan 'Tanya RT'.",
        "postcondition": "Pertanyaan warga terjawab oleh chatbot terverifikasi ATAU dialihkan ke obrolan WhatsApp resmi Ketua RT.",
        "main_flow": [
            ("1. Warga", "Membuka antarmuka percakapan 'Tanya RT'."),
            ("2. Sistem", "Menampilkan ruang chat dengan rekomendasi topik pertanyaan FAQ umum."),
            ("3. Warga", "Mengetikkan pertanyaan mengenai syarat layanan atau aturan RT pada kolom chat."),
            ("4. Warga", "Menekan tombol kirim pesan."),
            ("5. Sistem", "Menyimpan pesan warga ke ChatLog, memproses embedding, dan mencari kemiripan pada KnowledgeBase RT."),
            ("6. Sistem", "Mengevaluasi skor kemiripan: jika skor >= 0.70, sistem mengambil potongan dokumen resmi dan mensintesis jawaban melalui LLM."),
            ("7. Sistem", "Menampilkan gelembung balasan chatbot beserta badge kutipan dokumen sumber resmi RT 032."),
            ("8. Warga", "Membaca jawaban informasi dan kebutuhan konsultasi terpenuhi.")
        ],
        "alt_flow": [
            ("A1. Eskalasi Otomatis ke WhatsApp Ketua RT (Feedback Dosen #1)", "Pada langkah 6, jika skor kemiripan < 0.70 (pertanyaan di luar cakupan dokumen RT), sistem menampilkan pesan permohonan maaf, merangkum topik pertanyaan, dan menampilkan tombol aksi 'Hubungi Ketua RT via WhatsApp'. Warga menekan tombol tersebut dan sistem langsung membuka aplikasi WhatsApp dengan pesan terformat ke nomor Ketua RT.")
        ],
        "exc_flow": [
            ("E1. Layanan API AI Tidak Merespons", "Jika terjadi gangguan konektivitas ke layanan AI, sistem secara anggun menampilkan pesan fallback dan langsung menyajikan tombol WhatsApp darurat ke Ketua RT.")
        ]
    }
]

print("Specifications module loaded successfully.")
