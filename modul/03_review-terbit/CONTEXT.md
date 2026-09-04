# 03_review-terbit — tinjau dan render PDF

One job: meninjau draf dan menerbitkan bab sebagai PDF.

## Inputs
- Working (this run): `../02_draf/output/bab.qmd`
- Reference (every run): `../../_assets/Studio Dasar Perencanaan.md` (kesesuaian dengan CPL/CPMK, asesmen)

Do NOT load: `../02_draf` selain `output/`.

## Process
1. Baca `bab.qmd`.
2. Selesaikan atau perbaiki masalah rendering (callout meluber, tabel pecah, tautan wikilink tercetak mentah).
3. Render ke PDF via config Typst dari panduan Quarto.
4. Tandai versi final + uraian apa yang diterbitkan.

## Outputs
- `bab.pdf` → output/

## Human check
Buka PDF; verifikasi kerapian dan bahwa CPL/CPMK yang disasar tercakup. Edit `bab.qmd` bila perlu, lalu render ulang. Inilah gate terakhir — yang keluar dari sini adalah produk yang meninggalkan workspace.
