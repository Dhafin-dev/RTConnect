# -*- coding: utf-8 -*-
"""
Bab-bab Naratif Lengkap SRS RTConnect
Menyediakan teks narasi akademis, rincian teknis, dan matriks traceability
"""

USER_STORIES_DATA = [
    {
        "id": "US-01",
        "role": "Warga",
        "action": "mendaftarkan akun baru secara mandiri dengan mengunggah foto stempel tanda tangan",
        "benefit": "saya memiliki akun resmi terverifikasi dan dapat mengajukan surat tanpa perlu menyerahkan data diri berulang kali",
        "scenarios": [
            {
                "title": "Warga Berhasil Melakukan Registrasi Akun Mandiri",
                "given": "Warga berada pada halaman registrasi aplikasi RTConnect",
                "when": "Warga mengisi NIK 16 digit '3515082005040003', nama lengkap, alamat domisili, nomor HP, email aktif, password, dan mengunggah berkas stempel tanda tangan",
                "and": "Warga menekan tombol 'Daftar Akun'",
                "then": "Sistem berhasil memvalidasi seluruh isian, mengenkripsi password dengan bcrypt, menyimpan data pengguna baru, dan menampilkan notifikasi 'Registrasi Berhasil' serta mengalihkan ke halaman Login"
            },
            {
                "title": "Warga Gagal Registrasi Akibat Format NIK Tidak Sesuai",
                "given": "Warga berada pada formulir registrasi akun",
                "when": "Warga memasukkan NIK hanya 12 digit dan menekan tombol 'Daftar Akun'",
                "then": "Sistem menolak pengiriman dan menampilkan pesan kesalahan inline 'NIK harus terdiri dari 16 digit angka'"
            }
        ]
    },
    {
        "id": "US-02",
        "role": "Pengguna (Warga / Ketua RT)",
        "action": "masuk ke sistem menggunakan Email atau NIK beserta kata sandi yang valid",
        "benefit": "saya dapat mengakses fitur layanan yang sesuai dengan hak akses peran saya secara aman",
        "scenarios": [
            {
                "title": "Warga Berhasil Masuk ke Dashboard Warga",
                "given": "Warga berada pada halaman login RTConnect",
                "when": "Warga memasukkan email 'dafin@gmail.com' dan password yang benar lalu menekan 'Masuk'",
                "then": "Sistem menerbitkan token sesi JWT aktif dan mengarahkan antarmuka ke Dashboard Warga (/warga/home)"
            },
            {
                "title": "Ketua RT Berhasil Masuk ke Dashboard RT",
                "given": "Ketua RT berada pada halaman login RTConnect",
                "when": "Ketua RT memasukkan email 'rt032.griya@gmail.com' dan password yang benar lalu menekan 'Masuk'",
                "then": "Sistem mengenali role 'rt' dan mengarahkan antarmuka ke Antrean Pengajuan Surat (/rt/pengajuan)"
            }
        ]
    },
    {
        "id": "US-03",
        "role": "Warga",
        "action": "mengajukan permohonan surat pengantar secara online dari rumah dengan formulasi draf otomatis oleh AI",
        "benefit": "saya tidak perlu menunggu Ketua RT di rumah fisik untuk sekadar membuat draf surat pengantar",
        "scenarios": [
            {
                "title": "Warga Berhasil Mengajukan Surat Keterangan Domisili",
                "given": "Warga telah login dan membuka halaman '/warga/pengajuan/baru'",
                "when": "Warga memilih jenis surat 'Surat Keterangan Domisili', mengisi keperluan 'Pembukaan rekening bank', memilih metode tanda tangan 'Digital (Tempelan Gambar)', dan mengunggah berkas foto KTP",
                "and": "Warga menekan tombol 'Kirim Pengajuan'",
                "then": "Sistem menyimpan permohonan dengan status 'Diajukan', memicu formulasi draf formal narasi surat oleh Generative AI, dan mengirimkan notifikasi antrean baru ke Ketua RT"
            },
            {
                "title": "Warga Mengirimkan Ulang Formulir yang Memerlukan Revisi (Feedback Dosen #1)",
                "given": "Pengajuan warga memiliki status 'Perlu Revisi' dengan catatan RT 'Foto KTP buram'",
                "when": "Warga membuka detail permohonan pada riwayat, mengunggah ulang foto KTP yang jelas, dan menekan tombol 'Kirim Ulang Revisi'",
                "then": "Sistem memperbarui berkas lampiran, mengubah status kembali menjadi 'Diajukan', dan mengirimkan notifikasi perbaruan ke Ketua RT"
            }
        ]
    },
    {
        "id": "US-04",
        "role": "Warga",
        "action": "mengunduh dokumen surat pengantar resmi yang telah disahkan dalam format PDF",
        "benefit": "saya dapat langsung mencetak atau melampirkan berkas resmi tersebut ke kantor kelurahan/instansi tujuan",
        "scenarios": [
            {
                "title": "Warga Mengunduh Surat Pengantar Bertanda Tangan Digital Resmi",
                "given": "Warga berada pada halaman riwayat pengajuan dan permohonan memiliki status 'Selesai'",
                "when": "Warga menekan tombol 'Unduh Surat'",
                "then": "Sistem mengirimkan berkas aliran (stream) PDF resmi yang memuat kop surat, nomor resmi, biodata pemohon, dan stempel tanda tangan digital Ketua RT"
            }
        ]
    },
    {
        "id": "US-05",
        "role": "Ketua RT",
        "action": "meninjau data pemohon, berkas lampiran, dan draf AI, lalu menentukan keputusan tindak lanjut (Setuju, Revisi, Tolak) serta membubuhkan tanda tangan",
        "benefit": "administrasi RT berjalan cepat, valid, transparan, dan tidak memerlukan pengetikan ulang format surat berulang kali",
        "scenarios": [
            {
                "title": "Ketua RT Menyetujui Pengajuan dan Membubuhkan TTD Digital Resmi (Feedback Dosen #1)",
                "given": "Ketua RT membuka detail permohonan 'SRT-001' yang berstatus 'Diajukan' dengan metode 'Digital'",
                "when": "Ketua RT memeriksa kelengkapan berkas pemohon, menekan tombol 'Setujui Pengajuan', memasukkan PIN keamanan tanda tangan digital, dan menekan konfirmasi",
                "then": "Sistem menetapkan nomor surat resmi, menyematkan stempel gambar tanda tangan RT pada PDF final, mengubah status menjadi 'Selesai', dan mengirimkan notifikasi siap unduh ke warga"
            },
            {
                "title": "Ketua RT Mengonfirmasi Surat Bertanda Tangan Basah Siap Diambil (Feedback Dosen #1)",
                "given": "Ketua RT menyetujui pengajuan 'SRT-002' dengan metode 'Basah (Fisik)' dan telah mencetak serta menandatangani surat fisik",
                "when": "Ketua RT menekan tombol 'Konfirmasi Siap Diambil' di dashboard RT",
                "then": "Sistem memperbarui status menjadi 'Siap Diambil' dan mengirimkan notifikasi jadwal pengambilan fisik ke akun warga"
            },
            {
                "title": "Ketua RT Meminta Revisi Berkas Permohonan Warga",
                "given": "Ketua RT menemukan berkas lampiran pemohon tidak terbaca",
                "when": "Ketua RT menekan tombol 'Minta Revisi', mengisi catatan 'Mohon unggah ulang foto KTP yang lebih terang', dan menekan kirim",
                "then": "Sistem memperbarui status menjadi 'Perlu Revisi', mencatat instruksi pada catatan_revisi, dan mengirimkan notifikasi ke warga"
            },
            {
                "title": "Ketua RT Menolak Pengajuan Surat Warga",
                "given": "Ketua RT memeriksa pemohon yang tidak memenuhi kriteria domisili lingkungan",
                "when": "Ketua RT menekan tombol 'Tolak Pengajuan', mengisi alasan penolakan wajib, dan menekan konfirmasi",
                "then": "Sistem memperbarui status menjadi 'Ditolak' dan mengirimkan pemberitahuan resmi alasan penolakan ke warga"
            }
        ]
    },
    {
        "id": "US-06",
        "role": "Warga",
        "action": "bertanya kepada chatbot Tanya RT seputar prosedur dan syarat administrasi 24/7 dan mendapatkan eskalasi ke WhatsApp RT bila belum terjawab",
        "benefit": "saya memperoleh kejelasan informasi pelayanan kapan saja tanpa harus menunggu jam luang Ketua RT",
        "scenarios": [
            {
                "title": "Chatbot Menjawab Pertanyaan Prosedural Berdasarkan Basis Pengetahuan RT",
                "given": "Warga membuka ruang percakapan Tanya RT di aplikasi",
                "when": "Warga mengetikkan pertanyaan 'Apa saja syarat membuat surat pengantar domisili?' dan menekan kirim",
                "then": "Sistem menghitung kemiripan semantik (skor >= 0.70), mengambil potongan aturan RT yang relevan, dan menyajikan balasan akurat disertai kutipan sumber 'Peraturan Tata Tertib RT 032 Bab 3'"
            },
            {
                "title": "Sistem Mengeskalasi Pertanyaan di Luar Jangkauan ke WhatsApp Ketua RT (Feedback Dosen #1)",
                "given": "Warga menanyakan pertanyaan yang tidak terdapat pada dokumen aturan RT ('Bolehkah menyewa lapangan voli untuk acara keluarga?')",
                "when": "Sistem mendeteksi skor kemiripan semantik di bawah ambang batas (skor < 0.70)",
                "then": "Sistem menampilkan pesan maaf bahwa data belum tersedia dan menyajikan tombol interaktif 'Hubungi Ketua RT via WhatsApp' yang memuat tautan deep-link wa.me terformat"
            }
        ]
    }
]

RTM_DATA = [
    ("FR-01", "UC-01", "US-01", "Activity Registrasi", "Sequence Register", "users", "SCREEN-002 (Register)"),
    ("FR-02", "UC-02", "US-02", "Activity Login", "Sequence Login", "users", "SCREEN-003 (Login)"),
    ("FR-03", "UC-03", "US-03", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "pengajuan_surat, jenis_surat", "SCREEN-007 (Form Pengajuan)"),
    ("FR-04", "UC-03", "US-03", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "pengajuan_surat (draf_ai_konten)", "SCREEN-010 (Detail & Draf AI)"),
    ("FR-05", "UC-05", "US-05", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "pengajuan_surat, users", "SCREEN-009 (Antrean RT)"),
    ("FR-06", "UC-05", "US-05", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "pengajuan_surat", "SCREEN-010 (Detail & Tindak Lanjut)"),
    ("FR-07", "UC-05", "US-05", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "surat_final, pengajuan_surat", "SCREEN-010 (Detail & TTD Digital)"),
    ("FR-08", "UC-05", "US-05", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "pengajuan_surat", "SCREEN-010 (Detail & TTD Basah)"),
    ("FR-09", "UC-04", "US-04", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "surat_final", "SCREEN-006, SCREEN-012 (PDF Viewer)"),
    ("FR-10", "UC-03", "US-03", "Activity Pengajuan Surat", "Sequence Pengajuan Surat", "pengajuan_surat", "SCREEN-006, SCREEN-008 (Form Revisi)"),
    ("FR-11", "UC-06", "US-06", "Activity Chatbot", "Sequence Chatbot RAG", "knowledge_chunks, chat_messages", "SCREEN-011 (Chatbot Tanya RT)"),
    ("FR-12", "UC-06", "US-06", "Activity Chatbot", "Sequence Chatbot RAG", "chat_messages, notifikasi", "SCREEN-011 (Eskalasi WhatsApp)")
]

BPMN_TASKS_AS_IS = [
    ("T-AS-01", "Warga mengisi formulir/pesan pengajuan", "Warga", "KTP pemohon, keperluan surat", "Formulir kertas / Pesan teks WhatsApp"),
    ("T-AS-02", "Ketua RT memeriksa kelengkapan berkas", "Ketua RT", "Formulir fisik / Pesan teks WhatsApp", "Hasil verifikasi kelengkapan berkas"),
    ("T-AS-03", "Warga memperbaiki berkas (jika belum lengkap)", "Warga", "Instruksi perbaikan dari RT", "Berkas perbaikan fisik"),
    ("T-AS-04", "Ketua RT mengetik draf surat pengantar", "Ketua RT", "Data pemohon, template blangko Word", "Lembar fisik surat tercetak"),
    ("T-AS-05", "Ketua RT menandatangani dan membubuhkan stempel", "Ketua RT", "Lembar cetak surat, pulpen, stempel tinta RT", "Surat fisik bertandatangan basah"),
    ("T-AS-06", "Ketua RT mengabari warga via pesan singkat", "Ketua RT", "Nomor WhatsApp warga", "Pesan notifikasi pengambilan surat"),
    ("T-AS-07", "Warga mengambil surat fisik di rumah RT", "Warga", "Kehadiran fisik warga di rumah RT", "Fisik surat pengantar diterima warga")
]

BPMN_TASKS_TO_BE = [
    ("T-TB-01", "Warga mengisi formulir pengajuan surat", "Warga", "Profil akun login, jenis surat, keperluan, metode TTD, lampiran", "Data pengajuan terstruktur"),
    ("T-TB-02", "Sistem memvalidasi isian dan berkas lampiran", "Sistem", "Data pengajuan terstruktur", "Status validitas (Valid / Invalid)"),
    ("T-TB-03", "Sistem menyimpan rekor pengajuan ('Diajukan')", "Sistem", "Payload pengajuan valid", "pengajuan_id baru di basis data"),
    ("T-TB-04", "Sistem (Generative AI) merumuskan draf narasi surat", "Sistem (AI)", "Data pengajuan, biodata warga, template jenis surat", "draf_ai_konten tersimpan"),
    ("T-TB-05", "Sistem mengirim notifikasi permohonan baru ke RT", "Sistem", "ID Pengajuan, ID Ketua RT", "Notifikasi antrean masuk pada dashboard RT"),
    ("T-TB-06", "Ketua RT meninjau data pemohon, lampiran, dan draf AI", "Ketua RT", "Antrean masuk, draf AI, lampiran berkas", "Pertimbangan keputusan tindak lanjut"),
    ("T-TB-07", "Ketua RT memutuskan: Tolak Pengajuan", "Ketua RT", "Teks alasan penolakan wajib", "Status DB 'ditolak', notifikasi dikirim ke warga"),
    ("T-TB-08", "Ketua RT memutuskan: Minta Revisi", "Ketua RT", "Teks catatan perbaikan berkas", "Status DB 'perlu_revisi', notifikasi instruksi ke warga"),
    ("T-TB-09", "Warga mengirimkan ulang form perbaikan", "Warga", "Catatan revisi RT, perbaikan data/lampiran", "Status DB kembali 'diajukan', antrean RT terupdate"),
    ("T-TB-10", "Sistem menerbitkan nomor surat resmi RT 032", "Sistem", "Persetujuan Ketua RT, format nomor surat resmi", "nomor_surat_resmi ter-generate, status 'disetujui'"),
    ("T-TB-11", "Pengesahan Digital: RT konfirmasi PIN & Sistem sematkan stempel", "RT & Sistem", "PIN keamanan RT, gambar stempel TTD RT, draf surat", "Dokumen PDF resmi (surat_final), status 'selesai'"),
    ("T-TB-12", "Pengesahan Basah: RT cetak fisik, tanda tangan, update status", "Ketua RT", "Lembar fisik cetak draf, pulpen, stempel basah RT", "Surat fisik siap, status 'siap_diambil'"),
    ("T-TB-13", "Warga menerima hasil (Unduh PDF / Ambil Fisik di RT)", "Warga", "Notifikasi sistem, akses akun warga", "Surat pengantar resmi berhasil diterima warga")
]

print("Chapters content module loaded successfully.")
