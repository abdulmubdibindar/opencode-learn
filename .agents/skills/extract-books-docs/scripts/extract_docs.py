#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Universal Document & Book Extraction Router.

Mengarahkan dan mengeksekusi ekstraksi berbagai format dokumen:
  - PDF: Fast PyMuPDF (`ekstrak_pdf.py`) atau AI MinerU (`mineru_extractor.py`)
  - Office: MarkItDown (`convert_office.py` untuk .docx, .xlsx, .pptx)
  - EPUB: EPUB Extractor (`ekstrak_epub.py` / `epub-reader`)
  - Batch: Memproses seluruh direktori secara serentak

Pemakaian:
  # 1. Otomatis deteksi (Auto Router)
  python extract_docs.py --input "buku.pdf" --output "DIR_HASIL"
  python extract_docs.py --input "laporan.docx" --output-dir "DIR_HASIL"
  python extract_docs.py --input "ebook.epub" --output "hasil.md"

  # 2. PDF dengan Engine Cepat PyMuPDF (Default untuk buku tebal)
  python extract_docs.py --input "buku.pdf" --output "DIR_HASIL" --engine fast
  python extract_docs.py --input "dokumen.pdf" --output "hasil.md" --engine fast --tunggal

  # 3. PDF dengan Engine AI MinerU (Untuk rumus LaTeX, OCR scan, paper multikolom)
  python extract_docs.py --input "paper.pdf" --output "DIR_HASIL" --engine mineru

  # 4. Batch Folder
  python extract_docs.py --input "C:\path\ke\folder" --output-dir "C:\path\ke\output" --report "report.json"
"""

import argparse
import glob
import io
import json
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Jalur environment conda yang dikenal
CONDA_ENV_PATHS = [
    r"C:\Users\LENOVO\.conda\envs\extract-pdf\python.exe",
    r"C:\ProgramData\miniconda3\envs\markitdown\python.exe",
    r"C:\ProgramData\miniconda3\python.exe",
    sys.executable
]


def get_python_for_task(task="pdf"):
    """Dapatkan executable python yang paling sesuai untuk tugas tertentu."""
    if task == "pdf":
        p = r"C:\Users\LENOVO\.conda\envs\extract-pdf\python.exe"
        if os.path.exists(p):
            return p
    elif task == "office":
        p = r"C:\ProgramData\miniconda3\envs\markitdown\python.exe"
        if os.path.exists(p):
            return p
        p_alt = r"C:\Users\LENOVO\.conda\envs\extract-pdf\python.exe"
        if os.path.exists(p_alt):
            return p_alt

    # Fallback
    for p in CONDA_ENV_PATHS:
        if os.path.exists(p):
            return p
    return sys.executable


def process_pdf(file_path, output, engine="fast", is_single=False, is_hibrida=False, sumber=None):
    py_exe = get_python_for_task("pdf")
    if engine == "mineru":
        script = os.path.join(SCRIPT_DIR, "mineru_extractor.py")
        cmd = [py_exe, script, "--input", file_path]
        if output:
            cmd.extend(["--output-dir", output])
        print(f"[Engine MinerU] Memproses: {file_path}")
        return subprocess.call(cmd) == 0
    else:
        script = os.path.join(SCRIPT_DIR, "ekstrak_pdf.py")
        cmd = [py_exe, script, "--pdf", file_path]
        if output:
            cmd.extend(["--keluaran", output])
        if is_single:
            cmd.append("--tunggal")
        if is_hibrida:
            cmd.extend(["--tabel", "hibrida"])
        if sumber:
            cmd.extend(["--sumber", sumber])
        print(f"[Engine Fast PyMuPDF] Memproses: {file_path}")
        return subprocess.call(cmd) == 0


def process_office(file_path, output_dir=None, report_path=None):
    py_exe = get_python_for_task("office")
    script = os.path.join(SCRIPT_DIR, "convert_office.py")
    temp_report = report_path or os.path.join(output_dir or os.path.dirname(file_path) or ".", "_office_report.json")
    cmd = [py_exe, script, "--target", file_path, "--output", temp_report]
    if output_dir:
        cmd.extend(["--output-dir", output_dir])
    print(f"[Engine Office MarkItDown] Memproses: {file_path}")
    return subprocess.call(cmd) == 0


def process_epub(file_path, output=None, command="full"):
    py_exe = get_python_for_task("pdf")
    script = os.path.join(SCRIPT_DIR, "ekstrak_epub.py")
    cmd = [py_exe, script, command, file_path]
    if output and command == "full":
        cmd.extend(["--output", output])
    print(f"[Engine EPUB] Memproses: {file_path}")
    return subprocess.call(cmd) == 0


def main():
    parser = argparse.ArgumentParser(description="Universal Document & Book Extraction Router")
    parser.add_argument("--input", required=True, help="Berkas atau direktori sumber")
    parser.add_argument("--output", help="Jalur target output (direktori atau berkas markdown)")
    parser.add_argument("--output-dir", help="Direktori target output (alias untuk --output jika direktori)")
    parser.add_argument("--engine", default="auto", choices=["auto", "fast", "mineru", "office", "epub"],
                        help="Engine ekstraksi: auto, fast (PyMuPDF), mineru (AI), office (MarkItDown), epub")
    parser.add_argument("--tunggal", action="store_true", help="Mode satu berkas Markdown tunggal (untuk PDF fast engine)")
    parser.add_argument("--tabel", choices=["hibrida", "none"], default="none", help="Mode ekstraksi tabel PDF (hibrida = gambar + md)")
    parser.add_argument("--sumber", help="Teks rujukan sumber dokumen untuk header Markdown")
    parser.add_argument("--report", help="Jalur berkas JSON laporan hasil ekstraksi batch")

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"Error: Jalur input tidak ditemukan: {input_path}", file=sys.stderr)
        sys.exit(1)

    target_output = args.output or args.output_dir

    if os.path.isfile(input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext == ".pdf":
            eng = "mineru" if args.engine == "mineru" else "fast"
            success = process_pdf(input_path, target_output, engine=eng, is_single=args.tunggal,
                                  is_hibrida=(args.tabel == "hibrida"), sumber=args.sumber)
        elif ext in [".docx", ".xlsx", ".pptx", ".doc", ".xls", ".ppt"]:
            success = process_office(input_path, output_dir=target_output, report_path=args.report)
        elif ext == ".epub":
            success = process_epub(input_path, output=target_output, command="full")
        else:
            print(f"Format berkas {ext} tidak didukung langsung. Mencoba engine office/markitdown...", file=sys.stderr)
            success = process_office(input_path, output_dir=target_output, report_path=args.report)
        sys.exit(0 if success else 1)

    elif os.path.isdir(input_path):
        print(f"Memproses batch direktori: {input_path}")
        supported_exts = [".pdf", ".docx", ".xlsx", ".pptx", ".epub"]
        all_files = []
        for root, _, files in os.walk(input_path):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in supported_exts:
                    all_files.append(os.path.join(root, f))

        if not all_files:
            print(f"Tidak ditemukan berkas yang didukung ({', '.join(supported_exts)}) di {input_path}")
            sys.exit(0)

        results = {}
        success_count = 0
        failed_count = 0

        for fpath in all_files:
            ext = os.path.splitext(fpath)[1].lower()
            rel_path = os.path.relpath(fpath, input_path)
            out_dest = os.path.join(target_output, os.path.splitext(rel_path)[0]) if target_output else None

            print(f"\n[{success_count + failed_count + 1}/{len(all_files)}] Memproses: {rel_path}")
            if ext == ".pdf":
                eng = "mineru" if args.engine == "mineru" else "fast"
                ok = process_pdf(fpath, out_dest, engine=eng, is_single=args.tunggal, is_hibrida=(args.tabel == "hibrida"))
            elif ext in [".docx", ".xlsx", ".pptx"]:
                ok = process_office(fpath, output_dir=target_output or os.path.dirname(fpath))
            elif ext == ".epub":
                out_md = (out_dest + ".md") if out_dest else (os.path.splitext(fpath)[0] + ".md")
                ok = process_epub(fpath, output=out_md, command="full")
            else:
                ok = False

            results[fpath] = "Success" if ok else "Failed"
            if ok:
                success_count += 1
            else:
                failed_count += 1

        summary = {
            "total": len(all_files),
            "success": success_count,
            "failed": failed_count,
            "results": results
        }
        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
            print(f"\nLaporan batch disimpan ke: {args.report}")

        print(f"\nSelesai! Total: {len(all_files)}, Sukses: {success_count}, Gagal: {failed_count}")
        sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
