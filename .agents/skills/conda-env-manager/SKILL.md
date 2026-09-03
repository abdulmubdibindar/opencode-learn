---
name: conda-env-manager
description: Menganalisis lingkungan Conda di mesin (lokal atau mesin baru), memeriksa ketersediaan paket Python untuk berbagai profil tugas (ekstraksi dokumen, GIS, Quarto, ML), dan menawarkan instalasi paket on-demand. Jika sistem belum memiliki Conda, agen akan menghentikan proses dan memandu pengguna melakukan instalasi Conda terlebih dahulu.
---

# Conda Environment Manager Skill

Skill ini digunakan untuk mendeteksi, mendiagnosis, dan menyiapkan lingkungan Conda serta dependensi pustaka Python di mesin lokal maupun mesin baru yang belum terkonfigurasi.

---

## Protokol Wajib: Deteksi Conda di Mesin Baru

Setiap kali Anda diminta menjalankan tugas yang membutuhkan lingkungan Python/Conda di lingkungan baru atau saat inisialisasi lingkungan:

### 1. Periksa Keberadaan Conda
Jalankan skrip diagnosis:
```bash
python .agents/skills/conda-env-manager/scripts/analyze_conda_env.py
```

### 2. Penanganan Jika Conda BELUM Terpasang (WAJIB BERHENTI)
Jika skrip menghasilkan `status: CONDA_NOT_FOUND` (atau executable `conda` tidak ditemukan):

> [!CAUTION]
> **Agen DILARANG melanjutkan eksekusi tugas yang membutuhkan Python jika Conda belum ada.**
> Agen harus menyampaikan pesan jelas kepada pengguna:
> 1. Informasikan bahwa **Conda / Miniconda wajib diinstal terlebih dahulu** oleh pengguna.
> 2. Berikan tautan resmi ([Miniconda Download](https://docs.anaconda.com/miniconda/)) atau perintah terminal Windows: `winget install Anaconda.Miniconda3`.
> 3. **Agen berhenti dan menunggu** sampai pengguna mengonfirmasi bahwa instalasi Conda telah selesai.

---

## Profil Tugas & Analisis Dependensi

Gunakan profil yang sesuai dengan dharma / tugas yang sedang dikerjakan:

| Nama Profil | Deskripsi Tugas | Paket Utama |
| :--- | :--- | :--- |
| **`extract-docs`** | Ekstraksi buku, PDF, Word, Excel, PowerPoint, EPUB, MinerU | `PyMuPDF (fitz)`, `openpyxl`, `markitdown`, `pdfplumber`, `pypdf`, `pillow`, `mineru` |
| **`gis-analysis`** | Analisis spasial, GIS, pemodelan jaringan jalan | `geopandas`, `shapely`, `osmnx`, `folium`, `duckdb`, `matplotlib`, `pyogrio` |
| **`quarto-doc`** | Render komputasi dokumen Quarto & visualisasi | `ipykernel`, `matplotlib`, `pandas`, `seaborn`, `openpyxl`, `jupyterlab` |

### Perintah Analisis:
```bash
# Analisis profil ekstraksi dokumen pada environment tertentu (mis. extract-pdf)
python .agents/skills/conda-env-manager/scripts/analyze_conda_env.py --profile extract-docs --env extract-pdf

# Analisis profil GIS
python .agents/skills/conda-env-manager/scripts/analyze_conda_env.py --profile gis-analysis

# Cek daftar modul khusus
python .agents/skills/conda-env-manager/scripts/analyze_conda_env.py --check "fitz,markitdown,mineru" --env extract-pdf
```

---

## Alur Penawaran Instalasi Paket Saat Itu Juga

1. Jalankan analisis profil untuk melihat paket apa saja yang `BELUM ADA`.
2. Jika ada paket yang belum terpasang, sampaikan daftar paket tersebut kepada pengguna.
3. Tawarkan dan jalankan perintah instalasi di environment target:
   - **Jika `uv` tersedia (Sangat Cepat)**:
     ```bash
     uv pip install <paket1> <paket2>
     ```
   - **Jika menggunakan pip standar**:
     ```bash
     pip install <paket1> <paket2>
     ```
   - **Jika membuat environment baru**:
     ```bash
     conda create -n "<nama_env>" python=3.12 -y
     conda activate <nama_env>
     ```
4. Lakukan verifikasi ulang setelah instalasi selesai untuk memastikan semua status menjadi `Terpasang (OK)`.
