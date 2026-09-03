#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ekstraktor dan Pembaca EPUB mandiri (Python).

Mendukung:
  1. Metadata (judul, penulis, penerbit, tanggal, dll.)
  2. Table of Contents (TOC) / Struktur Bab
  3. Baca Bab Tertentu (1-indexed)
  4. Ekstraksi Penuh Seluruh Buku ke Markdown
  5. Pencarian Teks dengan Konteks

Pemakaian:
  python ekstrak_epub.py metadata "buku.epub"
  python ekstrak_epub.py toc "buku.epub"
  python ekstrak_epub.py chapter "buku.epub" 3
  python ekstrak_epub.py full "buku.epub" [--output "hasil.md"]
  python ekstrak_epub.py search "buku.epub" "kata_kunci"
"""

import argparse
import html
import io
import json
import os
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NAMESPACES = {
    'container': 'urn:oasis:names:tc:opendocument:xmlns:container',
    'opf': 'http://www.idpf.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'ncx': 'http://www.daisy.org/z3986/2005/ncx/',
    'xhtml': 'http://www.w3.org/1999/xhtml',
}


def html_to_markdown(html_text):
    """Konversi HTML sederhana dari berkas bab EPUB menjadi Markdown bersih."""
    # Bersihkan skrip & style
    text = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', html_text, flags=re.IGNORECASE)
    text = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<head[^>]*>[\s\S]*?</head>', '', text, flags=re.IGNORECASE)

    # Heading
    for i in range(6, 0, -1):
        text = re.sub(
            rf'<h{i}[^>]*>(.*?)</h{i}>',
            lambda m: f"\n\n{'#' * i} {clean_inline_html(m.group(1))}\n\n",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

    # Paragraph dan div
    text = re.sub(
        r'<p[^>]*>(.*?)</p>',
        lambda m: f"\n\n{clean_inline_html(m.group(1))}\n\n",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<hr\s*/?>', '\n\n---\n\n', text, flags=re.IGNORECASE)

    # List items
    text = re.sub(
        r'<li[^>]*>(.*?)</li>',
        lambda m: f"\n- {clean_inline_html(m.group(1))}",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r'</?(?:ul|ol)[^>]*>', '\n', text, flags=re.IGNORECASE)

    # Blockquote
    text = re.sub(
        r'<blockquote[^>]*>(.*?)</blockquote>',
        lambda m: "\n" + "\n".join(f"> {line}" for line in clean_inline_html(m.group(1)).splitlines() if line.strip()) + "\n",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Hapus tag sisa
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)

    # Rapikan whitespace
    lines = [l.strip() for l in text.splitlines()]
    result = []
    prev_empty = False
    for l in lines:
        if not l:
            if not prev_empty:
                result.append('')
                prev_empty = True
        else:
            result.append(l)
            prev_empty = False

    return '\n'.join(result).strip()


def clean_inline_html(s):
    """Tangani format inline (tebal, miring, link, kode)."""
    s = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r'<(?:em|i)[^>]*>(.*?)</(?:em|i)>', r'*\1*', s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


class EpubBook:
    def __init__(self, epub_path):
        self.epub_path = os.path.abspath(epub_path)
        if not os.path.exists(self.epub_path):
            raise FileNotFoundError(f"Berkas EPUB tidak ditemukan: {self.epub_path}")

        self.zip = zipfile.ZipFile(self.epub_path, 'r')
        self.rootfile_path = self._find_rootfile()
        self.base_dir = posixpath.dirname(self.rootfile_path)
        self.opf_tree = ET.fromstring(self.zip.read(self.rootfile_path))

        self.metadata = self._parse_metadata()
        self.manifest = self._parse_manifest()
        self.spine = self._parse_spine()
        self.toc = self._parse_toc()

    def _find_rootfile(self):
        container_data = self.zip.read('META-INF/container.xml')
        tree = ET.fromstring(container_data)
        rootfile = tree.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
        if rootfile is None or 'full-path' not in rootfile.attrib:
            raise ValueError("Struktur EPUB tidak valid: 'rootfile' tidak ditemukan di container.xml")
        return rootfile.attrib['full-path']

    def _parse_metadata(self):
        meta = {}
        meta_elem = self.opf_tree.find('{http://www.idpf.org/2007/opf}metadata')
        if meta_elem is None:
            return meta

        for elem in meta_elem:
            tag = elem.tag.split('}')[-1]
            val = (elem.text or '').strip()
            if not val:
                continue
            if tag == 'title':
                meta['title'] = val
            elif tag in ('creator', 'author'):
                meta['author'] = val
            elif tag == 'publisher':
                meta['publisher'] = val
            elif tag == 'date':
                meta['date'] = val
            elif tag == 'language':
                meta['language'] = val
            elif tag == 'description':
                meta['description'] = val
            elif tag == 'identifier':
                meta['identifier'] = val
        return meta

    def _parse_manifest(self):
        manifest = {}
        manifest_elem = self.opf_tree.find('{http://www.idpf.org/2007/opf}manifest')
        if manifest_elem is not None:
            for item in manifest_elem.findall('{http://www.idpf.org/2007/opf}item'):
                i_id = item.attrib.get('id')
                href = item.attrib.get('href')
                media_type = item.attrib.get('media-type', '')
                if i_id and href:
                    if self.base_dir:
                        full_href = posixpath.normpath(posixpath.join(self.base_dir, href))
                    else:
                        full_href = href
                    manifest[i_id] = {'href': full_href, 'media_type': media_type}
        return manifest

    def _parse_spine(self):
        spine = []
        spine_elem = self.opf_tree.find('{http://www.idpf.org/2007/opf}spine')
        if spine_elem is not None:
            for itemref in spine_elem.findall('{http://www.idpf.org/2007/opf}itemref'):
                idref = itemref.attrib.get('idref')
                if idref and idref in self.manifest:
                    spine.append(self.manifest[idref]['href'])
        return spine

    def _parse_toc(self):
        # Coba dari nav.xhtml (EPUB 3) atau toc.ncx (EPUB 2)
        toc = []
        # 1. Cek NCX
        for item in self.manifest.values():
            if 'ncx' in item['media_type'] or item['href'].endswith('.ncx'):
                try:
                    ncx_data = self.zip.read(item['href'])
                    ncx_tree = ET.fromstring(ncx_data)
                    for navpoint in ncx_tree.findall('.//{http://www.daisy.org/z3986/2005/ncx/}navPoint'):
                        label_elem = navpoint.find('.//{http://www.daisy.org/z3986/2005/ncx/}text')
                        content_elem = navpoint.find('{http://www.daisy.org/z3986/2005/ncx/}content')
                        label = (label_elem.text or '').strip() if label_elem is not None else ''
                        src = content_elem.attrib.get('src', '') if content_elem is not None else ''
                        if label:
                            toc.append({'label': label, 'src': src})
                    if toc:
                        return toc
                except Exception:
                    pass

        # Fallback jika tidak ada NCX: gunakan urutan spine
        for idx, href in enumerate(self.spine, 1):
            toc.append({'label': f"Section {idx} ({posixpath.basename(href)})", 'src': href})
        return toc

    def get_chapter_content(self, index_1_based):
        if index_1_based < 1 or index_1_based > len(self.spine):
            raise IndexError(f"Nomor bab {index_1_based} di luar rentang (total: {len(self.spine)})")

        href = self.spine[index_1_based - 1]
        try:
            raw_html = self.zip.read(href).decode('utf-8', errors='replace')
            return html_to_markdown(raw_html), href
        except Exception as e:
            return f"Error membaca bab {index_1_based} ({href}): {e}", href

    def get_full_book(self):
        all_md = []
        meta = self.metadata
        title = meta.get('title', 'Dokumen EPUB')
        author = meta.get('author', '')
        all_md.append(f"# {title}\n")
        if author:
            all_md.append(f"**Penulis**: {author}\n")
        if meta.get('publisher'):
            all_md.append(f"**Penerbit**: {meta.get('publisher')}\n")
        if meta.get('date'):
            all_md.append(f"**Tanggal**: {meta.get('date')}\n")
        all_md.append("\n---\n")

        for idx in range(1, len(self.spine) + 1):
            content, href = self.get_chapter_content(idx)
            if content.strip():
                all_md.append(f"\n<!-- Section {idx}: {posixpath.basename(href)} -->\n")
                all_md.append(content)
                all_md.append("\n\n---\n")

        return '\n'.join(all_md)

    def search(self, query, max_results_per_ch=5):
        query_lower = query.lower()
        results = []
        for idx in range(1, len(self.spine) + 1):
            content, href = self.get_chapter_content(idx)
            lines = content.splitlines()
            ch_matches = []
            for line_idx, line in enumerate(lines):
                if query_lower in line.lower():
                    # ambil konteks
                    start = max(0, line_idx - 1)
                    end = min(len(lines), line_idx + 2)
                    snippet = '\n'.join(lines[start:end])
                    ch_matches.append({'line': line_idx + 1, 'snippet': snippet})
                    if len(ch_matches) >= max_results_per_ch:
                        break
            if ch_matches:
                results.append({
                    'chapter_num': idx,
                    'file': posixpath.basename(href),
                    'matches': ch_matches
                })
        return results


def main():
    parser = argparse.ArgumentParser(description="Pengekstrak dan Pembaca EPUB")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # metadata
    p_meta = subparsers.add_parser("metadata", help="Tampilkan metadata buku")
    p_meta.add_argument("epub", help="Jalur ke berkas EPUB")

    # toc
    p_toc = subparsers.add_parser("toc", help="Daftar Table of Contents / Struktur Bab")
    p_toc.add_argument("epub", help="Jalur ke berkas EPUB")

    # chapter
    p_ch = subparsers.add_parser("chapter", help="Baca bab tertentu (1-indexed)")
    p_ch.add_argument("epub", help="Jalur ke berkas EPUB")
    p_ch.add_argument("num", type=int, help="Nomor bab (1-indexed)")

    # full
    p_full = subparsers.add_parser("full", help="Ekstrak seluruh buku ke Markdown")
    p_full.add_argument("epub", help="Jalur ke berkas EPUB")
    p_full.add_argument("--output", help="Jalur berkas output Markdown (opsional)")

    # search
    p_srch = subparsers.add_parser("search", help="Cari kata kunci dalam buku")
    p_srch.add_argument("epub", help="Jalur ke berkas EPUB")
    p_srch.add_argument("query", help="Kata kunci pencarian")

    args = parser.parse_args()

    try:
        book = EpubBook(args.epub)
    except Exception as e:
        print(f"Error membuka berkas EPUB: {e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "metadata":
        meta = book.metadata
        print("=== EPUB Metadata ===")
        for k, v in meta.items():
            print(f"{k.capitalize():<12}: {v}")
        print(f"Total Sections : {len(book.spine)}")

    elif args.command == "toc":
        print(f"=== Table of Contents: {book.metadata.get('title', 'Dokumen')} ===")
        for idx, item in enumerate(book.toc, 1):
            print(f"[{idx:02d}] {item['label']}  -->  {item['src']}")

    elif args.command == "chapter":
        content, href = book.get_chapter_content(args.num)
        print(f"=== Chapter {args.num} ({posixpath.basename(href)}) ===\n")
        print(content)

    elif args.command == "full":
        full_md = book.get_full_book()
        if args.output:
            out_path = os.path.abspath(args.output)
            os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(full_md)
            print(f"Ekstraksi selesai: {out_path} ({len(full_md)} karakter)")
        else:
            print(full_md)

    elif args.command == "search":
        res = book.search(args.query)
        print(f"=== Hasil Pencarian '{args.query}' ({sum(len(r['matches']) for r in res)} kecocokan) ===")
        for r in res:
            print(f"\n--- [Bab {r['chapter_num']}: {r['file']}] ---")
            for m in r['matches']:
                print(f"(Baris {m['line']}):\n{m['snippet']}\n")


if __name__ == "__main__":
    main()
