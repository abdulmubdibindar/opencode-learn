# _aturan — aturan kerja direktori ini

Satu job: memuat aturan penulisan dan penamaan yang berlaku lintas `modul/`, `diaries/`, `referensi/`. Stabil lintas sesi; tidak ikut berubah per run.

## Inputs
- Reference (every run): konten aturan itu sendiri (berkas `.md` di folder ini)

## Isi
- `rujukan-berkas.md` — cara merujuk berkas dalam teks (wikilink `.md` / `` `@nama.ext` `` untuk non-md; berlaku di mana pun, termasuk dalam sel tabel).
- `konvensi-penamaan.md` — kaidah penamaan berkas dan folder di direktori ini (stub, perlu dilengkapi dari sumber vault).
- `aturan-dokumentasi.md` — mengapa duplikasi dan bentuk dokumentasi di direktori ini seperti sekarang (stub, perlu dilengkapi dari sumber vault).

## Outputs
- Tidak ada output per run — ini factory, bukan stage.

## Human check
Ketika menulis konten baru di `modul/` atau `diaries/`, pastikan rujukan berkasnya mengikuti `rujukan-berkas.md`. Buka `_index.md` atau kontrak folder tersebut bila bingung arah rujukan — lihat catatan riwayat di `rujukan-berkas.md`.
