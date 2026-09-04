# OpenCode Learn

Direktori kerja **bekerja sambil belajar**: produknya satu bab buku studio perencanaan, pembelajarannya direkam di `diaries/` beserta cermin bahasa Inggris (`-en.md`).

Dibangun di atas ICM: folder membawa urutan, hierarki membawa konteks, berkas membawa keadaan. Struktur adalah dokumentasinya — kalau ada yang perlu dijelaskan, penjelasannya ada di `CONTEXT.md` folder itu, bukan di kepala.

## Di mana semuanya berada

| Direktori | Isinya |
|---|---|
| `modul/` | pipeline penulisan bab (jatah 1 bab), urutan eksekusi |
| `diaries/` | rekaman belajar per sesi — record library |
| `referensi/` | bahan ekstraksi buku + PDF mentah (factory untuk bab) |
| `_assets/` | pengetahuan persisten ITERA (factory; benar selalu) |
| `_aturan/` | aturan kerja - rujukan berkas, penamaan, dokumentasi |
| `_templates/` | starter kosong — pekerjaan baru = salinan, bukan halaman kosong |
| `rencana-icm.md` | rencana restrukturisasi yang menjadi kompas migrasi ini |

## Rute sesuai konteks

| Kalau | Masuk ke | Berhenti di |
|---|---|---|
| menulis bab | `modul/CONTEXT.md` | manusia baca tiap `output/` stage |
| merekam sesi belajar | `diaries/CONTEXT.md` | manusia baca diary + cermin `-en` |
| cari aturan rujukan/penamaan | `_aturan/CONTEXT.md` | — |
| butuh konteks MK / ITERA | `_assets/CONTEXT.md` | — |
| mulai riset materi bab | `modul/01_referensi/CONTEXT.md` | manusia baca `output/` |
| cek status belajar | scan `diaries/_log.md` | laporkan yang ada |

## Satu aturan

Tidak ada yang maju ke langkah berikut sebelum seseorang membaca hasil langkah terakhir. Setiap koleksi `.md` yang bernama besar (`CONTEXT.md`, `_index.md`) dijalur-lengkapkan saat dirujuk dari luar folder itu — lihat `_aturan/rujukan-berkas.md`.
