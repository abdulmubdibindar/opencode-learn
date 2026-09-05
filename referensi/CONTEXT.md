# referensi — bahan ekstraksi buku untuk bab

Satu job: menampung sumber materi penulisan bab — ekstraksi terstruktur dari buku referensi plus PDF mentahnya. Factory: bahan dibaca saat riset, tidak berubah per run bab.

## Inputs
- Reference (kadang-kadang): PDF mentah jika ekstraksi perlu diverifikasi/diperdalam.

## Isi
- `dunn-2017/` — ekstraksi terstruktur *Public Policy Analysis* (Dunn, 2017). Punya `_index.md` sendiri di dalamnya.
- `fyfe-concreteness-fading/` — ekstraksi terstruktur *Making Concreteness Fading More Concrete...*. Punya `_index.md` sendiri di dalamnya.
- `2366_Making-concreteness-fading.pdf` — PDF mentah makalah concreteness fading.
- `William N. Dunn - Public Policy Analysis_ An Integrated Approach-Routledge (2017).pdf` — PDF mentah buku Dunn.
- `OUTLINE MODUL STUDAS 2026.docx` — outline/kerangka Modul STUDAS 2026, dipakai `modul/acuan/` untuk menyegarkan struktur bab.

## Cara pakai
1. Buka `_index.md` di dalam subfolder untuk menemukan bagian yang relevan.
2. Baca bagian itu sebagai referensi saat merekam konten di `modul/`.
3. Buka PDF mentah hanya bila ekstraksi tidak cukup jelas — jangan meng-inline seluruh isi ke dalam kontrak stage.

## Outputs
- Tidak ada output per run — ini factory.

## Human check
Sebelum menulis draft modul, pastikan peta isu di `modul/01_referensi/output/` benar-benar dari ekstraksi di sini, bukan dari ingatan. Catat sumber halaman/bagian yang dipakai.
