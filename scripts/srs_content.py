# -*- coding: utf-8 -*-
"""
Modul Konten Resmi SRS RTConnect
Menyediakan teks terstruktur, tabel spesifikasi, dan data untuk pembentukan DOCX & PDF
"""

METADATA = {
    "title": "SOFTWARE REQUIREMENTS SPECIFICATION (SRS)",
    "project_name": "RTConnect: Perangkat Lunak Administrasi di Tingkat RT/RW dengan Integrasi NLP dan Generative AI",
    "course": "Praktikum Pembangunan Perangkat Lunak (Praktikum I1)",
    "lecturer": "Dr. Indra Kharisma Raharjana, S.Kom., M.T.",
    "lecturer_nip": "198110282006041003",
    "institution": "Program Studi Sarjana Sistem Informasi\nFakultas Sains dan Teknologi\nUniversitas Airlangga Surabaya\n2026",
    "members": [
        {"name": "Muhammad Nafidz Arradhin", "nim": "187241027"},
        {"name": "Mirza Diwa Luscakson", "nim": "187241042"},
        {"name": "Febrian Muhammad Yudhistira", "nim": "187241051"},
        {"name": "Ahmad Dhafin Al Farisy", "nim": "187241057"}
    ]
}

ABBREVIATIONS = [
    ("AI", "Artificial Intelligence (Kecerdasan Buatan)"),
    ("API", "Application Programming Interface"),
    ("BDD", "Behavior-Driven Development"),
    ("BPMN", "Business Process Model and Notation"),
    ("CDM", "Conceptual Data Model"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("ERD", "Entity Relationship Diagram"),
    ("FAQ", "Frequently Asked Questions"),
    ("FK", "Foreign Key"),
    ("GUI", "Graphical User Interface"),
    ("IEEE", "Institute of Electrical and Electronics Engineers"),
    ("JWT", "JSON Web Token"),
    ("KTP", "Kartu Tanda Penduduk"),
    ("LLM", "Large Language Model"),
    ("MVC", "Model-View-Controller"),
    ("NIK", "Nomor Induk Kependudukan"),
    ("NLP", "Natural Language Processing"),
    ("PDM", "Physical Data Model"),
    ("PK", "Primary Key"),
    ("RAG", "Retrieval-Augmented Generation"),
    ("RTM", "Requirement Traceability Matrix"),
    ("SKCK", "Surat Keterangan Catatan Kepolisian"),
    ("SKU", "Surat Keterangan Usaha"),
    ("SRS", "Software Requirements Specification"),
    ("SUS", "System Usability Scale"),
    ("TTD", "Tanda Tangan"),
    ("UC", "Use Case"),
    ("UI", "User Interface"),
    ("UML", "Unified Modeling Language")
]

CHANGE_LOG_DATA = [
    ("1", "Use Case Diagram", "Terdapat use case 'Mengisi Ulang Form (Revisi)' sebagai use case mandiri", "Dihapus sebagai use case independen. Proses revisi form diintegrasikan sebagai alur alternatif/eksepsi pada use case Mengajukan Surat Pengantar.", "Sesuai Feedback Resmi Dosen #1 (Revisi form bukan fitur utama mandiri)."),
    ("2", "Use Case Diagram", "Terdapat use case 'Menandatangani Surat Secara Basah' dan 'Mengonfirmasi Tanda Tangan Digital'", "Dilebur dan disederhanakan masuk ke dalam use case 'Menindaklanjuti Pengajuan Surat'.", "Sesuai Feedback Resmi Dosen #1 (Aksi tanda tangan disederhanakan masuk ke alur tindak lanjut RT)."),
    ("3", "Use Case Diagram", "Terdapat use case 'Menjawab Pertanyaan Warga (Eskalasi)' untuk Ketua RT", "Dihapus sebagai use case Ketua RT. Eskalasi WhatsApp dimodelkan sebagai perilaku sistem (system behavior) dan alur alternatif pada 'Bertanya kepada RT via Chatbot'.", "Sesuai Feedback Resmi Dosen #1 (Menjawab pertanyaan warga bukan fitur sistem yang disediakan untuk RT)."),
    ("4", "Use Case Diagram", "Fitur Registrasi dan Login tidak dimodelkan di Use Case, padahal ada di UI & Sequence", "Menambahkan use case 'Registrasi Akun' (Warga) dan 'Login ke Sistem' (Pengguna General).", "Menjaga integritas dan konsistensi requirement traceability."),
    ("5", "BPMN (AS-IS & TO-BE)", "Aktivitas tugas belum mencantumkan rincian input dan output data", "Setiap aktivitas (task) kini dilengkapi metadata [Input: ...] dan [Output: ...] secara eksplisit.", "Sesuai Feedback Resmi Dosen #2 (Input/output BPMN diperjelas detail)."),
    ("6", "BPMN (AS-IS & TO-BE)", "Gateway keputusan belum ditandai jenisnya (hanya tanda tanya biasa)", "Seluruh gateway keputusan diberi penandaan formal [XOR] dengan label kondisi cabang yang eksplisit dan mutually exclusive.", "Sesuai Feedback Resmi Dosen #2 (Gateway harus ditandai XOR/OR)."),
    ("7", "Sequence Diagram", "Pesan dari Aktor ke Boundary menggunakan sintaks kode/API (misal: inputEmail(), POST /login, submitForm())", "Seluruh pesan interaksi Aktor ke Boundary diubah menjadi narasi bahasa manusia murni (misal: Membuka formulir, Memasukkan email dan password, Menekan tombol Masuk).", "Sesuai Feedback Resmi Dosen #3 (Pesan aktor ke boundary tidak boleh memakai kode)."),
    ("8", "Sequence Diagram", "Aktor tidak memiliki activation bar (active bar) saat berinteraksi", "Menambahkan activation dan deactivation bar pada aktor di seluruh sequence diagram saat mengirim pesan dan menunggu respons.", "Sesuai Feedback Resmi Dosen #4 (Active bar pada aktor wajib ada)."),
    ("9", "Sequence Diagram", "Stereotype robustness belum konsisten di semua diagram", "Menerapkan stereotype Boundary-Control-Entity secara ketat (:Boundary, :Controller/Service, :Entity).", "Memenuhi kaidah Robustness Analysis rekayasa perangkat lunak."),
    ("10", "Struktur Basis Data", "Tabel pengguna terpecah dua secara fisik ('RT' dan 'Warga') yang redundan dan memicu konflik pada Sequence Login", "Diresolusi menjadi tabel terpadu 'users' dengan kolom 'role' (enum: 'warga', 'rt', 'admin') yang konsisten dengan objek :User.", "Normalisasi basis data dan konsistensi dengan Sequence Diagram Login."),
    ("11", "Teks Bab VI (User Story)", "Kalimat pembuka salah tulis: 'Pada Bab I ini, peta interaksi tersebut diturunkan...'", "Dikoreksi menjadi: 'Pada Bab VI ini, peta kebutuhan dan interaksi pengguna...'", "Koreksi editorial dan peningkatan kredibilitas akademis laporan."),
    ("12", "GUI Design (Bab IV)", "Sub-bab 4.7 hilang di Daftar Isi; Caption Gambar 4.3 tertulis 'Gambar 4.4 Home Page' sehingga duplikat", "Memasukkan 4.7 Page Formulir Pengajuan ke Daftar Isi; Memperbaiki caption Gambar 4.3 menjadi 'Login Page'.", "Koreksi penomoran dan konsistensi layout laporan resmi.")
]

CONTRIBUTION_DATA = [
    ("1", "Muhammad Nafidz Arradhin", "187241027", "[INSERT FOTO ANGGOTA]", "[ISI KONTRIBUSI AKTUAL ANGGOTA]"),
    ("2", "Mirza Diwa Luscakson", "187241042", "[INSERT FOTO ANGGOTA]", "[ISI KONTRIBUSI AKTUAL ANGGOTA]"),
    ("3", "Febrian Muhammad Yudhistira", "187241051", "[INSERT FOTO ANGGOTA]", "[ISI KONTRIBUSI AKTUAL ANGGOTA]"),
    ("4", "Ahmad Dhafin Al Farisy", "187241057", "[INSERT FOTO ANGGOTA]", "[ISI KONTRIBUSI AKTUAL ANGGOTA]")
]

REFERENCES_DATA = [
    "Agusman, Y., Yasir, A., Asrun, L., & Alauddin, M. R. S. (2023). Peningkatan Aparatur Desa dalam Pelayanan Publik di Era Digital Desa Tirawuta Kecamatan Tirawuta Provinsi Sulawesi Tenggara. Indonesian Journal of Community Services, 2(1), 25–30. https://doi.org/10.30659/ijcs.2.1.25-30",
    "Arafat, A., Rasyid, R., Hestiana, S., Rendi, R., Bantun, S., & Sari, J. Y. (2025). Designing an AI-Based Village Information System Using Research and Development Approach for Public Governance Modernization in Popalia Village. Jurnal Teknik Informatika (Jutif), 6(5), 5251–5269. https://doi.org/10.20884/1.jutif.2025.6.5.5257",
    "Aryfiyanto, H., & Alamsyah, A. (2024). Public service with generative AI: Exploring features and applications. In Proceedings of the 2024 7th International Conference of Computer and Informatics Engineering (IC2IE) (pp. 1–7). IEEE. https://doi.org/10.1109/IC2IE62602.2024.10708912",
    "Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the System Usability Scale. International Journal of Human-Computer Interaction, 24(6), 574–594. https://doi.org/10.1080/10447310802205776",
    "Brooke, J. (1996). SUS: A 'quick and dirty' usability scale. In P. W. Jordan, B. Thomas, B. A. Weerdmeester, & A. L. McClelland (Eds.), Usability Evaluation in Industry (pp. 189–194). Taylor & Francis.",
    "Chou, J. S., Chong, P. L., & Liu, C. Y. (2024). Deep learning-based chatbot by natural language processing for supportive risk management in river dredging projects. Engineering Applications of Artificial Intelligence, 131, 107744. https://doi.org/10.1016/j.engappai.2024.107744",
    "Dennis, A., Wixom, B. H., & Tegarden, D. (2020). Systems Analysis and Design: An Object-Oriented Approach with UML (6th ed.). John Wiley & Sons.",
    "Fowler, M. (2004). UML Distilled: A Brief Guide to the Standard Object Modeling Language (3rd ed.). Addison-Wesley Professional.",
    "IEEE Computer Society. (1998). IEEE Recommended Practice for Software Requirements Specifications (IEEE Std 830-1998). IEEE.",
    "Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W. T., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. In Advances in Neural Information Processing Systems (NeurIPS 2020) (Vol. 33, pp. 9459–9474).",
    "Myers, G. J., Sandler, C., & Badgett, T. (2011). The Art of Software Testing (3rd ed.). John Wiley & Sons.",
    "Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.",
    "Republik Indonesia. (2024). Undang-Undang Republik Indonesia Nomor 1 Tahun 2024 tentang Perubahan Kedua atas Undang-Undang Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik. Lembaran Negara RI Tahun 2024 Nomor 1. Sekretariat Negara.",
    "Smart, J. F. (2014). BDD in Action: Behavior-Driven Development for the Whole Software Lifecycle. Manning Publications.",
    "Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education."
]
