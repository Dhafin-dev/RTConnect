# -*- coding: utf-8 -*-
"""
Builder Skrip DOCX SRS RTConnect
Format: Karl E. Wiegers (1999) / IEEE Std 830-1998 Software Requirements Specification
Praktikum Pembangunan Perangkat Lunak (Praktikum I1) - Universitas Airlangga 2026
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(22)
    h.paragraph_format.space_after = Pt(8)
    for r in h.runs:
        r.font.name = 'Segoe UI'
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = RGBColor(26, 115, 232)
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.name = 'Segoe UI'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(32, 33, 36)
    return h

def add_heading_3(doc, text):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    for r in h.runs:
        r.font.name = 'Segoe UI'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(95, 99, 104)
    return h

def add_p(doc, text, bold_prefix="", italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Segoe UI'
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(32, 33, 36)
    r = p.add_run(text)
    r.font.name = 'Segoe UI'
    r.font.size = Pt(9.5)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Segoe UI'
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(32, 33, 36)
    r = p.add_run(text)
    r.font.name = 'Segoe UI'
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_callout(doc, title, text, border_color="#1A73E8", bg_color="#F8F9FA"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color.replace("#", ""))
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color.replace('#','')}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"{title}\n")
    r1.font.name = 'Segoe UI'
    r1.font.bold = True
    r1.font.size = Pt(10)
    r1.font.color.rgb = RGBColor(26, 115, 232)
    
    r2 = p.add_run(text)
    r2.font.name = 'Segoe UI'
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(60, 64, 67)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_diagram_image(doc, img_path, caption, width_inch=5.8):
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
            
    if real_path:
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(real_path, width=Inches(width_inch))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Segoe UI'
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(95, 99, 104)
    else:
        p = doc.add_paragraph(f"[Gambar tidak ditemukan: {img_path}]")
        p.runs[0].font.color.rgb = RGBColor(220, 38, 38)

def format_custom_table(table, col_widths, col_alignments=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for j, cell in enumerate(row.cells):
            cell.width = col_widths[j]
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            if i == 0:
                set_cell_background(cell, "E8F0FE")
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for r in p.runs:
                        r.font.name = 'Segoe UI'
                        r.font.size = Pt(8.5)
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(26, 115, 232)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                else:
                    set_cell_background(cell, "F8F9FA")
                for p in cell.paragraphs:
                    if col_alignments and j < len(col_alignments):
                        p.alignment = col_alignments[j]
                    for r in p.runs:
                        r.font.name = 'Segoe UI'
                        r.font.size = Pt(8)
                        r.font.color.rgb = RGBColor(32, 33, 36)

def generate_wiegers_srs_docx(output_filename=None):
    if output_filename is None:
        os.makedirs("UTS", exist_ok=True)
        output_filename = os.path.join("UTS", "UTS_I1_RTConnect_SRS.docx")
    doc = docx.Document()
    
    # Standard margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    print("Membangun Dokumen SRS Format Karl E. Wiegers (IEEE Std 830-1998)...")

    # ==================== COVER PAGE (WIEGERS STYLE) ====================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("PROGRAM STUDI SARJANA SISTEM INFORMASI\nFAKULTAS SAINS DAN TEKNOLOGI\nUNIVERSITAS AIRLANGGA SURABAYA\n")
    r_inst.font.name = 'Segoe UI'
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(95, 99, 104)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(12)
    r_t1 = p_title.add_run("Software Requirements Specification\n")
    r_t1.font.name = 'Segoe UI'
    r_t1.font.size = Pt(24)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(26, 115, 232)
    
    r_t2 = p_title.add_run("for\n\nRTConnect: Perangkat Lunak Administrasi di Tingkat RT/RW\ndengan Integrasi NLP dan Generative AI")
    r_t2.font.name = 'Segoe UI'
    r_t2.font.size = Pt(14)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(32, 33, 36)

    p_ver = doc.add_paragraph()
    p_ver.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ver.paragraph_format.space_before = Pt(20)
    p_ver.paragraph_format.space_after = Pt(20)
    r_ver = p_ver.add_run(f"Version {METADATA['version']}\n")
    r_ver.font.name = 'Segoe UI'
    r_ver.font.size = Pt(12)
    r_ver.font.bold = True
    r_ver.font.color.rgb = RGBColor(15, 157, 88)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(30)
    p_meta.paragraph_format.space_after = Pt(10)
    
    r_prep = p_meta.add_run("Prepared by Kelompok 3 (Praktikum I1):\n")
    r_prep.font.name = 'Segoe UI'
    r_prep.font.size = Pt(10.5)
    r_prep.font.bold = True
    
    for m in METADATA['authors']:
        r_auth = p_meta.add_run(f"{m['name']} — NIM: {m['nim']}\n")
        r_auth.font.name = 'Segoe UI'
        r_auth.font.size = Pt(9.5)
        
    p_dos = doc.add_paragraph()
    p_dos.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dos.paragraph_format.space_before = Pt(16)
    r_d = p_dos.add_run(f"Dosen Pengampu:\n{METADATA['lecturer']}\nNIP. {METADATA['lecturer_nip']}\n\nDate created: {METADATA['date_created']}")
    r_d.font.name = 'Segoe UI'
    r_d.font.size = Pt(9.5)
    r_d.font.color.rgb = RGBColor(60, 64, 67)

    doc.add_page_break()

    # ==================== TABLE OF CONTENTS ====================
    add_heading_1(doc, "Table of Contents")
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
    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    for idx, (sec_name, page_num) in enumerate(toc_items):
        r0 = tbl_toc.rows[idx].cells[0].paragraphs[0]
        r0.text = sec_name
        r1 = tbl_toc.rows[idx].cells[1].paragraphs[0]
        r1.text = page_num
        r1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_cell_margins(tbl_toc.rows[idx].cells[0], top=30, bottom=30, left=60, right=60)
        set_cell_margins(tbl_toc.rows[idx].cells[1], top=30, bottom=30, left=60, right=60)
        for r in r0.runs:
            r.font.name = 'Segoe UI'
            r.font.size = Pt(8.5)
            if not sec_name.startswith("   "):
                r.font.bold = True
                r.font.color.rgb = RGBColor(26, 115, 232)
        for r in r1.runs:
            r.font.name = 'Segoe UI'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(95, 99, 104)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_toc.columns[0].width = Inches(5.5)
    tbl_toc.columns[1].width = Inches(1.0)

    doc.add_page_break()

    # ==================== REVISION HISTORY ====================
    add_heading_1(doc, "Revision History")
    add_p(doc, "Tabel berikut mendokumentasikan riwayat perubahan formal spesifikasi kebutuhan perangkat lunak RTConnect, mencakup catatan perbaikan berdasarkan 4 arahan revisi resmi Dosen Pengampu:")
    
    tbl_rev = doc.add_table(rows=len(REVISION_HISTORY)+1, cols=4)
    tbl_rev.rows[0].cells[0].paragraphs[0].text = "Name"
    tbl_rev.rows[0].cells[1].paragraphs[0].text = "Date"
    tbl_rev.rows[0].cells[2].paragraphs[0].text = "Reason For Changes"
    tbl_rev.rows[0].cells[3].paragraphs[0].text = "Version"
    for idx, rev in enumerate(REVISION_HISTORY):
        tbl_rev.rows[idx+1].cells[0].paragraphs[0].text = rev['name']
        tbl_rev.rows[idx+1].cells[1].paragraphs[0].text = rev['date']
        tbl_rev.rows[idx+1].cells[2].paragraphs[0].text = rev['reason']
        tbl_rev.rows[idx+1].cells[3].paragraphs[0].text = rev['version']
    format_custom_table(tbl_rev, [Inches(1.8), Inches(1.1), Inches(2.8), Inches(0.8)])

    add_callout(doc, "Ringkasan 4 Poin Revisi Dosen Pengampu yang Diterapkan Penuh",
        "1. Use Case Diagram: Menghilangkan 'Mengisi Ulang Form' sebagai UC mandiri; Menyederhanakan proses tanda tangan (digital & basah) masuk ke 'Menindaklanjuti Pengajuan Surat'; Menghapus 'Menjawab Pertanyaan Warga' bagi RT (karena bukan fitur sistem bagi RT, melainkan system behavior chatbot).\n"
        "2. BPMN AS-IS & TO-BE: Memperinci data Input dan Output pada setiap aktivitas tugas (Task); Menandai seluruh gateway percabangan keputusan secara eksplisit sebagai [XOR] atau [OR].\n"
        "3. Sequence Diagram (Komunikasi Aktor ke Boundary): Mengubah pesan aktor ke batas sistem menjadi narasi bahasa manusia murni tanpa sintaks pemrograman atau endpoint API.\n"
        "4. Sequence Diagram (Lifeline Aktor): Membubuhkan activation bar (active bar) pada seluruh aktor saat mengirim instruksi dan menunggu respons sistem.")

    doc.add_page_break()

    # ==================== 1. INTRODUCTION ====================
    add_heading_1(doc, "1. Introduction")
    
    add_heading_2(doc, "1.1 Purpose")
    add_p(doc, "Dokumen Software Requirements Specification (SRS) ini merumuskan secara komprehensif seluruh spesifikasi kebutuhan fungsional, kebutuhan non-fungsional, karakteristik pengguna, antarmuka eksternal, batasan perancangan, dan arsitektur sistem informasi RTConnect versi 1.0 approved. Sistem ini dirancang untuk mendigitalkan birokrasi tata kelola rukun tetangga dan rukun warga di tingkat akar rumput dengan integrasi Natural Language Processing (NLP) dan Large Language Model (LLM). Dokumen ini menjadi pedoman tunggal (Single Source of Truth) bagi pengembang, penguji sistem, pengguna akhir, serta evaluator akademik.")

    add_heading_2(doc, "1.2 Document Conventions")
    add_p(doc, "Penyusunan dokumen ini mengadopsi struktur standar Karl E. Wiegers (1999) dan IEEE Std 830-1998. Konvensi tipografi dan penomoran yang digunakan adalah:")
    add_bullet(doc, "Kebutuhan fungsional spesifik pada setiap fitur ditandai dengan label deterministik berformat REQ-x (misalnya: REQ-1, REQ-2, dst.).", "• Tag Kebutuhan Fungsional: ")
    add_bullet(doc, "Kebutuhan non-fungsional dikelompokkan ke dalam NFR-01 s/d NFR-08.", "• Tag Non-Fungsional: ")
    add_bullet(doc, "Prioritas kebutuhan dievaluasi berdasarkan skala relatif 1 (terendah) hingga 9 (tertinggi) yang mencakup 4 parameter: Tingkat Manfaat (Benefit), Sanksi Kelalaian (Penalty), Biaya Implementasi (Cost), dan Risiko Kegagalan (Risk).", "• Skema Prioritas Wiegers: ")
    add_bullet(doc, "Pemodelan UML mematuhi kaidah Robustness Analysis Boundary-Control-Entity (BCE) dengan pesan narasi interaksi manusia pada batas sistem dan active bar pada aktor.", "• Konvensi Pemodelan Visual: ")

    add_heading_2(doc, "1.3 Intended Audience and Reading Suggestions")
    add_p(doc, "Dokumen ini ditujukan kepada beragam pemangku kepentingan:")
    add_bullet(doc, "Fokus membaca Bagian 2 (Overall Description), Bagian 4 (System Features), Bagian 6.1 (Database), dan Appendix B (Analysis Models) untuk implementasi backend Flask, antarmuka Flutter, serta skema MySQL.", "• Tim Pengembang (Developers): ")
    add_bullet(doc, "Fokus membaca Bagian 4 (Stimulus/Response Sequences), Bagian 5 (Quality Attributes), Bagian 6.3 (RTM), dan Appendix B.3 (BDD Scenarios) untuk merancang pengujian verifikasi otomatis.", "• Tim Penguji (Quality Assurance & Testers): ")
    add_bullet(doc, "Membaca Bagian 2, Bagian 3.1 (User Interfaces), dan Appendix B.1 (BPMN TO-BE) guna memahami hak akses dan alur pengajuan surat serta layanan Chatbot.", "• Pengguna Akhir (Warga & Ketua RT): ")
    add_bullet(doc, "Membaca Revision History, Ringkasan Audit, Bagian 4, Bagian 6, serta Appendix B untuk menilai kepatuhan terhadap 4 revisi resmi dan rigoritas rekayasa perangkat lunak.", "• Dosen Pengampu & Reviewer Akademik: ")

    add_heading_2(doc, "1.4 Product Scope")
    add_p(doc, "RTConnect adalah perangkat lunak administrasi mikro-pemerintahan yang dikembangkan secara presisi untuk wilayah RT 032 RW 08 Griya Taman Asri, Desa Tawangsari, Kecamatan Taman, Kabupaten Sidoarjo. Ruang lingkup produk mencakup:")
    add_bullet(doc, "Pendaftaran akun warga mandiri dengan verifikasi NIK 16 digit, enkripsi password bcrypt, dan autentikasi satu pintu (JWT).", "1. Registrasi & Manajemen Identitas: ")
    add_bullet(doc, "Pengajuan permohonan surat (Domisili, Pengantar KTP/KK, SKCK, Usaha) secara online dari rumah dengan formulasi draf narasi surat formal otomatis oleh Generative AI.", "2. Layanan Surat Pengantar Daring: ")
    add_bullet(doc, "Pemeriksaan berkas pemohon, draf AI, penerbitan nomor surat resmi, serta fleksibilitas pengesahan dokumen: jalur digital (stempel TTD elektronik) atau jalur basah (cetak fisik & cap stempel basah RT).", "3. Peninjauan & Pengesahan oleh Ketua RT: ")
    add_bullet(doc, "Layanan tanya jawab mandiri seputar persyaratan administrasi RT melalui chatbot semantik RAG, dengan mekanisme fallback eskalasi otomatis ke nomor WhatsApp Ketua RT jika informasi tidak ditemukan.", "4. Asisten Cerdas Warga 24/7 (Chatbot Tanya RT): ")

    add_heading_2(doc, "1.5 References")
    add_p(doc, "Dokumen SRS ini mengacu pada standar rekayasa perangkat lunak internasional, regulasi perundang-undangan nasional, dan pustaka akademik terindeks:")
    for ref in REFERENCES_DATA:
        add_bullet(doc, ref)

    # ==================== 2. OVERALL DESCRIPTION ====================
    add_heading_1(doc, "2. Overall Description")
    
    add_heading_2(doc, "2.1 Product Perspective")
    add_p(doc, "RTConnect diposisikan sebagai platform digital micro-governance mandiri (self-contained) yang mengintegrasikan warga dengan aparatur lingkungan RT dalam satu ekosistem terpadu. Sistem ini menggantikan alur manual konvensional (tatap muka fisik / pesan instan tidak terstruktur) dengan sistem informasi modern berbasis arsitektur client-server 4-tier: Presentation Tier (Flutter Web/Mobile), Application Tier (Python Flask Framework 3.1+), Persistence Tier (MySQL 8.0 RDBMS), dan External Services Tier (OpenAI API LLM & WhatsApp URI Gateway).")
    add_diagram_image(doc, "diagrams/system_architecture.png", "Gambar 2.1 Arsitektur Sistem 4-Tier & Diagram Lingkungan RTConnect")

    add_heading_2(doc, "2.2 Product Functions")
    add_p(doc, "Fungsi-fungsi utama sistem diringkas sebagai berikut:")
    add_bullet(doc, "Menyediakan registrasi mandiri, validasi NIK 16 digit, enkripsi kata sandi, dan pembatasan hak akses berbasis peran (Warga vs Ketua RT).", "• F-01 Manajemen Akun & Autentikasi: ")
    add_bullet(doc, "Menyediakan formulir permohonan surat pengantar dengan pengisian biodata otomatis dari profil pemohon dan pemilihan metode tanda tangan.", "• F-02 Pengajuan Surat Mandiri: ")
    add_bullet(doc, "Memanfaatkan model Large Language Model (LLM) untuk menyusun narasi formal draf surat resmi segera setelah formulir diserahkan warga.", "• F-03 Formulasi Draf Narasi AI: ")
    add_bullet(doc, "Menyediakan antrean pengajuan pada dashboard Ketua RT untuk menyetujui, meminta revisi berkas, atau menolak permohonan dengan alasan wajib.", "• F-04 Peninjauan & Tindak Lanjut RT: ")
    add_bullet(doc, "Menyediakan pembubuhan stempel tanda tangan digital dan pembuatan PDF resmi, serta opsi cetak fisik untuk tanda tangan basah konvensional.", "• F-05 Pengesahan & Penerbitan Dokumen: ")
    add_bullet(doc, "Menyediakan konsultasi 24/7 menggunakan arsitektur RAG yang mencocokkan kemiripan semantik query warga ke potongan aturan RT, serta eskalasi otomatis ke WhatsApp RT bila kemiripan < 0.70.", "• F-06 Chatbot Tanya RT & Eskalasi: ")

    add_heading_2(doc, "2.3 User Classes and Characteristics")
    add_bullet(doc, "Masyarakat umum domisili RT 032 RW 08. Frekuensi penggunaan: berkala (saat membutuhkan surat pengantar atau informasi). Keterampilan teknis: pengguna gawai dasar hingga menengah. Hak akses: mengajukan surat, melacak riwayat, mengunduh PDF, berkonsultasi dengan chatbot.", "1. Warga (Resident): ")
    add_bullet(doc, "Pejabat ketua RT yang berwenang memeriksa dan mengesahkan permohonan. Frekuensi penggunaan: harian / berkala saat terdapat antrean masuk. Keterampilan teknis: menengah. Hak akses: meninjau berkas pemohon, menyunting draf narasi, mengesahkan surat via PIN digital, mencetak surat basah, dan mengelola dokumen.", "2. Ketua RT (RT Administrator): ")

    add_heading_2(doc, "2.4 Operating Environment")
    add_bullet(doc, "Peramban web modern (Google Chrome v110+, Mozilla Firefox v115+, Safari v16+) atau gawai bergerak Android 8.0+ / iOS 14.0+.", "• Lingkungan Klien: ")
    add_bullet(doc, "Ubuntu Linux 22.04 LTS / Windows 11 Server, Python runtime 3.10+, WSGI Gunicorn/Werkzeug, Flask Framework 3.1+.", "• Lingkungan Server Backend: ")
    add_bullet(doc, "MySQL Server 8.0 / 8.4 LTS, konektor PyMySQL / SQLAlchemy ORM.", "• Lingkungan Basis Data: ")
    add_bullet(doc, "OpenAI API (model text-embedding-3-small untuk vektor RAG, model GPT-4o-mini / LLM setara untuk formulasi surat), serta WhatsApp Deep-link Gateway (wa.me protocol).", "• Layanan Eksternal: ")

    add_heading_2(doc, "2.5 Design and Implementation Constraints")
    add_bullet(doc, "Sistem secara ketat menerapkan batasan yurisdiksi administratif pada RT 032 RW 08 Desa Tawangsari Sidoarjo.", "1. Batasan Wilayah: ")
    add_bullet(doc, "Sistem bergantung pada koneksi internet stabil dan ketersediaan kuota token API pihak ketiga (OpenAI API). Apabila API gagal, sistem wajib memiliki mekanisme graceful fallback.", "2. Ketergantungan Eksternal: ")
    add_bullet(doc, "Jawaban chatbot dibatasi secara ketat hanya pada isi dokumen aturan RT 032 yang terindeks (Zero Hallucination Policy).", "3. Batasan Grounding AI: ")
    add_bullet(doc, "Pengesahan tanda tangan elektronik wajib memenuhi ketentuan integritas dokumen UU ITE No. 1 Tahun 2024.", "4. Batasan Hukum: ")

    add_heading_2(doc, "2.6 User Documentation")
    add_p(doc, "Pengembang akan menyediakan dokumentasi pengguna berupa: (1) Buku Panduan Pengguna Warga (format PDF interaktif); (2) Buku Petunjuk Teknis Operasional Ketua RT; dan (3) Panduan API & Deployment Panduan Administrator Server.")

    add_heading_2(doc, "2.7 Assumptions and Dependencies")
    add_p(doc, "Asumsi utama sistem meliputi: (1) Setiap pemohon memiliki NIK 16 digit yang sah; (2) Ketua RT memiliki nomor WhatsApp aktif untuk menerima eskalasi pertanyaan; (3) Server memiliki akses jaringan internet outbound untuk memanggil endpoint OpenAI API.")

    # ==================== 3. EXTERNAL INTERFACE REQUIREMENTS ====================
    add_heading_1(doc, "3. External Interface Requirements")
    
    add_heading_2(doc, "3.1 User Interfaces")
    add_p(doc, "Antarmuka grafis pengguna (GUI) RTConnect dirancang menggunakan Flutter dengan paradigma Material Design 3 yang adaptif (responsive web & mobile). Standar desain antarmuka mencakup konsistensi warna primer biru (#1A73E8), kartu putih berkontur halus, tipografi Segoe UI / Roboto, serta kepatuhan aksesibilitas WCAG 2.1 AA (kontras teks minimal 4.5:1 dan target sentuh minimal 48x48 dp).")
    
    add_p(doc, "Daftar inventaris layar antarmuka pengguna (Screen Inventory) yang disediakan sistem:")
    ui_screens = [
        ("SCREEN-001", "Landing / Welcome Page", "Halaman penyambutan publik yang menampilkan profil RT 032 dan tombol navigasi 'Masuk' serta 'Registrasi'."),
        ("SCREEN-002", "Halaman Registrasi Warga", "Formulir pendaftaran akun mandiri dengan isian NIK 16 digit, biodata, kata sandi, dan input unggah foto stempel tanda tangan."),
        ("SCREEN-003", "Halaman Login Terpadu", "Formulir autentikasi satu pintu bagi Warga dan Ketua RT dengan input Email/NIK dan Password."),
        ("SCREEN-004", "Dashboard Utama Warga", "Beranda akun warga yang menampilkan kartu aksi cepat 'Ajukan Surat Pengantar' dan 'Tanya RT via Chatbot'."),
        ("SCREEN-005", "Drawer Navigasi & Profil", "Menu bilah samping (drawer) untuk mengakses profil pengguna, pengaturan akun, dan tombol keluar (logout)."),
        ("SCREEN-006", "Riwayat Pengajuan Surat", "Daftar pemantauan permohonan surat warga lengkap dengan badge status berkode warna (Diajukan, Perlu Revisi, Disetujui, Selesai, Ditolak)."),
        ("SCREEN-007", "Formulir Permohonan Surat", "Formulir pengajuan surat pengantar dengan biodata terisi otomatis, pilihan jenis surat, kolom keperluan, opsi metode tanda tangan (Digital/Basah), dan unggah lampiran."),
        ("SCREEN-008", "Formulir Pengisian Ulang Revisi", "Formulir perbaikan data bagi permohonan berstatus 'Perlu Revisi' yang menyajikan catatan koreksi dari Ketua RT."),
        ("SCREEN-009", "Dashboard Antrean RT", "Antrean kerja administratif Ketua RT yang menyajikan daftar permohonan masuk yang siap diperiksa."),
        ("SCREEN-010", "Detail & Tindak Lanjut RT", "Halaman telaah berkas pemohon, lampiran, draf narasi hasil AI, input nomor surat resmi, dan tombol aksi (Setujui, Minta Revisi, Tolak)."),
        ("SCREEN-011", "Antarmuka Chatbot Tanya RT", "Ruang percakapan cerdas yang menampilkan balon dialog, tombol rekomendasi pertanyaan FAQ, badge sumber regulasi, dan tombol eskalasi WhatsApp RT."),
        ("SCREEN-012", "Penampil Dokumen PDF Resmi", "Halaman pratinjau surat pengantar resmi bertanda tangan digital dengan tombol cetak dan unduh dokumen ke perangkat lokal.")
    ]
    tbl_ui = doc.add_table(rows=len(ui_screens)+1, cols=3)
    tbl_ui.rows[0].cells[0].paragraphs[0].text = "ID Layar"
    tbl_ui.rows[0].cells[1].paragraphs[0].text = "Nama Antarmuka (Screen)"
    tbl_ui.rows[0].cells[2].paragraphs[0].text = "Fungsi Operasional & Interaksi Pengguna"
    for idx, (sid, sname, sdesc) in enumerate(ui_screens):
        tbl_ui.rows[idx+1].cells[0].paragraphs[0].text = sid
        tbl_ui.rows[idx+1].cells[1].paragraphs[0].text = sname
        tbl_ui.rows[idx+1].cells[2].paragraphs[0].text = sdesc
    format_custom_table(tbl_ui, [Inches(1.2), Inches(2.2), Inches(3.1)])

    add_heading_2(doc, "3.2 Hardware Interfaces")
    add_bullet(doc, "Smartphone (Android 8.0+ / iOS 14.0+) atau Komputer/Laptop (resolusi layar minimal 360x640 px hingga 1920x1080 px, RAM minimal 2GB).", "• Perangkat Klien: ")
    add_bullet(doc, "Processor minimal 2 Cores vCPU, RAM 4GB (direkomendasikan 8GB), media penyimpanan SSD minimal 20GB, koneksi jaringan 100 Mbps.", "• Perangkat Server: ")

    add_heading_2(doc, "3.3 Software Interfaces")
    add_bullet(doc, "Flask v3.1+ menyediakan RESTful API JSON untuk menangani logika autentikasi, transaksi permohonan, orkestrasi AI, dan penyajian dokumen PDF.", "• Python Flask Backend: ")
    add_bullet(doc, "MySQL Server v8.0/8.4 LTS mengelola data relasional pengguna, master surat, transaksi pengajuan, riwayat chat, dan potongan teks dokumen regulasi.", "• Database MySQL: ")
    add_bullet(doc, "Menghubungkan backend dengan model OpenAI (text-embedding-3-small untuk vektorisasi RAG 1536-dimensi, GPT-4o-mini untuk formulasi draf narasi surat dan sintesis jawaban).", "• OpenAI REST API: ")
    add_bullet(doc, "Protokol deep-link wa.me yang secara otomatis membuka obrolan ke nomor Ketua RT dengan teks pertanyaan yang telah terenkripsi URL encoding.", "• WhatsApp URI Gateway: ")

    add_heading_2(doc, "3.4 Communications Interfaces")
    add_p(doc, "Seluruh lalu lintas komunikasi data antara antarmuka Flutter dan backend Flask wajib melalui protokol terenkripsi HTTPS (HTTP/2 over TLS 1.3). Format transmisi payload data berstandar JSON (JavaScript Object Notation) dengan header otorisasi Bearer JWT. Protokol pengalihan ke WhatsApp memanfaatkan skema URI https://wa.me/{phone}?text={encoded_message}.")

    # ==================== 4. SYSTEM FEATURES ====================
    add_heading_1(doc, "4. System Features")
    add_p(doc, "Bagian ini mendokumentasikan secara rinci enam fitur sistem utama yang disediakan oleh perangkat lunak RTConnect, disusun menggunakan format standar Karl E. Wiegers: Deskripsi & Rating Prioritas, Rangkaian Stimulus/Respons (Stimulus/Response Sequences), dan Pernyataan Kebutuhan Fungsional (REQ-x).")

    for feat in SYSTEM_FEATURES_DATA:
        add_heading_2(doc, f"{feat['num']} {feat['name']}")
        
        # 4.x.1 Description and Priority
        add_heading_3(doc, f"{feat['num']}.1 Description and Priority")
        add_p(doc, feat['desc'])
        add_p(doc, feat['priority'], bold_prefix="Tingkat Prioritas (Wiegers Rating): ")
        
        # 4.x.2 Stimulus/Response Sequences
        add_heading_3(doc, f"{feat['num']}.2 Stimulus/Response Sequences")
        tbl_sr = doc.add_table(rows=len(feat['stimulus_response'])+1, cols=3)
        tbl_sr.rows[0].cells[0].paragraphs[0].text = "No"
        tbl_sr.rows[0].cells[1].paragraphs[0].text = "Stimulus (Aksi Pengguna / Kejadian)"
        tbl_sr.rows[0].cells[2].paragraphs[0].text = "Respons Sistem (Perilaku Perangkat Lunak)"
        for idx, (sno, stim, resp) in enumerate(feat['stimulus_response']):
            tbl_sr.rows[idx+1].cells[0].paragraphs[0].text = sno
            tbl_sr.rows[idx+1].cells[1].paragraphs[0].text = stim
            tbl_sr.rows[idx+1].cells[2].paragraphs[0].text = resp
        format_custom_table(tbl_sr, [Inches(0.5), Inches(2.8), Inches(3.2)])
        
        # 4.x.3 Functional Requirements
        add_heading_3(doc, f"{feat['num']}.3 Functional Requirements")
        for req_id, req_stmt in feat['reqs']:
            add_bullet(doc, req_stmt, bold_prefix=f"{req_id}: ")
        add_p(doc, "", space_after=4)

    # ==================== 5. OTHER NONFUNCTIONAL REQUIREMENTS ====================
    add_heading_1(doc, "5. Other Nonfunctional Requirements")
    
    add_heading_2(doc, "5.1 Performance Requirements")
    add_p(doc, "Kebutuhan performa kuantitatif yang harus dipenuhi oleh sistem RTConnect:")
    add_bullet(doc, "Waktu tanggap (response time) sistem untuk pemuatan antarmuka, perenderan daftar riwayat, dan verifikasi login tidak boleh melebihi 2.0 detik pada koneksi internet minimal 5 Mbps.", "• Waktu Tanggap UI/API: ")
    add_bullet(doc, "Proses orkestrasi pemanggilan LLM untuk perumusan draf narasi surat dan pencarian kemiripan semantik RAG tidak boleh melebihi 5.0 detik.", "• Waktu Komputasi AI: ")
    add_bullet(doc, "Sistem harus mampu melayani hingga 50 pengguna aktif bersamaan (concurrent users) tanpa penurunan performa lebih dari 10%.", "• Kapasitas Beban Bersamaan: ")

    add_heading_2(doc, "5.2 Safety Requirements")
    add_bullet(doc, "Setiap transaksi perubahan status pengajuan surat dan penerbitan nomor surat resmi wajib dibungkus dalam mekanisme database transaction atomicity (ACID) untuk mencegah korupsi atau inkonsistensi nomor surat jika terjadi gangguan server.", "• Atomisitas Transaksi Basis Data: ")
    add_bullet(doc, "Basis data MySQL wajib dicadangkan (automated backup) setiap 24 jam sekali pada media penyimpanan terisolasi.", "• Pencadangan Data: ")

    add_heading_2(doc, "5.3 Security Requirements")
    add_bullet(doc, "Seluruh kata sandi pengguna wajib di-hash menggunakan algoritma bcrypt dengan work factor (cost) minimal 10 sebelum disimpan. Dilarang keras menyimpan password dalam teks polos.", "• Proteksi Kata Sandi: ")
    add_bullet(doc, "Sesi login menggunakan token JWT bertanda tangan digital algoritma HS256 dengan masa kedaluwarsa maksimal 24 jam.", "• Manajemen Sesi JWT: ")
    add_bullet(doc, "Seluruh endpoint yang mengubah data mewajibkan verifikasi hak akses peran (Role-Based Access Control) dan sanitasi parameter input untuk mencegah serangan SQL Injection dan Cross-Site Scripting (XSS).", "• Otorisasi & Sanitasi: ")

    add_heading_2(doc, "5.4 Software Quality Attributes")
    add_bullet(doc, "Desain antarmuka ditargetkan mencapai skor System Usability Scale (SUS) minimal 70 (kategori Good/Acceptable) serta mematuhi panduan kontras warna WCAG 2.1 AA.", "• Usability (Kebergunaan): ")
    add_bullet(doc, "Tingkat ketersediaan layanan sistem ditargetkan mencapai minimal 99.0% waktu operasional per bulan.", "• Availability (Ketersediaan): ")
    add_bullet(doc, "Arsitektur kode backend Flask mengikuti konvensi PEP-8 Python dan prinsip Clean Architecture / MVC untuk mempermudah pemeliharaan jangka panjang.", "• Maintainability (Kemudahan Pemeliharaan): ")

    add_heading_2(doc, "5.5 Business Rules")
    add_bullet(doc, "Hanya warga yang berdomisili sah di RT 032 RW 08 yang berhak mengajukan surat pengantar.", "• BR-01 Kelayakan Pemohon: ")
    add_bullet(doc, "Nomor surat resmi wajib mengikuti format baku sekretariat RT: '470/{NO}/032.08/{BULAN}/{TAHUN}'. Nomor surat tidak boleh diterbitkan sebelum disetujui Ketua RT.", "• BR-02 Format Nomor Surat: ")
    add_bullet(doc, "Ketua RT wajib mencantumkan alasan tertulis spesifik apabila memilih tindakan 'Tolak Pengajuan' atau 'Minta Revisi'.", "• BR-03 Kewajiban Alasan Penolakan/Revisi: ")
    add_bullet(doc, "Ambang batas kemiripan kosinus (cosine similarity threshold) untuk jawaban chatbot ditetapkan pasti pada angka 0.70. Di bawah nilai tersebut, sistem dilarang mengarang jawaban dan wajib mengaktifkan tautan eskalasi WhatsApp Ketua RT (Zero Hallucination Policy).", "• BR-04 Integritas Faktual Chatbot AI: ")

    # ==================== 6. OTHER REQUIREMENTS ====================
    add_heading_1(doc, "6. Other Requirements")
    
    add_heading_2(doc, "6.1 Database Requirements (CDM, PDM, & RAG Architecture)")
    add_p(doc, "Perancangan basis data RTConnect membedakan secara tegas antara pemodelan data konseptual (Conceptual Data Model / CDM) yang menggambarkan entitas bisnis sistem dengan pemodelan fisik (Physical Data Model / PDM) yang diimplementasikan pada MySQL 8.0.")
    
    add_callout(doc, "Audit & Resolusi Normalisasi Skema Akun Pengguna",
        "Pada draf versi awal dokumen project, tabel pengguna terpecah menjadi dua tabel fisik ('RT' dan 'Warga') yang memicu redundansi kolom (nik, nama, email, password_hash) dan memicu konflik logika pada Sequence Diagram Login yang memanggil objek tunggal :User. Pada versi final ini, struktur data telah dinormalisasi menjadi arsitektur tabel tunggal terpusat 'users' dengan atribut pembeda 'role' (enum: 'warga', 'rt', 'admin').")

    add_p(doc, "Kamus Data Fisik (Physical Data Dictionary) Skema Database MySQL RTConnect:")
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
    tbl_db = doc.add_table(rows=len(db_dict)+1, cols=3)
    tbl_db.rows[0].cells[0].paragraphs[0].text = "Nama Tabel"
    tbl_db.rows[0].cells[1].paragraphs[0].text = "Kolom Kunci & Atribut Utama"
    tbl_db.rows[0].cells[2].paragraphs[0].text = "Fungsi Bisnis & Relasi Entitas"
    for idx, (tname, cols, func) in enumerate(db_dict):
        tbl_db.rows[idx+1].cells[0].paragraphs[0].text = tname
        tbl_db.rows[idx+1].cells[1].paragraphs[0].text = cols
        tbl_db.rows[idx+1].cells[2].paragraphs[0].text = func
    format_custom_table(tbl_db, [Inches(1.2), Inches(2.8), Inches(2.5)])

    add_heading_3(doc, "Pembedaan Arsitektural: Knowledge Base (Markdown) vs Knowledge Chunk (Database RAG)")
    add_p(doc, "Untuk menjamin akurasi dan kemudahan tata kelola basis pengetahuan kecerdasan buatan, sistem menerapkan pemisahan peran yang tegas antara Knowledge Base tingkat makro dan Knowledge Chunk tingkat mikro:")
    add_bullet(doc, "Knowledge Base diwujudkan dalam bentuk berkas-berkas dokumentasi Markdown (.md) yang tersimpan pada direktori proyek (misal: /docs/knowledge_base/ atau RTConnect-KnowledgeBase/). Berkas ini memuat teks lengkap peraturan RT 032, keputusan musyawarah warga, SOP pengurusan surat, dan tata tertib lingkungan. Berkas Markdown ini menjadi sumber kebenaran tunggal (Single Source of Truth) yang mudah dibaca, disunting, dan dikontrol versinya (git version control) oleh pengurus RT atau pengembang tanpa harus mengubah kode sistem.", "1. Knowledge Base Makro (Berkas Markdown Master): ")
    add_bullet(doc, "Knowledge Chunk adalah representasi operasional hasil pemecahan (segmentasi) berkas Markdown menjadi segmen-segmen teks kecil berukuran 300-500 token dengan overlap 50 token. Setiap potongan dihitung nilai vektor embedding-nya menggunakan model text-embedding-3-small (1536 dimensi numerik) dan disimpan ke tabel 'knowledge_chunks' di MySQL. Data inilah yang digunakan secara real-time oleh mesin pencarian kosinus (Cosine Similarity) saat warga mengajukan pertanyaan pada Chatbot Tanya RT.", "2. Knowledge Chunk Mikro (Tabel Basis Data RAG): ")
    
    add_p(doc, "Rincian Data yang Wajib Diketahui Model LLM pada Kedua Fitur AI:")
    add_bullet(doc, "(a) Data Pemohon Dinamis: Nama lengkap, NIK 16 digit, alamat domisili, tempat/tanggal lahir, pekerjaan, dan maksud keperluan surat; (b) Grounding Template Resmi: Kop surat resmi RT 032 RW 08, format nomor surat klasifikasi 470, konsiderans pengantar baku, dan klausul penutup administratif; (c) Parameter Kontrol: Temperature diatur rendah (0.2 - 0.3) agar hasil draf konsisten, formal, dan deterministik.", "• Pada Fitur Formulasi Draf Dokumen Surat: ")
    add_bullet(doc, "(a) Konteks Pertanyaan Warga: Teks query warga dan riwayat obrolan sesi aktif; (b) Potongan Chunk Terpilih: Teks aturan resmi yang memiliki cosine similarity >= 0.70; (c) Prompt Sistem Zero-Hallucination: LLM diinstruksikan hanya menyusun jawaban berdasarkan rujukan chunk yang dilampirkan. Jika similarity < 0.70, sistem langsung mengaktifkan tombol eskalasi WhatsApp ke Ketua RT tanpa memanggil model LLM generatif.", "• Pada Fitur Chatbot Tanya RT: ")

    add_heading_2(doc, "6.2 Legal & Regulatory Compliance")
    add_p(doc, "Sistem RTConnect dibangun dengan mematuhi regulasi perundang-undangan nasional:")
    add_bullet(doc, "Pengesahan surat pengantar digital dengan stempel tanda tangan resmi RT dan kode hash verifikasi memenuhi ketentuan Pasal 11 mengenai keabsahan dan kekuatan hukum tanda tangan elektronik serta jaminan integritas dokumen elektronik.", "• UU ITE No. 1 Tahun 2024: ")
    add_bullet(doc, "Penyimpanan data kependudukan (NIK, Nama, Alamat, No Telepon) memenuhi standar perlindungan kerahasiaan dan privasi data kependudukan warga dengan enkripsi password satu arah dan proteksi hak akses terenkapsulasi.", "• UU PDP No. 27 Tahun 2022: ")

    add_heading_2(doc, "6.3 Requirement Traceability Matrix (RTM)")
    add_p(doc, "Matriks Keterlacakan Kebutuhan (Requirement Traceability Matrix / RTM) menghubungkan setiap kebutuhan fungsional (REQ-1 s/d REQ-22) dengan Use Case, User Story, Diagram UML, Tabel Basis Data, dan Layar GUI pendukung guna membuktikan integritas 100% tanpa adanya kebutuhan yang tidak terimplementasi:")
    
    rtm_rows = [
        ("REQ-1..4", "UC-01, UC-02", "US-01, US-02", "Act Register, Act Login", "Seq Register, Seq Login", "users", "SCREEN-002, 003"),
        ("REQ-5..8", "UC-03", "US-03", "Act Pengajuan Surat", "Seq Pengajuan Surat", "pengajuan_surat, jenis_surat", "SCREEN-007, 008"),
        ("REQ-9..11", "UC-03", "US-03", "Act Pengajuan Surat", "Seq Pengajuan Surat", "pengajuan_surat (draf_ai_konten)", "SCREEN-010"),
        ("REQ-12..14", "UC-05", "US-05", "Act Pengajuan Surat", "Seq Pengajuan Surat", "pengajuan_surat, users", "SCREEN-009, 010"),
        ("REQ-15..18", "UC-04, UC-05", "US-04, US-05", "Act Pengajuan Surat", "Seq Pengajuan Surat", "surat_final, pengajuan_surat", "SCREEN-010, 012"),
        ("REQ-19..22", "UC-06", "US-06", "Act Chatbot Tanya RT", "Seq Chatbot RAG", "knowledge_chunks, chat_messages", "SCREEN-011")
    ]
    tbl_rtm = doc.add_table(rows=len(rtm_rows)+1, cols=7)
    tbl_rtm.rows[0].cells[0].paragraphs[0].text = "Tag REQ"
    tbl_rtm.rows[0].cells[1].paragraphs[0].text = "Use Case"
    tbl_rtm.rows[0].cells[2].paragraphs[0].text = "User Story"
    tbl_rtm.rows[0].cells[3].paragraphs[0].text = "Activity Diagram"
    tbl_rtm.rows[0].cells[4].paragraphs[0].text = "Sequence Diagram"
    tbl_rtm.rows[0].cells[5].paragraphs[0].text = "Tabel Basis Data"
    tbl_rtm.rows[0].cells[6].paragraphs[0].text = "Layar GUI"
    for idx, (req_tag, uc, us, act, seq, db, scr) in enumerate(rtm_rows):
        tbl_rtm.rows[idx+1].cells[0].paragraphs[0].text = req_tag
        tbl_rtm.rows[idx+1].cells[1].paragraphs[0].text = uc
        tbl_rtm.rows[idx+1].cells[2].paragraphs[0].text = us
        tbl_rtm.rows[idx+1].cells[3].paragraphs[0].text = act
        tbl_rtm.rows[idx+1].cells[4].paragraphs[0].text = seq
        tbl_rtm.rows[idx+1].cells[5].paragraphs[0].text = db
        tbl_rtm.rows[idx+1].cells[6].paragraphs[0].text = scr
    format_custom_table(tbl_rtm, [Inches(1.0), Inches(0.9), Inches(0.9), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.0)])

    # ==================== APPENDIX A: GLOSSARY ====================
    doc.add_page_break()
    add_heading_1(doc, "Appendix A: Glossary")
    add_p(doc, "Daftar istilah teknis, akronim, dan singkatan yang digunakan di dalam dokumen ini:")
    tbl_abbr = doc.add_table(rows=len(ABBREVIATIONS)+1, cols=2)
    tbl_abbr.rows[0].cells[0].paragraphs[0].text = "Istilah / Singkatan"
    tbl_abbr.rows[0].cells[1].paragraphs[0].text = "Definisi & Penjelasan Konseptual"
    for idx, (abbr, desc) in enumerate(ABBREVIATIONS):
        tbl_abbr.rows[idx+1].cells[0].paragraphs[0].text = abbr
        tbl_abbr.rows[idx+1].cells[1].paragraphs[0].text = desc
    format_custom_table(tbl_abbr, [Inches(1.5), Inches(5.0)])

    # ==================== APPENDIX B: ANALYSIS MODELS ====================
    doc.add_page_break()
    add_heading_1(doc, "Appendix B: Analysis Models")
    add_p(doc, "Lampiran ini menyajikan secara lengkap seluruh artefak model analisis perangkat lunak RTConnect yang telah disempurnakan berdasarkan 4 arahan revisi dosen pengampu.")

    # B.1 BPMN
    add_heading_2(doc, "B.1 Business Process Models (BPMN AS-IS & TO-BE)")
    add_p(doc, "Pemodelan proses bisnis membandingkan alur eksisting konvensional dengan alur usulan sistem RTConnect. Setiap aktivitas tugas (Task) dilengkapi metadata Input dan Output yang presisi, dan setiap titik percabangan keputusan ditandai dengan gateway eksplisit [XOR] sesuai Feedback Dosen #2.")
    
    add_diagram_image(doc, "diagrams/bpmn_as_is.png", "Gambar B.1 BPMN AS-IS Proses Pengajuan Surat Pengantar Konvensional")
    add_p(doc, "Tabel Metadata Input dan Output Tugas pada BPMN AS-IS:")
    tbl_asis = doc.add_table(rows=len(BPMN_TASKS_AS_IS)+1, cols=5)
    tbl_asis.rows[0].cells[0].paragraphs[0].text = "ID Task"
    tbl_asis.rows[0].cells[1].paragraphs[0].text = "Nama Aktivitas"
    tbl_asis.rows[0].cells[2].paragraphs[0].text = "Pelaksana"
    tbl_asis.rows[0].cells[3].paragraphs[0].text = "Input Data"
    tbl_asis.rows[0].cells[4].paragraphs[0].text = "Output Data"
    for idx, (tid, tname, actor, tinp, tout) in enumerate(BPMN_TASKS_AS_IS):
        tbl_asis.rows[idx+1].cells[0].paragraphs[0].text = tid
        tbl_asis.rows[idx+1].cells[1].paragraphs[0].text = tname
        tbl_asis.rows[idx+1].cells[2].paragraphs[0].text = actor
        tbl_asis.rows[idx+1].cells[3].paragraphs[0].text = tinp
        tbl_asis.rows[idx+1].cells[4].paragraphs[0].text = tout
    format_custom_table(tbl_asis, [Inches(0.8), Inches(1.8), Inches(0.9), Inches(1.5), Inches(1.5)])

    add_diagram_image(doc, "diagrams/bpmn_to_be.png", "Gambar B.2 BPMN TO-BE Pengajuan Surat Pengantar RTConnect (AI Drafting & Dual-Path)")
    add_p(doc, "Tabel Metadata Input dan Output Tugas pada BPMN TO-BE:")
    tbl_tobe = doc.add_table(rows=len(BPMN_TASKS_TO_BE)+1, cols=5)
    tbl_tobe.rows[0].cells[0].paragraphs[0].text = "ID Task"
    tbl_tobe.rows[0].cells[1].paragraphs[0].text = "Nama Aktivitas"
    tbl_tobe.rows[0].cells[2].paragraphs[0].text = "Pelaksana"
    tbl_tobe.rows[0].cells[3].paragraphs[0].text = "Input Data"
    tbl_tobe.rows[0].cells[4].paragraphs[0].text = "Output Data"
    for idx, (tid, tname, actor, tinp, tout) in enumerate(BPMN_TASKS_TO_BE):
        tbl_tobe.rows[idx+1].cells[0].paragraphs[0].text = tid
        tbl_tobe.rows[idx+1].cells[1].paragraphs[0].text = tname
        tbl_tobe.rows[idx+1].cells[2].paragraphs[0].text = actor
        tbl_tobe.rows[idx+1].cells[3].paragraphs[0].text = tinp
        tbl_tobe.rows[idx+1].cells[4].paragraphs[0].text = tout
    format_custom_table(tbl_tobe, [Inches(0.8), Inches(1.8), Inches(0.9), Inches(1.5), Inches(1.5)])

    add_diagram_image(doc, "diagrams/bpmn_as_is_tanyart.png", "Gambar B.3 BPMN AS-IS Tanya RT via Pesan Instan")
    add_diagram_image(doc, "diagrams/bpmn_to_be_tanyart.png", "Gambar B.4 BPMN TO-BE Tanya RT Cerdas RAG & Eskalasi WhatsApp")

    # B.2 Use Case Model
    add_heading_2(doc, "B.2 Use Case Model & Detailed Specifications")
    add_p(doc, "Use Case Diagram telah disempurnakan sesuai Feedback Dosen #1: (1) Mengeliminasi use case mandiri 'Mengisi Ulang Form (Revisi)'; (2) Menyederhanakan proses tanda tangan digital dan basah menjadi bagian terpadu dari 'Menindaklanjuti Pengajuan Surat'; serta (3) Menghapus 'Menjawab Pertanyaan Warga' bagi Ketua RT karena eskalasi WhatsApp dimodelkan sebagai system behavior pada alur chatbot.")
    add_diagram_image(doc, "diagrams/use_case_diagram.png", "Gambar B.5 Use Case Diagram RTConnect Hasil Penyempurnaan")

    for uc in USE_CASE_SPECS:
        add_heading_3(doc, f"Spesifikasi {uc['id']}: {uc['name']}")
        t_uc = doc.add_table(rows=5, cols=2)
        t_uc.rows[0].cells[0].paragraphs[0].text = "Nama Use Case"
        t_uc.rows[0].cells[1].paragraphs[0].text = f"{uc['id']}: {uc['name']}"
        t_uc.rows[1].cells[0].paragraphs[0].text = "Aktor Utama"
        t_uc.rows[1].cells[1].paragraphs[0].text = uc['actor']
        t_uc.rows[2].cells[0].paragraphs[0].text = "Deskripsi"
        t_uc.rows[2].cells[1].paragraphs[0].text = uc['desc']
        t_uc.rows[3].cells[0].paragraphs[0].text = "Kondisi Awal (Preconditions)"
        t_uc.rows[3].cells[1].paragraphs[0].text = uc['precondition']
        t_uc.rows[4].cells[0].paragraphs[0].text = "Kondisi Akhir (Postconditions)"
        t_uc.rows[4].cells[1].paragraphs[0].text = uc['postcondition']
        format_custom_table(t_uc, [Inches(1.8), Inches(4.7)])
        
        add_p(doc, "Alur Utama (Main Flow):", italic=True, space_after=2)
        t_mf = doc.add_table(rows=len(uc['main_flow'])+1, cols=2)
        t_mf.rows[0].cells[0].paragraphs[0].text = "Aktor / Pelaksana"
        t_mf.rows[0].cells[1].paragraphs[0].text = "Langkah Aksi Sistem / Pengguna"
        for idx, (actor_step, step_desc) in enumerate(uc['main_flow']):
            t_mf.rows[idx+1].cells[0].paragraphs[0].text = actor_step
            t_mf.rows[idx+1].cells[1].paragraphs[0].text = step_desc
        format_custom_table(t_mf, [Inches(1.8), Inches(4.7)])
        
        if uc['alt_flow']:
            add_p(doc, "Alur Alternatif (Alternative Flow):", italic=True, space_after=2)
            for af_title, af_desc in uc['alt_flow']:
                add_bullet(doc, af_desc, bold_prefix=f"{af_title}: ")
        if uc['exc_flow']:
            add_p(doc, "Alur Eksepsi (Exception Flow):", italic=True, space_after=2)
            for ef_title, ef_desc in uc['exc_flow']:
                add_bullet(doc, ef_desc, bold_prefix=f"{ef_title}: ")
        add_p(doc, "", space_after=4)

    # B.3 User Stories
    add_heading_2(doc, "B.3 User Stories & BDD Scenarios")
    for us in USER_STORIES_DATA:
        add_bullet(doc, f"Sebagai {us['role']}, saya ingin {us['action']}, sehingga {us['benefit']}.", bold_prefix=f"[{us['id']}] ")
        for sc in us['scenarios']:
            add_p(doc, f"Scenario: {sc['title']}", italic=True, space_after=2)
            add_p(doc, f"Given {sc['given']}")
            add_p(doc, f"When {sc['when']}")
            if 'and' in sc:
                add_p(doc, f"And {sc['and']}")
            add_p(doc, f"Then {sc['then']}")
            add_p(doc, "", space_after=3)

    # B.4 Activity Diagrams
    add_heading_2(doc, "B.4 Activity Diagrams")
    add_diagram_image(doc, "diagrams/activity_register.png", "Gambar B.6 Activity Diagram Registrasi Akun Warga Mandiri")
    add_diagram_image(doc, "diagrams/activity_login.png", "Gambar B.7 Activity Diagram Login ke Sistem")
    add_diagram_image(doc, "diagrams/activity_pengajuan_surat.png", "Gambar B.8 Activity Diagram Pengajuan dan Pemrosesan Surat Pengantar (AI & Dual-Path)")
    add_diagram_image(doc, "diagrams/activity_chatbot.png", "Gambar B.9 Activity Diagram Chatbot Tanya RT & Eskalasi WhatsApp")

    # B.5 Sequence Diagrams
    add_heading_2(doc, "B.5 Sequence Diagrams (Boundary-Control-Entity)")
    add_callout(doc, "Penerapan Feedback Dosen #3 & #4",
        "Pesan interaksi dari Aktor ke Boundary sepenuhnya menggunakan narasi bahasa manusia murni (tanpa kode atau method call). Seluruh aktor dilengkapi active bar (activation lifeline) saat berinteraksi.")
    add_diagram_image(doc, "diagrams/sequence_register.png", "Gambar B.10 Sequence Diagram Registrasi Akun")
    add_diagram_image(doc, "diagrams/sequence_login.png", "Gambar B.11 Sequence Diagram Login ke Sistem")
    add_diagram_image(doc, "diagrams/sequence_pengajuan_surat.png", "Gambar B.12 Sequence Diagram Pengajuan dan Tindak Lanjut Surat Pengantar", width_inch=5.4)
    add_diagram_image(doc, "diagrams/sequence_chatbot.png", "Gambar B.13 Sequence Diagram Chatbot Tanya RT (RAG & Eskalasi WhatsApp)")

    # B.6 Class Diagram
    add_heading_2(doc, "B.6 Domain & Class Diagrams")
    add_diagram_image(doc, "diagrams/class_diagram.png", "Gambar B.14 Class Diagram RTConnect Terpadu (Entity & Service Layer)")

    # B.7 Data Models (ERD)
    add_heading_2(doc, "B.7 Data Models (Conceptual & Physical ERD)")
    add_diagram_image(doc, "diagrams/database_er_diagram.png", "Gambar B.15 Entity Relationship Diagram (ERD / CDM & PDM)")

    # B.8 System Architecture
    add_heading_2(doc, "B.8 System Architecture & Deployment Diagram")
    add_diagram_image(doc, "diagrams/system_architecture.png", "Gambar B.16 System Architecture & Deployment Diagram RTConnect")

    # ==================== APPENDIX C: TBD LIST ====================
    doc.add_page_break()
    add_heading_1(doc, "Appendix C: To Be Determined (TBD) List")
    add_p(doc, "Daftar butir terbuka (TBD List) yang akan disepakati lebih lanjut pada fase pengujian sistem lapangan:")
    tbd_items = [
        ("TBD-1", "Batas Maksimal Kuota Harian Pengajuan Surat", "Penentuan batas maksimal frekuensi permohonan surat per NIK dalam satu hari untuk mencegah spamming."),
        ("TBD-2", "Waktu Retensi Otomatis Arsip Berkas Pengajuan", "Penetapan jadwal pembersihan berkas lampiran KTP/KK lama dari penyimpanan server (apakah 1 tahun atau 2 tahun)."),
        ("TBD-3", "Penyediaan Penyimpanan Vector Database Khusus", "Evaluasi migrasi penyimpanan vektor embedding dari kolom JSON MySQL ke ekstensi pgvector atau ChromaDB jika jumlah warga melebihi 1.000 kepala keluarga.")
    ]
    tbl_tbd = doc.add_table(rows=len(tbd_items)+1, cols=3)
    tbl_tbd.rows[0].cells[0].paragraphs[0].text = "ID TBD"
    tbl_tbd.rows[0].cells[1].paragraphs[0].text = "Topik Spesifikasi"
    tbl_tbd.rows[0].cells[2].paragraphs[0].text = "Rencana Tindak Lanjut Evaluasi"
    for idx, (tbd_id, top, nts) in enumerate(tbd_items):
        tbl_tbd.rows[idx+1].cells[0].paragraphs[0].text = tbd_id
        tbl_tbd.rows[idx+1].cells[1].paragraphs[0].text = top
        tbl_tbd.rows[idx+1].cells[2].paragraphs[0].text = nts
    format_custom_table(tbl_tbd, [Inches(1.0), Inches(2.2), Inches(3.3)])

    # ==================== APPENDIX D: TEAM CONTRIBUTION ====================
    doc.add_page_break()
    add_heading_1(doc, "Appendix D: Team Member Contribution Table")
    add_p(doc, "Tabel kontribusi anggota kelompok dalam perancangan dan penyusunan spesifikasi teknis RTConnect:")
    tbl_contrib = doc.add_table(rows=len(CONTRIBUTION_DATA)+1, cols=5)
    tbl_contrib.rows[0].cells[0].paragraphs[0].text = "No"
    tbl_contrib.rows[0].cells[1].paragraphs[0].text = "Nama Lengkap"
    tbl_contrib.rows[0].cells[1].paragraphs[0].runs[0].font.name = 'Segoe UI'
    tbl_contrib.rows[0].cells[2].paragraphs[0].text = "NIM"
    tbl_contrib.rows[0].cells[3].paragraphs[0].text = "Foto"
    tbl_contrib.rows[0].cells[4].paragraphs[0].text = "Rincian Kontribusi Proyek"
    for idx, (no, name, nim, foto, kontribusi) in enumerate(CONTRIBUTION_DATA):
        tbl_contrib.rows[idx+1].cells[0].paragraphs[0].text = no
        tbl_contrib.rows[idx+1].cells[1].paragraphs[0].text = name
        tbl_contrib.rows[idx+1].cells[2].paragraphs[0].text = nim
        tbl_contrib.rows[idx+1].cells[3].paragraphs[0].text = foto
        tbl_contrib.rows[idx+1].cells[4].paragraphs[0].text = kontribusi
    format_custom_table(tbl_contrib, [Inches(0.4), Inches(1.8), Inches(1.1), Inches(1.4), Inches(1.8)])

    # Save document
    doc.save(output_filename)
    print(f"SUCCESS: {output_filename} berhasil dibuat dan disimpan!")

if __name__ == '__main__':
    generate_wiegers_srs_docx()
