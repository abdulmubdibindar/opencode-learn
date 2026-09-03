#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conda Environment Analyzer & Package Installer.

Menganalisis lingkungan Conda di mesin (lokal atau mesin baru),
memeriksa ketersediaan paket untuk berbagai profil tugas,
serta menawarkan instalasi paket secara on-demand.

Pemakaian:
  # Cek status conda dan seluruh environment
  python analyze_conda_env.py

  # Analisis profil tugas tertentu (misal: extract-docs, gis, ml, quarto)
  python analyze_conda_env.py --profile extract-docs
  python analyze_conda_env.py --profile extract-docs --env extract-pdf

  # Cek paket tertentu
  python analyze_conda_env.py --check "fitz,markitdown,mineru" --env extract-pdf

  # Generate perintah instalasi
  python analyze_conda_env.py --profile extract-docs --suggest-install
"""

import argparse
import io
import json
import os
import shutil
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Profil paket yang sering dibutuhkan di direktori kerja
# Format: import_name -> pypi_name
TASK_PROFILES = {
    "extract-docs": {
        "description": "Ekstraksi buku, PDF, Office (.docx/.xlsx/.pptx), dan EPUB",
        "required": {
            "fitz": "PyMuPDF",
            "openpyxl": "openpyxl"
        },
        "recommended": {
            "markitdown": "markitdown",
            "pdfplumber": "pdfplumber",
            "pypdf": "pypdf",
            "pytesseract": "pytesseract",
            "PIL": "Pillow"
        },
        "optional_ai": {
            "mineru": "mineru[all]",
            "torch": "torch",
            "magic_pdf": "magic-pdf"
        }
    },
    "gis-analysis": {
        "description": "Analitika spasial, GIS, dan perencanaan perkotaan",
        "required": {
            "geopandas": "geopandas",
            "shapely": "shapely"
        },
        "recommended": {
            "osmnx": "osmnx",
            "folium": "folium",
            "duckdb": "duckdb",
            "matplotlib": "matplotlib",
            "pyogrio": "pyogrio"
        },
        "optional_ai": {
            "rasterio": "rasterio",
            "leafmap": "leafmap"
        }
    },
    "quarto-doc": {
        "description": "Render dokumen dan visualisasi data Quarto",
        "required": {
            "ipykernel": "ipykernel",
            "matplotlib": "matplotlib"
        },
        "recommended": {
            "pandas": "pandas",
            "seaborn": "seaborn",
            "openpyxl": "openpyxl",
            "jupyterlab": "jupyterlab"
        },
        "optional_ai": {
            "plotly": "plotly",
            "great_tables": "great_tables"
        }
    }
}


def find_conda():
    """Cari executable conda di sistem."""
    conda_exe = shutil.which("conda")
    if conda_exe:
        return conda_exe

    # Lokasi standar di Windows / Linux / macOS
    common_locations = [
        r"C:\ProgramData\miniconda3\Scripts\conda.exe",
        r"C:\ProgramData\miniconda3\condabin\conda.bat",
        r"C:\ProgramData\anaconda3\Scripts\conda.exe",
        os.path.expanduser(r"~\miniconda3\Scripts\conda.exe"),
        os.path.expanduser(r"~\miniconda3\condabin\conda.bat"),
        os.path.expanduser(r"~\anaconda3\Scripts\conda.exe"),
        os.path.expanduser(r"~\anaconda3\condabin\conda.bat"),
        os.path.expanduser(r"~/.conda/bin/conda"),
        "/opt/conda/bin/conda",
        "/usr/local/miniconda3/bin/conda",
    ]
    for loc in common_locations:
        if os.path.exists(loc):
            return loc
    return None


def get_conda_envs(conda_exe):
    """Ambil daftar environment conda."""
    try:
        res = subprocess.check_output([conda_exe, "info", "--envs", "--json"], text=True, errors="replace")
        data = json.loads(res)
        return data.get("envs", [])
    except Exception:
        # Fallback parsing teks jika --json gagal
        try:
            res = subprocess.check_output([conda_exe, "info", "--envs"], text=True, errors="replace")
            envs = []
            for line in res.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split()
                    if parts:
                        envs.append(parts[-1])
            return envs
        except Exception:
            return []


def get_env_python(env_path):
    """Dapatkan executable python dari direktori environment."""
    if os.name == "nt":
        py = os.path.join(env_path, "python.exe")
    else:
        py = os.path.join(env_path, "bin", "python")
    return py if os.path.exists(py) else None


def inspect_packages(python_exe, package_list):
    """Periksa status instalasi modul-modul di python target."""
    check_code = f"""
import sys, json
pkgs = {json.dumps(package_list)}
res = {{}}
for p in pkgs:
    try:
        mod = __import__(p)
        res[p] = {{"installed": True, "version": getattr(mod, '__version__', 'unknown')}}
    except ImportError as e:
        res[p] = {{"installed": False, "version": None, "error": str(e)}}
    except Exception as e:
        res[p] = {{"installed": False, "version": None, "error": str(e)}}
print(json.dumps(res))
"""
    try:
        out = subprocess.check_output([python_exe, "-c", check_code], text=True, errors="replace")
        return json.loads(out.strip())
    except Exception as e:
        return {p: {"installed": False, "error": str(e)} for p in package_list}


def main():
    parser = argparse.ArgumentParser(description="Conda Environment Analyzer")
    parser.add_argument("--profile", choices=list(TASK_PROFILES.keys()), help="Profil tugas yang ingin diperiksa")
    parser.add_argument("--env", help="Nama atau path environment conda sasaran")
    parser.add_argument("--check", help="Daftar nama modul Python yang dipisahkan koma (misal: 'fitz,markitdown')")
    parser.add_argument("--suggest-install", action="store_true", help="Tampilkan rekomendasi perintah instalasi paket")
    parser.add_argument("--json", action="store_true", help="Keluarkan hasil dalam format JSON")

    args = parser.parse_args()

    conda_exe = find_conda()

    if not conda_exe:
        msg = {
            "status": "CONDA_NOT_FOUND",
            "message": (
                "Conda / Miniconda TIDAK DITEMUKAN di sistem ini.\n\n"
                "Instruksi untuk Pengguna:\n"
                "1. Silakan unduh dan instal Miniconda dari: https://docs.anaconda.com/miniconda/\n"
                "   Atau via PowerShell (Windows):\n"
                "   winget install Anaconda.Miniconda3\n"
                "2. Setelah instalasi selesai, buka terminal baru atau restart terminal.\n\n"
                ">> Agen berhenti di sini dan menunggu Anda menyelesaikan instalasi Conda."
            )
        }
        if args.json:
            print(json.dumps(msg, indent=2))
        else:
            print("\n" + "!" * 70)
            print("PERINGATAN: CONDA BELUM TERPASANG DI MESIN INI")
            print("!" * 70)
            print(msg["message"])
            print("!" * 70 + "\n")
        sys.exit(2)

    envs = get_conda_envs(conda_exe)

    # Tentukan environment target
    target_env_path = None
    if args.env:
        for e in envs:
            if os.path.basename(e).lower() == args.env.lower() or os.path.abspath(e).lower() == os.path.abspath(args.env).lower():
                target_env_path = e
                break
        if not target_env_path:
            # Coba jalur langsung
            if os.path.exists(args.env):
                target_env_path = os.path.abspath(args.env)

    if not target_env_path and envs:
        # Default cari 'extract-pdf' jika profil extract-docs, atau ambil env pertama
        if args.profile == "extract-docs":
            for e in envs:
                if "extract-pdf" in e.lower():
                    target_env_path = e
                    break
        if not target_env_path:
            target_env_path = envs[0]

    target_py = get_env_python(target_env_path) if target_env_path else None

    # Tentukan daftar modul yang akan dicek
    to_check = []
    pypi_mapping = {}
    if args.profile:
        prof = TASK_PROFILES[args.profile]
        for section in ("required", "recommended", "optional_ai"):
            for mod_name, pypi_name in prof.get(section, {}).items():
                to_check.append(mod_name)
                pypi_mapping[mod_name] = pypi_name
    elif args.check:
        to_check = [c.strip() for c in args.check.split(",") if c.strip()]
        pypi_mapping = {c: c for c in to_check}
    else:
        # Tampilkan daftar environment saja jika tidak ada profil
        if args.json:
            print(json.dumps({"status": "OK", "conda_path": conda_exe, "envs": envs}, indent=2))
        else:
            print("=== Status Conda Terdeteksi ===")
            print(f"Conda Executable : {conda_exe}")
            print(f"Total Environment: {len(envs)}\n")
            print("Daftar Environment:")
            for idx, e in enumerate(envs, 1):
                name = os.path.basename(e)
                print(f"  [{idx:02d}] {name:<22} -> {e}")
            print("\nGunakan flag '--profile <nama_profil>' untuk memeriksa kecukupan paket.")
        return

    # Periksa paket
    results = inspect_packages(target_py, to_check) if target_py else {}

    missing = [pkg for pkg, data in results.items() if not data.get("installed")]
    installed = [pkg for pkg, data in results.items() if data.get("installed")]

    missing_pypi_names = [pypi_mapping.get(m, m) for m in missing]

    uv_path = shutil.which("uv")
    pip_cmd = f"pip install {' '.join(missing_pypi_names)}" if missing else None
    uv_cmd = f"uv pip install {' '.join(missing_pypi_names)}" if missing and uv_path else None

    output_data = {
        "status": "OK",
        "conda_path": conda_exe,
        "target_env": target_env_path,
        "python_exe": target_py,
        "profile": args.profile,
        "installed_count": len(installed),
        "missing_count": len(missing),
        "installed": {k: v for k, v in results.items() if v.get("installed")},
        "missing": {k: v for k, v in results.items() if not v.get("installed")},
        "install_suggestions": {
            "pip": pip_cmd,
            "uv": uv_cmd
        }
    }

    if args.json:
        print(json.dumps(output_data, indent=2))
        return

    print("=== Hasil Analisis Lingkungan Conda ===")
    print(f"Conda Path  : {conda_exe}")
    print(f"Target Env  : {target_env_path} ({os.path.basename(target_env_path) if target_env_path else 'None'})")
    print(f"Python Exec : {target_py}")
    if args.profile:
        print(f"Profil Tugas: {args.profile} ({TASK_PROFILES[args.profile]['description']})")
    print("-" * 65)

    print(f"{'Nama Modul':<20} | {'Status':<15} | {'Versi':<15}")
    print("-" * 65)
    for pkg in to_check:
        data = results.get(pkg, {})
        if data.get("installed"):
            status_str = "Terpasang (OK)"
            ver_str = str(data.get("version", "-"))
        else:
            status_str = "BELUM ADA"
            ver_str = "-"
        print(f"{pkg:<20} | {status_str:<15} | {ver_str:<15}")
    print("-" * 65)

    if missing:
        print(f"\n[!] Ditemukan {len(missing)} paket yang belum terpasang: {', '.join(missing)}")
        print("\nRekomendasi Perintah Instalasi:")
        if uv_cmd:
            print(f"  (Cepat via uv): {uv_cmd}")
        if pip_cmd:
            print(f"  (Standar pip) : {pip_cmd}")
    else:
        print("\n[V] Semua paket yang dibutuhkan untuk profil ini sudah terpasang dengan lengkap!")


if __name__ == "__main__":
    main()
