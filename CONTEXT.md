# OpenCode Learn — peta umbrella

Tiga kegiatan, satu lapisan aturan bersama. Tidak ada pipeline yang jalan sampai seseorang membaca hasil langkah terakhirnya.

| Area | Bentuk | Unit kerja | Entri | Status |
|---|---|---|---|---|
| `modul/` | Pipeline | 1 bab buku (jatah 1 dari sekian bab) | `modul/CONTEXT.md` | lihat `modul/*/output/` |
| `diaries/` | Record library | 1 sesi belajar | `diaries/CONTEXT.md` | lihat `diaries/_log.md` |
| `_assets/` + `_aturan/` + `referensi/` | Knowledge bundle (factory) | pengetahuan persisten ITERA + metode | `_assets/CONTEXT.md`, `_aturan/CONTEXT.md`, `referensi/CONTEXT.md` | — |
| `_templates/` | Stamp | pekerjaan baru = salinan | `_templates/diary.md` | — |

Factory (stabil lintas run): `_assets/` (konteks MK/ITERA), `_aturan/` (aturan penulisan), `referensi/` (metode analisis isu).

Product (baru tiap sesi): `modul/*/output/`, `diaries/*.md`.

Status setiap area dibaca dengan memindai apa yang ada di `output/` / `_log.md`, bukan dari sini.
