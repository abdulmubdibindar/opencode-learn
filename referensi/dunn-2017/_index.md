# Ekstraksi Penuh: Public Policy Analysis: An Integrated Approach

Ekstraksi lengkap teks **dan** gambar dari berkas PDF (499 halaman).

- **Sumber**: *Public Policy Analysis: An Integrated Approach* (William N. Dunn, 2017)
- **Penulis**: Dunn, William N.

## Isi Direktori

| Berkas | Bagian | Ukuran teks |
| --- | --- | ---: |
| [00_Title_Page.md](00_Title_Page.md) | Title Page | 0 KB |
| [01_Copyright.md](01_Copyright.md) | Copyright | 2 KB |
| [02_Dedication.md](02_Dedication.md) | Dedication | 0 KB |
| [03_Brief_Contents.md](03_Brief_Contents.md) | Brief Contents | 1 KB |
| [04_Box_Contents.md](04_Box_Contents.md) | Box Contents | 1 KB |
| [05_Case_Study_Contents.md](05_Case_Study_Contents.md) | Case Study Contents | 2 KB |
| [06_Visual_Display_Contents.md](06_Visual_Display_Contents.md) | Visual Display Contents | 13 KB |
| [07_Detailed_Contents.md](07_Detailed_Contents.md) | Detailed Contents | 21 KB |
| [08_Preface.md](08_Preface.md) | Preface | 6 KB |
| [09_Acknowledgements.md](09_Acknowledgements.md) | Acknowledgements | 6 KB |
| [10_PART_I_Methodology_of_Policy_Analysis.md](10_PART_I_Methodology_of_Policy_Analysis.md) | PART I: Methodology of Policy Analysis | 200 KB |
| [11_PART_II_Methods_of_Policy_Analysis.md](11_PART_II_Methods_of_Policy_Analysis.md) | PART II: Methods of Policy Analysis | 754 KB |
| [12_PART_III_Methods_of_Policy_Communication.md](12_PART_III_Methods_of_Policy_Communication.md) | PART III: Methods of Policy Communication | 245 KB |
| [13_APPENDIX_1_Policy_Issue_Papers.md](13_APPENDIX_1_Policy_Issue_Papers.md) | APPENDIX 1 Policy Issue Papers | 16 KB |
| [14_APPENDIX_2_Executive_Summaries.md](14_APPENDIX_2_Executive_Summaries.md) | APPENDIX 2 Executive Summaries | 0 KB |
| [15_APPENDIX_3_Policy_Memoranda.md](15_APPENDIX_3_Policy_Memoranda.md) | APPENDIX 3 Policy Memoranda | 1116 KB |
| [16_APPENDIX_4_Planning_Oral_Briefings.md](16_APPENDIX_4_Planning_Oral_Briefings.md) | APPENDIX 4 Planning Oral Briefings | 39 KB |
| `gambar/` | 8 gambar figur, render 200 dpi | — |
| `gambar/_raster_mentah/` | 100 raster asli dari PDF (arsip) | — |
| `_figur.json` | metadata gambar (nomor, halaman, caption) | — |

## Daftar Gambar

| No. | Judul | Hal. PDF | Berkas |
| --- | --- | ---: | --- |
| 1.3 | Opportunity Costs of Using Multiple Methods  18 | 18 | [figure_1_3.png](gambar/figure_1_3.png) |
| 1.4 | Elements of a Policy Argument  20 Chapter Summary  22 | 18 | [figure_1_4.png](gambar/figure_1_4.png) |
| 2.1 | Complexity, Feedback, and Short Circuiting in the Policymaking Process  46 Models of Policy Change  47 The Comprehensive Rationality Model  47 Second-Best Rationality  48 Table 2.2 The Voters’ Paradox  49 Disjointed Incrementalism  50 Bounded Rationality  50 Erotetic Rationality  51 Simultaneous Convergence  52 Punctuated Equilibrium  53 | 19 | [figure_2_1.png](gambar/figure_2_1.png) |
| 3.1 | The Process of Problem Structuring  71 | 19 | [figure_3_1.png](gambar/figure_3_1.png) |
| 3.10 | Set Union  95 Figure 3.11 Set Intersection  96 Figure 3.12 Classification Scheme  96 Figure 3.13 Cross break  96 Hierarchy Analysis  96 Figure 3.14 Hierarchy Analysis of the Causes of Fires  98 Synectics  99 Brainstorming  100 Multiple Perspective Analysis  102 Assumptional Analysis  104 Figure 3.15 The Process of Assumptional Analysis  105 Argument Mapping  106 Figure 3.16 Plausibility and Importance of Warrant about Opportunity Costs of Driving at Lower Speeds  107 | 20 | [figure_3_10.png](gambar/figure_3_10.png) |
| 4.1 | Processes of Intuition (System I) and Reasoning (System II)  120 Limitations of Forecasting  121 Societal Futures  123 Figure 4.2 Three Types of Societal Futures: Potential, Plausible, and Normative  124 | 20 | [figure_4_1.png](gambar/figure_4_1.png) |
| 5.6 | Objectives Tree for National Energy Policy  221 Values Clarification  222 Values Critique  223 Figure 5.7 Value-Critical Discourse  224 Cost Element Structuring  225 Table 5.7 Cost Element Structure  225 Figure 5.8 Simplified Partial Cost Model for Total Initial Investment  227 Cost Estimation  226 Shadow Pricing  226 Constraints Mapping  228 Cost Internalization  229 Figure 5.9 Constraints Map for National Energy Policy  230 Discounting  231 Table 5.8 Internal, External, and Total Costs of Maternal Care  231 Figure 5.10 Comparison of Discounted and Undiscounted Costs Cumulated for Two Programs with Equal Effectiveness  232 Table 5.9 Calculation of Present Value of Cost Stream at 10 Percent Discount Rate over 5 Years (in Millions of Dollars)  234 Sensitivity Analysis  235 Plausibility Analysis  235 Table 5.10 Sensitivity Analysis of Gasoline Prices on Costs of Training Programs  236 Figure 5.11 Threats to the Plausibility of Claims about the Benefits of the 55 mph Speed Limit  237 | 22 | [figure_5_6.png](gambar/figure_5_6.png) |
| 6.2 | Steps in Conducting a Systematic Review or Meta-Analysis  275 | 23 | [figure_6_2.png](gambar/figure_6_2.png) |

## Cara Ekstraksi

- Teks diambil per blok mengikuti urutan baca halaman; header/footer berjalan dibuang dan kata yang terpenggal antarbaris disambung kembali.
- Penanda `<!-- hal. PDF n -->` menandai awal tiap halaman PDF agar mudah dirujuk balik ke berkas aslinya.
- Judul bab dan subbab diangkat dari bookmark PDF, sehingga hierarki `##`–`######` mengikuti struktur asli dokumen. Bila PDF tidak punya bookmark, judul dikenali dari ukuran dan ketebalan fon.
- Gambar dirender ulang dari halaman pada wilayah di atas caption-nya, sehingga diagram vektor ikut terbawa utuh. Teks yang sudah termuat di dalam gambar tidak diulang sebagai paragraf.

> [!WARNING] Batas ketelitian
> Tabel terekstrak sebagai **teks berurutan**, bukan tabel Markdown — struktur baris dan kolomnya tidak dipertahankan. Rujuk PDF asli bila membutuhkan tabel yang presisi.
