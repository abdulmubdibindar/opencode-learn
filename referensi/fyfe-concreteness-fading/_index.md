# Ekstraksi Penuh: Dokumen PDF

Ekstraksi lengkap teks **dan** gambar dari berkas PDF (43 halaman).

- **Sumber**: 2366_Making-concreteness-fading.pdf

## Isi Direktori

| Berkas | Bagian | Ukuran teks |
| --- | --- | ---: |
| [00_Abstract_word_count_149_max_250.md](00_Abstract_word_count_149_max_250.md) | Abstract (word count = 149; max = 250) | 1 KB |
| [01_Making_Concreteness_Fading_More_Concrete_as_a_Theory_of_Instruction_fo.md](01_Making_Concreteness_Fading_More_Concrete_as_a_Theory_of_Instruction_fo.md) | Making “Concreteness Fading” More Concrete as a Theory of Instruction for Promoting Transfer | 2 KB |
| [02_Brief_Background_on_Concreteness_Fading.md](02_Brief_Background_on_Concreteness_Fading.md) | Brief Background on Concreteness Fading | 4 KB |
| [03_Aim_1_Define_Key_Terms_Relevant_for_Concreteness_Fading.md](03_Aim_1_Define_Key_Terms_Relevant_for_Concreteness_Fading.md) | Aim 1: Define Key Terms Relevant for Concreteness Fading | 2 KB |
| [04_What_is_an_Abstract_Representation.md](04_What_is_an_Abstract_Representation.md) | What is an Abstract Representation? | 9 KB |
| [05_What_is_a_Concrete_Representation.md](05_What_is_a_Concrete_Representation.md) | What is a Concrete Representation? | 7 KB |
| [06_What_is_Concreteness_Fading.md](06_What_is_Concreteness_Fading.md) | What is Concreteness Fading? | 9 KB |
| [07_Aim_2_Describe_Six_Testable_Hypotheses_for_Researchers.md](07_Aim_2_Describe_Six_Testable_Hypotheses_for_Researchers.md) | Aim 2: Describe Six Testable Hypotheses for Researchers | 0 KB |
| [08_Hypothesis_1.md](08_Hypothesis_1.md) | Hypothesis 1 | 4 KB |
| [09_Hypothesis_2.md](09_Hypothesis_2.md) | Hypothesis 2 | 2 KB |
| [10_Hypothesis_3.md](10_Hypothesis_3.md) | Hypothesis 3 | 4 KB |
| [11_Hypothesis_4.md](11_Hypothesis_4.md) | Hypothesis 4 | 2 KB |
| [12_Hypothesis_5.md](12_Hypothesis_5.md) | Hypothesis 5 | 2 KB |
| [13_Hypothesis_6.md](13_Hypothesis_6.md) | Hypothesis 6 | 4 KB |
| [14_Conclusion.md](14_Conclusion.md) | Conclusion | 3 KB |
| [15_References.md](15_References.md) | References | 14 KB |
| [16_Table_1.md](16_Table_1.md) | Table 1 | 0 KB |
| [17_Six_testable_hypotheses_that_should_support_research_on_concreteness_f.md](17_Six_testable_hypotheses_that_should_support_research_on_concreteness_f.md) | Six testable hypotheses that should support research on concreteness fading | 1 KB |
| [18_Figure_1.md](18_Figure_1.md) | Figure 1 | 0 KB |
| [19_Figure_2.md](19_Figure_2.md) | Figure 2 | 0 KB |
| [20_Figure_3.md](20_Figure_3.md) | Figure 3 | 0 KB |
| [21_Figure_4.md](21_Figure_4.md) | Figure 4 | 0 KB |
| [22_Figure_adapted_from_Palmer_1978.md](22_Figure_adapted_from_Palmer_1978.md) | Figure adapted from Palmer (1978) | 0 KB |
| `gambar/` | 0 gambar figur, render 200 dpi | — |
| `gambar/_raster_mentah/` | 5 raster asli dari PDF (arsip) | — |
| `_figur.json` | metadata gambar (nomor, halaman, caption) | — |


## Cara Ekstraksi

- Teks diambil per blok mengikuti urutan baca halaman; header/footer berjalan dibuang dan kata yang terpenggal antarbaris disambung kembali.
- Penanda `<!-- hal. PDF n -->` menandai awal tiap halaman PDF agar mudah dirujuk balik ke berkas aslinya.
- Judul bab dan subbab diangkat dari bookmark PDF, sehingga hierarki `##`–`######` mengikuti struktur asli dokumen. Bila PDF tidak punya bookmark, judul dikenali dari ukuran dan ketebalan fon.
- Gambar dirender ulang dari halaman pada wilayah di atas caption-nya, sehingga diagram vektor ikut terbawa utuh. Teks yang sudah termuat di dalam gambar tidak diulang sebagai paragraf.

> [!WARNING] Batas ketelitian
> Tabel terekstrak sebagai **teks berurutan**, bukan tabel Markdown — struktur baris dan kolomnya tidak dipertahankan. Rujuk PDF asli bila membutuhkan tabel yang presisi.
