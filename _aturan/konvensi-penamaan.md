---
type: aturan
title: konvensi-penamaan
description: Kaidah penamaan berkas dan folder di direktori LernOpenCode — kebab-case, tipe-prefix, dan underscore untuk folder sistem.
tags:
  - konvensi
---

# Konvensi Penamaan

> [!INFO] Stub — isi minimal dari sumber vault (dokumen induk). Lengkapi dari vault ITERA besar bila perlu; yang ditulis di sini sudah cukup untuk dipakai direktori ini.

## Aturan inti

- **Folder stage / berurutan**: prefiks ordinal `NN_kebab-name` (mis. `01_referensi`, `02_draf`). Mengubah nomor folder = mengubah urutan pipeline — itu intinya.
- **Folder sistem**: prefiks underscore `_` dan terurut ke atas (`_meta/`, `_system/`, `_shared/`, `_config/`, `_templates/`, `_index/`, `_archive/`, `_aturan/`, `_assets/`). Underscore = "tentang workspace, bukan dari workspace".
- **Berkas berurutan di dalam folder**: prefiks `NN_nama` atas dasar urutan (`00-tracker.md`).
- **Record / node**: kebab-case untuk berkas yang dibaca mesin; Title Case di Obsidian yang dibaca manusia sehari-hari. Pilih satu per workspace.
- **Berkas bertipe**: boleh ber-prefiks tipe — `data-<sesuatu>.md`.
- **Berkas cermin bahasa Inggris**: akhiran `-en.md` (mis. `2026-09-04-first-work-en.md`).

## Rujukan

- Cara merujuk berkas: [[rujukan-berkas]] (di direktori ini).
