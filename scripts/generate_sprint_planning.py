# -*- coding: utf-8 -*-
import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

template_path = r"C:\Users\Dhafin\.gemini\antigravity\brain\56bf70b8-f618-45b9-8fa9-793e5a71de31\.user_uploaded\media_1792039732799_37db1d9c.docx"
output_docx_path = os.path.abspath(r"monitoring\Sprint_Planning_Minggu_9_Kelompok_3.docx")
output_pdf_path = os.path.abspath(r"monitoring\Sprint_Planning_Minggu_9_Kelompok_3.pdf")

doc = docx.Document(template_path)

# Consistent Palette
COLOR_HEADER_BG = "1F497D"      # Dark Navy Blue
COLOR_SUBHEADER_BG = "2E5B94"   # Secondary Blue
COLOR_ZEBRA_BG = "F4F7FA"       # Subtle zebra gray/blue
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_TEXT = RGBColor(40, 40, 40)
COLOR_NAVY = RGBColor(31, 73, 125)
COLOR_BORDER = "CCCCCC"

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def style_cell(cell, text, bold=False, italic=False, font_size=10, font_name="Times New Roman", 
               align=WD_ALIGN_PARAGRAPH.LEFT, v_align=WD_ALIGN_VERTICAL.CENTER, 
               bg_color=None, text_color=COLOR_TEXT):
    cell.text = ""
    cell.vertical_alignment = v_align
    set_cell_margins(cell, top=100, bottom=100, left=130, right=130)
    
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i == 0:
            p = cell.paragraphs[0]
        else:
            p = cell.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        
        run = p.add_run(line)
        run.bold = bold
        run.italic = italic
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.color.rgb = text_color
    
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

print("1. Populating Table 0: Effort Estimation...")
t0 = doc.tables[0]
t0.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t0, color=COLOR_BORDER)

# Clear placeholder rows in t0
while len(t0.rows) > 1:
    t0._tbl.remove(t0.rows[-1]._tr)

col_widths_t0 = [Inches(3.8), Inches(1.2), Inches(1.6)]
headers_t0 = ["Backlog Item", "Priority", "Effort (T-shirt size)"]
for col_idx, text in enumerate(headers_t0):
    t0.rows[0].cells[col_idx].width = col_widths_t0[col_idx]
    style_cell(t0.rows[0].cells[col_idx], text, bold=True, font_size=10.5, 
               align=WD_ALIGN_PARAGRAPH.CENTER, bg_color=COLOR_HEADER_BG, text_color=COLOR_WHITE)

backlog_items = [
    ("PB-01", "Inisialisasi Arsitektur & Skema Basis Data MySQL", 
     "Setup repository monorepo, konfigurasi Flask, DDL tabel (User, Warga, RT, PengajuanSurat, LogStatus, KnowledgeChunk), dan koneksi basis data.", 
     "High", "M (2)"),
    ("PB-02", "Autentikasi & Otorisasi Pengguna Multi-Role", 
     "Registrasi akun warga, login multi-role (Warga dan Ketua RT), proteksi password hash (bcrypt), dan manajemen sesi JWT.", 
     "High", "M (2)"),
    ("PB-03", "Antarmuka Formulir Pengajuan Surat Mandiri", 
     "UI form dinamis pemilihan jenis surat, keperluan, metode tanda tangan (digital/basah), dan validasi kelengkapan isian warga.", 
     "High", "L (3)"),
    ("PB-04", "Endpoint API Pengajuan Surat & Upload Berkas", 
     "REST API pengajuan surat, penanganan upload lampiran pendukung (KTP/KK max 2MB), validasi format, dan persistensi berkas.", 
     "High", "M (2)"),
    ("PB-05", "Integrasi Generative AI Draf Narasi Surat", 
     "Pipeline otomatisasi LLM untuk menyusun draf narasi surat resmi berdasarkan keperluan warga dengan mekanisme prompt grounding & fallback.", 
     "Medium", "XL (4)"),
    ("PB-06", "Dashboard & Daftar Antrean Surat Ketua RT", 
     "Antarmuka ringkasan statistik layanan RT dan daftar antrean pengajuan surat warga (filter status, pencarian, badge status).", 
     "High", "M (2)"),
    ("PB-07", "Antarmuka Peninjauan Berkas & Editor Draf Surat", 
     "Modal review dokumen pengajuan, viewer berkas lampiran warga, dan antarmuka penyuntingan draf narasi surat AI oleh Ketua RT.", 
     "High", "M (2)"),
    ("PB-08", "Logika Bisnis Tindak Lanjut Surat (Setuju, Revisi, Tolak)", 
     "Penerbitan nomor surat resmi, alur catatan revisi (warga dapat mengisi ulang form), serta pencatatan alasan penolakan surat.", 
     "High", "L (3)"),
    ("PB-09", "Mekanisme Otorisasi PIN TTD Digital & Alur Basah", 
     "Modal otorisasi PIN rahasia Ketua RT untuk approval TTD digital, proteksi keamanan, dan routing informasi fisik untuk tanda tangan basah.", 
     "High", "L (3)"),
    ("PB-10", "Mesin Generator PDF Surat Resmi & QR Verifikasi", 
     "Penerbitan berkas PDF resmi (ReportLab), penyematan stempel digital, hash SHA-256 dokumen, dan QR code verifikasi keaslian.", 
     "High", "L (3)"),
    ("PB-11", "Antarmuka Riwayat, Pratinjau, & Download Warga", 
     "Daftar riwayat pengajuan surat warga, in-app PDF previewer, pengunduhan file PDF surat digital, dan kartu info pengambilan surat basah.", 
     "High", "M (2)"),
    ("PB-12", "Parser, Chunking, & Ingestion Knowledge Base Markdown", 
     "Modul pembaca dokumen Markdown panduan administrasi RT/RW, text chunking terstruktur, metadata tagging, dan embedding semantik.", 
     "High", "L (3)"),
    ("PB-13", "Chatbot TanyaRT (NLP/RAG) & Eskalasi WhatsApp", 
     "Antarmuka interaktif chat, semantic search (cosine similarity >= 0.70), prompt anti-halusinasi, dan tombol deep-link WhatsApp Ketua RT.", 
     "High", "XL (4)"),
    ("PB-14", "Pengujian BDD (Behat Gherkin) & Verifikasi DoD UAS", 
     "Penyusunan skenario BDD (Given-When-Then), pengujian fungsionalitas end-to-end, dan pemenuhan seluruh kriteria Definition of Done UAS.", 
     "Medium", "M (2)")
]

for idx, (pb_id, title, desc, prio, effort) in enumerate(backlog_items):
    row = t0.add_row()
    bg = COLOR_ZEBRA_BG if idx % 2 == 1 else None
    
    cell_0 = row.cells[0]
    cell_0.width = col_widths_t0[0]
    style_cell(cell_0, f"{pb_id}: {title}\n{desc}", bold=False, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=bg)
    cell_0.paragraphs[0].runs[0].bold = True
    
    cell_1 = row.cells[1]
    cell_1.width = col_widths_t0[1]
    style_cell(cell_1, prio, bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color=bg)
    
    cell_2 = row.cells[2]
    cell_2.width = col_widths_t0[2]
    style_cell(cell_2, effort, bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color=bg)

# Update paragraphs around Table 0
for p in doc.paragraphs:
    if "Total Effort:" in p.text:
        p.text = "Total Effort: 34 Story Points (14 Backlog Items: 7 Medium, 5 Large, 2 Extra Large)"
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(11)
        p.runs[0].bold = True
    elif "S(1) - M(2) - L(3) - XL(4) - XXL(5)" in p.text:
        p.text = "Skala Konversi: S(1) - M(2) - L(3) - XL(4) - XXL(5)"
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(10.5)
        p.runs[0].italic = True

print("2. Populating Table 1: Sprint Planning...")
t1 = doc.tables[1]
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t1, color=COLOR_BORDER)

while len(t1.rows) > 1:
    t1._tbl.remove(t1.rows[-1]._tr)

col_widths_t1 = [Inches(1.8), Inches(4.8)]
headers_t1 = ["Sprint & Waktu", "Feature, Cakupan Backlog, & Deliverables"]
for col_idx, text in enumerate(headers_t1):
    t1.rows[0].cells[col_idx].width = col_widths_t1[col_idx]
    style_cell(t1.rows[0].cells[col_idx], text, bold=True, font_size=10.5, 
               align=WD_ALIGN_PARAGRAPH.CENTER, bg_color=COLOR_HEADER_BG, text_color=COLOR_WHITE)

bullet = "-"
dash = "-"

sprint_data = [
    (f"Sprint 1\n(Minggu 10 - 11)\n\nEstimasi:\n13 Story Points", 
     f"Fitur Utama: Feature 1 {dash} Mengajukan Surat Pengantar & Pondasi Sistem\n\n"
     f"{bullet} PB-01: Inisialisasi Arsitektur, Repositori Monorepo, & Skema Basis Data MySQL (M / 2 pts)\n"
     f"{bullet} PB-02: Manajemen Autentikasi Pengguna Multi-Role (Warga & Ketua RT) via JWT (M / 2 pts)\n"
     f"{bullet} PB-03: Antarmuka Formulir Pengajuan Surat Mandiri oleh Warga (L / 3 pts)\n"
     f"{bullet} PB-04: Endpoint API Pengajuan Surat & Penanganan Upload Berkas Lampiran (M / 2 pts)\n"
     f"{bullet} PB-05: Integrasi Generative AI Pembuatan Draf Narasi Surat Pengantar Otomatis (XL / 4 pts)\n\n"
     f"Sprint Goal: Menghasilkan fungsionalitas pengajuan surat mandiri oleh warga, termasuk registrasi/login, pengisian formulir terintegrasi berkas lampiran, dan formulasi otomatis draf narasi surat berbasis Generative AI."),
    
    (f"Sprint 2\n(Minggu 12 - 13)\n\nEstimasi:\n10 Story Points", 
     f"Fitur Utama: Feature 2 {dash} Meninjau dan Menindaklanjuti Pengajuan Surat oleh RT\n\n"
     f"{bullet} PB-06: Antarmuka Dashboard & Antrean Pengajuan Surat Masuk Ketua RT (M / 2 pts)\n"
     f"{bullet} PB-07: Antarmuka Peninjauan Berkas Lampiran & Editor Penyuntingan Draf AI (M / 2 pts)\n"
     f"{bullet} PB-08: Logika Bisnis Tindak Lanjut Surat (Setuju, Revisi, Tolak) & Penomoran Resmi (L / 3 pts)\n"
     f"{bullet} PB-09: Mekanisme Otorisasi PIN Tanda Tangan Digital & Alur Pengambilan Surat Basah (L / 3 pts)\n\n"
     f"Sprint Goal: Menghasilkan modul operasional Ketua RT untuk memverifikasi berkas warga, menyunting draf narasi surat, mengotorisasi persetujuan dengan PIN tanda tangan digital, atau memberikan catatan revisi yang dapat diperbaiki kembali oleh warga."),
    
    (f"Sprint 3\n(Minggu 14 - 15)\n\nEstimasi:\n14 Story Points", 
     f"Fitur Utama:\n{bullet} Feature 3 {dash} Mendownload Surat Pengantar & Penerbitan Dokumen Resmi\n{bullet} Feature 4 {dash} Bertanya Kepada Chatbot TanyaRT (NLP & RAG) & Eskalasi WhatsApp\n\n"
     f"{bullet} PB-10: Mesin Generator PDF Surat Resmi (ReportLab), Stempel TTD, & QR Hash Verifikasi (L / 3 pts)\n"
     f"{bullet} PB-11: Antarmuka Riwayat, In-App PDF Viewer, & Pengunduhan Surat Warga (M / 2 pts)\n"
     f"{bullet} PB-12: Parser, Chunking, & Ingestion Knowledge Base Administrasi RT/RW Markdown (L / 3 pts)\n"
     f"{bullet} PB-13: Engine Chatbot TanyaRT (Semantic Search Cosine >= 0.70) & Eskalasi WhatsApp (XL / 4 pts)\n"
     f"{bullet} PB-14: Otomasi Pengujian BDD (Behat Gherkin) & Verifikasi Definition of Done (DoD) UAS (M / 2 pts)\n\n"
     f"Sprint Goal: Menyelesaikan penerbitan dan pengunduhan dokumen PDF resmi ber-QR code, mengimplementasikan Chatbot TanyaRT berbasis RAG dengan eskalasi WhatsApp, serta menjalankan pengujian menyeluruh hingga working software siap dievaluasi Product Owner.")
]

for idx, (sprint_info, content) in enumerate(sprint_data):
    row = t1.add_row()
    bg = COLOR_ZEBRA_BG if idx % 2 == 1 else None
    
    cell_0 = row.cells[0]
    cell_0.width = col_widths_t1[0]
    style_cell(cell_0, sprint_info, bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color=bg)
    
    cell_1 = row.cells[1]
    cell_1.width = col_widths_t1[1]
    style_cell(cell_1, content, bold=False, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=bg)

print("3. Adding Supplementary Section: Feature Ownership Matrix...")
def add_section_heading(document, title_text):
    p = document.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(title_text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

add_section_heading(doc, "PEMBAGIAN TANGGUNG JAWAB FITUR PER ANGGOTA")
p_desc = doc.add_paragraph()
p_desc.paragraph_format.space_after = Pt(6)
p_desc.paragraph_format.line_spacing = 1.15
r_desc = p_desc.add_run(
    "Sesuai Poin 3 Panduan Program Monitoring PPL Praktikum Pasca UTS, pembagian kerja tim dilakukan berdasarkan "
    "fitur utama yang terdapat pada Use Case Diagram. Setiap anggota kelompok bertanggung jawab penuh terhadap seluruh "
    "artefak perancangan (Use Case Specification, User Story Scenario format Behat, Activity Diagram, Sequence Diagram BCE, "
    "GUI Design, Database) serta implementasi modul perangkat lunak terkait hingga pengujian."
)
r_desc.font.name = "Times New Roman"
r_desc.font.size = Pt(10.5)

t_matrix = doc.add_table(rows=1, cols=4)
t_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t_matrix, color=COLOR_BORDER)

col_widths_matrix = [Inches(1.8), Inches(1.1), Inches(1.7), Inches(2.0)]
headers_matrix = ["Nama Anggota", "NIM", "Fitur Use Case (PIC Penuh)", "Cakupan Artefak & Implementasi"]

for c_idx, text in enumerate(headers_matrix):
    t_matrix.rows[0].cells[c_idx].width = col_widths_matrix[c_idx]
    style_cell(t_matrix.rows[0].cells[c_idx], text, bold=True, font_size=10, 
               align=WD_ALIGN_PARAGRAPH.CENTER, bg_color=COLOR_HEADER_BG, text_color=COLOR_WHITE)

matrix_data = [
    ("Muhammad Nafidz Arradhin", "187241027", 
     f"Feature 1:\nMengajukan Surat Pengantar", 
     f"{bullet} Artefak: Use Case Spec, Activity Diagram, Sequence Diagram BCE, GUI Form Pengajuan.\n"
     f"{bullet} Implementasi: Form pengajuan surat dinamis, upload berkas warga, validasi klien/server, dan formulasi draf narasi Generative AI."),
    
    ("Mirza Diwa Luscakson", "187241042", 
     f"Feature 2:\nMeninjau dan Menindaklanjuti Pengajuan Surat", 
     f"{bullet} Artefak: Use Case Spec, Activity Diagram, Sequence Diagram BCE, GUI Dashboard RT.\n"
     f"{bullet} Implementasi: Antrean surat Ketua RT, peninjauan lampiran, editor draf AI, aksi Setuju/Revisi/Tolak, serta PIN otorisasi TTD digital."),
    
    ("Febrian Muhammad Yudhistira", "187241051", 
     f"Feature 3:\nMendownload Surat Pengantar & Penerbitan Dokumen", 
     f"{bullet} Artefak: Use Case Spec, Activity Diagram, Sequence Diagram BCE, GUI Viewer & Riwayat.\n"
     f"{bullet} Implementasi: Engine PDF ReportLab, stempel TTD digital, hash SHA-256 dokumen, QR code keaslian, in-app viewer, dan info surat basah."),
    
    ("Ahmad Dhafin Al Farisy", "187241057", 
     f"Feature 4:\nBertanya Kepada Chatbot TanyaRT & Eskalasi WhatsApp", 
     f"{bullet} Artefak: Use Case Spec, Activity Diagram, Sequence Diagram BCE, GUI Chatbot.\n"
     f"{bullet} Implementasi: Ingestion & chunking basis pengetahuan Markdown, pencarian semantik (cosine similarity >= 0.70), prompt anti-halusinasi, dan eskalasi WhatsApp.")
]

for idx, (nama, nim, fitur, cakupan) in enumerate(matrix_data):
    row = t_matrix.add_row()
    bg = COLOR_ZEBRA_BG if idx % 2 == 1 else None
    
    style_cell(row.cells[0], nama, bold=True, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=bg)
    row.cells[0].width = col_widths_matrix[0]
    
    style_cell(row.cells[1], nim, bold=False, font_size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color=bg)
    row.cells[1].width = col_widths_matrix[1]
    
    style_cell(row.cells[2], fitur, bold=True, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=bg)
    row.cells[2].width = col_widths_matrix[2]
    
    style_cell(row.cells[3], cakupan, bold=False, font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=bg)
    row.cells[3].width = col_widths_matrix[3]

print("4. Adding Supplementary Section: Definition of Done (DoD) UAS Checklist...")
add_section_heading(doc, "DEFINITION OF DONE (DoD) & STRATEGI EVALUASI AKHIR (UAS)")
p_dod = doc.add_paragraph()
p_dod.paragraph_format.space_after = Pt(6)
p_dod.paragraph_format.line_spacing = 1.15
r_dod = p_dod.add_run(
    "Mengacu pada Poin 5 Panduan Program Monitoring PPL Praktikum Pasca UTS, seluruh anggota tim berkomitmen "
    "memenuhi 5 kriteria Definition of Done (DoD) sebagai syarat kelulusan evaluasi akhir (UAS):"
)
r_dod.font.name = "Times New Roman"
r_dod.font.size = Pt(10.5)

dod_items = [
    ("1. Working Software", "Perangkat lunak RTConnect dapat dieksekusi secara nyata tanpa crash pada lingkungan lokal/web, mencakup backend Flask (REST API, basis data MySQL, integrasi AI) dan frontend web/mobile Flutter yang responsif."),
    ("2. Product Owner Approval", "Pada sesi evaluasi akhir, Product Owner / Dosen Penguji telah menguji seluruh alur kerja sistem dan memberikan persetujuan resmi bahwa seluruh fitur berfungsi secara tepat sesuai spesifikasi kebutuhan."),
    ("3. Pertanggungjawaban Fitur Individu", "Setiap mahasiswa menyelesaikan penuh fitur use case yang ditugaskan kepadanya, mulai dari pembaruan artefak perancangan hingga kode program implementasi dan pengujian modul terkait."),
    ("4. Kelengkapan Artefak PlantUML di Repositori GitHub", "Seluruh teks sumber PlantUML disimpan rapi di repositori GitHub project pada folder /uml dan /diagrams, meliputi: Use Case Diagram & Specification, User Story & Scenario (standar Behat), GUI Wireframes, CDM/PDM Database, Activity Diagram, Sequence Diagram BCE (Boundary-Control-Entity), serta Class Diagram."),
    ("5. Pengujian BDD (Behavior Driven Development) & Test Execution Run", "Skenario pengujian disusun menggunakan format Gherkin Behat standar (Given-When-Then-And) yang diturunkan dari User Story Scenario. Hasil eksekusi test runner (pass/fail status) dilampirkan secara transparan dalam laporan akhir.")
]

for title, desc in dod_items:
    p_item = doc.add_paragraph()
    p_item.paragraph_format.left_indent = Inches(0.2)
    p_item.paragraph_format.space_before = Pt(2)
    p_item.paragraph_format.space_after = Pt(4)
    p_item.paragraph_format.line_spacing = 1.15
    
    r_t = p_item.add_run(f"{bullet} {title}: ")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(10)
    r_t.bold = True
    
    r_d = p_item.add_run(desc)
    r_d.font.name = "Times New Roman"
    r_d.font.size = Pt(10)

doc.save(output_docx_path)
print(f"Sprint Planning DOCX saved to: {output_docx_path}")

print("5. Converting DOCX to PDF using docx2pdf...")
try:
    from docx2pdf import convert
    convert(output_docx_path, output_pdf_path)
    print(f"Sprint Planning PDF generated successfully: {output_pdf_path}")
except Exception as e:
    print(f"docx2pdf note: {e}")

