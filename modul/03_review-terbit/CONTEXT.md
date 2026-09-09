# 03_review-terbit — tinjau dan render DOCX

One job: meninjau draf dan menerbitkan bab sebagai DOCX.

## Inputs
- Working (this run): `../02_draf/output/bab.qmd`
- Reference (every run): `../../_assets/Studio Dasar Perencanaan.md` (kesesuaian dengan CPL/CPMK, asesmen)
- Reference (every run): `../02_draf/output/_cetak.yml` (konfigurasi render DOCX)

Do NOT load: `../02_draf` selain `output/`.

## Process
1. Baca `bab.qmd`.
2. Selesaikan atau perbaiki masalah rendering (callout meluber, tabel pecah, gambar tidak muncul).
3. Render ke DOCX via Quarto (dijalankan di `../02_draf/output/`): `quarto render bab.qmd --to docx --metadata-file _cetak.yml`, lalu salin `bab.docx` ke `output/` folder ini.
4. Tandai versi final + uraian apa yang diterbitkan.

## Outputs
- `bab.docx` → output/

## Human check
Buka DOCX; verifikasi kerapian dan bahwa CPL/CPMK yang disasar tercakup. Edit `bab.qmd` bila perlu, lalu render ulang. Inilah gate terakhir — yang keluar dari sini adalah produk yang meninggalkan workspace.
