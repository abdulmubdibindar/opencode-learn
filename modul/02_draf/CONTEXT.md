# 02_draf — tulis draf bab dalam Quarto

One job: menulis draf Bab 4 dari peta isu menjadi dokumen Quarto.

## Inputs
- Working (this run): `../01_referensi/output/peta-isu.md`
- Working (this run): `../acuan/bab-05-analisis-isu-strategis.md` — jaga konsistensi istilah (USG), urutan konsep (kondisi → masalah → isu), dan batas bab (bab 4 berhenti di hipotesis isu; tapisan = bab 5).
- Reference (every run): `../../_assets/Studio Dasar Perencanaan.md` (spek MK — CPL/CPMK yang didukung, asesmen yang disasar)
- Reference (every run): skill `penulisan-quarto` (atur panduan penulisan dokumen Quarto + konfigurasi cetak Typst)
- Reference (style/sitasi): `../../_aturan/rujukan-berkas.md`

Do NOT load: `../01_referensi` selain `output/`; seluruh `referensi/`.

## Process
1. Baca `peta-isu.md`, spek MK, dan `acuan/bab-05-analisis-isu-strategis.md`.
2. Susun kerangka Bab 4 sesuai bab studio (belanja isu → perumusan isu awal), gaya penjelasan (selaras bab 5), tanpa narasi kasus dan tanpa "tujuh langkah".
3. Tulis draf `.qmd` mengikuti panduan Quarto (callout, tabel, tautan wikilink, konfigurasi Typst).
4. Pastikan tabel belanja isu berkonsisten dengan kolom input tapisan bab 5, dan ada jembatan eksplisit ke USG bab 5.
5. Pastikan kata/tabel mengiringi arah argumentasi, bukan sebaliknya.

## Outputs
- `bab.qmd` → output/

## Human check
Baca draf lalu verifikasi urutan argumentasi bertahan dari `peta-isu.md`. Edit `.qmd` di tempat — stage berikut membaca apa yang ada di sini.
