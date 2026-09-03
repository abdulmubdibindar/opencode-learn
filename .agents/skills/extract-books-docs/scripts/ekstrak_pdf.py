# -*- coding: utf-8 -*-
"""Ekstraksi buku PDF menjadi Markdown per bab beserta gambarnya.

Pemakaian:
    python ekstrak_pdf.py --pdf BUKU.pdf --keluaran DIR_HASIL
    python ekstrak_pdf.py --pdf BUKU.pdf --keluaran DIR_HASIL --tabel hibrida
    python ekstrak_pdf.py --pdf BUKU.pdf --keluaran HASIL.md --tunggal
    python ekstrak_pdf.py --pdf BUKU.pdf --profil            # kenali fon & ukuran
    python ekstrak_pdf.py --pdf BUKU.pdf --periksa 28,127    # bedah blok halaman

Butuh PyMuPDF (`pip install pymupdf`).
"""
import argparse, io, json, os, re, sys, unicodedata
from collections import Counter

import fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# dua nomor ("Gambar 2.1 …") atau satu nomor wajib bertitik ("Gambar 3. …")
FIGPAT = re.compile(r'^\s*(?:Figure|Gambar)\s+(\d+)(?:[.\-](\d+)\b|\.)')
TABPAT = re.compile(r'^\s*(?:Table|Tabel)\s+(\d+)(?:[.\-](\d+)\b|\.)')


def kunci_fig(m):
    return m.group(1) + ('.' + m.group(2) if m.group(2) else '')


SH = '­'          # soft hyphen: penanda kata terpenggal antarbaris
LIGA_TI = ('\x1f', '\x1e', '\x02', '\x03')   # ligatur "ti" pada sebagian fon


# --------------------------------------------------------------- pembersihan
def norm(s):
    s = unicodedata.normalize("NFKD", s)
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'),
                 ('”', '"'), ('–', '-'), ('—', '-'),
                 ('−', '-')):
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()


def clean(raw):
    """Rapikan teks satu blok tanpa menghilangkan isi.

    Dua hal yang gampang terlewat: ligatur yang tersimpan sebagai kode kontrol
    (jadi "creativity" terbaca "crea vity") dan kata yang terpenggal antarbaris
    (jadi "specific" terbaca "spe cific"). Keduanya ditangani di sini.
    """
    s = raw.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    for c in LIGA_TI:
        s = s.replace(c, 'ti')
    s = s.replace('​', '')
    s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1d]', '', s)
    for sp in (' ', ' ', ' ', ' ', ' ', ' '):
        s = s.replace(sp, ' ')
    s = s.replace('\t', ' ')
    out = ''
    for line in (l.strip() for l in s.split('\n')):
        if not line:
            continue
        line = line.lstrip(SH)
        if not out:
            out = line
        elif out.endswith(SH):                 # terpenggal -> sambung rapat
            out = out[:-1] + line
        elif out.endswith('-') and not out.endswith('--'):
            out += line                        # tanda hubung asli -> pertahankan
        else:
            out += ' ' + line
    return re.sub(r' {2,}', ' ', out.replace(SH, '')).strip()


def slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', norm(s)).strip('_')[:70]


# ------------------------------------------------------- profil fon dokumen
def profil_dokumen(doc):
    """Kenali ukuran & fon teks berjalan, lalu ukuran caption.

    Fon caption dan fon label di dalam gambar berbeda dari fon teks berjalan.
    Perbedaan itulah yang dipakai untuk (a) membedakan caption asli dari
    kalimat rujukan "Figure 6.3 helps depict…" di badan teks, dan (b) menandai
    mana teks yang sebenarnya bagian dari gambar. Karena tiap penerbit memakai
    fon berbeda, ukurannya dideteksi dari dokumen, bukan dipatok di kode.
    """
    per_ukuran, per_fon, cap_ukuran = Counter(), Counter(), Counter()
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b["type"] == 1:
                continue
            teks = "".join(sp["text"] for ln in b["lines"] for sp in ln["spans"])
            for ln in b["lines"]:
                for sp in ln["spans"]:
                    n = len(sp["text"])
                    per_ukuran[round(sp["size"], 1)] += n
                    per_fon[(sp["font"].split('-')[0], round(sp["size"], 1))] += n
            if FIGPAT.match(clean(teks)):
                cap_ukuran[round(max(sp["size"] for ln in b["lines"]
                                     for sp in ln["spans"]), 1)] += 1
    ukuran_badan = per_ukuran.most_common(1)[0][0]
    total = sum(per_ukuran.values())
    fon_prosa = {f for (f, u), n in per_fon.items()
                 if abs(u - ukuran_badan) < 1.2 and n > total * 0.01}
    # fon prosa utama = teks berjalan; fon prosa lain biasanya kotak sisipan
    # (mis. "Personal Reflection", "Case Scenario") yang layak jadi kutipan.
    per_keluarga = Counter()
    for (f, u), n in per_fon.items():
        if f in fon_prosa:
            per_keluarga[f] += n
    fon_badan = per_keluarga.most_common(1)[0][0] if per_keluarga else ""
    kandidat = [u for u in cap_ukuran if u < ukuran_badan - 0.2]
    ukuran_caption = max(kandidat) if kandidat else ukuran_badan
    return {"ukuran_badan": ukuran_badan, "fon_prosa": sorted(fon_prosa),
            "fon_badan": fon_badan, "ukuran_caption": ukuran_caption,
            "sebaran_ukuran": per_ukuran.most_common(8),
            "sebaran_caption": cap_ukuran.most_common(8)}


# ------------------------------------------------------------ blok halaman
def blok_halaman(doc, pno, prof):
    page = doc[pno]
    H, W = page.rect.height, page.rect.width
    items = []
    for b in page.get_text("dict")["blocks"]:
        x0, y0, x1, y1 = b["bbox"]
        if b["type"] == 1:
            items.append({"kind": "img", "bbox": b["bbox"], "y": y0})
            continue
        raw = "\n".join("".join(sp["text"] for sp in ln["spans"])
                        for ln in b["lines"])
        t = clean(raw)
        if not t:
            continue
        # header/footer berjalan: pendek dan menempel di tepi atas/bawah
        if ((y1 < H * 0.075 or y0 > H * 0.93) and len(t) < 90
                and not FIGPAT.match(t) and not TABPAT.match(t)):
            continue
        sizes = [sp["size"] for ln in b["lines"] for sp in ln["spans"]]
        fonts = [sp["font"] for ln in b["lines"] for sp in ln["spans"]]
        ukuran = max(sizes) if sizes else 0
        gaya_caption = (any('Itali' in f or 'Italic' in f for f in fonts)
                        and ukuran <= prof["ukuran_caption"] + 0.5)
        # dokumen tanpa pembeda gaya caption (ukuran caption = badan, tak
        # italik): terima caption polos yang pendek, asal bukan entri daftar
        # isi/gambar (bertitik pandu "....")
        if (not gaya_caption
                and prof["ukuran_caption"] >= prof["ukuran_badan"] - 0.2
                and ukuran <= prof["ukuran_caption"] + 0.5
                and len(t) < 100 and '....' not in t):
            gaya_caption = True
        items.append({
            "kind": "txt", "text": t, "bbox": b["bbox"], "y": y0, "size": ukuran,
            "bold": any('Bold' in f for f in fonts),
            "body": any(f.split('-')[0] in prof["fon_prosa"] for f in fonts),
            "panel": (all(f.split('-')[0] in prof["fon_prosa"] for f in fonts)
                      and all(f.split('-')[0] != prof["fon_badan"] for f in fonts)),
            "endhyph": raw.rstrip().endswith(SH),
            "figcap": bool(FIGPAT.match(t)) and gaya_caption,
            "tabcap": bool(TABPAT.match(t)) and gaya_caption,
        })
    items.sort(key=lambda it: (round(it["y"], 1), it["bbox"][0]))
    # caption yang terpecah jadi dua blok -> satukan kembali
    gabung = []
    for it in items:
        prev = gabung[-1] if gabung else None
        if (prev and (prev.get("figcap") or prev.get("tabcap"))
                and it["kind"] == "txt"
                and it["size"] <= prof["ukuran_caption"] + 0.5
                and not it["figcap"] and not it["tabcap"]
                and len(it["text"]) < 90    # sisa caption itu pendek;
                and -2 <= it["bbox"][1] - prev["bbox"][3] < 12):
            # paragraf badan yang menempel di bawah caption bukan sisa caption
            sep = "" if prev["endhyph"] else " "
            prev["text"] = (prev["text"].rstrip() + sep + it["text"]).strip()
            prev["endhyph"] = it["endhyph"]
            prev["bbox"] = tuple(fitz.Rect(prev["bbox"]) | fitz.Rect(it["bbox"]))
            continue
        gabung.append(it)
    return gabung, W, H


# --------------------------------------------------------------- diagnostik
def periksa(doc, prof, halaman):
    for pno in halaman:
        page = doc[pno - 1]
        print(f"=== hal. PDF {pno}  {page.rect}")
        for b in page.get_text("dict")["blocks"]:
            if b["type"] == 1:
                print("   RASTER", [round(v, 1) for v in b["bbox"]])
                continue
            t = "".join(sp["text"] for ln in b["lines"] for sp in ln["spans"])
            sp0 = b["lines"][0]["spans"][0]
            print(f"   {[round(v,1) for v in b['bbox']]} "
                  f"{sp0['font'][:26]:26s} {round(sp0['size'],1):5} {t[:60]!r}")
        dr = page.get_drawings()
        if dr:
            U = dr[0]["rect"]
            for g in dr[1:]:
                U = U | g["rect"]
            print(f"   VEKTOR n={len(dr)} gabungan={[round(v,1) for v in U]}")


# ------------------------------------------------------------ render gambar
def render_gambar(doc, prof, imgdir, dpi):
    """Render tiap figur dari halamannya, bukan sekadar mencomot raster.

    Banyak diagram buku berupa vektor: tidak ada raster yang bisa diekstrak.
    Yang selalu ada adalah caption-nya, jadi caption dipakai sebagai jangkar
    dan wilayah di atasnya dipotong.
    """
    zoom = fitz.Matrix(dpi / 72, dpi / 72)
    berkas, klip, meta = {}, {}, []
    for pno in range(doc.page_count):
        items, W, H = blok_halaman(doc, pno, prof)
        page = doc[pno]
        for idx, it in enumerate(items):
            if it["kind"] != "txt" or not it["figcap"]:
                continue
            m = FIGPAT.match(it["text"])
            kunci = kunci_fig(m)
            if kunci in berkas:              # caption lanjutan -> lewati
                continue
            nama = f"figure_{kunci.replace('.', '_')}.png"
            cx0, cy0, cx1, cy1 = it["bbox"]
            tegak = (cy1 - cy0) > (cx1 - cx0) * 1.2   # caption diputar 90°
            if tegak or W > H:
                clip = page.rect              # halaman lanskap -> ambil utuh
            else:
                # batas bawah figur sebelumnya di halaman yang sama
                dasar = max([o["bbox"][3] for o in items
                             if o["kind"] == "txt" and o["figcap"]
                             and o["bbox"][3] < cy0 - 2] or [0])
                unsur = [g["rect"] for g in page.get_drawings()
                         if g["rect"].y1 <= cy0 + 2 and g["rect"].y0 >= dasar - 1
                         and g["rect"].height > 1 and g["rect"].width > 1]
                for o in items:
                    if o is it or o["bbox"][3] > cy0 + 2 or o["bbox"][1] < dasar - 1:
                        continue
                    if o["kind"] == "img" or not o.get("body", True):
                        unsur.append(fitz.Rect(o["bbox"]))
                if unsur:
                    U = unsur[0]
                    for r in unsur[1:]:
                        U = U | r
                    atas = U.y0 - 6
                    for o in items:           # jangan memotong paragraf di atas
                        if (o["kind"] == "txt" and o.get("body", True)
                                and o["bbox"][3] <= U.y0 + 5):
                            atas = max(atas, o["bbox"][3] + 5)
                    clip = fitz.Rect(max(U.x0 - 8, 0), max(atas, dasar + 3, H * 0.05),
                                     min(U.x1 + 8, W), cy0 - 2)
                else:
                    atas = H * 0.07
                    for prev in items[:idx]:
                        if prev["kind"] == "txt" and prev["bbox"][3] < cy0 - 2:
                            atas = max(atas, prev["bbox"][3] + 4)
                    clip = fitz.Rect(W * 0.06, max(atas, H * 0.05), W * 0.94, cy0 - 2)
                if clip.height < 12 or clip.width < 25:
                    clip = page.rect          # potongan tak masuk akal
            page.get_pixmap(matrix=zoom, clip=clip, alpha=False).save(
                os.path.join(imgdir, nama))
            berkas[kunci] = nama
            meta.append({"key": kunci, "file": nama, "page": pno + 1,
                         "caption": it["text"]})
            klip.setdefault(pno, []).append(fitz.Rect(clip))
    return berkas, klip, meta


# ------------------------------------------------------------ tabel hibrida
def tabel_ke_markdown(data):
    """Susun tabel Markdown dari hasil Table.extract(), dengan perbaikan pola.

    Tiga hal yang diperbaiki (semuanya teramati pada instrumen LAMDEPILAR):
    header multi-baris ber-merge yang terfragmentasi per baris teks, sel merge
    vertikal yang muncul sebagai None di baris lanjutan, dan baris artefak
    berisi satu nilai yang terduplikasi ke seluruh kolom (mis. `|6|6|6|`).
    Mengembalikan (markdown, lolos_validasi, catatan).
    """
    catatan = []
    if not data or len(data) < 2:
        return "", False, ["tabel terlalu kecil"]
    ncol = max(len(r) for r in data)
    if ncol < 2:
        return "", False, ["hanya satu kolom"]
    rows = [list(r) + [None] * (ncol - len(r)) for r in data]
    sel = lambda c: '' if c is None else clean(str(c))
    # kolom yang seluruhnya kosong dibuang (sisa garis bantu deteksi)
    guna = [j for j in range(ncol) if any(sel(r[j]) for r in rows)]
    if len(guna) < 2:
        return "", False, ["hanya satu kolom berisi"]
    rows = [[r[j] for j in guna] for r in rows]
    while rows and not any(sel(c) for c in rows[0]):
        rows.pop(0)          # baris kosong di awal menggeser deteksi header
    if len(rows) < 2:
        return "", False, ["tabel terlalu kecil"]
    ncol = len(guna)
    if ncol > 20:
        return "", False, [f"{ncol} kolom — kemungkinan diagram yang salah "
                           "terdeteksi sebagai tabel"]
    # diagram/bagan yang salah terdeteksi sebagai tabel: selnya jarang terisi.
    # Tabel isian (rubrik dengan kolom skor kosong) juga jarang terisi, tapi
    # dikenali dari adanya sel prosa panjang — diagram tidak punya itu.
    prosa = any(len(sel(c)) >= 80 for r in rows for c in r)
    n_isi = sum(1 for r in rows for c in r if sel(c))
    if n_isi < len(rows) * ncol * 0.2 and not prosa:
        return "", False, [f"kepadatan sel rendah ({n_isi}/{len(rows)*ncol}) "
                           "— kemungkinan diagram, bukan tabel"]
    # teks terpotong batas kolom ("T"|"ahap 1. …") = garis grid memotong
    # tulisan; itu bukan tabel murni, cukup gambarnya saja
    potong = sum(1 for r in rows for a, b in zip(r, r[1:])
                 if 1 <= len(sel(a)) <= 2 and sel(b)[:1].islower())
    if potong >= 2:
        return "", False, [f"{potong} teks terpotong batas kolom — "
                           "kemungkinan diagram, bukan tabel"]
    # sel berisi kode data ("21", "A.2", "D.1 Legalitas…") menandai baris data
    kode = re.compile(r'^\d+$|^[A-Za-z]{1,3}\.\d+\b')
    ada_kode = lambda row: any(kode.match(sel(c)) for c in row if c)

    # wilayah header: baris 0 + baris lanjutan selama kolom pertamanya kosong
    # dan tidak ada sel berpola kode data (fragmen header terpecah per baris
    # teks). Tabel lanjutan lintas halaman mulai langsung dengan baris data —
    # baris 0 yang mengandung kode berarti tabel ini tanpa header.
    k = next((i for i, r in enumerate(rows[:11]) if ada_kode(r)), None)
    if k == 0:
        nhead = 0
    elif k and all(len(sel(c)) < 60 for r in rows[:k] for c in r):
        # semua baris sebelum baris berkode pertama bersel pendek ->
        # seluruhnya fragmen header (termasuk yang kolom pertamanya terisi)
        nhead = k
    else:
        nhead = 1
        while (nhead < len(rows) - 1 and nhead < 10
               and sel(rows[nhead][0]) == ''
               and not ada_kode(rows[nhead])
               and all(len(sel(c)) < 60 for c in rows[nhead])):
            nhead += 1
    header = []
    for j in range(ncol):
        frag, seen = [], None
        for i in range(nhead):
            f = sel(rows[i][j])
            if f and f != seen:
                frag.append(f)
                seen = f
        header.append(' '.join(frag).strip() or f"Kolom {j+1}")
    if nhead > 1:
        catatan.append(f"header direkonstruksi dari {nhead} baris fragmen")
    elif nhead == 0:
        catatan.append("tabel lanjutan tanpa header")

    body = []
    for i in range(nhead, len(rows)):
        r = [None if c is None else sel(c) for c in rows[i]]
        isi = [j for j in range(ncol) if r[j] not in (None, '')]
        if not isi:
            continue
        # baris seksi selebar tabel (satu sel teks di kolom pertama, sel lain
        # merge kosong) -> jangan warisi nilai kolom lain dari baris di atasnya
        if isi == [0] and not kode.match(r[0]):
            body.append([r[0]] + [''] * (ncol - 1))
            continue
        # None = sel merge vertikal -> warisi nilai baris sebelumnya
        rclean = [(body[-1][j] if body else '') if r[j] is None else r[j]
                  for j in range(ncol)]
        # baris yang hanya mengisi sel kosong baris sebelumnya (sel yang
        # merentang beberapa baris teks, mis. nomor elemen atau lanjutan
        # kalimat terbungkus) -> gabung ke atas, bukan baris baru
        if body and all(body[-1][j] in ('', rclean[j]) for j in range(ncol)):
            if body[-1] != rclean:
                catatan.append("baris rentang digabung ke baris sebelumnya")
            body[-1] = rclean
            continue
        body.append(rclean)

    if not body:
        return "", False, catatan + ["badan tabel kosong"]
    n_sel = ncol * len(body)
    n_kosong = sum(1 for r in body for c in r if c == '')
    if n_kosong > n_sel * 0.6 and not prosa:
        return "", False, catatan + [f"{n_kosong}/{n_sel} sel kosong"]

    esc = lambda c: c.replace('|', '\\|')
    md = ["| " + " | ".join(esc(h) for h in header) + " |",
          "|" + "---|" * ncol]
    md += ["| " + " | ".join(esc(c) for c in r) + " |" for r in body]
    return "\n".join(md), True, catatan


def ekstrak_tabel(doc, imgdir, dpi):
    """Deteksi tabel per halaman: render jadi gambar + ekstrak strukturnya.

    Deteksi memakai find_tables(), bukan caption — pada dokumen yang ukuran
    caption-nya sama dengan badan teks, caption bukan pegangan yang andal.

    `imgdir=None` melewati perenderan gambar dan hanya mengambil strukturnya;
    itu yang dipakai mode `--tunggal`, yang memang tidak punya folder gambar.
    """
    zoom = fitz.Matrix(dpi / 72, dpi / 72)
    per_hal, meta = {}, []
    for pno in range(doc.page_count):
        page = doc[pno]
        tabs = sorted(page.find_tables().tables,
                      key=lambda t: (t.bbox[1], t.bbox[0]))
        for k, t in enumerate(tabs, 1):
            kotak = fitz.Rect(t.bbox) + (-3, -3, 3, 3)
            kotak &= page.rect
            if kotak.height < 8 or kotak.width < 20:
                continue
            nama = None
            if imgdir:
                nama = f"tabel_hal{pno+1:03d}_{k}.png"
                page.get_pixmap(matrix=zoom, clip=kotak, alpha=False).save(
                    os.path.join(imgdir, nama))
            data = t.extract()
            md, ok, cat = tabel_ke_markdown(data)
            # baris terisi pertama = judul/header tabel; ditulis sebagai teks
            # agar tabel gambar-saja tetap bisa dicari isian kepalanya
            judul = ""
            for row in data:
                isi = [clean(str(c)) for c in row if c and clean(str(c))]
                if isi:
                    judul = " · ".join(isi)[:120]
                    break
            ent = {"page": pno + 1, "file": nama, "bbox": list(t.bbox),
                   "y": t.bbox[1], "md": md, "ok": ok, "catatan": cat,
                   "judul": judul, "baris": t.row_count, "kolom": t.col_count}
            per_hal.setdefault(pno, []).append(ent)
            meta.append(ent)
    return per_hal, meta


def simpan_raster(doc, rawdir):
    seen, n = set(), 0
    for pno in range(doc.page_count):
        for i, info in enumerate(doc[pno].get_images(full=True)):
            xref = info[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha >= 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(os.path.join(rawdir, f"hal{pno+1:03d}_{i+1}.png"))
                n += 1
            except Exception as e:
                print("  raster gagal", pno + 1, xref, e)
    return n


# pola front matter umum yang bukan heading konten
_FRONT_MATTER = re.compile(
    r'^(?:Contents|Table\s+of\s+Contents|Daftar\s+Isi|Contributors|Preface'
    r'|Kata\s+Pengantar|Acknowledgments|Ucapan\s+Terima\s+Kasih|Index'
    r'|Bibliography|Daftar\s+Pustaka|About\s+the\s+Authors?|Glosarium'
    r'|Glossary|Foreword|Prakata|Lampiran|Appendi(?:x|ces))$',
    re.IGNORECASE)


def dapatkan_toc(doc, prof):
    """Ambil daftar isi dari bookmark PDF; fallback ke deteksi ukuran fon.

    Mengembalikan `(toc, dari_bookmark)`. Bookmark dipakai apa adanya kecuali
    isinya sampah (nama berkas hash) — itu tidak bisa dipakai memecah bab.
    Tanpa bookmark yang berguna, heading level 1 dideteksi dari blok berukuran
    >= 1.6x badan dan level 2 dari blok yang cukup besar dan/atau tebal.
    Front matter umum (Contents, Preface, dll.) dilewati secara generik.
    """
    toc = doc.get_toc()
    if toc and all(re.fullmatch(r'[0-9a-f]{32,}\.pdf', t) for _, t, _ in toc):
        toc = []
    if toc:
        return toc, True

    kandidat = []
    terakhir_l1 = ""
    u_badan = prof.get("ukuran_badan", 10.0)
    ambang_l1 = u_badan * 1.6       # heading level 1: jauh lebih besar dari badan
    ambang_l2 = u_badan * 1.15      # heading level 2: sedikit lebih besar
    for pno in range(doc.page_count):
        page = doc[pno]
        H = page.rect.height
        blocks = page.get_text("dict")["blocks"]
        blks = []
        for b in blocks:
            if b.get("type") == 0:
                y0, y1 = b["bbox"][1], b["bbox"][3]
                if y1 < H * 0.075 or y0 > H * 0.93:
                    continue
                lines = b.get("lines", [])
                if not lines:
                    continue
                txt = clean("\n".join("".join(sp["text"] for sp in ln["spans"]) for ln in lines))
                if not txt:
                    continue
                sz = max(sp["size"] for ln in lines for sp in ln["spans"])
                fonts = [sp["font"] for ln in lines for sp in ln["spans"]]
                bold = any("Bold" in f or "Semi" in f or "Heavy" in f for f in fonts)
                blks.append((round(sz, 1), bold, txt))

        if not blks:
            continue

        # --- heading level 1: ukuran fon sangat besar
        l1_teks = [t for sz, bld, t in blks
                   if sz >= ambang_l1
                   and not _FRONT_MATTER.match(t)
                   and not FIGPAT.match(t) and not TABPAT.match(t)
                   and len(t) < 200]

        if l1_teks:
            full_l1 = " ".join(l1_teks)
            if full_l1 != terakhir_l1:
                kandidat.append((1, full_l1, pno + 1))
                terakhir_l1 = full_l1

        # --- heading level 2: ukuran fon cukup besar atau tebal
        for sz, bld, t in blks:
            if (sz >= ambang_l2 or (bld and sz > u_badan)) and len(t) < 140:
                if (FIGPAT.match(t) or TABPAT.match(t)
                        or _FRONT_MATTER.match(t)
                        or t.startswith("http") or t.startswith("Copyright")
                        or t.startswith("ISBN") or t in l1_teks):
                    continue
                if not (kandidat and kandidat[-1][1] == t
                        and kandidat[-1][2] == pno + 1):
                    kandidat.append((2, t, pno + 1))
    return kandidat, False


def _cocokkan_heading(t, kepala):
    """Level heading jika teks blok cocok dengan salah satu entri TOC halaman."""
    nt = norm(t)
    for lvl, ht in kepala:
        nh = norm(ht)
        pendek = nh.split(':')[-1].strip() if ':' in nh else nh
        if nt == nh or nt == pendek or (
                len(nt) < 130 and (nt.startswith(pendek)
                                   or pendek.startswith(nt))):
            return lvl
    return None


# --------------------------------------------------------------- markdown
def tulis_markdown(doc, prof, out, berkas, klip, sumber, tabel_hal=None):
    toc, dari_bookmark = dapatkan_toc(doc, prof)
    toc_hal = {}
    for lvl, judul, p in toc:
        toc_hal.setdefault(p - 1, []).append((lvl, judul))
    lv1 = [(t, p - 1) for l, t, p in toc if l == 1]
    if not lv1:
        lv1 = [("Dokumen", 0)]
    # tanpa bookmark: judul yang lolos dari deteksi TOC masih bisa dikenali
    # dari fon saat penulisan berlangsung
    judul_fon = not dari_bookmark
    bagian = [(t, p, lv1[i + 1][1] if i + 1 < len(lv1) else doc.page_count)
              for i, (t, p) in enumerate(lv1)]

    dipakai, daftar = set(), []
    for si, (judul, p0, p1) in enumerate(bagian):
        nama = f"{si:02d}_{slug(judul)}.md"
        baris = [f"# {judul}", "",
                 f"> Sumber: {sumber} — halaman PDF {p0+1}–{p1}.", ""]
        for pno in range(p0, p1):
            last_h = None   # judul heuristik terakhir: (level, y_bawah, idx)
            # sambungan judul tidak boleh melintasi batas halaman
            items, W, H = blok_halaman(doc, pno, prof)
            kotak = klip.get(pno, [])
            baris.append(f"<!-- hal. PDF {pno+1} -->")
            kepala = toc_hal.get(pno, [])
            antre = sorted(tabel_hal.get(pno, []), key=lambda e: e["y"]) \
                if tabel_hal else []

            def siram_tabel(sebelum_y):
                # sisipkan tabel yang posisinya sudah terlewati urutan bacanya
                while antre and antre[0]["y"] < sebelum_y:
                    e = antre.pop(0)
                    alt = e["judul"] or f"Tabel hal. {e['page']}"
                    baris.extend(["", f"![{alt}](gambar/{e['file']})", ""])
                    if e["ok"]:
                        baris.extend(["<!-- tabel hasil ekstraksi otomatis; "
                                      "rujuk gambar di atasnya bila ragu -->",
                                      e["md"], ""])
                    elif e["judul"]:
                        # tabel gambar-saja: kepala tabel tetap tertulis
                        # sebagai teks agar dapat dicari
                        baris.extend([f"*{e['judul']}*", ""])

            for it in items:
                if it["kind"] == "img":
                    continue
                siram_tabel(it["y"])
                t = it["text"]
                bx = fitz.Rect(it["bbox"])
                titik = fitz.Point((bx.x0 + bx.x1) / 2, (bx.y0 + bx.y1) / 2)
                if not it["figcap"] and any(titik in c for c in kotak):
                    continue          # teks ini sudah termuat di dalam gambar
                cocok = _cocokkan_heading(t, kepala)
                if cocok:
                    baris += ["", "#" * min(cocok + 1, 6) + " " + t, ""]
                    continue
                if judul_fon and not it["figcap"] and not it["tabcap"] \
                        and len(t) < 120:
                    lvl_h = 0
                    if it["size"] >= prof["ukuran_badan"] + 4:
                        lvl_h = 2                       # judul bab
                    elif (it["size"] >= prof["ukuran_badan"] + 0.8
                          and it["bold"]):
                        lvl_h = 3                       # subbab
                    if lvl_h:
                        # sambung potongan judul: nomor bab yang jadi blok
                        # sendiri, atau judul panjang yang terbungkus 2 baris.
                        # Blok berawalan penomoran ("3.1 …", "D.1 …") adalah
                        # judul baru, bukan sambungan
                        if (last_h and last_h[0] == lvl_h
                                and it["bbox"][1] - last_h[1] < 15
                                and not re.match(
                                    r'(?:\d+(?:\.\d+)+|[A-Z]\.\d+)[.)]?\s',
                                    t)):
                            baris[last_h[2]] += " " + t
                            last_h = (lvl_h, it["bbox"][3], last_h[2])
                        else:
                            baris += ["", "#" * lvl_h + " " + t, ""]
                            last_h = (lvl_h, it["bbox"][3], len(baris) - 2)
                        continue
                    last_h = None
                mf = FIGPAT.match(t) if it["figcap"] else None
                if mf:
                    kunci = kunci_fig(mf)
                    if kunci in berkas and kunci not in dipakai:
                        dipakai.add(kunci)
                        baris += ["", f"![{t}](gambar/{berkas[kunci]})", "",
                                  f"***{t}***", ""]
                    else:
                        baris += ["", f"***{t}***", ""]
                    continue
                if it["tabcap"]:
                    baris += ["", f"***{t}***", ""]
                    continue
                if it.get("panel"):       # kotak sisipan -> kutipan
                    baris += ["> " + t, ""]
                    continue
                baris += [t, ""]
            siram_tabel(float("inf"))
            baris.append("")
        teks = re.sub(r'\n{4,}', '\n\n\n', "\n".join(baris))
        io.open(os.path.join(out, nama), "w", encoding="utf-8",
                newline="\n").write(teks)
        daftar.append((nama, judul, len(teks)))
    return daftar, dipakai


def tulis_indeks(doc, out, daftar, meta, n_raster, dpi, sumber, tab_meta=None):
    meta = sorted(meta, key=lambda f: [int(x) for x in f["key"].split('.')])
    md = doc.metadata
    L = [f"# Ekstraksi Penuh: {md.get('title') or 'Dokumen PDF'}", "",
         f"Ekstraksi lengkap teks **dan** gambar dari berkas PDF "
         f"({doc.page_count} halaman).", "",
         f"- **Sumber**: {sumber}"]
    if md.get('author'):
        L.append(f"- **Penulis**: {md['author']}")
    L += ["", "## Isi Direktori", "", "| Berkas | Bagian | Ukuran teks |",
          "| --- | --- | ---: |"]
    for f, t, n in daftar:
        L.append(f"| [{f}]({f}) | {t} | {n/1000:.0f} KB |")
    L += [f"| `gambar/` | {len(meta)} gambar figur, render {dpi} dpi | — |",
          f"| `gambar/_raster_mentah/` | {n_raster} raster asli dari PDF (arsip) | — |",
          "| `_figur.json` | metadata gambar (nomor, halaman, caption) | — |", ""]
    if meta:
        L += ["## Daftar Gambar", "", "| No. | Judul | Hal. PDF | Berkas |",
              "| --- | --- | ---: | --- |"]
        for f in meta:
            cap = re.sub(r'^(?:Figure|Gambar)\s+[\d.\-]+\s*', '',
                         f["caption"]).strip().rstrip('.')
            L.append(f"| {f['key']} | {cap} | {f['page']} | "
                     f"[{f['file']}](gambar/{f['file']}) |")
    if tab_meta:
        n_ok = sum(1 for t in tab_meta if t["ok"])
        L += ["", "## Daftar Tabel", "",
              f"{len(tab_meta)} tabel terdeteksi; {n_ok} berhasil "
              "diekstrak terstruktur (sisanya gambar saja).", "",
              "| Hal. PDF | Kepala tabel | Ukuran | Status | Berkas | Catatan |",
              "| ---: | --- | --- | --- | --- | --- |"]
        for t in tab_meta:
            L.append(f"| {t['page']} | {t.get('judul', '')[:60]} | "
                     f"{t['baris']}×{t['kolom']} | "
                     f"{'terstruktur ✓' if t['ok'] else 'gambar saja'} | "
                     f"[{t['file']}](gambar/{t['file']}) | "
                     f"{'; '.join(t['catatan']) or '—'} |")
    L += ["", "## Cara Ekstraksi", "",
          "- Teks diambil per blok mengikuti urutan baca halaman; header/footer "
          "berjalan dibuang dan kata yang terpenggal antarbaris disambung kembali.",
          "- Penanda `<!-- hal. PDF n -->` menandai awal tiap halaman PDF agar "
          "mudah dirujuk balik ke berkas aslinya.",
          "- Judul bab dan subbab diangkat dari bookmark PDF, sehingga hierarki "
          "`##`–`######` mengikuti struktur asli dokumen. Bila PDF tidak punya "
          "bookmark, judul dikenali dari ukuran dan ketebalan fon.",
          "- Gambar dirender ulang dari halaman pada wilayah di atas caption-nya, "
          "sehingga diagram vektor ikut terbawa utuh. Teks yang sudah termuat di "
          "dalam gambar tidak diulang sebagai paragraf.", "",
          "> [!WARNING] Batas ketelitian"]
    if tab_meta is None:
        L += ["> Tabel terekstrak sebagai **teks berurutan**, bukan tabel "
              "Markdown — struktur baris dan kolomnya tidak dipertahankan. "
              "Rujuk PDF asli bila membutuhkan tabel yang presisi.", ""]
    else:
        L += ["> Tiap tabel dirender jadi **gambar** (rujukan kebenaran) dan, "
              "bila lolos validasi, disertai tabel Markdown hasil ekstraksi "
              "otomatis + perbaikan pola. Sel yang salah tempat namun lolos "
              "validasi mungkin ada — selalu rujuk gambar di atasnya bila "
              "isinya menentukan.", ""]
    io.open(os.path.join(out, "_index.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(L))


# -------------------------------------------------------------- mode tunggal
def tulis_tunggal(doc, prof, path_keluaran, sumber, tabel_hal=None):
    """Tulis seluruh isi PDF ke satu berkas Markdown tanpa gambar.

    Heading diambil dari bookmark atau fallback deteksi fon.
    Caption figur dicetak sebagai placeholder, panel sebagai kutipan.
    Dengan `tabel_hal` terisi (`--tabel hibrida`), tabel yang lolos validasi
    ditulis sebagai tabel Markdown di posisi bacanya.
    """
    toc, _ = dapatkan_toc(doc, prof)
    toc_hal = {}
    for lvl, judul, p in toc:
        toc_hal.setdefault(p - 1, []).append((lvl, judul))

    md = doc.metadata
    judul_doc = md.get('title') or os.path.splitext(os.path.basename(path_keluaran))[0]
    baris = [f"# {judul_doc}", ""]
    if sumber:
        baris += [f"> Sumber: {sumber}", ""]
    if md.get('author'):
        baris += [f"> Penulis: {md['author']}", ""]
    baris += [f"> Diekstrak dari {doc.page_count} halaman PDF.", "",
              "> [!WARNING] Batas ketelitian"]
    if tabel_hal is None:
        baris += ["> Tabel terekstrak sebagai **teks berurutan**, bukan tabel Markdown."]
    else:
        baris += ["> Tabel yang lolos validasi ditulis sebagai tabel Markdown "
                  "hasil ekstraksi otomatis; sisanya jadi penanda saja."]
    baris += ["> Gambar tidak disertakan; posisi aslinya ditandai sebagai placeholder.",
              "> Rujuk PDF asli untuk tabel dan gambar yang presisi.", ""]

    for pno in range(doc.page_count):
        items, W, H = blok_halaman(doc, pno, prof)
        baris.append(f"<!-- hal. PDF {pno + 1} -->")
        kepala = toc_hal.get(pno, [])
        ents = tabel_hal.get(pno, []) if tabel_hal else []
        antre = sorted(ents, key=lambda e: e["y"])
        kotak = [fitz.Rect(e["bbox"]) for e in ents]

        def siram_tabel(sebelum_y):
            while antre and antre[0]["y"] < sebelum_y:
                e = antre.pop(0)
                if e["judul"]:
                    baris += ["", f"***{e['judul']}***", ""]
                if e["ok"]:
                    baris += ["<!-- tabel hasil ekstraksi otomatis; "
                              "rujuk PDF asli bila ragu -->", e["md"], ""]
                else:
                    baris += [f"> [Tabel hal. {e['page']} — struktur tidak "
                              "terekstrak, lihat PDF asli]", ""]

        for it in items:
            if it["kind"] == "img":
                continue
            siram_tabel(it["y"])
            t = it["text"]
            # --- teks yang sudah termuat di dalam tabel jangan diulang
            bx = fitz.Rect(it["bbox"])
            titik = fitz.Point((bx.x0 + bx.x1) / 2, (bx.y0 + bx.y1) / 2)
            if kotak and any(titik in c for c in kotak):
                continue
            # --- cocokkan heading dari TOC
            cocok = _cocokkan_heading(t, kepala)
            if cocok:
                baris += ["", "#" * min(cocok + 1, 6) + " " + t, ""]
                continue
            # --- caption figur sebagai placeholder
            if it["figcap"]:
                baris += ["", f"> [Gambar: {t} — lihat PDF asli]", ""]
                continue
            # --- caption tabel sebagai penanda
            if it["tabcap"]:
                baris += ["", f"***{t}***", ""]
                continue
            # --- panel/kotak sisipan sebagai kutipan
            if it.get("panel"):
                baris += ["> " + t, ""]
                continue
            # --- teks biasa
            baris += [t, ""]
        siram_tabel(float("inf"))
        baris.append("")

    teks = re.sub(r'\n{4,}', '\n\n\n', "\n".join(baris))
    os.makedirs(os.path.dirname(os.path.abspath(path_keluaran)), exist_ok=True)
    io.open(path_keluaran, "w", encoding="utf-8", newline="\n").write(teks)
    print(f"berkas tunggal: {path_keluaran} ({len(teks)/1000:.0f} KB)")
    return teks


# -------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--keluaran", help="direktori hasil, atau path berkas .md bila --tunggal")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--tabel", choices=["hibrida"],
                    help="hibrida: tiap tabel dirender jadi gambar + tabel "
                         "Markdown hasil find_tables (default: tabel jadi "
                         "teks berurutan seperti semula). Pada --tunggal, "
                         "hanya tabel Markdown-nya yang ditulis")
    ap.add_argument("--sumber", help="kutipan sumber satu baris untuk kepala tiap berkas")
    ap.add_argument("--profil", action="store_true", help="tampilkan profil fon lalu berhenti")
    ap.add_argument("--periksa", help="bedah blok halaman tertentu, mis. 28,127")
    ap.add_argument("--tunggal", action="store_true",
                    help="keluarkan sebagai satu berkas Markdown tunggal tanpa folder gambar")
    a = ap.parse_args()

    doc = fitz.open(a.pdf)
    prof = profil_dokumen(doc)
    if a.profil or a.periksa:
        print("profil:", json.dumps(prof, ensure_ascii=False, indent=1))
        if a.periksa:
            periksa(doc, prof, [int(x) for x in a.periksa.split(',')])
        return
    if not a.keluaran:
        ap.error("--keluaran wajib diisi untuk ekstraksi")

    sumber = a.sumber or doc.metadata.get('title') or os.path.basename(a.pdf)
    print("profil:", {k: prof[k] for k in ("ukuran_badan", "ukuran_caption", "fon_prosa")})

    # ----- mode tunggal: satu berkas Markdown tanpa gambar -----
    if a.tunggal:
        path = a.keluaran
        if not path.lower().endswith('.md'):
            path += '.md'
        tabel_hal = None
        if a.tabel == "hibrida":
            tabel_hal, tab_meta = ekstrak_tabel(doc, None, a.dpi)
            n_ok = sum(1 for t in tab_meta if t["ok"])
            print(f"tabel terdeteksi: {len(tab_meta)} | terstruktur: {n_ok}")
        tulis_tunggal(doc, prof, path, sumber, tabel_hal)
        return

    # ----- mode penuh: direktori berisi Markdown per bab + gambar -----
    imgdir = os.path.join(a.keluaran, "gambar")
    rawdir = os.path.join(imgdir, "_raster_mentah")
    os.makedirs(rawdir, exist_ok=True)

    berkas, klip, meta = render_gambar(doc, prof, imgdir, a.dpi)
    print("figur dirender:", len(berkas))
    io.open(os.path.join(a.keluaran, "_figur.json"), "w", encoding="utf-8",
            newline="\n").write(
        json.dumps(meta, ensure_ascii=False, indent=1))

    tabel_hal = tab_meta = None
    if a.tabel == "hibrida":
        tabel_hal, tab_meta = ekstrak_tabel(doc, imgdir, a.dpi)
        n_ok = sum(1 for t in tab_meta if t["ok"])
        print(f"tabel dirender: {len(tab_meta)} | terstruktur: {n_ok}")
        io.open(os.path.join(a.keluaran, "_tabel.json"), "w", encoding="utf-8",
                newline="\n").write(json.dumps(
            [{k: v for k, v in t.items() if k != "md"} for t in tab_meta],
            ensure_ascii=False, indent=1))
        # teks sel tabel jangan diulang sebagai paragraf lepas
        for pno, ents in tabel_hal.items():
            klip.setdefault(pno, []).extend(fitz.Rect(e["bbox"]) for e in ents)

    n_raster = simpan_raster(doc, rawdir)
    print("raster mentah:", n_raster)

    daftar, dipakai = tulis_markdown(doc, prof, a.keluaran, berkas, klip,
                                     sumber, tabel_hal)
    tulis_indeks(doc, a.keluaran, daftar, meta, n_raster, a.dpi, sumber,
                 tab_meta)
    for d in daftar:
        print("  ", d)
    kurang = sorted(set(berkas) - dipakai)
    print(f"figur tertaut: {len(dipakai)}/{len(berkas)}",
          f"| belum tertaut: {kurang}" if kurang else "| semua tertaut")


if __name__ == "__main__":
    main()
