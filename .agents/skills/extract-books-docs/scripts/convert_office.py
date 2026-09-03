import argparse
import json
import os
import glob
import sys
import traceback
import shutil
import subprocess

try:
    from markitdown import MarkItDown
except ModuleNotFoundError:
    print("Warning: 'markitdown' library is not found in the current Python environment.", file=sys.stderr)
    uv_path = shutil.which("uv")
    if uv_path:
        print("Attempting to install 'markitdown' using 'uv'...", file=sys.stderr)
        try:
            subprocess.check_call([uv_path, "pip", "install", "markitdown"])
            from markitdown import MarkItDown
        except Exception as install_err:
            print(f"Error: Failed to install markitdown using uv: {install_err}", file=sys.stderr)
            sys.exit(1)
    else:
        print("'uv' not found. Falling back to standard 'pip'...", file=sys.stderr)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "markitdown"])
            from markitdown import MarkItDown
        except Exception as install_err:
            print(f"Error: Failed to install markitdown using pip: {install_err}", file=sys.stderr)
            sys.exit(1)

def convert_file(md_instance, file_path, output_dir):
    try:
        result = md_instance.convert(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Tentukan lokasi penyimpanan output
        if output_dir:
            target_dir = output_dir
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
        else:
            target_dir = os.path.dirname(file_path)
            
        md_path = os.path.join(target_dir, f"{base_name}.md")
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        return {"status": "Success", "md_path": md_path}
    except Exception as e:
        return {"status": "Failed", "error": str(e), "traceback": traceback.format_exc()}

def main():
    parser = argparse.ArgumentParser(description="Convert Office files to Markdown using markitdown")
    parser.add_argument("--target", required=True, help="Target file or directory to process")
    parser.add_argument("--output-dir", help="Target directory for Markdown files (optional)")
    parser.add_argument("--extensions", default=".docx,.xlsx,.pptx", help="Comma-separated list of extensions (default: .docx,.xlsx,.pptx)")
    parser.add_argument("--output", required=True, help="Path to write the JSON report")
    
    args = parser.parse_args()
    
    target_path = os.path.abspath(args.target)
    extensions = [ext.strip().lower() for ext in args.extensions.split(",") if ext.strip()]
    
    if not os.path.exists(target_path):
        print(f"Error: Target path does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        md = MarkItDown()
    except Exception as e:
        print(f"Error: Failed to initialize MarkItDown: {e}", file=sys.stderr)
        sys.exit(1)
    
    files_to_process = []
    
    if os.path.isfile(target_path):
        ext = os.path.splitext(target_path)[1].lower()
        if ext in extensions:
            files_to_process.append(target_path)
        else:
            print(f"Error: Target file {target_path} does not match extensions {extensions}", file=sys.stderr)
            sys.exit(1)
    elif os.path.isdir(target_path):
        for ext in extensions:
            search_pattern = os.path.join(target_path, f"*{ext}")
            files_to_process.extend(glob.glob(search_pattern))
            search_pattern_upper = os.path.join(target_path, f"*{ext.upper()}")
            files_to_process.extend(glob.glob(search_pattern_upper))
            
    files_to_process = list(set(files_to_process))
    
    if not files_to_process:
        print(f"No files found matching {extensions} in {target_path}", file=sys.stderr)
        report = {"summary": {"total": 0, "success": 0, "failed": 0}, "results": {}}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"Success! Report written to: {args.output}")
        sys.exit(0)
        
    results = {}
    success_count = 0
    failed_count = 0
    
    for file_path in files_to_process:
        res = convert_file(md, file_path, args.output_dir)
        results[file_path] = res
        if res["status"] == "Success":
            success_count += 1
        else:
            failed_count += 1
            
    report = {
        "summary": {
            "total": len(files_to_process),
            "success": success_count,
            "failed": failed_count
        },
        "results": results
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Success! Processed {len(files_to_process)} files. Report written to: {args.output}")

if __name__ == "__main__":
    main()
