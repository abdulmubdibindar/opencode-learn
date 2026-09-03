#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MinerU Extractor Adapter & Runner.

Menjalankan dan mengelola ekstraksi dokumen ilmiah kompleks, formula LaTeX,
tabel bertingkat, dan OCR menggunakan engine MinerU (OpenDataLab).

Mendukung:
  - Deteksi lingkungan runtime (GPU CUDA, Apple Silicon MPS, atau CPU).
  - Ekstraksi PDF / Dokumen ke format Markdown & JSON.
  - Formula matematika otomatis menjadi LaTeX ($...$ / $$...$$).
  - Ekstraksi tabel kompleks ke HTML/Markdown.
  - Pembersihan noise (header, footer, page number).

Pemakaian:
  python mineru_extractor.py --input "paper.pdf" --output-dir "hasil_mineru"
  python mineru_extractor.py --input "paper.pdf" --output-dir "hasil_mineru" --device cpu
  python mineru_extractor.py --check-env
"""

import argparse
import io
import json
import os
import shutil
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def check_mineru_env():
    """Periksa ketersediaan mineru di sistem dan lingkungan conda."""
    status = {
        "mineru_cli": False,
        "magic_pdf_cli": False,
        "python_module": False,
        "cuda_available": False,
        "device_recommendation": "cpu",
        "install_command": "pip install -U mineru[all]"
    }

    if shutil.which("mineru"):
        status["mineru_cli"] = True
    if shutil.which("magic-pdf"):
        status["magic_pdf_cli"] = True

    # Cek module python
    try:
        import magic_pdf
        status["python_module"] = True
    except ImportError:
        pass

    # Cek ketersediaan PyTorch CUDA jika ada
    try:
        import torch
        if torch.cuda.is_available():
            status["cuda_available"] = True
            status["device_recommendation"] = "cuda"
            status["gpu_name"] = torch.cuda.get_device_name(0)
    except Exception:
        pass

    return status


def run_mineru_cli(input_path, output_dir, device="auto", method="auto"):
    """Jalankan proses ekstraksi MinerU via CLI."""
    input_path = os.path.abspath(input_path)
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    env_status = check_mineru_env()

    if not env_status["mineru_cli"] and not env_status["magic_pdf_cli"] and not env_status["python_module"]:
        print("\n" + "=" * 60, file=sys.stderr)
        print("PERINGATAN: Paket 'mineru' belum terpasang di lingkungan aktif.", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("Untuk menginstal MinerU, jalankan salah satu perintah berikut:\n", file=sys.stderr)
        print("  1. Jika menggunakan conda/uv di environment target (mis. 'extract-pdf'):", file=sys.stderr)
        print("     uv pip install -U \"mineru[all]\"", file=sys.stderr)
        print("     # atau:", file=sys.stderr)
        print("     pip install -U \"mineru[all]\"\n", file=sys.stderr)
        print("  2. Jika ingin menggunakan CPU murni tanpa CUDA:", file=sys.stderr)
        print("     pip install -U \"mineru[cpu]\"\n", file=sys.stderr)
        print("Alternatif: Gunakan engine bawaan ringan (PyMuPDF) dengan opsi '--engine fast'.", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
        return False

    cmd = []
    if env_status["mineru_cli"]:
        cmd = ["mineru", "-p", input_path, "-o", output_dir]
    elif env_status["magic_pdf_cli"]:
        cmd = ["magic-pdf", "-p", input_path, "-o", output_dir]
    else:
        cmd = [sys.executable, "-m", "magic_pdf", "-p", input_path, "-o", output_dir]

    if method != "auto":
        cmd.extend(["-m", method])

    print(f"Menjalankan MinerU: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print(f"\nEkstraksi MinerU berhasil! Hasil tersimpan di: {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error saat menjalankan MinerU: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="MinerU Document Extractor Adapter")
    parser.add_argument("--input", help="Jalur ke berkas dokumen / PDF yang akan diekstrak")
    parser.add_argument("--output-dir", help="Direktori target penyimpanan hasil ekstraksi")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"], help="Perangkat komputasi")
    parser.add_argument("--method", default="auto", choices=["auto", "ocr", "txt"], help="Metode parsing")
    parser.add_argument("--check-env", action="store_true", help="Cek ketersediaan dan konfigurasi MinerU")

    args = parser.parse_args()

    if args.check_env:
        status = check_mineru_env()
        print("=== Status Lingkungan MinerU ===")
        print(f"MinerU CLI          : {'Tersedia' if status['mineru_cli'] else 'Belum Terpasang'}")
        print(f"Magic-PDF CLI       : {'Tersedia' if status['magic_pdf_cli'] else 'Belum Terpasang'}")
        print(f"Python Module       : {'Tersedia' if status['python_module'] else 'Belum Terpasang'}")
        print(f"CUDA Available      : {status['cuda_available']}")
        if status.get("gpu_name"):
            print(f"GPU Model           : {status['gpu_name']}")
        print(f"Rekomendasi Device  : {status['device_recommendation']}")
        print(f"Perintah Instalasi  : {status['install_command']}")
        return

    if not args.input:
        parser.error("Argumen --input diperlukan (atau gunakan --check-env).")

    output_dir = args.output_dir
    if not output_dir:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_dir = os.path.join(os.path.dirname(args.input) or ".", f"mineru_{base_name}")

    success = run_mineru_cli(args.input, output_dir, device=args.device, method=args.method)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
