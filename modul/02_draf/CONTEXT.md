# 02_draf — tulis draf bab dalam Quarto

One job: menulis draf bab dari peta isu menjadi dokumen Quarto.

## Inputs
- Working (this run): `../01_referensi/output/peta-isu.md`
- Reference (every run): `../../_assets/Studio Dasar Perencanaan.md` (spek MK — CPL/CPMK yang didukung, asesmen yang disasar)
- Reference (every run): skill QUARTO (atur panduan penulisan dokumen Quarto + konfigurasi cetak Typst)
- Reference (style/sitasi): `../../_aturan/rujukan-berkas.md`

Do NOT load: `../01_referensi` selain `output/`; seluruh `referensi/`.

## Process
1. Baca `peta-isu.md` dan spek MK.
2. Susun kerangka bab sesuai bab studio (perumusan isu perencanaan).
3. Tulis draf `.qmd` mengikuti panduan Quarto (callout, tabel, tautan wikilink, konfigurasi Typst).
4. Pastikan kata/tabel mengiringi arah argumentasi, bukan sebaliknya.

## Outputs
- `bab.qmd` → output/

## Human check
Baca draf lalu verifikasi urutan argumentasi bertahan dari `peta-isu.md`. Edit `.qmd` di tempat — stage berikut membaca apa yang ada di sini.
