# _assets — pengetahuan persisten ITERA

Satu job: menyimpan fakta tentang kurikulum dan perkuliahan di ITERA yang berlaku lintas mata kuliah dan lintas tahun. Factory — benar selalu, tidak ikut berubah per run bab.

## Inputs
- Reference (kadang-kadang): verifikasi ke dokumen resmi saat fakta diragukan.

## Isi
- `_index.md` — daftar berkas di folder ini + satu kalimat per berkas (katalog).
- Berkas fakta per topik: `OBE.md`, `CPL-CPMK.md`, `Materi Per Pekan.md`, `Penilaian.md`, `Penulisan RPS.md`, `Studio.md`, `hierarki-pelayanan.md`, `Studio Dasar Perencanaan.md` (spek MK proyek ini).
- Pendukung visual/file: `cpl-cpmk.svg`, `Alur Studio.svg`, logo ITERA, contoh RPS `.xlsx`.

> [!NOTE]
> Jangan menaruh berkas khas satu mata kuliah (ekspor Conda, cuplikan layar kerja) di sini — letakkan di direktori kerja yang bersangkutan (`diaries/assets/`). Perbarui `_index.md` tiap isi folder ini berubah.

## Outputs
- Tidak ada output per run — ini factory.

## Human check
Saat menulis konten di `modul/` yang menyangkut CPL/CPMK atau aturan ITERA, baca `_index.md` dulu lalu buka berkas fakta terkait — bukan menebak. Jangan mengutip fakta dari memori bila sudah ada berkasnya.
