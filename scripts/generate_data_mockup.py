# -*- coding: utf-8 -*-
"""
Script Generator PDF: UTS_I1_RTConnect_DATA.pdf
Dibuat untuk Praktikum Pembangunan Perangkat Lunak (Kelas I1)
Universitas Airlangga 2026
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip header and footer on cover page

        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#5F6368"))

        # Running Header
        self.drawString(54, 842 - 36, "RTConnect: Data Mock Up — UTS Praktikum PPL")
        self.drawRightString(595 - 54, 842 - 36, "Kelas I1 / Kelompok 3")
        self.setStrokeColor(colors.HexColor("#DADCE0"))
        self.setLineWidth(0.75)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)

        # Running Footer
        page_str = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawString(54, 36, "Program Studi Sistem Informasi — Fakultas Sains dan Teknologi, Universitas Airlangga")
        self.drawRightString(595 - 54, 36, page_str)
        self.line(54, 46, 595 - 54, 46)
        self.restoreState()

def build_pdf(filename=None):
    if filename is None:
        os.makedirs("UTS", exist_ok=True)
        filename = os.path.join("UTS", "UTS_I1_RTConnect_DATA.pdf")
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=28,
        textColor=colors.HexColor('#1A73E8'),
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#3C4043'),
        alignment=1
    )
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#202124'),
        alignment=1
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1A73E8'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#202124'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#202124'),
        spaceAfter=6
    )
    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#5F6368'),
        alignment=1,
        spaceAfter=6
    )
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#202124')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 40))
    story.append(Paragraph("DOKUMEN DATA MOCK UP SISTEM", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("RTConnect: Perangkat Lunak Administrasi Tingkat RT/RW<br/>dengan Integrasi NLP dan Generative AI", title_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Dataset Realistis Fiktif, Skenario Masukan Pengguna (Input), Keluaran Sistem (Output), dan Pemetaan Relasional Basis Data", subtitle_style))
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1A73E8"), spaceAfter=30))

    meta_text = """
    <b>Kelas Praktikum:</b> Praktikum I1<br/>
    <b>Mata Kuliah:</b> Praktikum Pembangunan Perangkat Lunak<br/>
    <b>Dosen Pengampu:</b> Dr. Indra Kharisma Raharjana, S.Kom., M.T. (NIP. 198110282006041003)<br/><br/>
    <b>Disusun Oleh Kelompok 3:</b><br/>
    1. Muhammad Nafidz Arradhin — NIM: 187241027<br/>
    2. Mirza Diwa Luscakson — NIM: 187241042<br/>
    3. Febrian Muhammad Yudhistira — NIM: 187241051<br/>
    4. Ahmad Dhafin Al Farisy — NIM: 187241057<br/><br/>
    <b>Program Studi Sarjana Sistem Informasi</b><br/>
    <b>Fakultas Sains dan Teknologi — Universitas Airlangga</b><br/>
    <b>Surabaya — 2026</b>
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(PageBreak())

    # ==================== BAB 1 ====================
    story.append(Paragraph("BAB 1: MASTER DATA & KONFIGURASI SISTEM", h1_style))
    story.append(Paragraph(
        "Dokumen ini menyajikan data mock up komprehensif yang dirancang secara spesifik untuk memverifikasi dan menguji alur kerja perangkat lunak <b>RTConnect</b> pada lingkungan rukun tetangga. Seluruh data identitas warga, nomor surat, pertanyaan chatbot, dan stempel tanda tangan adalah data simulasi fiktif yang konsisten dengan skema basis data MySQL 8.0, spesifikasi Graphical User Interface (GUI), skenario Use Case, BPMN, dan skenario BDD Gherkin.",
        body_style
    ))

    story.append(Paragraph("1.1 Data Profil Lingkungan RT/RW", h2_style))
    lingkungan_data = [
        [Paragraph("<b>Parameter</b>", table_cell_bold), Paragraph("<b>Nilai Konfigurasi</b>", table_cell_bold), Paragraph("<b>Deskripsi Kontekstual</b>", table_cell_bold)],
        [Paragraph("Nomor RT / RW", table_cell), Paragraph("RT 032 / RW 08", table_cell), Paragraph("Lingkungan pemukiman Griya Taman Asri", table_cell)],
        [Paragraph("Kelurahan / Desa", table_cell), Paragraph("Desa Tawangsari", table_cell), Paragraph("Wilayah administratif tingkat desa/kelurahan", table_cell)],
        [Paragraph("Kecamatan / Kabupaten", table_cell), Paragraph("Kecamatan Taman, Kab. Sidoarjo", table_cell), Paragraph("Provinsi Jawa Timur", table_cell)],
        [Paragraph("Format Nomor Surat", table_cell), Paragraph("470/{NO_URUT}/032.08/{BULAN_ROMAWI}/{TAHUN}", table_cell), Paragraph("Standar resmi penomoran surat pengantar kependudukan", table_cell)],
        [Paragraph("Threshold Relevansi RAG", table_cell), Paragraph("0.70 (Cosine Similarity)", table_cell), Paragraph("Ambang batas penentuan apakah chatbot menjawab atau eskalasi ke RT", table_cell)]
    ]
    t_ling = Table(lingkungan_data, colWidths=[130, 160, 197])
    t_ling.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ling)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.2 Master Data Pengguna (Users)", h2_style))
    users_data = [
        [Paragraph("<b>ID</b>", table_cell_bold), Paragraph("<b>NIK / Nama</b>", table_cell_bold), Paragraph("<b>Email / No. HP</b>", table_cell_bold), Paragraph("<b>Alamat Domisili</b>", table_cell_bold), Paragraph("<b>Role</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("3515081203650001<br/><b>Drs. Bambang Sutrisno</b>", table_cell), Paragraph("rt032.griya@gmail.com<br/>081234567890", table_cell), Paragraph("Jl. Griya Taman Asri Blok A-01", table_cell), Paragraph("<b>rt</b> (Ketua RT)", table_cell)],
        [Paragraph("2", table_cell), Paragraph("3515082005040003<br/><b>Ahmad Dhafin Al Farisy</b>", table_cell), Paragraph("dafin@gmail.com<br/>085711223344", table_cell), Paragraph("Jl. Griya Taman Asri Blok B-12", table_cell), Paragraph("<b>warga</b>", table_cell)],
        [Paragraph("3", table_cell), Paragraph("3515085507920002<br/><b>Siti Aminah, S.Pd.</b>", table_cell), Paragraph("siti.aminah@gmail.com<br/>081399887766", table_cell), Paragraph("Jl. Griya Taman Asri Blok C-05", table_cell), Paragraph("<b>warga</b>", table_cell)],
        [Paragraph("4", table_cell), Paragraph("3515080911880004<br/><b>Budi Santoso</b>", table_cell), Paragraph("budi.santoso@gmail.com<br/>082155667788", table_cell), Paragraph("Jl. Griya Taman Asri Blok D-18", table_cell), Paragraph("<b>warga</b>", table_cell)]
    ]
    t_users = Table(users_data, colWidths=[25, 125, 120, 137, 80])
    t_users.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_users)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.3 Master Jenis Surat Pengantar", h2_style))
    surat_data = [
        [Paragraph("<b>Kode</b>", table_cell_bold), Paragraph("<b>Nama Layanan Surat</b>", table_cell_bold), Paragraph("<b>Syarat Dokumen</b>", table_cell_bold), Paragraph("<b>Template Narasi Standar</b>", table_cell_bold)],
        [Paragraph("SP-DOM", table_cell), Paragraph("Surat Keterangan Domisili", table_cell), Paragraph("Foto KTP & Kartu Keluarga", table_cell), Paragraph("Menerangkan bahwa pemohon benar-benar warga yang bertempat tinggal di lingkungan RT 032...", table_cell)],
        [Paragraph("SP-KTP", table_cell), Paragraph("Surat Pengantar KTP / KK Baru", table_cell), Paragraph("Foto KK lama & Akta Kelahiran", table_cell), Paragraph("Menerangkan pengantar permohonan penerbitan KTP-el / perbaruan Kartu Keluarga ke Kantor Kelurahan...", table_cell)],
        [Paragraph("SP-SKCK", table_cell), Paragraph("Surat Pengantar SKCK", table_cell), Paragraph("Foto KTP, KK, & Pas Foto", table_cell), Paragraph("Menerangkan bahwa pemohon berkelakuan baik dan tidak pernah melanggar norma lingkungan RT 032...", table_cell)],
        [Paragraph("SP-SKU", table_cell), Paragraph("Surat Keterangan Usaha (SKU)", table_cell), Paragraph("Foto Usaha & KTP Pemohon", table_cell), Paragraph("Menerangkan bahwa pemohon memiliki unit usaha mandiri aktif di wilayah domisili RT 032...", table_cell)]
    ]
    t_surat = Table(surat_data, colWidths=[55, 125, 117, 190])
    t_surat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_surat)
    story.append(PageBreak())

    # ==================== BAB 2 ====================
    story.append(Paragraph("BAB 2: INPUT MOCK UP (MASUKAN PENGGUNA)", h1_style))
    story.append(Paragraph(
        "Bagian ini merepresentasikan seluruh masukan (input) dari pengguna yang disubmit ke antarmuka aplikasi RTConnect, mencakup registrasi akun warga, kredensial login, formulir pengajuan surat pengantar dengan berbagai skenario, serta pertanyaan percakapan pada fitur Chatbot Tanya RT.",
        body_style
    ))

    story.append(Paragraph("2.1 Input Registrasi Akun Warga Baru", h2_style))
    reg_mock = [
        [Paragraph("<b>Field Antarmuka (UI)</b>", table_cell_bold), Paragraph("<b>Tipe / Kontrol</b>", table_cell_bold), Paragraph("<b>Contoh Nilai Masukan (Input Mock)</b>", table_cell_bold)],
        [Paragraph("Nomor Induk Kependudukan (NIK)", table_cell), Paragraph("Text Field (Numeric, 16 Digits)", table_cell), Paragraph("3515082005040003", table_cell)],
        [Paragraph("Nama Lengkap", table_cell), Paragraph("Text Field (String)", table_cell), Paragraph("Ahmad Dhafin Al Farisy", table_cell)],
        [Paragraph("Alamat Domisili", table_cell), Paragraph("Text Field (Multilined)", table_cell), Paragraph("Griya Taman Asri Blok B-12, RT 032 RW 08", table_cell)],
        [Paragraph("Nomor Telepon / WhatsApp", table_cell), Paragraph("Text Field (Phone)", table_cell), Paragraph("085711223344", table_cell)],
        [Paragraph("Alamat Email", table_cell), Paragraph("Text Field (Email)", table_cell), Paragraph("dafin@gmail.com", table_cell)],
        [Paragraph("Kata Sandi & Konfirmasi", table_cell), Paragraph("Password Field", table_cell), Paragraph("•••••••••••• (Password123!)", table_cell)],
        [Paragraph("Unggahan Stempel Tanda Tangan", table_cell), Paragraph("File Upload (PNG/JPG < 2MB)", table_cell), Paragraph("ttd_dafin_specimen.png (Transparan 400x200 px)", table_cell)]
    ]
    t_reg = Table(reg_mock, colWidths=[150, 140, 197])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.2 Input Permohonan Pengajuan Surat (5 Kasus Skenario)", h2_style))
    pengajuan_mock = [
        [Paragraph("<b>No / ID</b>", table_cell_bold), Paragraph("<b>Pemohon / Jenis</b>", table_cell_bold), Paragraph("<b>Keperluan Surat</b>", table_cell_bold), Paragraph("<b>Metode TTD</b>", table_cell_bold), Paragraph("<b>Lampiran Berkas</b>", table_cell_bold), Paragraph("<b>Target Status</b>", table_cell_bold)],
        [Paragraph("SRT-001", table_cell), Paragraph("Ahmad Dhafin<br/>SP-DOM", table_cell), Paragraph("Persyaratan administrasi pembukaan rekening bank dan verifikasi domisili tinggal.", table_cell), Paragraph("<b>Digital</b> (Tempelan)", table_cell), Paragraph("ktp_dafin.pdf<br/>kk_dafin.pdf", table_cell), Paragraph("<b>Selesai</b><br/>(Terbit PDF)", table_cell)],
        [Paragraph("SRT-002", table_cell), Paragraph("Siti Aminah<br/>SP-KTP", table_cell), Paragraph("Pengurusan penggantian KTP-el rusak akibat fisik kartu patah.", table_cell), Paragraph("<b>Basah</b> (Fisik)", table_cell), Paragraph("ktp_rusak.jpg<br/>kk_siti.pdf", table_cell), Paragraph("<b>Siap Diambil</b><br/>(Ambil di RT)", table_cell)],
        [Paragraph("SRT-003", table_cell), Paragraph("Budi Santoso<br/>SP-SKU", table_cell), Paragraph("Pengajuan kredit usaha mikro (KUR) untuk usaha toko kelontong berkah.", table_cell), Paragraph("<b>Digital</b> (Tempelan)", table_cell), Paragraph("foto_toko_buram.jpg", table_cell), Paragraph("<b>Perlu Revisi</b><br/>(Foto buram)", table_cell)],
        [Paragraph("SRT-004", table_cell), Paragraph("Siti Aminah<br/>SP-SKCK", table_cell), Paragraph("Melamar pekerjaan di instansi BUMN perbankan.", table_cell), Paragraph("<b>Basah</b> (Fisik)", table_cell), Paragraph("ktp_siti.pdf", table_cell), Paragraph("<b>Ditolak</b><br/>(Iuran nunggak)", table_cell)],
        [Paragraph("SRT-005", table_cell), Paragraph("Ahmad Dhafin<br/>SP-DOM", table_cell), Paragraph("Kelengkapan berkas pendaftaran sertifikasi profesi kelembagaan.", table_cell), Paragraph("<b>Digital</b> (Tempelan)", table_cell), Paragraph("ktp_dafin.pdf", table_cell), Paragraph("<b>Diajukan</b><br/>(Draf AI Siap)", table_cell)]
    ]
    t_peng = Table(pengajuan_mock, colWidths=[50, 85, 142, 65, 80, 65])
    t_peng.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_peng)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.3 Input Pertanyaan Warga pada Chatbot Tanya RT", h2_style))
    chat_input_mock = [
        [Paragraph("<b>Kasus</b>", table_cell_bold), Paragraph("<b>Pertanyaan Warga (String Query)</b>", table_cell_bold), Paragraph("<b>Klasifikasi Intent</b>", table_cell_bold), Paragraph("<b>Ekspektasi Sistem</b>", table_cell_bold)],
        [
            Paragraph("<b>Kasus 1</b><br/>(In-Domain)", table_cell),
            Paragraph("\"Halo min, apa saja syarat untuk mengajukan surat keterangan domisili di RT 032?\"", table_cell),
            Paragraph("Inquiry: Syarat Dokumen Domisili", table_cell),
            Paragraph("Skor relevansi >= 0.70. Chatbot menjawab langsung menggunakan dokumen aturan RT 032.", table_cell)
        ],
        [
            Paragraph("<b>Kasus 2</b><br/>(In-Domain)", table_cell),
            Paragraph("\"Berapa iuran kebersihan dan keamanan bulanan warga RT 032 serta kapan batas pembayarannya?\"", table_cell),
            Paragraph("Inquiry: Iuran Warga & Jadwal", table_cell),
            Paragraph("Skor relevansi >= 0.70. Chatbot mengutip Peraturan Lingkungan RT 032 Pasal 5.", table_cell)
        ],
        [
            Paragraph("<b>Kasus 3</b><br/>(Out-of-Domain)", table_cell),
            Paragraph("\"Apakah balai RT atau lapangan warga bisa dipinjam untuk acara resepsi pernikahan tanggal 25 bulan depan?\"", table_cell),
            Paragraph("Special Inquiry: Peminjaman Fasilitas", table_cell),
            Paragraph("Skor relevansi < 0.70. Chatbot mengeskalasi dengan tautan WhatsApp langsung ke Ketua RT.", table_cell)
        ]
    ]
    t_cin = Table(chat_input_mock, colWidths=[65, 172, 110, 140])
    t_cin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cin)
    story.append(PageBreak())

    # ==================== BAB 3 ====================
    story.append(Paragraph("BAB 3: OUTPUT MOCK UP (KELUARAN SISTEM & AI)", h1_style))
    story.append(Paragraph(
        "Bab ini memaparkan bentuk nyata dari keluaran (output) perangkat lunak RTConnect, mencakup rumusan draf otomatis Generative AI, struktur visual dokumen surat pengantar final bertanda tangan digital resmi, keputusan peninjauan RT, notifikasi sistem, respons chatbot, dan tautan eskalasi WhatsApp.",
        body_style
    ))

    story.append(Paragraph("3.1 Rumusan Draf Narasi Dokumen Hasil Generative AI", h2_style))
    ai_box = """
    <b>[SYSTEM PROMPT]:</b> Anda adalah asisten sekretariat RT 032 RW 08 Griya Taman Asri. Formulasikan teks pengantar resmi berbahasa Indonesia baku berdasarkan data pemohon: {nama: 'Ahmad Dhafin Al Farisy', nik: '3515082005040003', alamat: 'Griya Taman Asri B-12', keperluan: 'Pembukaan rekening bank dan administrasi domisili'}.<br/><br/>
    <b>[GENERATIVE AI OUTPUT (draf_ai_konten)]:</b><br/>
    <i>\"Yang bertanda tangan di bawah ini, Ketua RT 032 RW 08 Desa Tawangsari, Kecamatan Taman, Kabupaten Sidoarjo, dengan ini menerangkan dengan sebenarnya bahwa:<br/>
    Nama Lengkap : Ahmad Dhafin Al Farisy<br/>
    NIK : 3515082005040003<br/>
    Tempat Tinggal : Griya Taman Asri Blok B-12, RT 032 RW 08, Desa Tawangsari<br/>
    Adalah benar-benar warga yang bertempat tinggal di lingkungan kami dan tercatat berkelakuan baik. Surat pengantar ini diterbitkan secara khusus sebagai persyaratan kelengkapan administrasi pembukaan rekening perbankan dan pencatatan domisili. Demikian surat pengantar ini dibuat untuk dapat dipergunakan sebagaimana mestinya.\"</i>
    """
    story.append(Table([[Paragraph(ai_box, table_cell)]], colWidths=[487], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FA')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1A73E8')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.2 Contoh Berkas Surat Pengantar Resmi Final (PDF Mock Up)", h2_style))
    surat_pdf_mock = """
    <div align="center">
    <b>PEMERINTAH KABUPATEN SIDOARJO — KECAMATAN TAMAN</b><br/>
    <b>RUKUN TETANGGA 032 RUKUN WARGA 08 GRIYA TAMAN ASRI</b><br/>
    <font size="7.5">Sekretariat: Balai Pertemuan RT 032, Desa Tawangsari, Taman, Sidoarjo, Kode Pos 61257</font><br/>
    ========================================================================================
    </div>
    <div align="center">
    <b><u>SURAT KETERANGAN PENGANTAR</u></b><br/>
    Nomor: 470/001/032.08/VII/2026
    </div><br/>
    Ketua Rukun Tetangga 032 Rukun Warga 08 Desa Tawangsari, Kecamatan Taman, Kabupaten Sidoarjo, menerangkan bahwa:<br/>
    &nbsp;&nbsp;1. Nama Lengkap &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: <b>Ahmad Dhafin Al Farisy</b><br/>
    &nbsp;&nbsp;2. NIK &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: 3515082005040003<br/>
    &nbsp;&nbsp;3. Tempat, Tgl Lahir &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: Sidoarjo, 20 Mei 2004<br/>
    &nbsp;&nbsp;4. Jenis Kelamin / Agama &nbsp;&nbsp;: Laki-laki / Islam<br/>
    &nbsp;&nbsp;5. Alamat Domisili &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: Griya Taman Asri Blok B-12, RT 032 RW 08<br/>
    &nbsp;&nbsp;6. Maksud / Keperluan &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: Persyaratan pembukaan rekening bank dan administrasi domisili.<br/><br/>
    Demikian Surat Pengantar ini dibuat dengan sebenarnya dan diberikan kepada yang bersangkutan untuk dipergunakan sebagaimana mestinya.<br/><br/>
    <table width="100%">
      <tr>
        <td width="55%">
          <font size="7"><i>Validasi Keaslian Dokumen Digital:</i><br/>
          Terverifikasi secara elektronik oleh RTConnect.<br/>
          Kode Verifikasi: <b>RTC-VERIF-2026-07-8891</b><br/>
          Status: <b>SAH / DIGITAL_VERIFIED</b></font>
        </td>
        <td width="45%" align="center">
          Tawangsari, 17 Juli 2026<br/>
          Ketua RT 032 RW 08<br/>
          <font color="#1A73E8"><b>[STEMPEL TTD DIGITAL RESMI]</b></font><br/>
          <b><u>Drs. Bambang Sutrisno</u></b>
        </td>
      </tr>
    </table>
    """
    story.append(Table([[Paragraph(surat_pdf_mock, table_cell)]], colWidths=[487], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#3C4043')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.3 Output Respons Chatbot Tanya RT & Eskalasi WhatsApp", h2_style))
    bot_out_data = [
        [Paragraph("<b>Skenario Query</b>", table_cell_bold), Paragraph("<b>Hasil Skor & Tindakan</b>", table_cell_bold), Paragraph("<b>Keluaran Respons Sistem (Output)</b>", table_cell_bold)],
        [
            Paragraph("Syarat Pembuatan Surat Domisili", table_cell),
            Paragraph("<b>Cosine Score: 0.94</b><br/>(>= 0.70)<br/><i>Dijawab oleh Chatbot</i>", table_cell),
            Paragraph("\"Halo! Untuk mengajukan Surat Keterangan Domisili di RT 032, persyaratannya adalah: (1) Foto e-KTP asli pemohon, dan (2) Foto Kartu Keluarga (KK). Anda dapat langsung mengklik menu 'Ajukan Surat' pada dashboard warga.\"<br/><font color='#1A73E8'><b>[Sumber: Peraturan Tata Tertib Warga RT 032 Bab 3 Pasal 4]</b></font>", table_cell)
        ],
        [
            Paragraph("Peminjaman Balai/Lapangan RT untuk Resepsi Pernikahan", table_cell),
            Paragraph("<b>Cosine Score: 0.38</b><br/>(< 0.70)<br/><i>Eskalasi ke WhatsApp RT</i>", table_cell),
            Paragraph("\"Mohon maaf, informasi mengenai peminjaman balai/lapangan warga untuk resepsi pernikahan belum tercantum pada basis data regulasi RT 032. Pertanyaan Anda telah kami rangkum untuk diteruskan langsung kepada Ketua RT.\"<br/><br/><b>Tombol Aksi UI:</b> [Hubungi Ketua RT via WhatsApp]<br/><b>Target URL:</b> <code>https://wa.me/6281234567890?text=Halo%20Pak%20RT,%20saya%20warga%20RT%20032%20ingin%20menanyakan:%20Peminjaman%20balai%20untuk%20resepsi%20pernikahan</code>", table_cell)
        ]
    ]
    t_bout = Table(bot_out_data, colWidths=[120, 110, 257])
    t_bout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_bout)
    story.append(PageBreak())

    # ==================== BAB 4 ====================
    story.append(Paragraph("BAB 4: TABULASI RELASIONAL DATA MOCK UP (DATABASE STATE)", h1_style))
    story.append(Paragraph(
        "Tabel-tabel di bawah ini menggambarkan snapshot relasional isi basis data MySQL (rtconnect_db) yang menyimpan seluruh data mock up di atas. Hal ini membuktikan bahwa rancangan basis data, model PDM, Class Diagram, dan alur use case terhubung secara presisi (*traceable*).",
        body_style
    ))

    story.append(Paragraph("4.1 Tabel 'pengajuan_surat'", h2_style))
    t_ps_data = [
        [Paragraph("<b>pengajuan_id</b>", table_cell_bold), Paragraph("<b>warga_id / jenis_id</b>", table_cell_bold), Paragraph("<b>keperluan</b>", table_cell_bold), Paragraph("<b>metode_ttd</b>", table_cell_bold), Paragraph("<b>status</b>", table_cell_bold), Paragraph("<b>catatan / alasan</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("2 / 1 (SP-DOM)", table_cell), Paragraph("Buka rekening tabungan", table_cell), Paragraph("digital", table_cell), Paragraph("<font color='#0D9488'><b>selesai</b></font>", table_cell), Paragraph("-", table_cell)],
        [Paragraph("2", table_cell), Paragraph("3 / 2 (SP-KTP)", table_cell), Paragraph("KTP patah/rusak", table_cell), Paragraph("basah", table_cell), Paragraph("<font color='#D97706'><b>siap_diambil</b></font>", table_cell), Paragraph("Fisik telah dicap RT", table_cell)],
        [Paragraph("3", table_cell), Paragraph("4 / 4 (SP-SKU)", table_cell), Paragraph("Pengajuan KUR Mikro", table_cell), Paragraph("digital", table_cell), Paragraph("<font color='#DC2626'><b>perlu_revisi</b></font>", table_cell), Paragraph("Foto tempat usaha buram, mohon upload ulang", table_cell)],
        [Paragraph("4", table_cell), Paragraph("3 / 3 (SP-SKCK)", table_cell), Paragraph("Lamaran BUMN", table_cell), Paragraph("basah", table_cell), Paragraph("<font color='#991B1B'><b>ditolak</b></font>", table_cell), Paragraph("Tunggakan iuran warga belum diselesaikan", table_cell)],
        [Paragraph("5", table_cell), Paragraph("2 / 1 (SP-DOM)", table_cell), Paragraph("Sertifikasi profesi", table_cell), Paragraph("digital", table_cell), Paragraph("<font color='#2563EB'><b>diajukan</b></font>", table_cell), Paragraph("Draf AI siap ditinjau RT", table_cell)]
    ]
    t_ps = Table(t_ps_data, colWidths=[65, 85, 115, 62, 70, 90])
    t_ps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ps)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.2 Tabel 'surat_final'", h2_style))
    t_sf_data = [
        [Paragraph("<b>surat_final_id</b>", table_cell_bold), Paragraph("<b>pengajuan_id</b>", table_cell_bold), Paragraph("<b>nomor_surat_resmi</b>", table_cell_bold), Paragraph("<b>file_pdf_path</b>", table_cell_bold), Paragraph("<b>status_pengesahan</b>", table_cell_bold), Paragraph("<b>tanggal_terbit</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("1", table_cell), Paragraph("470/001/032.08/VII/2026", table_cell), Paragraph("uploads/pdf/SP-DOM-001-DAFIN.pdf", table_cell), Paragraph("digital_sah", table_cell), Paragraph("2026-07-17 10:30:00", table_cell)],
        [Paragraph("2", table_cell), Paragraph("2", table_cell), Paragraph("470/002/032.08/VII/2026", table_cell), Paragraph("uploads/pdf/SP-KTP-002-SITI.pdf", table_cell), Paragraph("basah_selesai", table_cell), Paragraph("2026-07-17 11:15:00", table_cell)]
    ]
    t_sf = Table(t_sf_data, colWidths=[65, 65, 120, 127, 60, 50])
    t_sf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sf)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.3 Tabel 'notifikasi'", h2_style))
    t_notif_data = [
        [Paragraph("<b>ID</b>", table_cell_bold), Paragraph("<b>Penerima</b>", table_cell_bold), Paragraph("<b>Tipe Notifikasi</b>", table_cell_bold), Paragraph("<b>Judul & Pesan Notifikasi</b>", table_cell_bold), Paragraph("<b>Status Baca</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("Drs. Bambang (RT)", table_cell), Paragraph("pengajuan_baru", table_cell), Paragraph("<b>Pengajuan Surat Masuk:</b> Ahmad Dhafin mengajukan Surat Keterangan Domisili.", table_cell), Paragraph("Sudah Dibaca", table_cell)],
        [Paragraph("2", table_cell), Paragraph("Ahmad Dhafin", table_cell), Paragraph("surat_disetujui", table_cell), Paragraph("<b>Surat Selesai:</b> Surat Domisili Anda telah diterbitkan dengan stempel TTD digital resmi.", table_cell), Paragraph("Sudah Dibaca", table_cell)],
        [Paragraph("3", table_cell), Paragraph("Budi Santoso", table_cell), Paragraph("perlu_revisi", table_cell), Paragraph("<b>Permintaan Revisi:</b> Foto usaha buram. Silakan unggah ulang pada formulir revisi.", table_cell), Paragraph("Belum Dibaca", table_cell)],
        [Paragraph("4", table_cell), Paragraph("Siti Aminah", table_cell), Paragraph("surat_siap_diambil", table_cell), Paragraph("<b>Surat Fisik Siap:</b> Pengantar KTP bertanda tangan basah siap diambil di kediaman RT.", table_cell), Paragraph("Sudah Dibaca", table_cell)]
    ]
    t_notif = Table(t_notif_data, colWidths=[25, 95, 87, 215, 65])
    t_notif.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_notif)
    story.append(Spacer(1, 15))

    story.append(Paragraph("4.4 Pernyataan Konsistensi dan Integritas Data", h2_style))
    story.append(Paragraph(
        "Seluruh data mock up yang disajikan dalam dokumen ini telah melalui proses audit konsistensi silang (*cross-artifact consistency audit*). Atribut-atribut data masukan warga tepat bersesuaian dengan kolom tabel basis data (`schema.sql`), wireframe antarmuka pengguna (`screens.md`), parameter pesan sequence diagram (`sequence_*.puml`), dan kriteria penerimaan skenario BDD Gherkin. Tidak ditemukan adanya *orphan data* atau inkonsistensi terminologi di seluruh alur sistem RTConnect.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Document {filename} generated successfully!")

if __name__ == '__main__':
    build_pdf()
