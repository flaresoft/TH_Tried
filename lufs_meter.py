#!/usr/bin/env python3
"""Measure LUFS of audio files using ffmpeg.

This script supports scanning directories for audio files and a
simple drag & drop GUI if `tkinterdnd2` is installed. It falls back
gracefully when optional dependencies are missing.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List

AUDIO_EXTS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma"}


def has_ffmpeg() -> bool:
    """Return True if ffmpeg is available."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def measure_lufs(file_path: Path) -> float:
    """Measure LUFS for ``file_path`` using ffmpeg's ebur128 filter."""
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-i",
        str(file_path),
        "-filter_complex",
        "ebur128=framelog=0",
        "-f",
        "null",
        "-",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stderr
    match = re.search(r"I:\s*([\-\d.]+)\s*LUFS", output)
    if not match:
        raise RuntimeError(f"Could not parse LUFS from ffmpeg output for {file_path}")
    return float(match.group(1))


def scan_directory(path: Path) -> Iterable[Path]:
    """Yield audio files recursively under ``path``."""
    for root, _dirs, files in os.walk(path):
        for name in files:
            if Path(name).suffix.lower() in AUDIO_EXTS:
                yield Path(root) / name


def cli(files: Iterable[Path]) -> int:
    if not has_ffmpeg():
        print("ffmpeg not found. Please install ffmpeg to measure LUFS.", file=sys.stderr)
        return 1
    exit_code = 0
    for f in files:
        try:
            lufs = measure_lufs(f)
            print(f"{f}: {lufs:.2f} LUFS")
        except Exception as exc:  # pragma: no cover - defensive
            exit_code = 1
            print(f"{f}: error ({exc})", file=sys.stderr)
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Measure LUFS of audio files using ffmpeg.",
        epilog="Drag & drop files onto this script on supported platforms.",
    )
    parser.add_argument("paths", nargs="*", type=Path, help="Files or directories to process")
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Recursively scan provided directories for audio files.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch GUI with drag & drop (requires tkinterdnd2)",
    )
    return parser


def run_gui() -> None:
    """Launch a simple GUI supporting drag & drop if possible."""
    import tkinter as tk
    from tkinter import messagebox, ttk

    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
    except Exception as exc:  # pragma: no cover - optional feature
        messagebox.showerror(
            "Drag & Drop unavailable", f"tkinterdnd2 not installed: {exc}"
        )
        return

    root = TkinterDnD.Tk()
    root.title("LUFS Meter")
    dropped: List[Path] = []

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    listbox = tk.Listbox(frame, width=60, height=10)
    listbox.pack(fill="both", expand=True)
    listbox.drop_target_register(DND_FILES)

    def on_drop(event: tk.Event) -> None:
        for item in root.splitlist(event.data):
            p = Path(item)
            if p.is_file():
                dropped.append(p)
                listbox.insert("end", str(p))

    listbox.dnd_bind("<<Drop>>", on_drop)

    def analyze() -> None:
        if not has_ffmpeg():
            messagebox.showerror("Error", "ffmpeg not found.")
            return
        results = []
        for p in dropped:
            try:
                lufs = measure_lufs(p)
                results.append(f"{p.name}: {lufs:.2f} LUFS")
            except Exception as exc:  # pragma: no cover - defensive
                results.append(f"{p.name}: error ({exc})")
        messagebox.showinfo("Results", "\n".join(results) if results else "No files.")

    ttk.Button(frame, text="Analyze", command=analyze).pack(pady=5)
    root.mainloop()


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.gui:
        run_gui()
        return

    targets: List[Path] = []
    for p in args.paths:
        if p.is_dir():
            if args.scan:
                targets.extend(scan_directory(p))
            else:
                print(f"{p} is a directory; use --scan to search it", file=sys.stderr)
        else:
            targets.append(p)
    if args.scan and not args.paths:
        targets.extend(scan_directory(Path.cwd()))
    if not targets:
        parser.print_help()
        return
    cli(targets)


if __name__ == "__main__":
    main()
