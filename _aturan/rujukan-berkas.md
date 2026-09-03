---
type: aturan
project: itera-umum
title: rujukan-berkas
description: Cara merujuk berkas dalam teks — wikilink untuk berkas .md, awalan @ untuk berkas non-md — berlaku di mana pun rujukan ditulis, termasuk sel tabel.
tags:
  - itera
  - icm
---

# Rujukan Berkas dalam Teks

## Aturan Inti

Ketika sebuah dokumen merujuk berkas lain, bentuk rujukannya ditentukan oleh **jenis berkas yang dituju**, bukan oleh tempat rujukan itu ditulis:

- **Berkas `.md`** → tautan wiki `[[nama-berkas]]`, tanpa ekstensi.
- **Berkas non-md** (skrip, dataset, dokumen kantor, gambar, PDF, dst.) → awalan `` `@nama-berkas.ext` ``, lengkap dengan ekstensinya, ditulis dalam kutip balik.

Aturan ini berlaku **di mana pun** rujukan ditulis — dalam kalimat naratif, paragraf, maupun **di dalam sel tabel perutean**. Tidak ada pengecualian bentuk tabel: sebuah `.md` tetap wikilink meski berada di dalam sel, bukan `` `@spec.md` ``.

| Ditulis di... | Merujuk `.md` | Merujuk non-md |
| --- | --- | --- |
| Kalimat/paragraf | `[[nama-berkas]]` | `` `@nama-berkas.py` `` |
| Sel tabel perutean | `[[nama-berkas]]` | `` `@nama-berkas.xlsx` `` |

## Kenapa Dua Bentuk

- **Wikilink `[[..]]`** dipahami Obsidian: ia ikut diperbarui saat berkas dinamai ulang lewat Obsidian (lihat [[konvensi-penamaan]] bagian 5), dan Obsidian bisa menavigasikannya langsung. Wikilink hanya berfungsi untuk berkas yang Obsidian kenali sebagai catatan — yaitu `.md`.
- **Awalan `@`** dipakai untuk berkas yang wikilink Obsidian tidak menanganinya dengan baik (skrip, dataset, dokumen kantor, gambar), dan sudah dikenali agen (Claude Code) sebagai penanda "ini rujukan ke berkas dalam teks" — bukan kata biasa.

## Dua Pengecualian

**Nama berkas yang tidak unik di seluruh direktori ITERA** (`spec.md`, `_index.md`, `CONTEXT.md`, `CONTEXT_QUARTO.md`, dst. — ada puluhan salinan dengan nama sama, satu per mata kuliah/subproyek). Wikilink polos `[[spec]]` akan menggantung ke sasaran yang salah karena Obsidian tidak tahu salinan mana yang Anda maksud. Tulis wikilink dengan jalur lengkap dari akar vault, beri alias supaya tetap terbaca ringkas:

```
[[01 PENDIDIKAN/PL25-41003 Analitika Perkotaan/_assets/_index|_index]]
```

Ini mengikuti pola yang sudah dipakai di [[AGENTS]] akar untuk `[[00 JAKE VAN CLIEF's ICM/MODULES/MODULE 02-07|MODULE 02-07]]`. Berkas dengan nama yang memang unik di seluruh direktori (mis. `AGENTS-ANKOT-2026.md`, `overview-bab-buku.md`) tidak perlu jalur lengkap — `[[AGENTS-ANKOT-2026]]` sudah cukup.

**Penyebutan pola nama berkas, bukan rujukan ke satu berkas tertentu** — mis. "lihat `_index.md` di setiap direktori" atau "riwayatnya ada di `_log.md`" ketika yang dimaksud bukan satu berkas spesifik, melainkan konvensi penamaan yang berulang di banyak tempat (lihat [[konvensi-penamaan]] bagian 1). Ini bukan rujukan berkas — tulis polos dalam kutip balik, tanpa `@` dan tanpa wikilink: `` `_index.md` ``, `` `_log.md` ``.

## Contoh

Benar:

- "Baca [[konvensi-penamaan]] sebelum menamai berkas baru." (nama unik)
- "Jalankan `` `@ekstrak_pdf.py` `` dengan flag `--tabel`." (non-md)
- Tabel perutean, nama tidak unik: `| Menulis buku ajar | ./buku-ajar | [[01 PENDIDIKAN/PL25-41003 Analitika Perkotaan/2026/buku-ajar/spec\|spec]] |`
- Penyebutan pola: "Setiap direktori punya `_index.md` sendiri."

Salah:

- `` `@spec.md` `` — `spec.md` adalah berkas `.md`, harus wikilink.
- `[[spec]]` polos ketika ada banyak `spec.md` di direktori lain — menggantung ke sasaran yang tak pasti, harus dijalur-lengkapkan.
- `[[dataset.xlsx]]` — Obsidian tidak akan me-resolve ini sebagai catatan; harus `` `@dataset.xlsx` ``.

## Catatan Riwayat

Sebelum aturan ini ditulis, `@` sempat dipakai juga untuk berkas `.md` di beberapa tabel perutean (`@spec.md`, `@_index.md`, `@CONTEXT_QUARTO.md`, dan semacamnya). Itu bukan bentuk yang benar menurut aturan ini, dan sudah dimigrasikan ke wikilink di berkas-berkas entri tingkat mata kuliah dan templat. Dicatat di sini supaya pola lama itu tidak ditiru sebagai contoh oleh dokumen baru.

Pengecualian yang **tetap sah** dan sengaja tidak ikut dimigrasikan: subproyek yang sudah memakai `@nama.md` sebagai gaya sitasi pustaka (mis. `@anderson1995guidelines.md` di `Buku-Brimeta/brainstorm`) — itu konvensi sitasi akademik yang lebih dulu ada di subproyek itu, bukan rujukan berkas ICM, dan berada di luar cakupan aturan ini.

## Rujukan

- Nama berkas dan folder: [[konvensi-penamaan]]
- Kenapa duplikasi dan bentuk dokumentasi lain di direktori ini seperti sekarang: [[aturan-dokumentasi]]
