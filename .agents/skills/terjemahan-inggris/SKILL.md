---
name: terjemahan-inggris
description: >-
  Membantu menerjemahkan dan menuliskan ulang kalimat atau teks dari bahasa Indonesia ke bahasa Inggris dengan penyesuaian register (formal/informal), laras bahasa (kasual/saintifik/profesional), dan platform sasaran (artikel panjang/jurnal, email, komentar media sosial, dll), dilengkapi analisis mendalam tentang kosakata, struktur kalimat, gaya penulisan, serta penggunaan ungkapan/idiom. Gunakan setiap kali pengguna meminta "bantu saya terjemahkan ke bahasa Inggris", "terjemahkan ini ke bahasa Inggris", "translate this", "terjemahkan ke english", atau permintaan sejenis untuk alih bahasa/parafrasa ke bahasa Inggris.
---

# Instruksi Skill: terjemahan-inggris

Skill ini digunakan untuk membantu pengguna menerjemahkan, memparafrasa, dan menuliskan ulang (*rephrase*) kalimat atau paragraf dari bahasa Indonesia ke bahasa Inggris secara alami (*native-like*), kontekstual, dan bernas, lengkap dengan analisis linguistik mendalam.

---

## 1. Ambang Pemakaian & Pemicu (*Trigger*)

Gunakan skill ini ketika pengguna memberikan perintah atau kalimat masukan dengan frasa seperti:
- *"bantu saya terjemahkan ke bahasa Inggris"*
- *"terjemahkan ini ke bahasa Inggris"*
- *"translate this"*
- *"terjemahkan ke english"*
- *"bagaimana bahasa Inggrisnya kalimat ini..."*
- *"tulis ulang teks ini dalam bahasa Inggris"*

---

## 2. Alur Kerja (*Workflow*)

Proses penerjemahan dan penulisan ulang mengikuti 3 langkah:

```
[Masukan Teks & Permintaan] 
       │
       ▼
[Langkah 1: Identifikasi / Klarifikasi Suasana & Platform]
       │
       ▼
[Langkah 2: Eksekusi Terjemahan & Variasi]
       │
       ▼
[Langkah 3: Analisis Mendalam (Kosakata, Struktur, Gaya, Ungkapan)]
```

### Langkah 1: Identifikasi / Klarifikasi Konteks

Sebelum menerjemahkan, periksa apakah pengguna telah menyebutkan konteks penuturan dan platform sasaran:

1. **Jika konteks sudah jelas dari permintaan awal** (misalnya: *"terjemahkan ini untuk paper jurnal ilmiah"* atau *"translate this for a casual Instagram comment"*):
   - Langsung lakukan penerjemahan sesuai konteks tersebut tanpa perlu bertanya lagi.
2. **Jika konteks belum ditentukan / ambigu**:
   - Berikan identifikasi dan tanyakan/konfirmasikan preferensi suasana penuturan kepada pengguna secara ringkas:
     - **Tingkat Formalitas (*Register*)**: Formal vs Informal.
     - **Laras Bahasa (*Tone/Domain*)**: Kasual (santai/sehari-hari) vs Profesional/Bisnis vs Akademik/Saintifik.
     - **Platform Sasaran**: 
       - *Tulisan Panjang / Artikel*: Naskah jurnal ilmiah, esai, laporan teknis, buku ajar, blog post.
       - *Komunikasi Profesional*: Email resmi, surat pengantar (*cover letter*), proposal kerja sama.
       - *Media Sosial & Komentar*: Komentar LinkedIn/X/Instagram/Reddit, caption singkat, forum diskusi.
       - *Presentasi & Salindia*: Poin salindia (*bullet points*), naskah pidato (*speech script*).
   - *(Tips Proaktif)*: Anda dapat menyodorkan draf terjemahan berdasarkan asumsi paling logis (misalnya laras akademik/profesional untuk tulisan dosen) sambil menawarkan opsi penyesuaian jika pengguna menginginkan suasana lain.

---

### Langkah 2: Penyusunan Terjemahan & Variasi Kalimat

Sajikan hasil terjemahan dalam beberapa opsi yang terkalibrasi:

1. **Terjemahan Rekomendasi Utama (*Primary Recommendation*)**:
   - Versi yang paling seimbang, alami (*natural flow*), dan sesuai dengan suasana serta platform yang dituju.
2. **Variasi Alternatif (*Alternative Variations*)**:
   - **Versi Ringkas & Tegas (*Concise & Direct*)**: Cocok untuk media sosial, email cepat, atau slide.
   - **Versi Idiomatis / Ekspresif (*Native Idiomatic / Conversational*)**: Cocok untuk obrolan santai atau tulisan naratif.
   - **Versi Formal / Akademik Tingkat Tinggi (*High Academic / Formal*)**: Menggunakan kosakata akademik lanjutan (*advanced academic vocabulary*) dan struktur klausa yang elegan.

---

### Langkah 3: Analisis Mendalam (*In-Depth Linguistic Breakdown*)

Setiap hasil terjemahan wajib disertai 4–5 dimensi analisis mendalam:

#### A. Analisis Kosakata & Diksi (*Vocabulary & Diction*)
- **Pemilihan Kata Kunci**: Jelaskan alasan pemilihan kata tertentu (*word choice*) dan padanan maknanya.
- **Nuansa Kata (*Connotation vs. Denotation*)**: Bedakan nuansa antar kata (misal: *examine* vs *scrutinize* vs *investigate*; *crucial* vs *essential* vs *vital*).
- **Alternatif Diksi Tingkat Lanjut**: Berikan opsi sinonim atau istilah spesifik bidang (*field-specific terminology*).

#### B. Analisis Struktur Kalimat & Sintaksis (*Sentence Structure & Grammar*)
- **Pola Kalimat**: Uraikan pola tata bahasa yang digunakan (misal: *compound-complex sentence*, *participial phrase*, *nominalization*, *inversion*, *active vs passive voice*).
- **Aliran & Irama Kalimat (*Flow & Rhythm*)**: Jelaskan mengapa struktur tersebut dipilih agar terhindar dari kesan terjemahan harfiah (*literal/word-by-word translation*).

#### C. Analisis Gaya Penulisan & Kesesuaian Platform (*Style & Tone Fit*)
- **Kesesuaian Nada**: Jelaskan bagaimana kalimat tersebut cocok dengan platform sasaran (misal: penggunaan *hedging language* seperti *suggests/indicates* untuk jurnal ilmiah; atau gaya *engaging & hook-driven* untuk media sosial).
- **Elemen Gaya**: Penggunaan kontraksi (*it's* vs *it is*), sudut pandang (*first-person vs third-person*), serta tingkat kehangatan/jarak interpersonal.

#### D. Penggunaan Ungkapan, Idiom & Kolokasi (*Expressions, Collocations & Idioms*)
- **Kolokasi Alami (*Natural Collocations*)**: Tunjukkan pasangan kata lazim yang digunakan penutur asli (misal: *conduct research* bukan *make research*; *pose a challenge*, *pave the way*).
- **Kata Penghubung / Transisi (*Connectors & Discourse Markers*)**: Penggunaan transisi yang tepat (misal: *furthermore*, *on the other hand*, *consequently*, *meanwhile*).
- **Frasa Idiomatis**: Ungkapan atau idiom khas bahasa Inggris yang memperkaya rasa bahasa.

#### E. Catatan Nuansa Lintas Bahasa & Budaya (*Cross-Cultural / Pragmatic Notes*)
- Catatan khusus jika ada pergeseran konsep budaya, ungkapan khas Indonesia yang tidak memiliki padanan langsung 1-ke-1, atau kaidah kesantunan (*politeness strategies*) dalam bahasa Inggris.

---

## 3. Matriks Acuan Laras Bahasa & Platform

Gunakan tabel acuan ini untuk memandu pemilihan gaya bahasa:

| Laras Bahasa | Platform Sasaran | Karakteristik Diksi & Struktur | Contoh Ciri Khas |
| :--- | :--- | :--- | :--- |
| **Saintifik / Akademik** | Jurnal, Prosiding, Skripsi/Tesis, Buku Ajar | Diksi presisi, formal, tanpa kontraksi, *nominalization*, penggunaan *hedging* (*tends to, indicates*) | *"The findings suggest a substantial correlation..."* |
| **Profesional / Bisnis** | Email kantor, Proposal kerja sama, LinkedIn | Sopan, ringkas, berorientasi tindakan (*action-oriented*), *active voice* yang jelas | *"I would welcome the opportunity to discuss how we can collaborate on..."* |
| **Media Sosial / Kasual** | Twitter/X, Instagram, Komentar Reddit/TikTok | Luwes, ekspresif, menggunakan kontraksi (*I'm, don't*), idiomatis, ritme cepat | *"Totally agree! That really hits the nail on the head."* |
| **Presentasi / Salindia** | Slide deck, Catatan pembicara (*speaker notes*) | Frasa nominal padat, kata kerja kuat (*action verbs*), minim kata sambung bertele-tele | *"Accelerating urban mobility through AI-driven traffic systems."* |

---

## 4. Format Keluaran Standar (*Standard Output Template*)

Gunakan templat berikut saat menyajikan respons kepada pengguna:

```markdown
### 🎯 Konteks & Suasana Penuturan
- **Formalitas & Laras Bahasa**: [Formal / Informal] — [Akademik / Profesional / Kasual]
- **Platform Sasaran**: [Artikel Ilmiah / Email / Komentar Media Sosial / dll.]

---

### 📝 Hasil Terjemahan & Penulisan Ulang

#### 1. Rekomendasi Utama (Primary Recommendation)
> **"..."**

#### 2. Variasi Alternatif (Alternative Variations)
- **Versi Ringkas (*Concise*)**: *"..."*
- **Versi Idiomatis / Ekspresif (*Idiomatic*)**: *"..."*
- **Versi Formal Lanjutan (*Advanced / High Academic*)**: *"..."*

---

### 🔍 Analisis Linguistik Mendalam

#### A. Kosakata & Diksi (Vocabulary & Diction)
- `[Kata/Frasa]`: [Alasan pemilihan kata, nuansa makna, dan alternatif sinonim].
- `[Kata/Frasa]`: [Penjelasan nuansa].

#### B. Struktur Kalimat & Sintaksis (Sentence Structure)
- **Pola Kalimat**: [Penjelasan struktur gramatikal, pemecahan klausa, atau penyusunan subjek-predikat].
- **Kenapa Alami**: [Alasan mengapa susunan ini lebih luwes dibandingkan terjemahan kata-per-kata].

#### C. Gaya Penulisan & Platform (Style & Platform Fit)
- [Penjelasan keselarasan nada dengan media/platform yang dipilih].

#### D. Ungkapan, Kolokasi & Idiom (Expressions & Collocations)
- **Kolokasi**: `[Pasangan kata]` — [Penjelasan kelaziman pemakaian].
- **Transisi/Idiom**: `[Frasa]` — [Makna kontekstual].

#### E. Catatan Pragmatik / Budaya (Optional / Cultural Nuance)
- [Catatan penyesuaian konteks jika relevan].
```

---

## 5. Contoh Penerapan (*Worked Example*)

### Contoh: Teks Masukan Pengguna
> *"bantu saya terjemahkan ke bahasa Inggris: Penelitian ini dilakukan untuk mengetahui seberapa besar pengaruh kemacetan lalu lintas terhadap tingkat stres dosen di lingkungan kampus ITERA. Hasilnya menunjukkan bahwa sebagian besar dosen merasa sangat terbebani kalau jalanan macet parah di pagi hari."*
> 
> *Konteks: Artikel Jurnal Ilmiah (Akademik Formal)*

### Contoh Keluaran yang Dihasilkan:

```markdown
### 🎯 Konteks & Suasana Penuturan
- **Formalitas & Laras Bahasa**: Formal — Akademik / Saintifik
- **Platform Sasaran**: Naskah Jurnal Ilmiah / Artikel Penelitian

---

### 📝 Hasil Terjemahan & Penulisan Ulang

#### 1. Rekomendasi Utama (Primary Recommendation)
> **"This study aims to examine the extent to which traffic congestion affects stress levels among faculty members within the ITERA campus environment. The findings indicate that the majority of lecturers experience substantial psychological strain during severe morning traffic jams."**

#### 2. Variasi Alternatif (Alternative Variations)
- **Versi Ringkas (*Concise*)**: *"This study investigates the impact of traffic congestion on faculty stress levels at ITERA, revealing that severe morning delays significantly heighten lecturer strain."*
- **Versi Pasif Akademik Tradisional (*Traditional Academic Passive*)**: *"An investigation was conducted to determine the influence of traffic congestion on faculty stress at ITERA, with results demonstrating notable morning distress."*

---

### 🔍 Analisis Linguistik Mendalam

#### A. Kosakata & Diksi (Vocabulary & Diction)
- `faculty members` / `lecturers`: Digunakan alih-alih sekadar *teachers* karena dalam konteks perguruan tinggi, staf pengajar akademik disebut *faculty members* atau *lecturers/academics*.
- `psychological strain` / `stress levels`: Padanan yang lebih akademis untuk *"sangat terbebani"*, menggantikan frasa informal seperti *felt very burdened*.
- `examine the extent to which`: Frasa standar dalam metodologi riset untuk menerjemahkan *"mengetahui seberapa besar pengaruh"*, lebih terukur daripada *to know how big the influence is*.

#### B. Struktur Kalimat & Sintaksis (Sentence Structure)
- Menggunakan struktur klausa *noun clause* (*"the extent to which..."*) untuk merangkai objek tujuan penelitian secara akademis dan elegan.
- Kalimat kedua membagi fokus temuan dengan subjek penegas *"The findings indicate that..."* yang umum dalam abstrak artikel ilmiah (*academic reporting verbs*).

#### C. Gaya Penulisan & Platform (Style & Platform Fit)
- Tanpa kontraksi (*this study aims* bukan *it's aiming*).
- Menggunakan kata kerja pengantar objektif (*aims to examine*, *findings indicate*) yang lazim pada publikasi IMRaD (Introduction, Methods, Results, and Discussion).

#### D. Ungkapan, Kolokasi & Idiom (Expressions & Collocations)
- **Kolokasi**: `traffic congestion` (pasangan kata baku untuk kemacetan lalu lintas, lebih formal daripada sekadar *traffic jam*).
- **Kolokasi**: `severe morning traffic` (penggabungan intensitas *severe* dengan waktu *morning traffic*).
```
