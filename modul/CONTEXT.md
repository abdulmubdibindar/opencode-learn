# modul — pipeline penulisan bab (jatah 1 bab)

Alur dalam satu kalimat: kumpulkan isu dari referensi, tulis draf bab dalam Quarto, review dan terbitkan.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| `01_referensi` | Kumpulkan peta isu perencanaan | `referensi/` ekstraksi + `_assets/` | `output/peta-isu.md` | orang membaca peta isu; periksa sumbernya |
| `02_draf` | Tulis draf bab (Quarto) | `01_referensi/output/peta-isu.md` | `output/bab.qmd` | orang membaca draf; verifikasi urutan argumen |
| `03_review-terbit` | Review & render PDF | `02_draf/output/bab.qmd` | `output/bab.pdf` | orang meninjau hasil akhir, periksa kuartal |

Factory (stabil tiap run): `../_assets/`, `../_aturan/`, `../referensi/`
Product (baru tiap run): `output/` tiap stage

Status adalah apa yang ada: sebuah stage SELESAI bila `output/`-nya memuat berkas selain `.gitkeep`. Batas antar stage adalah tempat manusia berhenti dan memeriksa.
