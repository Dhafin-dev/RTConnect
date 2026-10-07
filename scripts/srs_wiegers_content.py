# -*- coding: utf-8 -*-
"""
Modul Konten Spesifikasi Teknis SRS RTConnect
Mengikuti Struktur Template Karl E. Wiegers (IEEE Std 830-1998)
Praktikum Pembangunan Perangkat Lunak (Praktikum I1) - Universitas Airlangga 2026
"""

METADATA = {
    "title": "Software Requirements Specification",
    "project_name": "RTConnect: Perangkat Lunak Administrasi di Tingkat RT/RW dengan Integrasi NLP dan Generative AI",
    "version": "1.0 approved",
    "authors": [
        {"name": "Muhammad Nafidz Arradhin", "nim": "187241027"},
        {"name": "Mirza Diwa Luscakson", "nim": "187241042"},
        {"name": "Febrian Muhammad Yudhistira", "nim": "187241051"},
        {"name": "Ahmad Dhafin Al Farisy", "nim": "187241057"}
    ],
    "organization": "Program Studi Sarjana Sistem Informasi\nFakultas Sains dan Teknologi\nUniversitas Airlangga Surabaya",
    "date_created": "Oktober 2026",
    "course": "Praktikum Pembangunan Perangkat Lunak (Kelas I1)",
    "lecturer": "Dr. Indra Kharisma Raharjana, S.Kom., M.T.",
    "lecturer_nip": "198110282006041003"
}

REVISION_HISTORY = [
    {
        "name": "Kelompok 3 (Praktikum I1)",
        "date": "24 September 2026",
        "reason": "Initial Draft tugas week 6 (Pemodelan awal proses bisnis dan fungsionalitas sistem)",
        "version": "0.1"
    },
    {
        "name": "Dr. Indra Kharisma Raharjana, S.Kom., M.T.",
        "date": "28 September 2026",
        "reason": "Review dan arahan revisi dosen pengampu (Penyederhanaan use case, detail I/O & XOR BPMN, narasi sequence, dan active bar)",
        "version": "0.2"
    },
    {
        "name": "Kelompok 3 (Praktikum I1)",
        "date": "29 September 2026",
        "reason": "Penerapan menyeluruh 4 revisi dosen pengampu, normalisasi data model (tabel users terpusat), dan integrasi RAG",
        "version": "0.9"
    },
    {
        "name": "Kelompok 3 (Praktikum I1)",
        "date": "07 Oktober 2026",
        "reason": "Restrukturisasi dokumen ke dalam template Karl E. Wiegers (IEEE Std 830-1998) resmi, pengayaan System Features & Stimulus/Response",
        "version": "1.0 approved"
    }
]

SYSTEM_FEATURES_DATA = [
    {
        "num": "4.1",
        "name": "Registrasi dan Autentikasi Pengguna Terpadu",
        "priority": "Tinggi (High) — Benefit: 9, Penalty: 9, Cost: 4, Risk: 3",
        "desc": "Fitur ini menyediakan mekanisme pendaftaran akun mandiri bagi warga RT 032 RW 08 serta autentikasi satu pintu (single-door authentication) bagi Warga dan Ketua RT dengan penerbitan token sesi JSON Web Token (JWT). Fitur ini menjamin privasi dan otorisasi hak akses peran secara ketat.",
        "stimulus_response": [
            ("1", "Pengguna membuka form registrasi", "Sistem menampilkan form isian NIK, nama lengkap, alamat, no telepon, email, password, dan tombol unggah stempel tanda tangan"),
            ("2", "Warga mengirimkan data pendaftaran", "Sistem memvalidasi format NIK 16 digit, keunikan email/NIK di database, mengenkripsi password dengan bcrypt, menyimpan file stempel TTD, dan mengarahkan ke halaman login"),
            ("3", "Pengguna membuka halaman login", "Sistem menampilkan antarmuka login dengan field Email/NIK dan Password"),
            ("4", "Pengguna memasukkan kredensial dan menekan tombol 'Masuk'", "Sistem memverifikasi kecocokan hash password, menerbitkan token sesi JWT, mencatat log login, dan mengarahkan pengguna ke dashboard sesuai peran (Warga -> /warga/home, Ketua RT -> /rt/pengajuan)"),
            ("5", "Pengguna memasukkan kredensial tidak valid", "Sistem menolak otentikasi dan menyajikan pesan galat spesifik tanpa membocorkan eksistensi data privat")
        ],
        "reqs": [
            ("REQ-1", "Sistem hanya mengizinkan pengguna masuk dengan kredensial yang valid dan terdaftar."),
            ("REQ-2", "Sistem wajib mengenkripsi seluruh kata sandi menggunakan algoritma bcrypt (salt work factor >= 10)."),
            ("REQ-3", "Sistem wajib memvalidasi bahwa NIK pemohon terdiri dari tepat 16 digit angka kependudukan."),
            ("REQ-4", "Sistem wajib mengalihkan antarmuka secara otomatis ke Dashboard Warga atau Dashboard RT berdasarkan klaim 'role' pada token JWT.")
        ]
    },
    {
        "num": "4.2",
        "name": "Pengajuan Permohonan Surat Pengantar Mandiri",
        "priority": "Tinggi (High) — Benefit: 9, Penalty: 8, Cost: 5, Risk: 3",
        "desc": "Fitur ini memungkinkan warga mengajukan permohonan surat pengantar (Surat Keterangan Domisili, Pengantar KTP/KK, Pengantar SKCK, dan Surat Keterangan Usaha) secara daring. Formulir secara otomatis memuat data profil pemohon, menyediakan pilihan metode tanda tangan (Digital vs Basah), serta mengizinkan pengunggahan berkas lampiran pendukung. Proses pengisian ulang form akibat revisi diakomodasi sebagai alur alternatif dari fitur ini (sesuai Feedback Dosen #1).",
        "stimulus_response": [
            ("1", "Warga menekan tombol 'Ajukan Surat Pengantar'", "Sistem merender formulir permohonan dengan biodata pemohon terisi otomatis dari profil akun"),
            ("2", "Warga memilih jenis surat, mengisi keperluan, memilih opsi TTD, dan mengunggah berkas pendukung opsional", "Sistem memvalidasi kelengkapan isian secara real-time pada layer UI"),
            ("3", "Warga menekan tombol 'Kirim Pengajuan'", "Sistem memvalidasi format berkas, menyimpan permohonan dengan status 'diajukan', dan memicu proses formulasi draf AI"),
            ("4", "Warga menerima notifikasi 'Perlu Revisi' dan membuka detail permohonan", "Sistem menyajikan form perbaikan dengan catatan revisi RT dan data lama yang siap diperbarui warga"),
            ("5", "Warga menekan 'Kirim Ulang Revisi'", "Sistem memperbarui berkas pengajuan dan mengembalikan status menjadi 'diajukan' untuk ditinjau ulang oleh RT")
        ],
        "reqs": [
            ("REQ-5", "Sistem wajib mengisi otomatis data nama, NIK, dan alamat pemohon dari profil pengguna yang terotentikasi."),
            ("REQ-6", "Sistem harus memvalidasi bahwa kolom 'keperluan' terisi minimal 10 karakter teks bermakna."),
            ("REQ-7", "Sistem wajib membatasi ukuran berkas lampiran maksimal 2MB dengan format PDF, PNG, atau JPG."),
            ("REQ-8", "Sistem harus mendukung pengiriman ulang formulir perbaikan jika status permohonan adalah 'perlu_revisi'.")
        ]
    },
    {
        "num": "4.3",
        "name": "Formulasi Draf Narasi Surat Berbasis Generative AI",
        "priority": "Tinggi (High) — Benefit: 9, Penalty: 6, Cost: 6, Risk: 5",
        "desc": "Fitur ini mengintegrasikan model Large Language Model (LLM) melalui API untuk menyusun draf narasi formal surat pengantar resmi berbahasa Indonesia baku sesaat setelah permohonan berhasil dikirim oleh warga. Draf ini disajikan kepada Ketua RT untuk mengeliminasi beban pengetikan manual format surat.",
        "stimulus_response": [
            ("1", "Sistem mendeteksi pencatatan permohonan surat baru", "Sistem mengumpulkan payload data pemohon, jenis surat, dan maksud keperluan"),
            ("2", "Sistem menyuntikkan data ke dalam prompt template baku sekretariat RT 032", "Sistem memanggil endpoint LLM API secara asinkron"),
            ("3", "Model LLM mengembalikan teks narasi formal", "Sistem menyimpan teks pada kolom 'draf_ai_konten' dan mencatat audit draf surat"),
            ("4", "Terjadi kegagalan koneksi atau timeout pada LLM API", "Sistem secara anggun (graceful fallback) menggunakan template teks standar berbasis placeholder tanpa menghentikan alur pengajuan")
        ],
        "reqs": [
            ("REQ-9", "Sistem wajib memanggil LLM API dengan parameter temperature <= 0.3 untuk menjamin konsistensi dan formalitas bahasa."),
            ("REQ-10", "Draf narasi yang dihasilkan wajib memuat identitas lengkap pemohon, maksud keperluan, dan klausul pengesahan standar RT 032."),
            ("REQ-11", "Sistem wajib menyimpan rekor draf narasi pada basis data agar dapat ditinjau dan disunting oleh Ketua RT.")
        ]
    },
    {
        "num": "4.4",
        "name": "Peninjauan dan Tindak Lanjut Pengajuan oleh Ketua RT",
        "priority": "Tinggi (High) — Benefit: 9, Penalty: 9, Cost: 5, Risk: 4",
        "desc": "Fitur ini menyediakan antrean kerja administratif (inbox) bagi Ketua RT untuk memeriksa berkas pemohon, menelaah draf rumusan AI, dan mengambil salah satu dari 3 tindakan keputusan resmi: Menyetujui, Meminta Revisi, atau Menolak permohonan. Seluruh proses pengesahan tanda tangan (digital maupun basah) disatukan ke dalam fitur tindak lanjut ini (sesuai Feedback Dosen #1).",
        "stimulus_response": [
            ("1", "Ketua RT membuka menu antrean pengajuan", "Sistem menyajikan daftar kartu permohonan warga yang berstatus 'diajukan'"),
            ("2", "Ketua RT memilih salah satu pengajuan", "Sistem menampilkan data pemohon, dokumen lampiran, dan pratinjau draf narasi hasil AI"),
            ("3", "Ketua RT menekan tombol 'Setujui Pengajuan'", "Sistem menerbitkan nomor surat resmi RT 032 dan melanjutkan ke alur pengesahan sesuai metode TTD yang dipilih pemohon"),
            ("4", "Ketua RT menekan tombol 'Minta Revisi' dan menginput catatan kekurangan", "Sistem memperbarui status menjadi 'perlu_revisi' dan mengirim notifikasi instruksi ke warga"),
            ("5", "Ketua RT menekan tombol 'Tolak Pengajuan' dan menginput alasan penolakan wajib", "Sistem memperbarui status menjadi 'ditolak' dan mengirim pemberitahuan penolakan ke warga")
        ],
        "reqs": [
            ("REQ-12", "Sistem wajib menampilkan antrean permohonan masuk dengan penyaringan status dan tanggal secara kronologis."),
            ("REQ-13", "Sistem wajib mewajibkan input teks alasan penolakan sebelum status 'ditolak' dapat diproses."),
            ("REQ-14", "Sistem wajib menerbitkan nomor surat resmi otomatis berformat '470/{NO}/032.08/{BULAN}/{TAHUN}' saat permohonan disetujui.")
        ]
    },
    {
        "num": "4.5",
        "name": "Pengesahan Dokumen (Digital & Basah) serta Penerbitan Surat Resmi",
        "priority": "Tinggi (High) — Benefit: 8, Penalty: 7, Cost: 6, Risk: 4",
        "desc": "Fitur ini mengelola siklus akhir penerbitan dokumen surat pengantar resmi. Pada jalur digital, sistem memvalidasi otorisasi Ketua RT, menyematkan stempel gambar tanda tangan resmi, menghasilkan file PDF final, dan memungkinkan warga mengunduhnya. Pada jalur basah, sistem menyediakan berkas siap cetak fisik dan memfasilitasi Ketua RT memperbarui status siap diambil setelah dokumen dicap basah.",
        "stimulus_response": [
            ("1", "Ketua RT memproses persetujuan dengan metode 'Digital'", "Sistem meminta input PIN otorisasi tanda tangan digital Ketua RT"),
            ("2", "Ketua RT memasukkan PIN yang valid dan menekan konfirmasi", "Sistem menyematkan stempel tanda tangan resmi pada berkas PDF, menerbitkan kode verifikasi, mengubah status menjadi 'selesai', dan menerbitkan notifikasi siap unduh"),
            ("3", "Warga membuka riwayat pengajuan dan menekan 'Unduh Surat'", "Sistem mengirimkan berkas PDF surat pengantar resmi ke penyimpanan perangkat warga"),
            ("4", "Ketua RT memproses persetujuan dengan metode 'Basah'", "Sistem menyediakan tombol cetak dokumen fisik dan tombol 'Konfirmasi Siap Diambil'"),
            ("5", "Ketua RT menekan 'Konfirmasi Siap Diambil' setelah menandatangani fisik", "Sistem memperbarui status menjadi 'siap_diambil' dan mengirimkan notifikasi jadwal pengambilan di rumah RT ke warga")
        ],
        "reqs": [
            ("REQ-15", "Sistem wajib memvalidasi PIN otorisasi sebelum stempel tanda tangan digital Ketua RT disematkan ke berkas PDF."),
            ("REQ-16", "Dokumen PDF yang diterbitkan wajib memuat kode verifikasi unik (hash) untuk pembuktian keabsahan elektronik."),
            ("REQ-17", "Sistem wajib menyediakan PDF viewer bawaan dan tombol unduh langsung bagi warga."),
            ("REQ-18", "Sistem wajib mencatat tanggal dan waktu pengambilan berkas fisik untuk pembaruan status akhir.")
        ]
    },
    {
        "num": "4.6",
        "name": "Layanan Asisten Cerdas Chatbot Tanya RT & Eskalasi WhatsApp",
        "priority": "Tinggi (High) — Benefit: 8, Penalty: 6, Cost: 7, Risk: 4",
        "desc": "Fitur ini menyediakan layanan tanya jawab mandiri 24/7 bagi warga seputar persyaratan berkas dan tata tertib RT menggunakan teknik Retrieval-Augmented Generation (RAG). Pertanyaan warga dicocokkan secara semantik terhadap basis pengetahuan resmi RT (dokumen Markdown yang diindeks ke tabel basis data). Jika kemiripan semantik >= 0.70, sistem menyajikan jawaban faktual beserta kutipan rujukan. Jika di bawah 0.70, sistem secara otomatis merangkum pertanyaan dan menyajikan tombol eskalasi langsung ke WhatsApp Ketua RT (sesuai Feedback Dosen #1).",
        "stimulus_response": [
            ("1", "Warga membuka tab layanan 'Tanya RT'", "Sistem menampilkan antarmuka obrolan dan menyajikan rekomendasi pertanyaan FAQ seputar layanan"),
            ("2", "Warga mengetikkan pertanyaan pada kolom chat dan menekan kirim", "Sistem mencatat pesan ke ChatLog, menghasilkan vector embedding query, dan mencari kemiripan semantik (Cosine Similarity) pada basis pengetahuan"),
            ("3", "Skor kemiripan semantik >= 0.70 (Informasi Ditemukan)", "Sistem menyintesis jawaban menggunakan LLM berbasis konteks rujukan resmi dan menampilkan gelembung jawaban beserta badge dokumen sumber"),
            ("4", "Skor kemiripan semantik < 0.70 (Informasi Tidak Ditemukan)", "Sistem menampilkan pesan permohonan maaf, merangkum inti pertanyaan, dan menyajikan tombol interaktif 'Hubungi Ketua RT via WhatsApp'"),
            ("5", "Warga menekan tombol 'Hubungi Ketua RT via WhatsApp'", "Sistem mengarahkan peramban/aplikasi ke tautan deep-link WhatsApp resmi Ketua RT (wa.me) dengan pesan pertanyaan yang terisi otomatis")
        ],
        "reqs": [
            ("REQ-19", "Sistem wajib menggunakan representasi vektor numerik untuk mengukur kemiripan teks pertanyaan warga dengan potongan aturan RT."),
            ("REQ-20", "Sistem wajib menetapkan ambang batas kemiripan kosinus (cosine similarity threshold) sebesar 0.70."),
            ("REQ-21", "Sistem dilarang keras mengarang informasi di luar konteks dokumen resmi RT yang terindeks (Zero Hallucination Policy)."),
            ("REQ-22", "Sistem wajib memformat tautan URL WhatsApp dengan enkripsi URI encoding yang memuat nomor telepon resmi Ketua RT dan ringkasan pertanyaan warga.")
        ]
    }
]

print("Wiegers specifications content loaded!")
