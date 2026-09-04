# diaries — record library sesi belajar

Satu job: merekam pembelajaran tiap sesi bekerja. Unit = 1 sesi belajar; record dibuat sebagai salinan template, bukan halaman kosong.

## Bentuk record
- Nama: `YYYY-MM-DD-ringkasan-slug.md` (ID + slug ringkas).
- Cermin bahasa Inggris wajib: `YYYY-MM-DD-ringkasan-slug-en.md`, dibuat via skill `terjemahan-inggris` setelah konten Indonesia final.
- Lampiran (cuplikan layar, fail percakapan JSON) → `assets/`, dirujuk dari record.
- Struktur isi mengikuti `_templates/diary.md`: bagian **Apa yang dilakukan** wajib; bagian *Apa yang saya pelajari* dan *Pertanyaan yang muncul* opsional (diisi hanya bila ada muatan belajar/pertanyaan).

## Katalog
- `_log.md` — satu baris per sesi: id + status + tautan ID / `-en`. **Katalog, bukan isi** — jangan simpan isi sesi di sini.

## Aturan
- Satu fail tidak harus satu hari; boleh satu sesi.
- Rekam pembelajaran nyata, bukan sekadar kronologi kerja.
- `_log.md` dirawat saat record dibuat/diubah. Ini adalah katalog satu-garis-per-record dengan siklus status sederhana.

## Rujukan
- Nama berkas dan cara rujuk: rujukan berkas (di `_aturan/rujukan-berkas.md`).
- Cara menulis langkah prosedural: skill `penulisan-prosedur`.
