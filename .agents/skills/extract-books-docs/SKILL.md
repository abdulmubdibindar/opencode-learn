---
name: extract-books-docs
description: Ekstraksi dan konversi komprehensif aneka format buku dan dokumen (PDF, EPUB, Word .docx, Excel .xlsx, PowerPoint .pptx, scan/gambar) menjadi Markdown terstruktur, rumus LaTeX, tabel HTML/MD, dan gambar/diagram. Mengintegrasikan mesin cepat PyMuPDF, AI layout parser MinerU (OpenDataLab), MarkItDown, dan EPUB reader. Gunakan setiap kali diminta mengekstrak buku referensi, membaca EPUB, mengonversi dokumen Office, atau membedah PDF ilmiah bertabel/berumus.
---

# Extract Books & Docs Skill

Skill terpadu untuk mengekstrak, membaca, dan mengonversi berbagai jenis bahan pustaka dan dokumen ke dalam format Markdown bersih, diagram/figur beresolusi tinggi, rumus matematika LaTeX, tabel terstruktur, serta metadata lengkap.

---

## Matriks Pemilihan Engine

| Tipe Dokumen / Kebutuhan | Format | Engine yang Digunakan | Karakteristik & Keunggulan | Perintah Cepat |
| :--- | :--- | :--- | :--- | :--- |
| **Buku Teks Akademik / Laporan Panjang** | `.pdf` | **PyMuPDF Fast Engine** (`ekstrak_pdf.py`) | Super cepat (5–15 detik untuk 300 hal), pemecahan bab otomatis, diagram vektor dirender 200 DPI terikat *caption*, tabel hibrida. | `python scripts/extract_docs.py --input "buku.pdf" --output "DIR_HASIL"` |
| **Paper Ilmiah, Rumus Matematika, OCR Scan, Multikolom** | `.pdf`, `.png`, `.jpg` | **MinerU AI Engine** (`mineru_extractor.py`) | Deep-learning layout analysis, rumus ke LaTeX (`$...$`), tabel kompleks ke HTML/MD, hapus header/footer otomatis. | `python scripts/extract_docs.py --input "paper.pdf" --output "DIR_HASIL" --engine mineru` |
| **Dokumen Microsoft Office** | `.docx`, `.xlsx`, `.pptx` | **Office Engine** (`convert_office.py` / MarkItDown) | Konversi dokumen Word, sheet Excel, slide presentasi ke tabel dan teks Markdown, pemrosesan batch. | `python scripts/extract_docs.py --input "berkas.docx" --output-dir "DIR_HASIL"` |
| **Buku Elektronik (E-Book)** | `.epub` | **EPUB Engine** (`ekstrak_epub.py` / `epub-reader`) | Ekstraksi penuh, navigasi daftar isi (TOC), baca bab tertentu, pencarian kata kunci dengan konteks. | `python scripts/ekstrak_epub.py full "buku.epub" --output "buku.md"` |

---

## Lingkungan & Dependensi Python

Skill ini dirancang untuk memanfaatkan *environment* conda lokal:
1. **`extract-pdf`** (`C:\Users\LENOVO\.conda\envs\extract-pdf`): Berisi `PyMuPDF (fitz)`, `pdfplumber`, `pypdf`, `pytesseract`, `openpyxl`, `pillow`.
2. **`markitdown`** (`C:\ProgramData\miniconda3\envs\markitdown`): Berisi pustaka `markitdown`.
3. **MinerU** (*opsional untuk AI parser*):
   - Dapat diinstal di environment target via: `pip install -U "mineru[all]"` atau `pip install -U "mineru[cpu]"`.
   - Gunakan skill `conda-env-manager` jika perlu menganalisis atau menginstal dependensi baru di mesin lain.

---

## 1. Ekstraksi PDF (Fast PyMuPDF Engine)

### A. Mode Tunggal (Dokumen Ringkas / Regulasi / Teks Dominan)
Untuk handbook, SK, peraturan, atau dokumen ringkas tanpa ekstraksi gambar:
```bash
python scripts/ekstrak_pdf.py --pdf "DOKUMEN.pdf" --keluaran "HASIL.md" --tunggal --sumber "*Judul Dokumen* (Penerbit, Tahun)"
```
- Menghasilkan 1 berkas `.md` utuh dengan penanda halaman `<!-- hal. PDF n -->`, heading dari bookmark PDF, dan placeholder gambar `> [Gambar: ... — lihat PDF asli]`.

### B. Mode Penuh (Buku Teks Akademik dengan Banyak Figur/Diagram)
Empat langkah pengerjaan:
1. **Kenali wajah dokumen**:
   ```bash
   python scripts/ekstrak_pdf.py --pdf "BUKU.pdf" --profil
   ```
2. **Jalankan ekstraksi**:
   ```bash
   python scripts/ekstrak_pdf.py --pdf "BUKU.pdf" --keluaran "DIR_HASIL" --sumber "*Judul Buku* (Penulis, Tahun)"
   ```
3. **Periksa visual**: Buka 3–5 gambar di folder `gambar/` untuk memastikan potongan pas, tidak terpotong, dan judul gambar di `_index.md` sesuai dengan *List of Figures* asli.
4. **Bedah halaman bermasalah (jika ada)**:
   ```bash
   python scripts/ekstrak_pdf.py --pdf "BUKU.pdf" --periksa 28,127
   ```

### C. Tabel Hibrida (`--tabel hibrida`)
Untuk dokumen yang bertumpu pada tabel (rubrik, borang akreditasi, lampiran tabel):
```bash
python scripts/ekstrak_pdf.py --pdf "DOKUMEN.pdf" --keluaran "DIR_HASIL" --tabel hibrida --sumber "*Judul Dokumen*"
```
Tiap tabel diekstrak dua kali: sebagai gambar (rujukan visual mutlak) dan tabel Markdown terformat.

---

## 2. Ekstraksi PDF Ilmiah & Rumus (MinerU AI Engine)

Gunakan ketika dokumen memiliki:
- Rumus matematika / statistik padat yang perlu diubah ke notasi LaTeX.
- Tata letak 2–3 kolom (jurnal / prosiding konferensi).
- PDF hasil pemindaian (*scanned document*) yang membutuhkan OCR mendalam.

### Perintah:
```bash
# Periksa status ketersediaan MinerU
python scripts/mineru_extractor.py --check-env

# Jalankan ekstraksi
python scripts/mineru_extractor.py --input "paper.pdf" --output-dir "DIR_HASIL"

# Atau via router universal:
python scripts/extract_docs.py --input "paper.pdf" --output "DIR_HASIL" --engine mineru
```

> [!NOTE]
> **GPU vs CPU pada MinerU**:
> - Pada CPU murni (16-thread), MinerU memproses ~10–25 detik per halaman. Paper 20 halaman selesai dalam 3–8 menit.
> - Pada GPU CUDA, proses memakan ~1–3 detik per halaman.

---

## 3. Konversi Dokumen Office (`.docx`, `.xlsx`, `.pptx`)

Mengonversi dokumen Word, Excel, dan PowerPoint menjadi format Markdown bersih.

```bash
# Memproses satu file dengan output direktori khusus
python scripts/convert_office.py --target "C:\path\ke\dokumen.docx" --output-dir "C:\path\ke\output" --output "report.json"

# Memproses batch seluruh file di sebuah folder
python scripts/convert_office.py --target "C:\path\ke\folder" --output "report.json"

# Atau melalui router universal:
python scripts/extract_docs.py --input "C:\path\ke\folder" --output-dir "C:\path\ke\output" --report "report.json"
```

---

## 4. Pembacaan & Ekstraksi EPUB

Mendukung membaca e-book tanpa merusak struktur bab.

```bash
# 1. Lihat Metadata Buku
python scripts/ekstrak_epub.py metadata "buku.epub"

# 2. Lihat Daftar Isi (TOC)
python scripts/ekstrak_epub.py toc "buku.epub"

# 3. Baca Bab Tertentu (1-indexed)
python scripts/ekstrak_epub.py chapter "buku.epub" 3

# 4. Ekstrak Seluruh Buku ke Satu Berkas Markdown
python scripts/ekstrak_epub.py full "buku.epub" --output "buku.md"

# 5. Cari Kata Kunci / Topik Tertentu
python scripts/ekstrak_epub.py search "buku.epub" "metodologi"
```

*(Jika lingkungan Node.js tersedia, CLI TypeScript `scripts/epub-reader/dist/index.js` juga dapat digunakan).*

---

## 5. Router Universal (`extract_docs.py`)

Router otomatis yang mendeteksi ekstensi berkas atau memproses direktori secara batch:

```bash
# Otomatis deteksi tipe berkas
python scripts/extract_docs.py --input "path/to/file.pdf" --output "DIR_HASIL"
python scripts/extract_docs.py --input "path/to/file.docx" --output-dir "DIR_HASIL"
python scripts/extract_docs.py --input "path/to/file.epub" --output "hasil.md"

# Batch satu direktori penuh
python scripts/extract_docs.py --input "C:\path\ke\folder_dokumen" --output-dir "C:\path\ke\hasil" --report "laporan.json"
```

---

## Jebakan yang Sering Terjadi & Solusinya

| Gejala pada Hasil | Penyebab | Solusi / Penanganan |
| :--- | :--- | :--- |
| Judul gambar berbunyi seperti kalimat ("Figure 6.3 helps depict…") | Kalimat rujukan teks tertangkap sebagai caption | Caption harus berupa huruf miring (*italic*) dan seukuran fon caption hasil `--profil`. |
| Kata terputus: "spe cific", "admin istrative" | Pemenggalan kata antarbaris (*soft hyphen* `U+00AD`) | Ditangani otomatis di `ekstrak_pdf.py` (disambung rapat). |
| Ligatur hilang: "crea vity", "situa ons" | Karakter kontrol `\x1f`, `\x1e`, `\x02` | Dipetakan kembali menjadi "ti" secara otomatis. |
| Rumus matematika rusak / karakter aneh pada PDF ilmiah | PDF memakai encoding fon matematika khusus | Gunakan engine **MinerU** (`--engine mineru`) untuk mengenali rumus ke notasi LaTeX. |
| Seluruh dokumen jadi 1 berkas `00_Dokumen.md` | PDF tidak memiliki bookmark / outline | Skrip otomatis beralih ke deteksi heading berdasarkan rasio ukuran fon (≥1,6× teks badan). |
| Batas path Windows (260 karakter) | Path direktori target terlalu dalam | Pendekkan nama folder keluaran (misal `NN_ekstraksi_penulis_tahun`). |

---

## Yang Dilaporkan kepada Pengguna

Sesuai `AGENTS.md`, agen adalah eksekutor dan pengguna adalah verifikator:
1. **Lokasi & Struktur Hasil**: Beritahu lokasi direktori/berkas keluaran.
2. **Engine yang Digunakan**: Jelaskan engine yang dipilih (Fast PyMuPDF / MinerU / MarkItDown / EPUB) dan alasannya.
3. **Limitasi & Catatan Khusus**: Misalnya catatan tentang tabel Markdown hibrida (hasil inferensi cerdas, rujuk gambar jika ragu), atau waktu komputasi MinerU.
4. **Langkah Verifikasi Mandiri**: Berikan 2–3 langkah konkret untuk dicek pengguna (contoh: buka `_index.md`, periksa gambar bab utama, atau tinjau rumus LaTeX yang dihasilkan).
