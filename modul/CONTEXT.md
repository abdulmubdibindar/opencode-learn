# modul — pipeline penulisan bab (jatah 1 bab)

Jatah: **Bab 4 "Perumusan Isu Awal"** (M Abdul Mubdi B). Bab sekelas yang sudah ditulis tim ada di `acuan/` — acuan yang paling menentukan adalah `acuan/bab-05-analisis-isu-strategis.md` (target handoff: bab 4 berakhir di hipotesis isu, tapisan USG dimiliki bab 5).

Alur dalam satu kalimat: kumpulkan isu dari referensi, tulis draf bab dalam Quarto, review dan terbitkan.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| `01_referensi` | Kumpulkan peta isu perencanaan | `referensi/` ekstraksi + `_assets/` + `acuan/bab-05-…` | `output/peta-isu.md` | orang membaca peta isu; periksa sumbernya |
| `02_draf` | Tulis draf bab (Quarto) | `01_referensi/output/peta-isu.md` + `acuan/bab-05-…` | `output/bab.qmd` | orang membaca draf; verifikasi urutan argumen |
| `03_review-terbit` | Review & render PDF | `02_draf/output/bab.qmd` | `output/bab.pdf` | orang meninjau hasil akhir, periksa kuartal |

Factory (stabil tiap run): `../_assets/`, `../_aturan/`, `../referensi/`, `acuan/`
Product (baru tiap run): `output/` tiap stage

Status adalah apa yang ada: sebuah stage SELESAI bila `output/`-nya memuat berkas selain `.gitkeep`. Batas antar stage adalah tempat manusia berhenti dan memeriksa.
