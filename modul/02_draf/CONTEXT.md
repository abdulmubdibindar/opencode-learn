# 02_draf — tulis draf bab dalam Quarto

One job: menulis draf Bab 4 dari peta isu menjadi dokumen Quarto.

## Inputs
- Working (this run): `../01_referensi/output/peta-isu.md`
- Working (this run): `../01_referensi/aspek-aspek-isu.md` — lima aspek kajian (fisik-lingkungan, sosial kependudukan-budaya, sosial ekonomi, infrastruktur, kelembagaan-pembiayaan) untuk 4.2.3.
- Working (this run): `../acuan/bab-05-analisis-isu-strategis.md` — jaga konsistensi istilah (USG), urutan konsep (kondisi → masalah → isu), dan batas bab (bab 4 berhenti di hipotesis isu; tapisan = bab 5).
- Reference (every run): `../../_assets/Studio Dasar Perencanaan.md` (spek MK — CPL/CPMK yang didukung, asesmen yang disasar)
- Reference (every run): `_cetak.yml` (konfigurasi render DOCX; output final dirender di `03_review-terbit`)
- Reference (style/sitasi): `../../_aturan/rujukan-berkas.md`

Do NOT load: `../01_referensi` selain `output/peta-isu.md` dan `aspek-aspek-isu.md`; seluruh `referensi/`.

## Struktur bab
1. Pembuka: isu perencanaan = celah antara "yang diinginkan" (ditelusuri lewat dokumen rencana) dan "kondisi realita" (ditelusuri lewat belanja masalah).
2. `4.1 Menelaah Dokumen-dokumen Rencana` — RTRW/RDTR (tata ruang) dan RPJP/RPJM (pembangunan); horizon & cakupan; hasil ke tabel terstruktur.
3. `4.2 Belanja Masalah` — `4.2.1` konsep kondisi/masalah/isu; `4.2.2` sumber belanja + status informasi; `4.2.3` pemilahan aspek; `4.2.4` tabel data terstruktur; `4.2.5` peta sebaran.
4. `4.3 Menyusun Daftar Panjang Isu`.
5. `4.4 Dari Daftar Panjang Isu ke Tapisan Isu` — handoff ke USG bab 5.

## Process
1. Baca `peta-isu.md`, `aspek-aspek-isu.md`, spek MK, dan `acuan/bab-05-analisis-isu-strategis.md`.
2. Susun kerangka Bab 4 sesuai struktur di atas; gaya penjelasan selaras bab 5, tanpa narasi kasus dan tanpa "tujuh langkah".
3. Tulis draf `.qmd` (callout, tabel, gambar alur `diagram/alur-penyempitan-isu.png`).
4. Bila alur berubah: edit `diagram/alur-penyempitan-isu.mmd`, lalu render ulang PNG: `mmdc -i diagram/alur-penyempitan-isu.mmd -o diagram/alur-penyempitan-isu.png -w 1200 -b white`.
5. Pastikan tabel belanja masalah berkonsisten dengan kolom input tapisan bab 5, dan ada jembatan eksplisit ke USG bab 5.
6. Pastikan kata/tabel mengiringi arah argumentasi, bukan sebaliknya.

## Outputs
- `bab.qmd` → output/ (merujuk gambar alur `diagram/alur-penyempitan-isu.png`)
- `diagram/alur-penyempitan-isu.mmd` + `diagram/alur-penyempitan-isu.png` → output/ (sumber & render alur mermaid; PNG disisipkan ke docx)
- `prompt-ilustrasi-peta-sebaran.md` → output/ (prompt gambar ilustrasi 4.2.5)

## Human check
Baca draf lalu verifikasi urutan argumentasi bertahan dari `peta-isu.md`. Edit `.qmd` di tempat — stage berikut membaca apa yang ada di sini.
