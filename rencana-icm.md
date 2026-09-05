# Rencana ICM — `opencode-learn`

> Cara mengomentari: tambahkan callout di bawah bagian yang dikomentari, contoh:
> `[!INFO] Komentar saya: ...`

Status: **rencana (build mode, belum dieksekusi)**. Skill `icm-architecture`, mode **Restructure, berhenti di langkah 4** (propose before moving). Tidak ada pemindahan berkas sebelum rencana ini disetujui.

Keputusan user yang sudah dikonfirmasi:

- Unit utama: pipeline modul untuk **satu bab spesifik** (jatah 1 dari sekian bab bersama dosen lain).
- Direktori ini "bekerja sambil belajar": selain produk, pembelajaran direkam — salah satunya via mirror diary `-en`.
- Wikilink mati ke vault ITERA besar: **inline copy + perbaiki**.
- Pipeline modul: **3–4 stage penuh** dengan gate manusia.

## 1. Inventarisasi

| Area | Isi / kondisi | Dirujuk oleh |
|---|---|---|
| `AGENTS.md` | 8 baris, campur identitas + routing + aturan | seluruh agen |
| `README.md` | Identitas belajar OpenCode (EN) | — (tumpang tindih identitas dengan `AGENTS.md`) |
| `Studio Dasar Perencanaan.md` | Spesifikasi MK (identitas, CPL/CPMK, asesmen) | `AGENTS.md` |
| `_assets/` | 14 berkas pengetahuan persisten ITERA + `_index.md` | `AGENTS.md` |
| `_aturan/rujukan-berkas.md` | Aturan rujukan berkas (factory, matang, frontmatter OK) | — (belum dirujuk `AGENTS.md`, seharusnya dirujuk) |
| `referensi/` | 2 ekstraksi buku (`dunn-2017/`, `fyfe-concreteness-fading/`, masing-masing sudah punya `_index.md` + `_figur.json` + `gambar/`) + 2 PDF mentah | `AGENTS.md`, calon input pipeline |
| `modul/` | Kosong | `AGENTS.md`, calon pipeline |
| `diaries/` | 1 record (`2026-09-04-first-work.md`) + `diaries/assets/` (1 png + 1 json) | `AGENTS.md` |
| `.agents/skills/`, `.obsidian/`, `.git/` | System, tidak disentuh | — |

Temuan kunci:

1. Kebingungan `_assets` vs `assets`: `AGENTS.md` menulis `/assets` dan `assets/`, faktanya ada **dua** hal berbeda — `_assets/` (factory persisten, pakai underscore = benar) dan `diaries/assets/` (lampiran produk sesi, tanpa underscore = benar menurut konvensi). Belum pernah dijelaskan — agen berikutnya pasti salah sangka.
2. Tiga wikilink mati: `[[konvensi-penamaan]]`, `[[aturan-dokumentasi]]` di `_aturan/rujukan-berkas.md`, dan dua path absolut `[[01 PENDIDIKAN/...]]` di `_assets/_index.md` dan `_aturan/rujukan-berkas.md`. Sampahan dari vault ITERA besar.
3. `modul/` kosong + `referensi/` tanpa router = pipeline belum punya tulang punggung.

## 2. Hidden form

**Umbrella tipis** atas tiga hal, satu factory bersama:

- **Pipeline single-run** — `modul/` menulis 1 bab (perumusan isu perencanaan). Satu kali jalan, 3 stage, tiap batas ada gate baca-edit manusia. Catatan guardrail: pipeline untuk proses yang baru sekali jalan memang prematur secara teori — tapi di sini batas berhentinya nyata (kumpul referensi → draf Quarto → review/terbit) dan tujuan pembelajarannya justru butuh scaffolding eksplisit. Jadi bangun minimal, tanpa kedalaman spekulatif.
- **Record library** — `diaries/`, unit berulang = sesi belajar. Setiap record = `YYYY-MM-DD-slug.md` + cermin `-en.md`.
- **Knowledge bundle (factory)** — `_assets/` + `_aturan/` + spec MK. Stabil lintas sesi dan lintas bab.

## 3. Klasifikasi peran

- **Catalog**: `AGENTS.md`, `_assets/_index.md`, `_index.md` di tiap sub-`referensi/`.
- **Contract**: belum ada — semua `CONTEXT.md` harus ditulis saat eksekusi.
- **Factory**: `_aturan/rujukan-berkas.md`, isi `_assets/`, `Studio Dasar Perencanaan.md`, PDF/metode di `referensi/`.
- **Product**: `modul/` (nanti), `diaries/*.md`, `diaries/assets/*`.
- **Dead / perlu pindah**: `README.md` (identitas ganda di root), 2 baris logo absolut di `_assets/_index.md`, path salah di `AGENTS.md`.

## 4. Target tree yang diusulkan

```text
opencode-learn/
├─ AGENTS.md                    # L0, routing saja, <60 baris (tulis ulang)
├─ CONTEXT.md                   # L1, peta umbrella (BARU)
├─ _aturan/
│  ├─ CONTEXT.md                # router aturan (BARU)
│  ├─ rujukan-berkas.md         # tetap
│  ├─ konvensi-penamaan.md      # inline-copy minimal dari vault (BARU, saat eksekusi)
│  └─ aturan-dokumentasi.md     # inline-copy minimal dari vault (BARU, saat eksekusi)
├─ _assets/
│  ├─ CONTEXT.md                # router factory (BARU)
│  └─ _index.md                 # perbaiki 2 link logo absolut
├─ referensi/
│  ├─ CONTEXT.md                # router knowledge bundle (BARU)
│  ├─ dunn-2017/                # tetap (sudah rapi)
│  └─ fyfe-concreteness-fading/ # tetap (sudah rapi)
├─ modul/                       # pipeline single-run, 1 bab
│  ├─ CONTEXT.md                # definisi pipeline (BARU)
│  ├─ 01_referensi/{CONTEXT.md,output/}
│  ├─ 02_draf/{CONTEXT.md,output/}          # .qmd, pakai skill penulisan-quarto
│  └─ 03_review-terbit/{CONTEXT.md,output/} # gate akhir + render PDF
├─ diaries/
│  ├─ CONTEXT.md                # kontrak record library + aturan mirror -en (BARU)
│  ├─ _log.md                   # 1 baris per sesi: id + status + link ID/-en (BARU)
│  └─ assets/                   # tetap, ditegaskan sebagai lampiran produk
├─ _templates/
│  └─ diary.md                  # stamp record baru ID + -en (BARU)
├─ Studio Dasar Perencanaan.md  # PINDAH ke _assets/ sebagai factory context
└─ README.md                    # tetap di root sebagai sampul repo, isi identitas dipangkas
                                # agar tidak drift dengan AGENTS.md (1 kalimat + pointer)
```

### Migration map

| Lama | Baru | Peran |
|---|---|---|
| `AGENTS.md` | tulis ulang di tempat | Catalog L0 |
| — | `CONTEXT.md` root | Catalog L1 |
| `Studio Dasar Perencanaan.md` | `_assets/Studio Dasar Perencanaan.md` | Factory |
| `_assets/_index.md` (2 baris logo) | path relatif + alias | Catalog fix |
| `_aturan/` | + `CONTEXT.md` + 2 inline-copy | Factory lengkap |
| `referensi/` | + `CONTEXT.md` root | Contract router |
| `modul/` | + `CONTEXT.md` + 3 stage | Pipeline baru |
| `diaries/` | + `CONTEXT.md` + `_log.md` | Contract + index |
| — | `_templates/diary.md` | Stamp |
| `README.md` | pangkas jadi pointer | Dead → sampul |

## 5. Kontrak yang akan ditulis saat eksekusi (sketsa)

- Root `CONTEXT.md`, `modul/CONTEXT.md`, tiga stage `CONTEXT.md` (inputs = path eksak, split working vs reference; 1 human check konkret, mis. "baca draf aloud, verifikasi urutan argumen dari `01_referensi/output/peta-isu.md`, edit di tempat"), `diaries/CONTEXT.md` (aturan `YYYY-MM-DD-slug.md` + pasangan `-en.md` via skill `terjemahan-inggris`, lampiran ke `assets/`), `_assets/CONTEXT.md`, `_aturan/CONTEXT.md`, `referensi/CONTEXT.md`.
- Detail L3 (Quarto, prosedur, gaya sitasi `@nama.md` yang sudah ada) tetap di file factory masing-masing — kontrak hanya menunjuk, tidak merestate.
- Aturan penamaan: folder system `_`-prefix, stage `NN_kebab-name`, record diary `YYYY-MM-DD-slug` + `YYYY-MM-DD-slug-en`, wikilink untuk `.md` / `` `@nama.ext` `` untuk non-md sesuai `_aturan/rujukan-berkas.md`.

## 6. Walk test (proyeksi)

- Root → tugas: `AGENTS.md` (routing per tugas) + maksimal 2 baca tambahan. Hari ini gagal (path salah, tidak ada tabel routing); setelah eksekusi lolos.
- Tiap stage punya input path eksak + 1 human check. Hari ini gagal (tidak ada `CONTEXT.md`); setelah eksekusi lolos.
- Status pipeline dari `modul/*/output/`, status belajar dari `diaries/_log.md`. Hari ini gagal; setelah eksekusi lolos.
- Satu home per fakta: spec MK pindah ke `_assets/`, identitas root hanya di `AGENTS.md`. Estimasi konteks per stage: entry + 1 kontrak + input ≈ 2–8k token (L3 besar seperti Dunn tidak pernah di-inline, hanya ditunjuk).

## 7. Human gate

Setujui atau komentari rencana ini (callout `[!INFO]`). Setelah disetujui saya eksekusi migrasi: pindah berkas, tulis `AGENTS.md` + 8 `CONTEXT.md` + `_log.md` + 1 template, perbaiki link mati, lalu walk test dingin.
