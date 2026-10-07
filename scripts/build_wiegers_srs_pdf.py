# -*- coding: utf-8 -*-
"""
Builder Skrip PDF SRS RTConnect
Format: Karl E. Wiegers (1999) / IEEE Std 830-1998 Software Requirements Specification
Dibuat dengan ReportLab 5.0
Praktikum Pembangunan Perangkat Lunak (Praktikum I1) - Universitas Airlangga 2026
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
    METADATA as BASE_META, ABBREVIATIONS, CHANGE_LOG_DATA, CONTRIBUTION_DATA, REFERENCES_DATA
)
from srs_wiegers_content import (
    METADATA, REVISION_HISTORY, SYSTEM_FEATURES_DATA
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
        print(f"Total Pages Generated in PDF: {num_pages}")
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
        self.drawString(40, 842 - 28, "RTConnect: Software Requirements Specification (SRS) — Karl E. Wiegers / IEEE Std 830")
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
    candidate_paths = [
        img_path,
        os.path.join("UTS", img_path),
        os.path.join("UTS", "diagrams", os.path.basename(img_path)),
        os.path.join("diagrams", os.path.basename(img_path))
    ]
    real_path = None
    for p in candidate_paths:
        if os.path.exists(p):
            real_path = p
            break
            
    if not real_path:
        return None
        
    try:
        im = Image.open(real_path)
        w, h = im.size
        aspect = w / h
        
        target_w = max_width
        target_h = target_w / aspect
        
        if target_h > max_height:
            target_h = max_height
            target_w = target_h * aspect
            
        return RLImage(real_path, width=target_w, height=target_h)
    except Exception as e:
        print(f"Error loading image {real_path}: {e}")
        return None

def build_wiegers_srs_pdf(filename=None):
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

    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
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
        fontName='Helvetica-Bold', fontSize=13.5, leading=17,
        textColor=colors.HexColor('#1A73E8'), spaceBefore=14, spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=colors.HexColor('#202124'), spaceBefore=10, spaceAfter=4,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'H3_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
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
    story.append(Spacer(1, 35))
    story.append(Paragraph("PROGRAM STUDI SARJANA SISTEM INFORMASI<br/>FAKULTAS SAINS DAN TEKNOLOGI — UNIVERSITAS AIRLANGGA", subtitle_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Software Requirements Specification", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("for<br/><br/><b>RTConnect: Perangkat Lunak Administrasi di Tingkat RT/RW<br/>dengan Integrasi NLP dan Generative AI</b>", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"<b>Version {METADATA['version']}</b>", ParagraphStyle('Ver', parent=subtitle_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F9D58'))))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#1A73E8"), spaceAfter=20))

    meta_text = f"""
    <b>LAPORAN TUGAS UTS PROJECT-BASED ASSIGNMENT</b><br/>
    <b>Mata Kuliah:</b> Praktikum Pembangunan Perangkat Lunak (Praktikum I1)<br/><br/>
    <b>Dosen Pengampu:</b><br/>
    {METADATA['lecturer']}<br/>
    NIP. {METADATA['lecturer_nip']}<br/><br/>
    <b>Prepared by Kelompok 3 (Praktikum I1):</b><br/>
    1. Muhammad Nafidz Arradhin — NIM: 187241027<br/>
    2. Mirza Diwa Luscakson — NIM: 187241042<br/>
    3. Febrian Muhammad Yudhistira — NIM: 187241051<br/>
    4. Ahmad Dhafin Al Farisy — NIM: 187241057<br/><br/>
    <b>Date created: {METADATA['date_created']}</b>
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(PageBreak())

    # ==================== TABLE OF CONTENTS ====================
    story.append(Paragraph("Table of Contents", h1_style))
    toc_items = [
        ("Table of Contents", "ii"),
        ("Revision History", "iii"),
        ("1. Introduction", "1"),
        ("   1.1 Purpose", "1"),
        ("   1.2 Document Conventions", "1"),
        ("   1.3 Intended Audience and Reading Suggestions", "1"),
        ("   1.4 Product Scope", "2"),
        ("   1.5 References", "2"),
        ("2. Overall Description", "3"),
        ("   2.1 Product Perspective", "3"),
        ("   2.2 Product Functions", "3"),
        ("   2.3 User Classes and Characteristics", "4"),
        ("   2.4 Operating Environment", "4"),
        ("   2.5 Design and Implementation Constraints", "4"),
        ("   2.6 User Documentation", "5"),
        ("   2.7 Assumptions and Dependencies", "5"),
        ("3. External Interface Requirements", "6"),
        ("   3.1 User Interfaces", "6"),
        ("   3.2 Hardware Interfaces", "7"),
        ("   3.3 Software Interfaces", "7"),
        ("   3.4 Communications Interfaces", "7"),
        ("4. System Features", "8"),
        ("   4.1 Registrasi dan Autentikasi Pengguna Terpadu", "8"),
        ("   4.2 Pengajuan Permohonan Surat Pengantar Mandiri", "9"),
        ("   4.3 Formulasi Draf Narasi Surat Berbasis Generative AI", "9"),
        ("   4.4 Peninjauan dan Tindak Lanjut Pengajuan oleh Ketua RT", "10"),
        ("   4.5 Pengesahan Dokumen (Digital & Basah) serta Penerbitan Surat Resmi", "11"),
        ("   4.6 Layanan Asisten Cerdas Chatbot Tanya RT & Eskalasi WhatsApp", "12"),
        ("5. Other Nonfunctional Requirements", "13"),
        ("   5.1 Performance Requirements", "13"),
        ("   5.2 Safety Requirements", "13"),
        ("   5.3 Security Requirements", "14"),
        ("   5.4 Software Quality Attributes", "14"),
        ("   5.5 Business Rules", "14"),
        ("6. Other Requirements", "15"),
        ("   6.1 Database Requirements (CDM, PDM, & RAG Architecture)", "15"),
        ("   6.2 Legal & Regulatory Compliance", "16"),
        ("   6.3 Requirement Traceability Matrix (RTM)", "17"),
        ("Appendix A: Glossary", "18"),
        ("Appendix B: Analysis Models (UML & BPMN Artifacts)", "19"),
        ("   B.1 Business Process Models (BPMN AS-IS & TO-BE)", "19"),
        ("   B.2 Use Case Model & Specifications", "22"),
        ("   B.3 User Stories & BDD Scenarios", "25"),
        ("   B.4 Activity Diagrams", "26"),
        ("   B.5 Sequence Diagrams (Boundary-Control-Entity)", "27"),
        ("   B.6 Class Diagram", "29"),
        ("   B.7 Data Models (ERD / CDM & PDM)", "30"),
        ("   B.8 System Architecture & Deployment Diagram", "30"),
        ("Appendix C: To Be Determined (TBD) List", "31"),
        ("Appendix D: Team Member Contribution Table", "32")
    ]
    toc_table_data = []
    for item, pg in toc_items:
        is_sub = item.startswith("   ")
        f_style = table_cell_bold if not is_sub else table_cell
        toc_table_data.append([
            Paragraph(f"<b>{item}</b>" if not is_sub else item, f_style),
            Paragraph(pg, ParagraphStyle('RAlign', parent=table_cell, alignment=2))
        ])
    t_toc = Table(toc_table_data, colWidths=[435, 80])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor('#F1F3F4'))
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==================== REVISION HISTORY ====================
    story.append(Paragraph("Revision History", h1_style))
    story.append(Paragraph("Tabel riwayat perubahan formal spesifikasi kebutuhan perangkat lunak RTConnect:", body_style))
    
    rev_rows = [[
        Paragraph("<b>Name</b>", table_cell_bold),
        Paragraph("<b>Date</b>", table_cell_bold),
        Paragraph("<b>Reason For Changes</b>", table_cell_bold),
        Paragraph("<b>Version</b>", table_cell_bold)
    ]]
    for rev in REVISION_HISTORY:
        rev_rows.append([
            Paragraph(rev['name'], table_cell),
            Paragraph(rev['date'], table_cell),
            Paragraph(rev['reason'], table_cell),
            Paragraph(f"<b>{rev['version']}</b>", table_cell)
        ])
    t_rev = Table(rev_rows, colWidths=[120, 85, 245, 65])
    t_rev.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_rev)
    story.append(Spacer(1, 10))

    callout_p = Paragraph(
        "<b>Ringkasan 4 Poin Revisi Dosen Pengampu yang Diterapkan Penuh:</b><br/>"
        "1. <b>Use Case Diagram:</b> Mengeliminasi 'Mengisi Ulang Form' sebagai UC mandiri; Menyederhanakan proses tanda tangan (digital & basah) masuk ke 'Menindaklanjuti Pengajuan Surat'; Menghapus 'Menjawab Pertanyaan Warga' bagi RT (karena bukan fitur sistem untuk RT, melainkan alur eskalasi sistem chatbot).<br/>"
        "2. <b>BPMN AS-IS & TO-BE:</b> Memperinci data Input dan Output pada setiap aktivitas tugas (Task); Menandai seluruh gateway percabangan keputusan secara eksplisit sebagai [XOR] atau [OR].<br/>"
        "3. <b>Sequence Diagram:</b> Mengubah seluruh pesan komunikasi dari Aktor ke Boundary menjadi narasi bahasa manusia murni (tanpa kode atau method call).<br/>"
        "4. <b>Sequence Diagram:</b> Membubuhkan active bar (activation lifeline) pada seluruh aktor saat berinteraksi.",
        body_style
    )
    t_callout = Table([[callout_p]], colWidths=[515])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FA')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#1A73E8')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_callout)
    story.append(PageBreak())

    # ==================== 1. INTRODUCTION ====================
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph("1.1 Purpose", h2_style))
    story.append(Paragraph(
        "Dokumen Software Requirements Specification (SRS) ini merumuskan secara komprehensif seluruh spesifikasi kebutuhan fungsional, kebutuhan non-fungsional, karakteristik pengguna, antarmuka eksternal, batasan perancangan, dan arsitektur sistem informasi RTConnect versi 1.0 approved. Sistem ini dirancang untuk mendigitalkan birokrasi tata kelola rukun tetangga dan rukun warga di tingkat akar rumput dengan integrasi Natural Language Processing (NLP) dan Large Language Model (LLM). Dokumen ini menjadi pedoman tunggal (Single Source of Truth) bagi pengembang, penguji sistem, pengguna akhir, serta evaluator akademik.",
        body_style
    ))

    story.append(Paragraph("1.2 Document Conventions", h2_style))
    story.append(Paragraph(
        "Penyusunan dokumen ini mengadopsi struktur standar Karl E. Wiegers (1999) dan IEEE Std 830-1998. Konvensi tipografi dan penomoran yang digunakan mencakup:",
        body_style
    ))
    story.append(Paragraph("• <b>Tag Kebutuhan Fungsional:</b> Diberikan label deterministik berformat REQ-x (misalnya: REQ-1, REQ-2, dst.).", bullet_style))
    story.append(Paragraph("• <b>Tag Kebutuhan Non-Fungsional:</b> Dikelompokkan ke dalam NFR-01 s/d NFR-08.", bullet_style))
    story.append(Paragraph("• <b>Skema Prioritas Wiegers:</b> Dievaluasi berdasarkan 4 parameter relatif (Benefit, Penalty, Cost, dan Risk) dengan skala 1 sampai 9.", bullet_style))
    story.append(Paragraph("• <b>Konvensi Pemodelan Visual:</b> Menerapkan kaidah Robustness Analysis Boundary-Control-Entity (BCE) dengan narasi interaksi manusia pada batas sistem dan active bar pada aktor.", bullet_style))

    story.append(Paragraph("1.3 Intended Audience and Reading Suggestions", h2_style))
    story.append(Paragraph(
        "Dokumen ini ditujukan kepada pengembang (membaca Bagian 2, 4, 6.1, dan Appendix B untuk implementasi), tim penguji QA (membaca Bagian 4, 5, 6.3, dan Appendix B.3 untuk skenario uji), pengguna akhir (membaca Bagian 2, 3.1, dan Appendix B.1 untuk pemahaman alur), serta dosen penilai akademik.",
        body_style
    ))

    story.append(Paragraph("1.4 Product Scope", h2_style))
    story.append(Paragraph(
        "RTConnect adalah perangkat lunak administrasi mikro-pemerintahan yang dikembangkan secara presisi untuk wilayah RT 032 RW 08 Griya Taman Asri, Desa Tawangsari, Kecamatan Taman, Kabupaten Sidoarjo. Ruang lingkup produk mencakup: (1) Registrasi akun warga mandiri dengan validasi NIK 16 digit dan spesimen tanda tangan; (2) Pengajuan surat pengantar daring (Domisili, KTP/KK, SKCK, Usaha); (3) Formulasi draf narasi formal surat otomatis oleh Generative AI; (4) Peninjauan dan tindak lanjut keputusan oleh Ketua RT (Setuju, Revisi, Tolak); (5) Fleksibilitas pengesahan dokumen melalui jalur digital (stempel TTD elektronik) atau jalur basah (cetak fisik & cap stempel basah RT); serta (6) Layanan konsultasi asisten cerdas 24/7 (Chatbot Tanya RT) berbasis RAG dan eskalasi otomatis ke WhatsApp Ketua RT.",
        body_style
    ))

    story.append(Paragraph("1.5 References", h2_style))
    for ref in REFERENCES_DATA:
        story.append(Paragraph(f"• {ref}", bullet_style))

    story.append(Spacer(1, 8))

    # ==================== 2. OVERALL DESCRIPTION ====================
    story.append(Paragraph("2. Overall Description", h1_style))
    story.append(Paragraph("2.1 Product Perspective", h2_style))
    story.append(Paragraph(
        "RTConnect diposisikan sebagai platform digital micro-governance mandiri (self-contained) yang mengintegrasikan warga dengan aparatur lingkungan RT dalam satu ekosistem terpadu. Sistem menggunakan arsitektur 4-tier: Presentation Tier (Flutter Web/Mobile), Application Tier (Python Flask Framework 3.1+), Persistence Tier (MySQL 8.0 RDBMS), dan External Services Tier (OpenAI API LLM & WhatsApp URI Gateway).",
        body_style
    ))
    
    img_arch = get_fitted_image("diagrams/system_architecture.png", max_width=470, max_height=260)
    if img_arch:
        story.append(img_arch)
        story.append(Paragraph("Gambar 2.1 Arsitektur Sistem 4-Tier & Diagram Lingkungan RTConnect", caption_style))

    story.append(Paragraph("2.2 Product Functions", h2_style))
    story.append(Paragraph("• <b>F-01 Manajemen Akun:</b> Registrasi mandiri, validasi NIK 16 digit, enkripsi password bcrypt, otentikasi JWT.", bullet_style))
    story.append(Paragraph("• <b>F-02 Pengajuan Surat Mandiri:</b> Formulir pengajuan surat pengantar dengan biodata terisi otomatis dan opsi metode tanda tangan.", bullet_style))
    story.append(Paragraph("• <b>F-03 Formulasi Draf Narasi AI:</b> Penyusunan draf narasi surat resmi secara otomatis oleh LLM sesaat setelah pengajuan masuk.", bullet_style))
    story.append(Paragraph("• <b>F-04 Peninjauan & Tindak Lanjut RT:</b> Antrean permohonan, peninjauan berkas, dan pengambilan keputusan (Setuju, Revisi, Tolak).", bullet_style))
    story.append(Paragraph("• <b>F-05 Pengesahan Dokumen:</b> Pembubuhan stempel digital dan penerbitan PDF resmi, atau alur cetak tanda tangan basah fisik.", bullet_style))
    story.append(Paragraph("• <b>F-06 Chatbot Tanya RT & Eskalasi:</b> Tanya jawab mandiri berbasis RAG pada aturan RT dan eskalasi otomatis ke WhatsApp RT bila kemiripan < 0.70.", bullet_style))

    story.append(Paragraph("2.3 User Classes and Characteristics", h2_style))
    story.append(Paragraph("• <b>Warga (Resident):</b> Masyarakat umum RT 032. Kebutuhan: kemudahan pengajuan surat dari rumah dan akses informasi instan 24/7.", bullet_style))
    story.append(Paragraph("• <b>Ketua RT (RT Administrator):</b> Pejabat lingkungan berwenang. Kebutuhan: efisiensi peninjauan berkas, otomasi pengetikan draf surat, dan rekapitulasi arsip digital.", bullet_style))

    story.append(Paragraph("2.4 Operating Environment", h2_style))
    story.append(Paragraph("• <b>Client:</b> Peramban web modern (Chrome v110+, Firefox v115+, Safari v16+) atau gawai Android 8.0+ / iOS 14.0+.", bullet_style))
    story.append(Paragraph("• <b>Server:</b> Ubuntu Linux 22.04 LTS / Windows 11 Server, Python 3.10+, WSGI Gunicorn, Flask Framework 3.1+.", bullet_style))
    story.append(Paragraph("• <b>Database:</b> MySQL Server 8.0 / 8.4 LTS.", bullet_style))
    story.append(Paragraph("• <b>AI & External:</b> OpenAI API (text-embedding-3-small & GPT-4o-mini), WhatsApp Deep-link (wa.me).", bullet_style))

    story.append(Paragraph("2.5 Design and Implementation Constraints", h2_style))
    story.append(Paragraph("Batasan meliputi yurisdiksi administratif RT 032 RW 08 Desa Tawangsari Sidoarjo, ketergantungan kuota token API OpenAI, batasan pengetahuan AI yang strictly grounded pada dokumen RT, serta kepatuhan UU ITE No. 1 Tahun 2024.", body_style))

    story.append(Paragraph("2.6 User Documentation", h2_style))
    story.append(Paragraph("Dokumentasi yang disediakan meliputi Buku Panduan Pengguna Warga (PDF), Buku Petunjuk Teknis Operasional Ketua RT, dan Panduan Deployment Administrator.", body_style))

    story.append(Paragraph("2.7 Assumptions and Dependencies", h2_style))
    story.append(Paragraph("Diasumsikan setiap pemohon memiliki NIK 16 digit yang valid, Ketua RT memiliki nomor WhatsApp aktif, dan server memiliki koneksi internet outbound stabil.", body_style))

    story.append(PageBreak())

    # ==================== 3. EXTERNAL INTERFACE REQUIREMENTS ====================
    story.append(Paragraph("3. External Interface Requirements", h1_style))
    story.append(Paragraph("3.1 User Interfaces", h2_style))
    story.append(Paragraph(
        "Antarmuka pengguna RTConnect dibangun dengan Flutter menggunakan Material Design 3 yang responsif (desktop, tablet, mobile). Mengadopsi palet warna primer biru (#1A73E8), kartu putih bersih, tipografi Segoe UI / Roboto, dan kepatuhan WCAG 2.1 AA (rasio kontras >= 4.5:1 dan target sentuh >= 48dp).",
        body_style
    ))
    
    ui_rows = [[
        Paragraph("<b>ID Layar</b>", table_cell_bold),
        Paragraph("<b>Nama Antarmuka</b>", table_cell_bold),
        Paragraph("<b>Fungsi Operasional & Interaksi Pengguna</b>", table_cell_bold)
    ]]
    ui_screens = [
        ("SCREEN-001", "Landing / Welcome Page", "Halaman penyambutan publik yang menampilkan profil RT 032 dan tombol navigasi 'Masuk' serta 'Registrasi'."),
        ("SCREEN-002", "Halaman Registrasi Warga", "Formulir pendaftaran akun mandiri dengan isian NIK 16 digit, biodata, kata sandi, dan input unggah foto stempel tanda tangan."),
        ("SCREEN-003", "Halaman Login Terpadu", "Formulir autentikasi satu pintu bagi Warga dan Ketua RT dengan input Email/NIK dan Password."),
        ("SCREEN-004", "Dashboard Utama Warga", "Beranda akun warga yang menampilkan kartu aksi cepat 'Ajukan Surat Pengantar' dan 'Tanya RT via Chatbot'."),
        ("SCREEN-005", "Drawer Navigasi & Profil", "Menu bilah samping (drawer) untuk mengakses profil pengguna, pengaturan akun, dan tombol keluar (logout)."),
        ("SCREEN-006", "Riwayat Pengajuan Surat", "Daftar pemantauan permohonan surat warga lengkap dengan badge status berkode warna."),
        ("SCREEN-007", "Formulir Permohonan Surat", "Formulir pengajuan surat pengantar dengan biodata terisi otomatis, pilihan jenis surat, kolom keperluan, opsi metode tanda tangan (Digital/Basah), dan unggah lampiran."),
        ("SCREEN-008", "Formulir Pengisian Ulang Revisi", "Formulir perbaikan data bagi permohonan berstatus 'Perlu Revisi' yang menyajikan catatan koreksi dari Ketua RT."),
        ("SCREEN-009", "Dashboard Antrean RT", "Antrean kerja administratif Ketua RT yang menyajikan daftar permohonan masuk yang siap diperiksa."),
        ("SCREEN-010", "Detail & Tindak Lanjut RT", "Halaman telaah berkas pemohon, lampiran, draf narasi hasil AI, input nomor surat resmi, dan tombol aksi (Setujui, Minta Revisi, Tolak)."),
        ("SCREEN-011", "Antarmuka Chatbot Tanya RT", "Ruang percakapan cerdas yang menampilkan balon dialog, tombol rekomendasi pertanyaan FAQ, badge sumber regulasi, dan tombol eskalasi WhatsApp RT."),
        ("SCREEN-012", "Penampil Dokumen PDF Resmi", "Halaman pratinjau surat pengantar resmi bertanda tangan digital dengan tombol cetak dan unduh dokumen ke perangkat lokal.")
    ]
    for sid, sname, sdesc in ui_screens:
        ui_rows.append([Paragraph(f"<b>{sid}</b>", table_cell), Paragraph(sname, table_cell), Paragraph(sdesc, table_cell)])
    t_ui = Table(ui_rows, colWidths=[80, 150, 285])
    t_ui.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_ui)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Hardware Interfaces", h2_style))
    story.append(Paragraph("• <b>Perangkat Klien:</b> Smartphone (Android 8.0+ / iOS 14.0+) atau PC/Laptop layar minimal 360x640 hingga 1920x1080 px, RAM minimal 2GB.", bullet_style))
    story.append(Paragraph("• <b>Perangkat Server:</b> vCPU minimal 2 Cores, RAM 4GB (rekomendasi 8GB), media penyimpanan SSD 20GB+, koneksi internet 100 Mbps.", bullet_style))

    story.append(Paragraph("3.3 Software Interfaces", h2_style))
    story.append(Paragraph("• <b>Python Flask Backend:</b> RESTful JSON API untuk autentikasi, transaksi permohonan, dan orkestrasi AI.", bullet_style))
    story.append(Paragraph("• <b>MySQL Server 8.0:</b> Manajemen basis data relasional terpusat.", bullet_style))
    story.append(Paragraph("• <b>OpenAI API:</b> text-embedding-3-small (1536 dim) dan GPT-4o-mini untuk inferensi narasi formal dan RAG.", bullet_style))
    story.append(Paragraph("• <b>WhatsApp Gateway:</b> Skema URI wa.me untuk pengalihan eskalasi percakapan otomatis.", bullet_style))

    story.append(Paragraph("3.4 Communications Interfaces", h2_style))
    story.append(Paragraph(
        "Lalu lintas data menggunakan protokol HTTPS/TLS 1.3 terenkripsi. Komunikasi API berbasis JSON dengan Bearer JWT token. Protokol eskalasi eksternal memanfaatkan tautan URI scheme https://wa.me/{phone}?text={encoded_message}.",
        body_style
    ))

    story.append(PageBreak())

    # ==================== 4. SYSTEM FEATURES ====================
    story.append(Paragraph("4. System Features", h1_style))
    story.append(Paragraph("Spesifikasi rinci enam fitur sistem utama menggunakan format baku Karl E. Wiegers (Deskripsi & Rating Prioritas, Stimulus/Respons, dan Kebutuhan Fungsional REQ-x):", body_style))

    for feat in SYSTEM_FEATURES_DATA:
        story.append(Paragraph(f"{feat['num']} {feat['name']}", h2_style))
        story.append(Paragraph(f"{feat['num']}.1 Description and Priority", h3_style))
        story.append(Paragraph(feat['desc'], body_style))
        story.append(Paragraph(f"<b>Tingkat Prioritas (Wiegers Rating):</b> {feat['priority']}", body_style))
        
        story.append(Paragraph(f"{feat['num']}.2 Stimulus/Response Sequences", h3_style))
        sr_rows = [[
            Paragraph("<b>No</b>", table_cell_bold),
            Paragraph("<b>Stimulus (Aksi Pengguna / Kejadian)</b>", table_cell_bold),
            Paragraph("<b>Respons Sistem (Perilaku Perangkat Lunak)</b>", table_cell_bold)
        ]]
        for sno, stim, resp in feat['stimulus_response']:
            sr_rows.append([Paragraph(sno, table_cell), Paragraph(stim, table_cell), Paragraph(resp, table_cell)])
        t_sr = Table(sr_rows, colWidths=[25, 230, 260])
        t_sr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3)
        ]))
        story.append(t_sr)
        
        story.append(Paragraph(f"{feat['num']}.3 Functional Requirements", h3_style))
        for req_id, req_stmt in feat['reqs']:
            story.append(Paragraph(f"• <b>{req_id}:</b> {req_stmt}", bullet_style))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ==================== 5. OTHER NONFUNCTIONAL REQUIREMENTS ====================
    story.append(Paragraph("5. Other Nonfunctional Requirements", h1_style))
    story.append(Paragraph("5.1 Performance Requirements", h2_style))
    story.append(Paragraph("• <b>Waktu Tanggap UI/API:</b> Latensi pemuatan antarmuka dan API tidak melebihi 2.0 detik pada jaringan minimal 5 Mbps.", bullet_style))
    story.append(Paragraph("• <b>Waktu Komputasi AI:</b> Formulasi draf narasi oleh LLM dan pencarian semantik RAG tidak melebihi 5.0 detik.", bullet_style))
    story.append(Paragraph("• <b>Kapasitas Beban Bersamaan:</b> Mampu melayani hingga 50 pengguna aktif bersamaan tanpa degradasi performa lebih dari 10%.", bullet_style))

    story.append(Paragraph("5.2 Safety Requirements", h2_style))
    story.append(Paragraph("• <b>Atomisitas Transaksi Basis Data:</b> Pembaruan status dan penerbitan nomor surat dibungkus transaksi ACID guna mencegah inkonsistensi data.", bullet_style))
    story.append(Paragraph("• <b>Pencadangan Data:</b> Basis data dicadangkan otomatis setiap 24 jam sekali ke penyimpanan terisolasi.", bullet_style))

    story.append(Paragraph("5.3 Security Requirements", h2_style))
    story.append(Paragraph("• <b>Proteksi Kata Sandi:</b> Hash menggunakan bcrypt work factor minimal 10 sebelum disimpan. Dilarang menyimpan password teks polos.", bullet_style))
    story.append(Paragraph("• <b>Manajemen Sesi JWT:</b> Token sesi HS256 bertanda tangan digital dengan masa kedaluwarsa maksimal 24 jam.", bullet_style))
    story.append(Paragraph("• <b>Otorisasi & Sanitasi:</b> Role-Based Access Control pada setiap rute API dan sanitasi input untuk mencegah SQL Injection & XSS.", bullet_style))

    story.append(Paragraph("5.4 Software Quality Attributes", h2_style))
    story.append(Paragraph("• <b>Usability:</b> Target skor System Usability Scale (SUS) minimal 70 (kategori Good/Acceptable) dan kepatuhan WCAG 2.1 AA.", bullet_style))
    story.append(Paragraph("• <b>Availability:</b> Tingkat ketersediaan operasional minimal 99.0% per bulan di luar maintenance terencana.", bullet_style))
    story.append(Paragraph("• <b>Maintainability:</b> Kepatuhan PEP-8 Python dan struktur MVC / Clean Architecture.", bullet_style))

    story.append(Paragraph("5.5 Business Rules", h2_style))
    story.append(Paragraph("• <b>BR-01 Kelayakan Pemohon:</b> Hanya warga berdomisili sah di RT 032 RW 08 yang berhak mengajukan surat.", bullet_style))
    story.append(Paragraph("• <b>BR-02 Format Nomor Surat:</b> Format baku '470/{NO}/032.08/{BULAN}/{TAHUN}'. Nomor tidak terbit sebelum pengajuan disetujui.", bullet_style))
    story.append(Paragraph("• <b>BR-03 Alasan Penolakan/Revisi Wajib:</b> Ketua RT wajib mengisi alasan tertulis jika memilih tolak atau minta revisi.", bullet_style))
    story.append(Paragraph("• <b>BR-04 Zero Hallucination Policy:</b> Threshold cosine similarity chatbot ditetapkan 0.70. Di bawah angka tersebut, chatbot dilarang mengarang jawaban dan wajib mengaktifkan tautan eskalasi WhatsApp Ketua RT.", bullet_style))

    story.append(PageBreak())

    # ==================== 6. OTHER REQUIREMENTS ====================
    story.append(Paragraph("6. Other Requirements", h1_style))
    story.append(Paragraph("6.1 Database Requirements (CDM, PDM, & RAG Architecture)", h2_style))
    story.append(Paragraph(
        "Perancangan basis data RTConnect memisahkan secara tegas Conceptual Data Model (CDM) yang menggambarkan entitas bisnis dengan Physical Data Model (PDM) pada MySQL 8.0. Normalisasi skema telah menyatukan tabel pengguna yang terpecah menjadi tabel terpusat 'users' dengan kolom pembeda 'role'.",
        body_style
    ))
    
    db_rows = [[
        Paragraph("<b>Nama Tabel</b>", table_cell_bold),
        Paragraph("<b>Kolom Kunci & Atribut Utama</b>", table_cell_bold),
        Paragraph("<b>Fungsi Bisnis & Relasi Entitas</b>", table_cell_bold)
    ]]
    db_dict = [
        ("users", "user_id (PK), nik (UQ), nama_lengkap, email (UQ), password_hash, nomor_telepon, alamat, nomor_rt, nomor_rw, role, tanda_tangan_url, pin_otorisasi, is_active, created_at", "Menyimpan data akun terpusat warga dan Ketua RT, kredensial terenkripsi bcrypt, spesimen tanda tangan, dan hak akses."),
        ("jenis_surat", "jenis_surat_id (PK), kode_surat (UQ), nama_surat, template_dokumen, persyaratan_dokumen, is_aktif, created_at", "Menyimpan master jenis surat pengantar (Domisili, KTP, SKCK, Usaha), template draf baku, dan syarat lampiran."),
        ("pengajuan_surat", "pengajuan_id (PK), nomor_pengajuan (UQ), warga_id (FK), rt_id (FK), jenis_surat_id (FK), keperluan, metode_tanda_tangan, berkas_lampiran_url, draf_ai_konten, status, catatan_revisi, alasan_penolakan, tanggal_pengajuan, tanggal_diverifikasi, tanggal_selesai", "Menyimpan transaksi permohonan surat warga, draf rumusan narasi AI, status keputusan RT, dan berkas lampiran."),
        ("surat_final", "surat_final_id (PK), pengajuan_id (FK, UQ), nomor_surat_resmi (UQ), file_pdf_path, signature_image_path, verification_hash, status_pengesahan, tanggal_terbit, tanggal_diambil", "Menyimpan arsip dokumen PDF resmi yang telah disahkan digital (stempel gambar) atau basah, beserta hash verifikasi integritas."),
        ("knowledge_base", "knowledge_id (PK), judul_dokumen, kategori, isi_dokumen, file_markdown_path, diunggah_oleh_rt (FK), created_at, updated_at", "Menyimpan metadata dan isi lengkap dokumen regulasi resmi RT 032 yang berakar dari berkas Markdown master."),
        ("knowledge_chunks", "chunk_id (PK), knowledge_id (FK), urutan_chunk, isi_chunk, kata_kunci, embedding_vector (JSON), created_at", "Menyimpan potongan teks dokumen regulasi (chunk 300-500 token) beserta representasi vektor numerik 1536 dimensi untuk RAG."),
        ("chat_sessions", "session_id (PK), warga_id (FK), status_sesi, started_at, ended_at", "Mencatat sesi percakapan warga dengan asisten cerdas Tanya RT."),
        ("chat_messages", "message_id (PK), session_id (FK), pengirim, isi_pesan, top_chunk_id (FK), similarity_score, waktu_kirim", "Mencatat setiap pesan obrolan, skor kemiripan semantik (cosine similarity), dan rujukan dokumen aturan."),
        ("notifikasi", "notifikasi_id (PK), penerima_id (FK), tipe_notifikasi, judul, pesan_notifikasi, tautan_tujuan, is_dibaca, created_at", "Menyimpan notifikasi real-time untuk pembaruan status surat dan instruksi tindak lanjut.")
    ]
    for tname, cols, func in db_dict:
        db_rows.append([Paragraph(f"<b>{tname}</b>", table_cell), Paragraph(cols, table_cell), Paragraph(func, table_cell)])
    t_db = Table(db_rows, colWidths=[80, 235, 200])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_db)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Pembedaan Arsitektural: Knowledge Base (Markdown) vs Knowledge Chunk (Database RAG)", h3_style))
    story.append(Paragraph(
        "<b>1. Knowledge Base Makro (Berkas Markdown Master):</b> Berkas dokumentasi Markdown (.md) tersimpan di direktori repositori (misal: /docs/knowledge_base/ atau RTConnect-KnowledgeBase/). Berkas ini memuat teks lengkap peraturan RT 032, keputusan musyawarah warga, SOP pengurusan surat, dan tata tertib lingkungan. Berkas Markdown ini menjadi sumber kebenaran tunggal (Single Source of Truth) yang mudah dibaca, disunting, dan dikontrol versinya (git version control) oleh pengurus RT atau pengembang tanpa harus mengubah kode sistem.<br/><br/>"
        "<b>2. Knowledge Chunk Mikro (Tabel Basis Data RAG):</b> Segmen-segmen teks kecil berukuran 300-500 token dengan overlap 50 token yang dihasilkan melalui skrip pra-pemrosesan teks. Setiap potongan dihitung representasi vektor embedding-nya menggunakan model text-embedding-3-small (1536 dimensi) dan disimpan ke tabel 'knowledge_chunks' di MySQL. Data inilah yang digunakan secara real-time oleh mesin pencarian kosinus saat warga bertanya pada Chatbot Tanya RT.<br/><br/>"
        "<b>Data yang Wajib Diketahui Model LLM pada Kedua Fitur AI:</b><br/>"
        "• <b>Fitur Formulasi Draf Dokumen Surat:</b> (a) Data Pemohon Dinamis: Nama lengkap, NIK 16 digit, alamat domisili, tempat/tanggal lahir, pekerjaan, dan maksud keperluan surat; (b) Grounding Template Resmi: Kop surat resmi RT 032 RW 08, format nomor surat klasifikasi 470, konsiderans pengantar baku, dan klausul penutup administratif; (c) Parameter Kontrol: Temperature diatur rendah (0.2 - 0.3) agar hasil draf konsisten, formal, dan deterministik.<br/>"
        "• <b>Fitur Chatbot Tanya RT:</b> (a) Konteks Pertanyaan Warga: Teks query warga dan riwayat obrolan sesi aktif; (b) Potongan Chunk Terpilih: Teks aturan resmi yang memiliki cosine similarity >= 0.70; (c) Prompt Sistem Zero-Hallucination: LLM diinstruksikan hanya menyusun jawaban berdasarkan rujukan chunk yang dilampirkan. Jika similarity < 0.70, sistem langsung mengaktifkan tombol eskalasi WhatsApp ke Ketua RT tanpa memanggil model LLM generatif.",
        body_style
    ))

    story.append(Paragraph("6.2 Legal & Regulatory Compliance", h2_style))
    story.append(Paragraph("• <b>UU ITE No. 1 Tahun 2024:</b> Menjamin keabsahan tanda tangan elektronik resmi RT dan keutuhan dokumen PDF ber-hash.", bullet_style))
    story.append(Paragraph("• <b>UU PDP No. 27 Tahun 2022:</b> Perlindungan kerahasiaan data kependudukan (NIK, profil) dengan enkripsi bcrypt dan RBAC.", bullet_style))

    story.append(Paragraph("6.3 Requirement Traceability Matrix (RTM)", h2_style))
    story.append(Paragraph("Matriks keterlacakan kebutuhan menghubungkan kebutuhan fungsional dengan Use Case, User Story, UML, Database, dan GUI:", body_style))
    
    rtm_headers = [[
        Paragraph("<b>Tag REQ</b>", table_cell_bold),
        Paragraph("<b>Use Case</b>", table_cell_bold),
        Paragraph("<b>User Story</b>", table_cell_bold),
        Paragraph("<b>Activity</b>", table_cell_bold),
        Paragraph("<b>Sequence</b>", table_cell_bold),
        Paragraph("<b>Database</b>", table_cell_bold),
        Paragraph("<b>Layar GUI</b>", table_cell_bold)
    ]]
    rtm_rows_data = [
        ("REQ-1..4", "UC-01, UC-02", "US-01, US-02", "Act Register, Login", "Seq Register, Login", "users", "SCREEN-002, 003"),
        ("REQ-5..8", "UC-03", "US-03", "Act Pengajuan", "Seq Pengajuan", "pengajuan_surat, jenis_surat", "SCREEN-007, 008"),
        ("REQ-9..11", "UC-03", "US-03", "Act Pengajuan", "Seq Pengajuan", "pengajuan_surat (draf_ai)", "SCREEN-010"),
        ("REQ-12..14", "UC-05", "US-05", "Act Pengajuan", "Seq Pengajuan", "pengajuan_surat, users", "SCREEN-009, 010"),
        ("REQ-15..18", "UC-04, UC-05", "US-04, US-05", "Act Pengajuan", "Seq Pengajuan", "surat_final, pengajuan", "SCREEN-010, 012"),
        ("REQ-19..22", "UC-06", "US-06", "Act Chatbot", "Seq Chatbot RAG", "knowledge_chunks, chat", "SCREEN-011")
    ]
    for rtag, uc, us, act, seq, db, scr in rtm_rows_data:
        rtm_headers.append([
            Paragraph(f"<b>{rtag}</b>", table_cell),
            Paragraph(uc, table_cell),
            Paragraph(us, table_cell),
            Paragraph(act, table_cell),
            Paragraph(seq, table_cell),
            Paragraph(db, table_cell),
            Paragraph(scr, table_cell)
        ])
    t_rtm = Table(rtm_headers, colWidths=[65, 75, 75, 80, 80, 75, 65])
    t_rtm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_rtm)

    story.append(PageBreak())

    # ==================== APPENDIX A: GLOSSARY ====================
    story.append(Paragraph("Appendix A: Glossary", h1_style))
    story.append(Paragraph("Daftar istilah dan singkatan teknis dalam dokumen spesifikasi kebutuhan:", body_style))
    abbr_rows = [[Paragraph("<b>Istilah / Singkatan</b>", table_cell_bold), Paragraph("<b>Definisi Konseptual</b>", table_cell_bold)]]
    for abbr, desc in ABBREVIATIONS:
        abbr_rows.append([Paragraph(f"<b>{abbr}</b>", table_cell), Paragraph(desc, table_cell)])
    t_abbr = Table(abbr_rows, colWidths=[100, 415])
    t_abbr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_abbr)

    story.append(PageBreak())

    # ==================== APPENDIX B: ANALYSIS MODELS ====================
    story.append(Paragraph("Appendix B: Analysis Models (UML & BPMN Artifacts)", h1_style))
    story.append(Paragraph("Kompilasi lengkap seluruh model analisis dan diagram visual yang telah diaudit dan disempurnakan berdasarkan 4 feedback resmi dosen:", body_style))

    # B.1 BPMN
    story.append(Paragraph("B.1 Business Process Models (BPMN AS-IS & TO-BE)", h2_style))
    story.append(Paragraph("Setiap aktivitas tugas (Task) memuat data Input dan Output eksplisit, dan seluruh gateway percabangan keputusan ditandai dengan gateway [XOR] sesuai Feedback Dosen #2.", body_style))
    
    img_asis = get_fitted_image("diagrams/bpmn_as_is.png", max_width=470, max_height=260)
    if img_asis:
        story.append(img_asis)
        story.append(Paragraph("Gambar B.1 BPMN AS-IS Proses Pengajuan Surat Pengantar Konvensional", caption_style))

    story.append(Paragraph("<b>Tabel Metadata Input dan Output Tugas pada BPMN AS-IS:</b>", body_style))
    asis_table_data = [[
        Paragraph("<b>ID</b>", table_cell_bold),
        Paragraph("<b>Nama Tugas (Task)</b>", table_cell_bold),
        Paragraph("<b>Aktor</b>", table_cell_bold),
        Paragraph("<b>Input Data</b>", table_cell_bold),
        Paragraph("<b>Output Data</b>", table_cell_bold)
    ]]
    for tid, tname, actor, tinp, tout in BPMN_TASKS_AS_IS:
        asis_table_data.append([Paragraph(tid, table_cell), Paragraph(tname, table_cell), Paragraph(actor, table_cell), Paragraph(tinp, table_cell), Paragraph(tout, table_cell)])
    t_asis = Table(asis_table_data, colWidths=[45, 140, 65, 130, 135])
    t_asis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_asis)
    story.append(Spacer(1, 10))

    img_tobe = get_fitted_image("diagrams/bpmn_to_be.png", max_width=470, max_height=260)
    if img_tobe:
        story.append(img_tobe)
        story.append(Paragraph("Gambar B.2 BPMN TO-BE Pengajuan Surat Pengantar RTConnect (AI Drafting & Dual-Path Verification)", caption_style))

    story.append(Paragraph("<b>Tabel Metadata Input dan Output Tugas pada BPMN TO-BE:</b>", body_style))
    tobe_table_data = [[
        Paragraph("<b>ID</b>", table_cell_bold),
        Paragraph("<b>Nama Tugas (Task)</b>", table_cell_bold),
        Paragraph("<b>Aktor</b>", table_cell_bold),
        Paragraph("<b>Input Data</b>", table_cell_bold),
        Paragraph("<b>Output Data</b>", table_cell_bold)
    ]]
    for tid, tname, actor, tinp, tout in BPMN_TASKS_TO_BE:
        tobe_table_data.append([Paragraph(tid, table_cell), Paragraph(tname, table_cell), Paragraph(actor, table_cell), Paragraph(tinp, table_cell), Paragraph(tout, table_cell)])
    t_tobe = Table(tobe_table_data, colWidths=[45, 140, 65, 130, 135])
    t_tobe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_tobe)
    story.append(Spacer(1, 10))

    img_asis_tanya = get_fitted_image("diagrams/bpmn_as_is_tanyart.png", max_width=470, max_height=240)
    if img_asis_tanya:
        story.append(img_asis_tanya)
        story.append(Paragraph("Gambar B.3 BPMN AS-IS Tanya RT via Pesan Instan", caption_style))

    img_tobe_tanya = get_fitted_image("diagrams/bpmn_to_be_tanyart.png", max_width=470, max_height=240)
    if img_tobe_tanya:
        story.append(img_tobe_tanya)
        story.append(Paragraph("Gambar B.4 BPMN TO-BE Tanya RT Cerdas RAG & Eskalasi WhatsApp", caption_style))

    story.append(PageBreak())

    # B.2 Use Case Model
    story.append(Paragraph("B.2 Use Case Model & Detailed Specifications", h2_style))
    story.append(Paragraph(
        "Penerapan Feedback Dosen #1: (1) Mengeliminasi use case mandiri 'Mengisi Ulang Form (Revisi)'; (2) Menyederhanakan proses tanda tangan (digital dan basah) masuk ke 'Menindaklanjuti Pengajuan Surat'; serta (3) Menghapus 'Menjawab Pertanyaan Warga' bagi RT karena eskalasi WhatsApp merupakan perilaku otomatis sistem chatbot.",
        body_style
    ))
    img_uc = get_fitted_image("diagrams/use_case_diagram.png", max_width=470, max_height=260)
    if img_uc:
        story.append(img_uc)
        story.append(Paragraph("Gambar B.5 Use Case Diagram RTConnect Hasil Penyempurnaan", caption_style))

    for uc in USE_CASE_SPECS:
        story.append(Paragraph(f"Spesifikasi {uc['id']}: {uc['name']}", h3_style))
        uc_meta_table = [
            [Paragraph("<b>Nama Use Case</b>", table_cell_bold), Paragraph(f"{uc['id']}: {uc['name']}", table_cell)],
            [Paragraph("<b>Aktor Utama</b>", table_cell_bold), Paragraph(uc['actor'], table_cell)],
            [Paragraph("<b>Deskripsi</b>", table_cell_bold), Paragraph(uc['desc'], table_cell)],
            [Paragraph("<b>Preconditions</b>", table_cell_bold), Paragraph(uc['precondition'], table_cell)],
            [Paragraph("<b>Postconditions</b>", table_cell_bold), Paragraph(uc['postcondition'], table_cell)]
        ]
        t_ucm = Table(uc_meta_table, colWidths=[120, 395])
        t_ucm.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F8F9FA')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3)
        ]))
        story.append(t_ucm)
        story.append(Spacer(1, 4))
        
        story.append(Paragraph("<b>Alur Utama (Main Flow):</b>", body_style))
        mf_rows = [[Paragraph("<b>Aktor / Pelaksana</b>", table_cell_bold), Paragraph("<b>Langkah Aksi Sistem / Pengguna</b>", table_cell_bold)]]
        for actor_step, step_desc in uc['main_flow']:
            mf_rows.append([Paragraph(actor_step, table_cell), Paragraph(step_desc, table_cell)])
        t_mf = Table(mf_rows, colWidths=[120, 395])
        t_mf.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5)
        ]))
        story.append(t_mf)
        
        if uc['alt_flow']:
            story.append(Paragraph("<b>Alur Alternatif:</b>", body_style))
            for af_title, af_desc in uc['alt_flow']:
                story.append(Paragraph(f"• <b>{af_title}:</b> {af_desc}", bullet_style))
        if uc['exc_flow']:
            story.append(Paragraph("<b>Alur Eksepsi:</b>", body_style))
            for ef_title, ef_desc in uc['exc_flow']:
                story.append(Paragraph(f"• <b>{ef_title}:</b> {ef_desc}", bullet_style))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # B.3 User Stories
    story.append(Paragraph("B.3 User Stories & BDD Scenarios", h2_style))
    for us in USER_STORIES_DATA:
        story.append(Paragraph(f"<b>[{us['id']}]</b> Sebagai {us['role']}, saya ingin {us['action']}, sehingga {us['benefit']}.", body_style))
        for sc in us['scenarios']:
            story.append(Paragraph(f"<i>Scenario: {sc['title']}</i>", ParagraphStyle('ScTitle', parent=body_style, fontName='Helvetica-BoldOblique', textColor=colors.HexColor('#1A73E8'))))
            story.append(Paragraph(f"<b>Given</b> {sc['given']}", bullet_style))
            story.append(Paragraph(f"<b>When</b> {sc['when']}", bullet_style))
            if 'and' in sc:
                story.append(Paragraph(f"<b>And</b> {sc['and']}", bullet_style))
            story.append(Paragraph(f"<b>Then</b> {sc['then']}", bullet_style))
            story.append(Spacer(1, 3))

    # B.4 Activity Diagrams
    story.append(Paragraph("B.4 Activity Diagrams", h2_style))
    img_act_reg = get_fitted_image("diagrams/activity_register.png", max_width=470, max_height=260)
    if img_act_reg:
        story.append(img_act_reg)
        story.append(Paragraph("Gambar B.6 Activity Diagram Registrasi Akun Warga Mandiri", caption_style))

    img_act_log = get_fitted_image("diagrams/activity_login.png", max_width=470, max_height=260)
    if img_act_log:
        story.append(img_act_log)
        story.append(Paragraph("Gambar B.7 Activity Diagram Login ke Sistem", caption_style))

    img_act_surat = get_fitted_image("diagrams/activity_pengajuan_surat.png", max_width=470, max_height=260)
    if img_act_surat:
        story.append(img_act_surat)
        story.append(Paragraph("Gambar B.8 Activity Diagram Pengajuan dan Pemrosesan Surat Pengantar", caption_style))

    img_act_chat = get_fitted_image("diagrams/activity_chatbot.png", max_width=470, max_height=260)
    if img_act_chat:
        story.append(img_act_chat)
        story.append(Paragraph("Gambar B.9 Activity Diagram Chatbot Tanya RT & Eskalasi WhatsApp", caption_style))

    story.append(PageBreak())

    # B.5 Sequence Diagrams
    story.append(Paragraph("B.5 Sequence Diagrams (Boundary-Control-Entity)", h2_style))
    story.append(Paragraph("Penerapan Feedback Dosen #3 & #4: Seluruh pesan interaksi aktor ke boundary menggunakan narasi bahasa manusia murni (tanpa kode). Seluruh aktor dilengkapi active bar (activation lifeline).", body_style))
    
    img_seq_reg = get_fitted_image("diagrams/sequence_register.png", max_width=470, max_height=260)
    if img_seq_reg:
        story.append(img_seq_reg)
        story.append(Paragraph("Gambar B.10 Sequence Diagram Registrasi Akun", caption_style))

    img_seq_log = get_fitted_image("diagrams/sequence_login.png", max_width=470, max_height=260)
    if img_seq_log:
        story.append(img_seq_log)
        story.append(Paragraph("Gambar B.11 Sequence Diagram Login ke Sistem", caption_style))

    img_seq_surat = get_fitted_image("diagrams/sequence_pengajuan_surat.png", max_width=470, max_height=280)
    if img_seq_surat:
        story.append(img_seq_surat)
        story.append(Paragraph("Gambar B.12 Sequence Diagram Pengajuan dan Tindak Lanjut Surat Pengantar", caption_style))

    img_seq_chat = get_fitted_image("diagrams/sequence_chatbot.png", max_width=470, max_height=260)
    if img_seq_chat:
        story.append(img_seq_chat)
        story.append(Paragraph("Gambar B.13 Sequence Diagram Chatbot Tanya RT (RAG & Eskalasi WhatsApp)", caption_style))

    story.append(PageBreak())

    # B.6 Class Diagram
    story.append(Paragraph("B.6 Domain & Class Diagrams", h2_style))
    img_cls = get_fitted_image("diagrams/class_diagram.png", max_width=470, max_height=280)
    if img_cls:
        story.append(img_cls)
        story.append(Paragraph("Gambar B.14 Class Diagram RTConnect Terpadu (Entity & Service Layer)", caption_style))

    # B.7 Data Models (ERD)
    story.append(Paragraph("B.7 Data Models (ERD CDM & PDM)", h2_style))
    img_erd = get_fitted_image("diagrams/database_er_diagram.png", max_width=470, max_height=280)
    if img_erd:
        story.append(img_erd)
        story.append(Paragraph("Gambar B.15 Entity Relationship Diagram (ERD / CDM & PDM)", caption_style))

    # B.8 System Architecture
    story.append(Paragraph("B.8 System Architecture & Deployment Diagram", h2_style))
    if img_arch:
        story.append(img_arch)
        story.append(Paragraph("Gambar B.16 System Architecture & Deployment Diagram RTConnect", caption_style))

    story.append(PageBreak())

    # ==================== APPENDIX C: TBD LIST ====================
    story.append(Paragraph("Appendix C: To Be Determined (TBD) List", h1_style))
    story.append(Paragraph("Daftar butir terbuka (TBD List) yang akan disepakati lebih lanjut pada pengujian sistem:", body_style))
    tbd_rows = [[
        Paragraph("<b>ID TBD</b>", table_cell_bold),
        Paragraph("<b>Topik Spesifikasi</b>", table_cell_bold),
        Paragraph("<b>Rencana Tindak Lanjut Evaluasi</b>", table_cell_bold)
    ]]
    tbd_items = [
        ("TBD-1", "Batas Maksimal Kuota Harian Pengajuan Surat", "Penentuan batas maksimal frekuensi permohonan surat per NIK dalam satu hari untuk mencegah spamming."),
        ("TBD-2", "Waktu Retensi Otomatis Arsip Berkas Pengajuan", "Penetapan jadwal pembersihan berkas lampiran KTP/KK lama dari penyimpanan server (apakah 1 tahun atau 2 tahun)."),
        ("TBD-3", "Penyediaan Penyimpanan Vector Database Khusus", "Evaluasi migrasi penyimpanan vektor embedding dari kolom JSON MySQL ke ekstensi pgvector atau ChromaDB jika jumlah warga melebihi 1.000 kepala keluarga.")
    ]
    for tid, top, nts in tbd_items:
        tbd_rows.append([Paragraph(f"<b>{tid}</b>", table_cell), Paragraph(top, table_cell), Paragraph(nts, table_cell)])
    t_tbd = Table(tbd_rows, colWidths=[70, 200, 245])
    t_tbd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_tbd)

    story.append(PageBreak())

    # ==================== APPENDIX D: TEAM CONTRIBUTION ====================
    story.append(Paragraph("Appendix D: Team Member Contribution Table", h1_style))
    story.append(Paragraph("Tabel kontribusi anggota kelompok dalam perancangan dan penyusunan spesifikasi teknis RTConnect:", body_style))
    contrib_rows = [[
        Paragraph("<b>No</b>", table_cell_bold),
        Paragraph("<b>Nama Lengkap</b>", table_cell_bold),
        Paragraph("<b>NIM</b>", table_cell_bold),
        Paragraph("<b>Foto</b>", table_cell_bold),
        Paragraph("<b>Rincian Kontribusi Proyek</b>", table_cell_bold)
    ]]
    for no, name, nim, foto, kontribusi in CONTRIBUTION_DATA:
        contrib_rows.append([
            Paragraph(no, table_cell),
            Paragraph(name, table_cell),
            Paragraph(nim, table_cell),
            Paragraph(foto, table_cell),
            Paragraph(kontribusi, table_cell)
        ])
    t_contrib = Table(contrib_rows, colWidths=[30, 140, 85, 110, 150])
    t_contrib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F0FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DADCE0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_contrib)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: {filename} berhasil dibangun dan disimpan!")

if __name__ == '__main__':
    build_wiegers_srs_pdf()
