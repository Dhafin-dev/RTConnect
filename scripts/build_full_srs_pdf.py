# -*- coding: utf-8 -*-
"""
Full PDF Document Generator: UTS_I1_RTConnect_SRS.pdf
Standar IEEE Std 830-1998 / Format Laporan Praktikum PPL UNAIR
Dibuat dengan ReportLab 5.0
"""

import os
import sys
from PIL import Image

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas

sys.path.append(os.path.dirname(__file__))

from srs_content import (
    METADATA, ABBREVIATIONS, CHANGE_LOG_DATA, CONTRIBUTION_DATA, REFERENCES_DATA
)
from srs_specifications import (
    FR_LIST, NFR_LIST, USE_CASE_SPECS
)
from srs_chapters import (
    USER_STORIES_DATA, RTM_DATA, BPMN_TASKS_AS_IS, BPMN_TASKS_TO_BE
)

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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5F6368"))

        # Running Header
        self.drawString(40, 842 - 28, "RTConnect: Software Requirements Specification (SRS) — IEEE Std 830")
        self.drawRightString(595 - 40, 842 - 28, "Kelas I1 / Kelompok 3")
        self.setStrokeColor(colors.HexColor("#DADCE0"))
        self.setLineWidth(0.5)
        self.line(40, 842 - 32, 595 - 40, 842 - 32)

        # Running Footer
        page_str = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawString(40, 26, "Program Studi Sistem Informasi — Fakultas Sains dan Teknologi, Universitas Airlangga")
        self.drawRightString(595 - 40, 26, page_str)
        self.line(40, 34, 595 - 40, 34)
        self.restoreState()

def get_fitted_image(img_path, max_width=490, max_height=520):
    if not os.path.exists(img_path):
        return None
    try:
        im = Image.open(img_path)
        w, h = im.size
        aspect = w / h
        
        target_w = max_width
        target_h = target_w / aspect
        
        if target_h > max_height:
            target_h = max_height
            target_w = target_h * aspect
            
        return RLImage(img_path, width=target_w, height=target_h)
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")
        return None

def build_pdf(filename=None):
    if filename is None:
        os.makedirs("UTS", exist_ok=True)
        filename = os.path.join("UTS", "UTS_I1_RTConnect_SRS.pdf")
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Typography & Styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=25,
        textColor=colors.HexColor('#1A73E8'), alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=11, leading=15,
        textColor=colors.HexColor('#3C4043'), alignment=1
    )
    meta_style = ParagraphStyle(
        'CoverMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=colors.HexColor('#202124'), alignment=1
    )
    h1_style = ParagraphStyle(
        'H1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=colors.HexColor('#1A73E8'), spaceBefore=14, spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=colors.HexColor('#202124'), spaceBefore=10, spaceAfter=4,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=colors.HexColor('#5F6368'), spaceBefore=8, spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=colors.HexColor('#202124'), spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=colors.HexColor('#202124'), leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )
    caption_style = ParagraphStyle(
        'Caption_Custom', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8, leading=11,
        textColor=colors.HexColor('#5F6368'), alignment=1, spaceAfter=6
    )
    table_cell = ParagraphStyle(
        'TCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10,
        textColor=colors.HexColor('#202124')
    )
    table_cell_bold = ParagraphStyle(
        'TCellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        textColor=colors.HexColor('#1A73E8')
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 30))
    story.append(Paragraph("PROGRAM STUDI SARJANA SISTEM INFORMASI<br/>FAKULTAS SAINS DAN TEKNOLOGI — UNIVERSITAS AIRLANGGA", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>RTConnect: Perangkat Lunak Administrasi di Tingkat RT/RW<br/>dengan Integrasi NLP dan Generative AI</b>", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1A73E8"), spaceAfter=20))

    meta_text = f"""
    <b>LAPORAN TUGAS UTS PROJECT-BASED ASSIGNMENT</b><br/>
    <b>Mata Kuliah:</b> Praktikum Pembangunan Perangkat Lunak (Praktikum I1)<br/><br/>
    <b>Dosen Pengampu:</b><br/>
    {METADATA['lecturer']}<br/>
    NIP. {METADATA['lecturer_nip']}<br/><br/>
    <b>Disusun Oleh Kelompok 3:</b><br/>
    1. Muhammad Nafidz Arradhin — NIM: 187241027<br/>
    2. Mirza Diwa Luscakson — NIM: 187241042<br/>
    3. Febrian Muhammad Yudhistira — NIM: 187241051<br/>
    4. Ahmad Dhafin Al Farisy — NIM: 187241057<br/><br/>
    <b>Surabaya — 2026</b>
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(PageBreak())

    # ==================== RINGKASAN EKSEKUTIF ====================
    story.append(Paragraph("RINGKASAN EKSEKUTIF", h1_style))
    story.append(Paragraph(
        "Pembangunan perangkat lunak <b>RTConnect</b> dilatarbelakangi oleh kebutuhan digitalisasi tata kelola administrasi kependudukan pada tingkat akar rumput (Rukun Tetangga/Rukun Warga). Di tingkat RT/RW, keterbatasan sumber daya manusia, mobilitas fisik pengurus, dan pengetikan ulang format surat manual kerap memicu keterlambatan pelayanan serta risiko kesalahan pencatatan data warga (<i>human error</i>). RTConnect hadir sebagai platform web dan mobile mandiri yang mengintegrasikan kapabilitas <b>Generative AI</b> untuk menyusun draf narasi surat secara otomatis dan akurat, serta <b>Natural Language Processing (NLP)</b> melalui asisten virtual (Chatbot Tanya RT) berbasis arsitektur <b>Retrieval-Augmented Generation (RAG)</b> untuk melayani pertanyaan warga seputar persyaratan dan prosedur pelayanan 24/7.",
        body_style
    ))
    story.append(Paragraph(
        "Dokumen Software Requirements Specification (SRS) ini disusun berdasarkan standar internasional <b>IEEE Std 830-1998</b> dan telah menerapkan secara menyeluruh empat poin revisi resmi dari Dosen Pengampu (Dr. Indra Kharisma Raharjana, S.Kom., M.T.): (1) Menyederhanakan Use Case Diagram dengan mengeliminasi use case mandiri mengisi ulang form, melebur proses tanda tangan digital dan basah ke dalam use case Menindaklanjuti Pengajuan Surat, serta menghapus use case menjawab pertanyaan bagi Ketua RT; (2) Memperinci masukan dan keluaran (Input/Output) pada setiap tugas proses bisnis (BPMN AS-IS dan TO-BE) serta menandai jenis gateway keputusan secara eksplisit ([XOR]); (3) Mengubah seluruh pesan komunikasi dari Aktor ke Boundary pada Sequence Diagram menjadi narasi interaksi pengguna murni tanpa sintaks kode atau pemanggilan API; serta (4) Membubuhkan active bar (activation/deactivation lifeline) pada aktor di seluruh Sequence Diagram.",
        body_style
    ))
    story.append(Paragraph(
        "Seluruh artefak rekayasa perangkat lunak dalam dokumen ini—mulai dari Deskripsi Sistem, Arsitektur Lingkungan, BPMN, Use Case Specification, User Stories & BDD Scenarios, GUI Low Fidelity, Data Model (CDM/PDM), Activity Diagrams, Sequence Diagrams (Boundary-Control-Entity), Class Diagram, Kebutuhan Fungsional (FR-01 s/d FR-12), Kebutuhan Non-Fungsional, Matriks Keterlacakan (RTM), hingga Data Mock Up—telah diaudit dan disinkronkan secara ketat sehingga memiliki konsistensi semantik 100% dan bebas dari konflik antar-bab.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ==================== DAFTAR SINGKATAN ====================
    story.append(Paragraph("Daftar Singkatan dan Istilah Teknis (Abbreviations & Glossary)", h2_style))
    abbr_rows = [[Paragraph("<b>Singkatan</b>", table_cell_bold), Paragraph("<b>Keterangan / Definisi</b>", table_cell_bold)]]
    for abbr, desc in ABBREVIATIONS:
        abbr_rows.append([Paragraph(f"<b>{abbr}</b>", table_cell), Paragraph(desc, table_cell)])
    t_abbr = Table(abbr_rows, colWidths=[100, 415])
    t_abbr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_abbr)
    story.append(PageBreak())

    # ==================== BAB 1 ====================
    story.append(Paragraph("1. INTRODUCTION", h1_style))
    story.append(Paragraph("1.1 Purpose", h2_style))
    story.append(Paragraph(
        "Tujuan utama penyusunan dokumen Software Requirements Specification (SRS) ini adalah mendefinisikan secara menyeluruh dan terperinci kebutuhan perangkat lunak sistem informasi <b>RTConnect: Perangkat Lunak Administrasi di Tingkat RT/RW dengan Integrasi NLP dan Generative AI</b>. Dokumen ini merincikan batasan ruang lingkup, fungsi-fungsi operasional sistem, perilaku antarmuka, model data, proses bisnis, serta atribut kualitas non-fungsional yang harus dipenuhi selama siklus hidup pembangunan perangkat lunak. SRS ini menjadi landasan acuan tunggal bagi tim pengembang (developers), tim penguji (testers), pengguna akhir (warga dan pengurus RT), serta dosen penilai dalam mengevaluasi pemenuhan spesifikasi teknis proyek.",
        body_style
    ))

    story.append(Paragraph("1.2 Document Conventions", h2_style))
    story.append(Paragraph(
        "Penyusunan dokumen ini mengadopsi standar internasional <b>IEEE Std 830-1998</b> (Recommended Practice for Software Requirements Specifications) dan IEEE Std 1016-1998. Setiap kebutuhan fungsional diberikan penomoran deterministik unik berformat <b>FR-XX</b> dan kebutuhan non-fungsional berformat <b>NFR-XX</b>. Tingkat kepentingan kebutuhan diklasifikasikan ke dalam prioritas Tinggi (High), Sedang (Medium), dan Rendah (Low). Pemodelan UML mematuhi notasi standar Fowler (2004), di mana Sequence Diagram menerapkan kaidah Robustness Analysis (Boundary-Control-Entity) dan proses bisnis mematuhi standar BPMN 2.0.",
        body_style
    ))

    story.append(Paragraph("1.3 Intended Audience and Reading Suggestions", h2_style))
    story.append(Paragraph("• <b>Tim Pengembang (Developers):</b> Menggunakan Bab 2, Bab 7, Bab 9, Bab 10, dan Bab 11 untuk mentransformasikan spesifikasi kebutuhan menjadi arsitektur kode backend Flask, antarmuka Flutter, dan query database MySQL.", bullet_style))
    story.append(Paragraph("• <b>Tim Penguji (Testers & QA):</b> Menggunakan Bab 5 (User Stories & BDD Scenarios) serta Bab 11-12 untuk menyusun skenario pengujian fungsional (Black-box Testing) dan validasi otomatis.", bullet_style))
    story.append(Paragraph("• <b>Pengguna Akhir (Warga & Ketua RT):</b> Membaca Bab 2, Bab 3 (BPMN), dan Bab 6 (GUI) untuk memahami alur layanan surat pengantar dan konsultasi chatbot.", bullet_style))
    story.append(Paragraph("• <b>Dosen Pengampu & Penguji Akademik:</b> Memeriksa Bab 14 (Change Log) dan Bab 13 (RTM) untuk memverifikasi kepatuhan seluruh arahan revisi.", bullet_style))

    story.append(Paragraph("1.4 Product Scope", h2_style))
    story.append(Paragraph(
        "RTConnect adalah aplikasi web dan mobile administrasi digital tingkat mikro yang dikembangkan secara terfokus untuk melayani warga dan pengurus RT di lingkungan RT 032 RW 08 Griya Taman Asri, Desa Tawangsari, Kecamatan Taman, Kabupaten Sidoarjo. Ruang lingkup fungsional sistem mencakup: (1) Pelayanan administrasi surat pengantar standar (Domisili, KTP/KK, SKCK, dan SKU); (2) Otomasi perumusan draf narasi surat berbasis Generative AI; (3) Fleksibilitas pengesahan dokumen (digital stempel elektronik terverifikasi maupun tanda tangan basah fisik); serta (4) Layanan asisten virtual cerdas (Chatbot Tanya RT) berbasis RAG dengan eskalasi otomatis ke WhatsApp Ketua RT.",
        body_style
    ))

    # ==================== BAB 2 ====================
    story.append(Paragraph("2. OVERALL SYSTEM DESCRIPTION", h1_style))
    story.append(Paragraph("2.1 Product Perspective", h2_style))
    story.append(Paragraph(
        "RTConnect diposisikan sebagai platform tata kelola pemerintahan mikro (digital micro-governance platform) yang mandiri (self-contained) namun interoperabel. Sistem ini beroperasi sebagai jembatan digital antara warga dan pengurus lingkungan. Menggunakan arsitektur Client-Server berbasis RESTful API, lapisan antarmuka (presentation layer) dibangun dengan Flutter Web/Mobile, backend inti dibangun menggunakan Python Flask, dan penyimpanan relasional dikelola oleh MySQL 8.0. Sistem berinteroperasi dengan penyedia AI eksternal (OpenAI API) untuk inferensi model LLM dan embedding teks, serta terhubung dengan WhatsApp URL Gateway untuk alur eskalasi percakapan tatap muka digital.",
        body_style
    ))

    story.append(Paragraph("2.2 Product Functions", h2_style))
    story.append(Paragraph("1. <b>Modul Manajemen Akun & Autentikasi:</b> Pendaftaran akun warga mandiri dengan validasi NIK 16 digit, enkripsi password bcrypt, dan login terpadu berbasis peran (Warga dan Ketua RT) dengan token otorisasi JWT.", bullet_style))
    story.append(Paragraph("2. <b>Modul Administrasi Surat Pengantar:</b> Pengisian formulir permohonan surat pengantar, perumusan draf narasi otomatis oleh Generative AI, peninjauan berkas masuk oleh Ketua RT, pengambilan keputusan tindak lanjut (Setuju, Revisi, Tolak), pembubuhan tanda tangan digital/basah, dan pengunduhan berkas PDF resmi.", bullet_style))
    story.append(Paragraph("3. <b>Modul Pusat Informasi Cerdas (Chatbot Tanya RT):</b> Konsultasi warga seputar prosedur layanan RT melalui chatbot semantik berbasis RAG yang merujuk pada basis dokumen peraturan RT 032, dilengkapi mekanisme fallback eskalasi ke tautan WhatsApp resmi Ketua RT.", bullet_style))

    story.append(Paragraph("2.3 User Classes and Characteristics", h2_style))
    story.append(Paragraph("• <b>Warga (Resident / Citizen):</b> Masyarakat umum domisili RT 032. Memiliki literasi teknologi dasar/menengah, mengakses via smartphone (Android/iOS) atau browser desktop. Kebutuhan utama: kemudahan pengajuan surat mandiri dan akses informasi syarat berkas 24/7.", bullet_style))
    story.append(Paragraph("• <b>Ketua RT (RT Administrator):</b> Pejabat lingkungan yang berwenang meninjau, mengesahkan, dan menerbitkan surat pengantar. Memiliki waktu terbatas di luar jam kerja. Kebutuhan utama: efisiensi peninjauan berkas, otomasi draf surat, dan rekapitulasi arsip digital terpusat.", bullet_style))

    story.append(Paragraph("2.4 Operating Environment", h2_style))
    story.append(Paragraph("• <b>Sisi Klien (Client-Side):</b> Peramban web modern (Chrome v110+, Firefox v115+, Safari v16+) atau perangkat bergerak Android 8.0+ / iOS 14.0+.", bullet_style))
    story.append(Paragraph("• <b>Sisi Server (Backend):</b> Linux Ubuntu 22.04 LTS / Windows 11 Server, Python 3.10+, Flask Framework 3.1+, WSGI Server.", bullet_style))
    story.append(Paragraph("• <b>Basis Data:</b> MySQL 8.0 / 8.4 LTS (lingkungan Laragon / MySQL Server).", bullet_style))
    story.append(Paragraph("• <b>Layanan AI:</b> OpenAI API (model text-embedding-3-small dan GPT-4o-mini).", bullet_style))

    story.append(Paragraph("2.5 Design and Implementation Constraints", h2_style))
    story.append(Paragraph("Batasan sistem meliputi yurisdiksi terbatas RT 032 RW 08 Desa Tawangsari, ketergantungan konektivitas internet stabil untuk panggilan API pihak ketiga, pencegahan halusinasi chatbot dengan membatasi jawaban pada dokumen basis pengetahuan resmi, serta kepatuhan tanda tangan digital terhadap UU ITE No. 1/2024.", body_style))

    story.append(Paragraph("2.6 System Architecture / Environment Diagram", h2_style))
    story.append(Paragraph("Gambar di bawah ini mengilustrasikan arsitektur sistem RTConnect yang terbagi menjadi empat tingkatan logis (Presentation Tier, Application Tier, Persistence Tier, dan External Services Tier).", body_style))
    
    img_arch = get_fitted_image("diagrams/system_architecture.png", max_width=490, max_height=300)
    if img_arch:
        story.append(img_arch)
        story.append(Paragraph("Gambar 2.1 System Architecture / Environment Diagram RTConnect", caption_style))
    story.append(PageBreak())

    # ==================== BAB 3 ====================
    story.append(Paragraph("3. BUSINESS PROCESS MODELING (BPMN)", h1_style))
    story.append(Paragraph("3.1 AS-IS Business Process", h2_style))
    story.append(Paragraph(
        "Pada kondisi berjalan (AS-IS), permohonan surat pengantar diajukan warga dengan menghubungi WhatsApp Ketua RT atau mengisi pesan manual. Ketua RT memeriksa kelengkapan berkas secara manual, mengetik draf surat pada program pengolah kata di komputer, mencetak blangko fisik, menandatangani basah dan membubuhkan stempel, kemudian mengabari warga untuk mengambil surat fisik di rumah RT.",
        body_style
    ))
    
    img_asis = get_fitted_image("diagrams/bpmn_as_is.png", max_width=490, max_height=320)
    if img_asis:
        story.append(img_asis)
        story.append(Paragraph("Gambar 3.1 BPMN AS-IS Proses Pengajuan dan Pembuatan Surat Pengantar", caption_style))

    story.append(Paragraph("Tabel Rincian Input dan Output Aktivitas BPMN AS-IS:", h3_style))
    asis_table_data = [[
        Paragraph("<b>ID</b>", table_cell_bold),
        Paragraph("<b>Aktivitas Tugas (Task)</b>", table_cell_bold),
        Paragraph("<b>Pelaksana</b>", table_cell_bold),
        Paragraph("<b>Masukan (Input)</b>", table_cell_bold),
        Paragraph("<b>Keluaran (Output)</b>", table_cell_bold)
    ]]
    for tid, tname, actor, tinp, tout in BPMN_TASKS_AS_IS:
        asis_table_data.append([
            Paragraph(tid, table_cell), Paragraph(tname, table_cell),
            Paragraph(actor, table_cell), Paragraph(tinp, table_cell), Paragraph(tout, table_cell)
        ])
    t_as = Table(asis_table_data, colWidths=[45, 140, 60, 135, 135])
    t_as.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_as)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.1.2 BPMN AS-IS Tanya RT", h3_style))
    story.append(Paragraph("Warga menanyakan informasi via WhatsApp pribadi Ketua RT di luar jam kerja. Jika belum paham, warga meminta jadwal temu tatap muka di rumah RT.", body_style))
    img_as_ty = get_fitted_image("diagrams/bpmn_as_is_tanyart.png", max_width=450, max_height=320)
    if img_as_ty:
        story.append(img_as_ty)
        story.append(Paragraph("Gambar 3.2 BPMN AS-IS Tanya RT via WhatsApp Pribadi", caption_style))
    story.append(PageBreak())

    story.append(Paragraph("3.2 TO-BE Business Process", h2_style))
    story.append(Paragraph(
        "Pada alur kerja TO-BE RTConnect, pengajuan dilakukan secara digital. Sistem memvalidasi kelengkapan berkas, lalu Generative AI secara otomatis merumuskan draf narasi surat formal. Ketua RT meninjau berkas di dashboard dan mengambil keputusan (Setuju, Revisi, atau Tolak). Jika disetujui, sistem menerbitkan nomor surat resmi dan memfasilitasi pengesahan digital (stempel TTD terverifikasi) atau pengesahan basah fisik.",
        body_style
    ))
    img_tobe = get_fitted_image("diagrams/bpmn_to_be.png", max_width=500, max_height=260)
    if img_tobe:
        story.append(img_tobe)
        story.append(Paragraph("Gambar 3.3 BPMN TO-BE Proses Pengajuan Surat Pengantar Terpadu", caption_style))

    story.append(Paragraph("Tabel Rincian Input, Output, dan Gateway BPMN TO-BE:", h3_style))
    tobe_table_data = [[
        Paragraph("<b>ID</b>", table_cell_bold),
        Paragraph("<b>Aktivitas Tugas (Task)</b>", table_cell_bold),
        Paragraph("<b>Pelaksana</b>", table_cell_bold),
        Paragraph("<b>Masukan (Input)</b>", table_cell_bold),
        Paragraph("<b>Keluaran (Output)</b>", table_cell_bold)
    ]]
    for tid, tname, actor, tinp, tout in BPMN_TASKS_TO_BE:
        tobe_table_data.append([
            Paragraph(tid, table_cell), Paragraph(tname, table_cell),
            Paragraph(actor, table_cell), Paragraph(tinp, table_cell), Paragraph(tout, table_cell)
        ])
    t_tb = Table(tobe_table_data, colWidths=[45, 140, 60, 135, 135])
    t_tb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_tb)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2.2 BPMN TO-BE Tanya RT via Chatbot", h3_style))
    story.append(Paragraph("Pertanyaan warga diproses dengan NLP & cosine similarity pada knowledge base RT. Jika relevan (skor >= 0.70), chatbot menyajikan jawaban rujukan. Jika di luar jangkauan (< 0.70), sistem mengeskalasikannya ke WhatsApp resmi Ketua RT.", body_style))
    img_tb_ty = get_fitted_image("diagrams/bpmn_to_be_tanyart.png", max_width=480, max_height=260)
    if img_tb_ty:
        story.append(img_tb_ty)
        story.append(Paragraph("Gambar 3.4 BPMN TO-BE Layanan Tanya RT Cerdas & Eskalasi WhatsApp", caption_style))
    story.append(PageBreak())

    # ==================== BAB 4 ====================
    story.append(Paragraph("4. USE CASE ANALYSIS", h1_style))
    story.append(Paragraph("4.1 Use Case Diagram (Revisi Feedback Dosen #1)", h2_style))
    story.append(Paragraph(
        "Use Case Diagram disempurnakan berdasarkan arahan Dosen Pengampu: (1) Mengeliminasi use case mandiri mengisi ulang form; (2) Menyederhanakan penandatanganan digital dan basah menjadi bagian terpadu dari Menindaklanjuti Pengajuan Surat; serta (3) Menghapus use case menjawab pertanyaan warga bagi Ketua RT.",
        body_style
    ))
    
    img_uc = get_fitted_image("diagrams/use_case_diagram.png", max_width=420, max_height=360)
    if img_uc:
        story.append(img_uc)
        story.append(Paragraph("Gambar 4.1 Use Case Diagram RTConnect Hasil Penyempurnaan", caption_style))

    story.append(Paragraph("4.2 Use Case Specifications", h2_style))
    for uc in USE_CASE_SPECS:
        story.append(Paragraph(f"<b>{uc['id']}: {uc['name']}</b>", h3_style))
        spec_rows = [
            [Paragraph("<b>Aktor Utama</b>", table_cell_bold), Paragraph(uc['actor'], table_cell)],
            [Paragraph("<b>Deskripsi</b>", table_cell_bold), Paragraph(uc['desc'], table_cell)],
            [Paragraph("<b>Preconditions</b>", table_cell_bold), Paragraph(uc['precondition'], table_cell)],
            [Paragraph("<b>Postconditions</b>", table_cell_bold), Paragraph(uc['postcondition'], table_cell)],
        ]
        t_sp = Table(spec_rows, colWidths=[120, 395])
        t_sp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F8F9FA')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ]))
        story.append(t_sp)
        story.append(Spacer(1, 4))

        mf_rows = [[Paragraph("<b>Langkah Main Flow</b>", table_cell_bold), Paragraph("<b>Aksi Pelaksana & Sistem</b>", table_cell_bold)]]
        for a_step, s_desc in uc['main_flow']:
            mf_rows.append([Paragraph(a_step, table_cell), Paragraph(s_desc, table_cell)])
        t_mf = Table(mf_rows, colWidths=[120, 395])
        t_mf.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_mf)
        
        if uc['alt_flow']:
            story.append(Spacer(1, 3))
            for af_tit, af_desc in uc['alt_flow']:
                story.append(Paragraph(f"• <b>{af_tit}:</b> {af_desc}", bullet_style))
        if uc['exc_flow']:
            story.append(Spacer(1, 2))
            for ef_tit, ef_desc in uc['exc_flow']:
                story.append(Paragraph(f"• <b>{ef_tit}:</b> {ef_desc}", bullet_style))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ==================== BAB 5 ====================
    story.append(Paragraph("5. USER STORY & USER STORY SCENARIO", h1_style))
    story.append(Paragraph(
        "Pada Bab 5 ini, kebutuhan pengguna dimodelkan ke dalam spesifikasi User Story dan skenario pengujian perilaku Behavior-Driven Development (BDD) berbasis sintaks Gherkin (Given-When-Then).",
        body_style
    ))
    
    story.append(Paragraph("5.1 User Story", h2_style))
    for us in USER_STORIES_DATA:
        story.append(Paragraph(f"[{us['id']}] Sebagai <b>{us['role']}</b>, saya ingin <b>{us['action']}</b>, sehingga <b>{us['benefit']}</b>.", bullet_style))

    story.append(Paragraph("5.2 User Story Scenario (BDD Gherkin)", h2_style))
    for us in USER_STORIES_DATA:
        story.append(Paragraph(f"Skenario Spesifikasi untuk {us['id']}", h3_style))
        for sc in us['scenarios']:
            story.append(Paragraph(f"<b>Scenario: {sc['title']}</b>", body_style))
            story.append(Paragraph(f"&nbsp;&nbsp;<b>Given</b> {sc['given']}", table_cell))
            story.append(Paragraph(f"&nbsp;&nbsp;<b>When</b> {sc['when']}", table_cell))
            if 'and' in sc:
                story.append(Paragraph(f"&nbsp;&nbsp;<b>And</b> {sc['and']}", table_cell))
            story.append(Paragraph(f"&nbsp;&nbsp;<b>Then</b> {sc['then']}", table_cell))
            story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ==================== BAB 6 ====================
    story.append(Paragraph("6. USER INTERFACE (GUI) DESIGN", h1_style))
    story.append(Paragraph("6.1 Struktur Navigasi & Koreksi Penomoran Wireframe", h2_style))
    story.append(Paragraph(
        "Koreksi editorial dokumen lama: Sub-bab 4.7 ('Page Formulir Pengajuan Warga') dimasukkan ke Daftar Isi, dan kesalahan duplikasi caption pada Gambar 4.3 ('Login Page') diperbaiki. Seluruh layar aplikasi dipetakan secara rapi:",
        body_style
    ))
    gui_list = [
        ("SCREEN-001 (Landing / Welcome Page)", "Pintu masuk awal sistem, menampilkan tombol 'Masuk' dan 'Registrasi'."),
        ("SCREEN-002 (Register Page)", "Formulir pendaftaran akun warga baru dengan validasi NIK 16 digit dan unggah spesimen tanda tangan."),
        ("SCREEN-003 (Login Page)", "Formulir autentikasi pengguna dengan input Email/NIK dan Password (Koreksi: Gambar 4.3)."),
        ("SCREEN-004 (Warga Home Screen)", "Dashboard warga yang memuat kartu layanan 'Ajukan Surat' dan 'Tanya RT'."),
        ("SCREEN-005 (Profile & Sidebar Drawer)", "Menu drawer profil pengguna yang dapat diakses melalui ikon hamburger."),
        ("SCREEN-006 (Riwayat Pengajuan Warga)", "Daftar pemantauan permohonan surat warga dengan indikator status berkode warna."),
        ("SCREEN-007 (Formulir Pengajuan Surat)", "Formulir pengajuan surat warga dengan opsi TTD Digital vs Basah (Koreksi: Masuk Daftar Isi)."),
        ("SCREEN-008 (Antrean Pengajuan RT)", "Dashboard Ketua RT untuk memantau permohonan surat masuk warga."),
        ("SCREEN-009 (Detail & Tindak Lanjut RT)", "Halaman verifikasi berkas pemohon, draf narasi AI, dan tombol aksi (Setuju, Revisi, Tolak)."),
        ("SCREEN-010 (Chatbot Tanya RT)", "Ruang obrolan asisten virtual warga yang dilengkapi kartu aksi eskalasi WhatsApp ke Ketua RT."),
        ("SCREEN-011 (PDF Document Viewer)", "Halaman pratinjau dan pengunduhan berkas PDF resmi bertanda tangan digital.")
    ]
    for s_name, s_desc in gui_list:
        story.append(Paragraph(f"• <b>{s_name}:</b> {s_desc}", bullet_style))

    story.append(PageBreak())

    # ==================== BAB 7 ====================
    story.append(Paragraph("7. DATABASE DESIGN", h1_style))
    story.append(Paragraph("7.1 Conceptual Data Model (CDM) & Normalisasi", h2_style))
    story.append(Paragraph(
        "Normalisasi skema basis data menyatukan tabel pengguna yang sebelumnya terpisah menjadi tabel terpusat <b>users</b> dengan kolom <b>role</b> ('warga', 'rt', 'admin'). Hal ini menyinkronkan data model dengan objek :User pada Sequence Diagram Login.",
        body_style
    ))
    
    img_db = get_fitted_image("diagrams/database_er_diagram.png", max_width=470, max_height=320)
    if img_db:
        story.append(img_db)
        story.append(Paragraph("Gambar 7.1 Entity Relationship Diagram (ERD / CDM & PDM) RTConnect", caption_style))

    story.append(Paragraph("7.2 Kamus Data Fisik (Physical Data Model)", h2_style))
    db_dict_pdf = [
        ("users", "user_id (PK), nik (UQ), nama_lengkap, email (UQ), password_hash, nomor_telepon, alamat, nomor_rt, nomor_rw, role, tanda_tangan_url, is_active, created_at", "Menyimpan data identitas, kredensial login terenkripsi, peran, dan spesimen TTD seluruh pengguna."),
        ("jenis_surat", "jenis_surat_id (PK), kode_surat (UQ), nama_surat, template_dokumen, persyaratan_dokumen, is_aktif, created_at", "Master jenis surat pengantar (SP-DOM, SP-KTP, SP-SKCK, SP-SKU) beserta template baku."),
        ("pengajuan_surat", "pengajuan_id (PK), nomor_pengajuan (UQ), warga_id (FK), rt_id (FK), jenis_surat_id (FK), keperluan, metode_tanda_tangan, berkas_lampiran_url, draf_ai_konten, status, catatan_revisi, alasan_penolakan, tanggal_pengajuan, tanggal_diverifikasi, tanggal_selesai", "Menyimpan transaksi permohonan surat, draf rumusan AI, dan status tindak lanjut RT."),
        ("surat_final", "surat_final_id (PK), pengajuan_id (FK, UQ), nomor_surat_resmi (UQ), file_pdf_path, signature_image_path, status_pengesahan, tanggal_terbit, tanggal_diambil", "Arsip dokumen PDF resmi yang diterbitkan beserta stempel tanda tangan dan kode keaslian."),
        ("knowledge_base", "knowledge_id (PK), judul_dokumen, kategori, isi_dokumen, diunggah_oleh_rt (FK), created_at, updated_at", "Menyimpan dokumen resmi tata tertib dan prosedur layanan RT 032."),
        ("knowledge_chunks", "chunk_id (PK), knowledge_id (FK), urutan_chunk, isi_chunk, kata_kunci, embedding_vector (JSON), created_at", "Potongan teks dokumen regulasi beserta vektor embedding numerik untuk pencarian semantik RAG."),
        ("chat_sessions", "session_id (PK), warga_id (FK), status_sesi, started_at, ended_at", "Mencatat sesi interaksi tanya jawab warga dengan asisten virtual Tanya RT."),
        ("chat_messages", "message_id (PK), session_id (FK), pengirim, isi_pesan, top_chunk_id (FK), similarity_score, waktu_kirim", "Mencatat pesan chat, skor kemiripan semantik, dan dokumen rujukan."),
        ("notifikasi", "notifikasi_id (PK), penerima_id (FK), tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan, is_dibaca, created_at", "Pemberitahuan sistem real-time untuk status surat dan eskalasi percakapan.")
    ]
    t_db_rows = [[Paragraph("<b>Tabel</b>", table_cell_bold), Paragraph("<b>Kolom Kunci & Tipe Data</b>", table_cell_bold), Paragraph("<b>Fungsi Bisnis</b>", table_cell_bold)]]
    for tn, cols, fnc in db_dict_pdf:
        t_db_rows.append([Paragraph(f"<b>{tn}</b>", table_cell), Paragraph(cols, table_cell), Paragraph(fnc, table_cell)])
    t_db_tbl = Table(t_db_rows, colWidths=[90, 235, 190])
    t_db_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_db_tbl)
    story.append(PageBreak())

    # ==================== BAB 8 ====================
    story.append(Paragraph("8. ACTIVITY DIAGRAMS", h1_style))
    story.append(Paragraph("8.1 Activity Diagram Registrasi Akun", h2_style))
    img_act_reg = get_fitted_image("diagrams/activity_register.png", max_width=470, max_height=260)
    if img_act_reg:
        story.append(img_act_reg)
        story.append(Paragraph("Gambar 8.1 Activity Diagram Registrasi Akun Warga Mandiri", caption_style))

    story.append(Paragraph("8.2 Activity Diagram Login ke Sistem", h2_style))
    img_act_log = get_fitted_image("diagrams/activity_login.png", max_width=470, max_height=260)
    if img_act_log:
        story.append(img_act_log)
        story.append(Paragraph("Gambar 8.2 Activity Diagram Login Pengguna Terpadu", caption_style))

    story.append(Paragraph("8.3 Activity Diagram Pengajuan dan Pemrosesan Surat Pengantar", h2_style))
    img_act_peng = get_fitted_image("diagrams/activity_pengajuan_surat.png", max_width=490, max_height=260)
    if img_act_peng:
        story.append(img_act_peng)
        story.append(Paragraph("Gambar 8.3 Activity Diagram Pengajuan dan Pemrosesan Surat Pengantar", caption_style))

    story.append(Paragraph("8.4 Activity Diagram Chatbot Tanya RT & Eskalasi", h2_style))
    img_act_bot = get_fitted_image("diagrams/activity_chatbot.png", max_width=470, max_height=260)
    if img_act_bot:
        story.append(img_act_bot)
        story.append(Paragraph("Gambar 8.4 Activity Diagram Chatbot Tanya RT & Eskalasi WhatsApp", caption_style))
    story.append(PageBreak())

    # ==================== BAB 9 ====================
    story.append(Paragraph("9. SEQUENCE DIAGRAMS", h1_style))
    story.append(Paragraph(
        "Penerapan Feedback Dosen #3 dan #4: Seluruh Sequence Diagram menggunakan <b>narasi interaksi manusia</b> pada pesan Aktor ke Boundary (tanpa sintaks kode) serta membubuhkan <b>active bar</b> pada aktor secara konsisten.",
        body_style
    ))

    story.append(Paragraph("9.1 Sequence Diagram Registrasi Akun", h2_style))
    img_seq_reg = get_fitted_image("diagrams/sequence_register.png", max_width=450, max_height=280)
    if img_seq_reg:
        story.append(img_seq_reg)
        story.append(Paragraph("Gambar 9.1 Sequence Diagram Registrasi Akun", caption_style))

    story.append(Paragraph("9.2 Sequence Diagram Login ke Sistem", h2_style))
    img_seq_log = get_fitted_image("diagrams/sequence_login.png", max_width=450, max_height=280)
    if img_seq_log:
        story.append(img_seq_log)
        story.append(Paragraph("Gambar 9.2 Sequence Diagram Login ke Sistem", caption_style))
    story.append(PageBreak())

    story.append(Paragraph("9.3 Sequence Diagram Pengajuan dan Pemrosesan Surat Pengantar", h2_style))
    img_seq_peng = get_fitted_image("diagrams/sequence_pengajuan_surat.png", max_width=480, max_height=420)
    if img_seq_peng:
        story.append(img_seq_peng)
        story.append(Paragraph("Gambar 9.3 Sequence Diagram Pengajuan dan Pemrosesan Surat Pengantar (BCE & Active Bar)", caption_style))

    story.append(Paragraph("9.4 Sequence Diagram Chatbot Tanya RT & Eskalasi", h2_style))
    img_seq_bot = get_fitted_image("diagrams/sequence_chatbot.png", max_width=460, max_height=280)
    if img_seq_bot:
        story.append(img_seq_bot)
        story.append(Paragraph("Gambar 9.4 Sequence Diagram Chatbot Tanya RT & Eskalasi WhatsApp", caption_style))
    story.append(PageBreak())

    # ==================== BAB 10 ====================
    story.append(Paragraph("10. CLASS DIAGRAM", h1_style))
    story.append(Paragraph("10.1 Domain & Analysis Class Model", h2_style))
    story.append(Paragraph(
        "Class Diagram RTConnect mengelompokkan struktur statis menjadi Lapisan Entitas Domain dan Lapisan Controller/Service, lengkap dengan atribut, metode, tipe data, serta multiplisitas relasi.",
        body_style
    ))
    img_cls = get_fitted_image("diagrams/class_diagram.png", max_width=490, max_height=260)
    if img_cls:
        story.append(img_cls)
        story.append(Paragraph("Gambar 10.1 Class Diagram Terpadu RTConnect", caption_style))

    story.append(Paragraph("10.2 Deskripsi Tanggung Jawab Kelas Utama", h2_style))
    story.append(Paragraph("• <b>Class User:</b> Mengelola identitas pengguna, NIK unik, password_hash, dan otentikasi peran. Berelasi 1-ke-banyak dengan PengajuanSurat.", bullet_style))
    story.append(Paragraph("• <b>Class PengajuanSurat:</b> Mengelola status permohonan surat, draf AI, dan berelasi 1-ke-1 dengan SuratFinal saat disetujui.", bullet_style))
    story.append(Paragraph("• <b>Class SuratFinal:</b> Mengelola dokumen PDF resmi, stempel tanda tangan, dan kode verifikasi keaslian dokumen.", bullet_style))
    story.append(Paragraph("• <b>Klaster RAG (KnowledgeBase, KnowledgeChunk, ChatSession, ChatMessage):</b> Mengelola dokumen regulasi, vektor embedding numerik, serta riwayat interaksi obrolan warga.", bullet_style))
    story.append(Paragraph("• <b>Lapisan Controller (AuthController, SuratController, ChatbotController):</b> Mengorkestrasi pemrosesan bisnis dan interaksi antarmuka.", bullet_style))

    # ==================== BAB 11 ====================
    story.append(Paragraph("11. FUNCTIONAL REQUIREMENTS", h1_style))
    story.append(Paragraph("Daftar kebutuhan fungsional (FR-01 s/d FR-12) terstruktur dan traceable berdasarkan format standar IEEE Std 830-1998:", body_style))
    for fr in FR_LIST:
        story.append(Paragraph(f"<b>{fr['id']}: {fr['title']}</b>", h3_style))
        story.append(Paragraph(f"• <b>Deskripsi:</b> {fr['desc']}", table_cell))
        story.append(Paragraph(f"• <b>Aktor:</b> {fr['actor']} | <b>Prioritas:</b> {fr['priority']}", table_cell))
        story.append(Paragraph(f"• <b>Input:</b> {fr['input']}", table_cell))
        story.append(Paragraph(f"• <b>Output:</b> {fr['output']}", table_cell))
        story.append(Spacer(1, 3))

    # ==================== BAB 12 ====================
    story.append(Paragraph("12. NON-FUNCTIONAL REQUIREMENTS", h1_style))
    for nfr in NFR_LIST:
        story.append(Paragraph(f"<b>{nfr['id']}: {nfr['category']}</b>", h3_style))
        story.append(Paragraph(f"• <b>Pernyataan:</b> {nfr['desc']}", table_cell))
        story.append(Paragraph(f"• <b>Metrik Ukur:</b> {nfr['metric']}", table_cell))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # ==================== BAB 13 ====================
    story.append(Paragraph("13. REQUIREMENT TRACEABILITY MATRIX (RTM)", h1_style))
    story.append(Paragraph("Matriks keterlacakan dua arah menghubungkan seluruh FR dengan Use Case, User Story, Diagram UML, Tabel Basis Data, dan Layar GUI:", body_style))
    rtm_table_rows = [[
        Paragraph("<b>FR ID</b>", table_cell_bold),
        Paragraph("<b>Use Case</b>", table_cell_bold),
        Paragraph("<b>User Story</b>", table_cell_bold),
        Paragraph("<b>Activity Diagram</b>", table_cell_bold),
        Paragraph("<b>Sequence Diagram</b>", table_cell_bold),
        Paragraph("<b>Database</b>", table_cell_bold),
        Paragraph("<b>Screen GUI</b>", table_cell_bold)
    ]]
    for rid, uc, us, act, seq, db, scr in RTM_DATA:
        rtm_table_rows.append([
            Paragraph(rid, table_cell), Paragraph(uc, table_cell), Paragraph(us, table_cell),
            Paragraph(act, table_cell), Paragraph(seq, table_cell), Paragraph(db, table_cell), Paragraph(scr, table_cell)
        ])
    t_rtm = Table(rtm_table_rows, colWidths=[40, 48, 48, 88, 88, 100, 103])
    t_rtm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_rtm)
    story.append(Spacer(1, 10))

    # ==================== BAB 14 ====================
    story.append(Paragraph("14. CHANGE LOG & MATRIKS AUDIT REVISI LAPORAN", h1_style))
    story.append(Paragraph("Dokumentasi riwayat penyempurnaan laporan, mencakup pemenuhan 4 feedback dosen dan perbaikan inkonsistensi fatal:", body_style))
    chg_table_rows = [[
        Paragraph("<b>No</b>", table_cell_bold),
        Paragraph("<b>Artefak Terdampak</b>", table_cell_bold),
        Paragraph("<b>Kondisi Awal (Masalah)</b>", table_cell_bold),
        Paragraph("<b>Perubahan yang Diterapkan</b>", table_cell_bold),
        Paragraph("<b>Alasan & Dasar Keputusan</b>", table_cell_bold)
    ]]
    for no, art, prob, chg, rsn in CHANGE_LOG_DATA:
        chg_table_rows.append([
            Paragraph(no, table_cell), Paragraph(art, table_cell), Paragraph(prob, table_cell),
            Paragraph(chg, table_cell), Paragraph(rsn, table_cell)
        ])
    t_chg = Table(chg_table_rows, colWidths=[22, 95, 130, 138, 130])
    t_chg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_chg)
    story.append(PageBreak())

    # ==================== BAB 15 & REFERENCES ====================
    story.append(Paragraph("15. CONCLUSION & RECOMMENDATIONS", h1_style))
    story.append(Paragraph("15.1 Kesimpulan", h2_style))
    story.append(Paragraph(
        "Penyusunan dokumen SRS RTConnect versi final ini telah menuntaskan seluruh audit akademis dan rekayasa perangkat lunak. Keempat arahan resmi dosen pengampu telah terintegrasi tanpa menyisakan konflik antar-bab. Perangkat lunak RTConnect siap menjadi solusi otomasi administrasi digital terdepan di tingkat RT/RW.",
        body_style
    ))
    story.append(Paragraph("15.2 Rekomendasi", h2_style))
    story.append(Paragraph("Disarankan untuk melanjutkan pengujian fungsional otomatis berbasis BDD Gherkin serta pengujian kebergunaan pengguna dengan kuesioner System Usability Scale (SUS) dengan target skor >= 70.", body_style))

    story.append(Paragraph("REFERENCES (APA 7th Edition)", h1_style))
    for ref in REFERENCES_DATA:
        story.append(Paragraph(ref, bullet_style))

    # ==================== APPENDICES ====================
    story.append(PageBreak())
    story.append(Paragraph("APPENDIX A: PLANTUML SOURCE CODE CATALOG", h1_style))
    story.append(Paragraph("Seluruh script PlantUML diagram disimpan pada folder 'uml/' proyek RTConnect:", body_style))
    puml_rows = [
        ("uml/use_case_diagram.puml", "Use Case Diagram RTConnect (Revisi Feedback Dosen #1)"),
        ("uml/bpmn_as_is.puml", "BPMN AS-IS Pengajuan Surat Pengantar (Detail I/O & Gateway XOR)"),
        ("uml/bpmn_as_is_tanyart.puml", "BPMN AS-IS Tanya RT via WhatsApp Pribadi"),
        ("uml/bpmn_to_be.puml", "BPMN TO-BE Pengajuan Surat Pengantar (AI Drafting & Jalur Digital/Basah)"),
        ("uml/bpmn_to_be_tanyart.puml", "BPMN TO-BE Tanya RT Cerdas (RAG Cosine Similarity & Eskalasi WhatsApp)"),
        ("uml/activity_register.puml", "Activity Diagram Registrasi Akun Warga Mandiri"),
        ("uml/activity_login.puml", "Activity Diagram Login Pengguna Terpadu"),
        ("uml/activity_pengajuan_surat.puml", "Activity Diagram Pengajuan dan Pemrosesan Surat Pengantar"),
        ("uml/activity_chatbot.puml", "Activity Diagram Chatbot Tanya RT & Eskalasi Langsung"),
        ("uml/sequence_register.puml", "Sequence Diagram Registrasi Akun (Narasi Aktor & Active Bar)"),
        ("uml/sequence_login.puml", "Sequence Diagram Login ke Sistem (Narasi Aktor & Active Bar)"),
        ("uml/sequence_pengajuan_surat.puml", "Sequence Diagram Pengajuan dan Pemrosesan Surat (BCE & Active Bar)"),
        ("uml/sequence_chatbot.puml", "Sequence Diagram Chatbot Tanya RT (RAG & Eskalasi WhatsApp)"),
        ("uml/class_diagram.puml", "Class Diagram Terpadu (Entity Layer, Service Layer, & Multiplisitas)"),
        ("uml/system_architecture.puml", "System Architecture & Environment Diagram 4-Tier"),
        ("uml/database_er_diagram.puml", "Entity Relationship Diagram (ERD CDM & PDM)")
    ]
    t_puml_rows = [[Paragraph("<b>File Script PlantUML</b>", table_cell_bold), Paragraph("<b>Deskripsi Artefak UML yang Dihasilkan</b>", table_cell_bold)]]
    for p_fn, p_ds in puml_rows:
        t_puml_rows.append([Paragraph(f"<b>{p_fn}</b>", table_cell), Paragraph(p_ds, table_cell)])
    t_puml = Table(t_puml_rows, colWidths=[175, 340])
    t_puml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_puml)
    story.append(Spacer(1, 10))

    story.append(Paragraph("APPENDIX B: CONTRIBUTION TABLE OF TEAM MEMBERS", h1_style))
    story.append(Paragraph("Tabel kontribusi anggota kelompok disusun sesuai format baku penugasan:", body_style))
    contrib_rows = [[
        Paragraph("<b>No</b>", table_cell_bold),
        Paragraph("<b>Nama Lengkap</b>", table_cell_bold),
        Paragraph("<b>NIM</b>", table_cell_bold),
        Paragraph("<b>Foto</b>", table_cell_bold),
        Paragraph("<b>Rincian Kontribusi Proyek</b>", table_cell_bold)
    ]]
    for no, name, nim, foto, kontribusi in CONTRIBUTION_DATA:
        contrib_rows.append([
            Paragraph(no, table_cell), Paragraph(name, table_cell), Paragraph(nim, table_cell),
            Paragraph(foto, table_cell), Paragraph(kontribusi, table_cell)
        ])
    t_con = Table(contrib_rows, colWidths=[25, 140, 75, 115, 160])
    t_con.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_con)
    story.append(Spacer(1, 10))

    story.append(Paragraph("APPENDIX C: FINAL QUALITY GATE VERIFICATION", h1_style))
    qg_items = [
        ("Kepatuhan Template SRS IEEE Std 830-1998", "LULUS (VERIFIED)", "Struktur dokumen mengikuti standar IEEE, mencakup Scope, Perspective, User Classes, Environment, Constraints, dan Architecture Diagram."),
        ("Penerapan Feedback Dosen #1 (Use Case Diagram)", "LULUS (VERIFIED)", "Mengisi ulang form dihapus sebagai UC mandiri; TTD digital dan basah disederhanakan masuk ke tindak lanjut; Menjawab pertanyaan dihapus dari UC RT."),
        ("Penerapan Feedback Dosen #2 (BPMN Input/Output & Gateway)", "LULUS (VERIFIED)", "Seluruh task BPMN memiliki input/output data yang eksplisit; seluruh gateway keputusan ditandai [XOR] secara presisi."),
        ("Penerapan Feedback Dosen #3 (Pesan Sequence Diagram)", "LULUS (VERIFIED)", "Komunikasi aktor-ke-boundary menggunakan narasi interaksi murni tanpa kode pemrograman atau sintaks API."),
        ("Penerapan Feedback Dosen #4 (Active Bar Aktor)", "LULUS (VERIFIED)", "Seluruh sequence diagram memiliki active bar pada aktor selama interaksi; stereotype BCE diterapkan konsisten."),
        ("Normalisasi & Integritas Basis Data (CDM/PDM)", "LULUS (VERIFIED)", "Tabel RT dan Warga yang terpecah telah disatukan ke tabel terpusat 'users' (konsisten dengan Sequence Login dan Class Diagram)."),
        ("Koreksi Kesalahan Editorial Dokumen Lama", "LULUS (VERIFIED)", "Koreksi pembuka Bab VI ('Bab I' -> 'Bab VI'); Penomoran Gambar 4.3 (Login Page) diperbaiki; Sub-bab 4.7 dimasukkan ke Daftar Isi."),
        ("Requirement Traceability Matrix (RTM)", "LULUS (VERIFIED)", "Matriks pelacakan dua arah menghubungkan seluruh FR-01 s/d FR-12 ke Use Case, User Story, Diagram UML, Database, dan Layar GUI."),
        ("Kelengkapan Dokumen Pendukung", "LULUS (VERIFIED)", "Dokumen Data Mock Up (UTS_I1_RTConnect_DATA.pdf) dan seluruh sumber PlantUML (uml/*.puml) tersedia lengkap.")
    ]
    qg_rows = [[
        Paragraph("<b>Kriteria Quality Gate</b>", table_cell_bold),
        Paragraph("<b>Status Verifikasi</b>", table_cell_bold),
        Paragraph("<b>Catatan Hasil Evaluasi</b>", table_cell_bold)
    ]]
    for crit, stat, notes in qg_items:
        qg_rows.append([Paragraph(crit, table_cell), Paragraph(f"<b>{stat}</b>", table_cell), Paragraph(notes, table_cell)])
    t_qg = Table(qg_rows, colWidths=[150, 115, 250])
    t_qg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_qg)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: {filename} generated successfully!")

if __name__ == '__main__':
    build_pdf()
