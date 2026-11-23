#!/usr/bin/env python3
"""Pengelola render project "Magnet dan Elektromagnetik".

Contoh:
  python main.py list
  python main.py test
  python main.py render 3                    # preview scene 3 (480p15)
  python main.py render 3 -q medium          # 720p30
  python main.py render 3 -q final           # 1920x1080 30 FPS
  python main.py all -q final                # semua scene, satu per satu
  python main.py concat -q final             # gabung hasil render (tanpa audio)
"""
import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
RENDERS = ROOT / "renders"

# (nomor, nama file di scenes/, nama kelas)
SCENES = [
    (1, "scene_01_opening", "Scene01Opening"),
    (2, "scene_02_magnetism", "Scene02Magnetism"),
    (3, "scene_03_magnetic_field", "Scene03MagneticField"),
    (4, "scene_04_magnetic_induction", "Scene04MagneticInduction"),
    (5, "scene_05_lorentz_force", "Scene05LorentzForce"),
    (6, "scene_06_electromagnetic_induction", "Scene06ElectromagneticInduction"),
    (7, "scene_07_generator_transformer", "Scene07GeneratorTransformer"),
    (8, "scene_08_summary", "Scene08Summary"),
    (9, "scene_09_closing", "Scene09Closing"),
]

# Catatan: `-qh` Manim = 1080p 60 FPS, sedangkan target kita 30 FPS,
# jadi kualitas final memakai resolusi dan FPS eksplisit.
QUALITY = {
    "preview": {"flags": ["-ql"], "folder": "480p15"},
    "medium":  {"flags": ["-qm"], "folder": "720p30"},
    "final":   {"flags": ["-r", "1920,1080", "--fps", "30"], "folder": "1080p30"},
}


def scene_by_number(n):
    for s in SCENES:
        if s[0] == n:
            return s
    sys.exit(f"Scene {n} tidak ada. Pilih 1-{len(SCENES)}.")


def output_path(scene, quality):
    _, mod, cls = scene
    return RENDERS / "videos" / mod / QUALITY[quality]["folder"] / f"{cls}.mp4"


def render(scene, quality):
    n, mod, cls = scene
    # --disable_caching: hindari penggunaan ulang potongan animasi lama yang bisa menggeser jumlah frame.
    cmd = [sys.executable, "-m", "manim", "render", *QUALITY[quality]["flags"], "--disable_caching",
           "--media_dir", str(RENDERS), f"scenes/{mod}.py", cls]
    print(f"\n=== Render scene {n:02d} ({cls}) kualitas {quality} ===")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(f"Render scene {n} gagal.")
    out = output_path(scene, quality)
    print(f"-> {out}" if out.exists() else f"(file tidak ditemukan di {out})")


def concat(quality):
    files = [output_path(s, quality) for s in SCENES]
    missing = [f.name for f in files if not f.exists()]
    if missing:
        sys.exit(f"Belum dirender pada kualitas '{quality}': {', '.join(missing)}")
    list_file = RENDERS / f"concat_{quality}.txt"
    list_file.write_text("".join(f"file '{f}'\n" for f in files))
    out = RENDERS / f"magnet_{quality}_tanpa_audio.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
           "-i", str(list_file), "-c", "copy", str(out)]
    subprocess.run(cmd, check=True)
    print(f"Digabung -> {out}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="daftar scene")
    sub.add_parser("test", help="jalankan tes perhitungan fisika")
    r = sub.add_parser("render", help="render satu scene")
    r.add_argument("number", type=int)
    r.add_argument("-q", "--quality", choices=QUALITY, default="preview")
    a = sub.add_parser("all", help="render semua scene satu per satu")
    a.add_argument("-q", "--quality", choices=QUALITY, default="preview")
    c = sub.add_parser("concat", help="gabungkan hasil render (tanpa audio)")
    c.add_argument("-q", "--quality", choices=QUALITY, default="final")
    args = p.parse_args()

    if args.cmd == "list":
        for n, mod, cls in SCENES:
            print(f"{n:02d}  scenes/{mod}.py  {cls}")
    elif args.cmd == "test":
        sys.exit(subprocess.run([sys.executable, "-m", "unittest", "discover", "tests", "-v"], cwd=ROOT).returncode)
    elif args.cmd == "render":
        render(scene_by_number(args.number), args.quality)
    elif args.cmd == "all":
        for s in SCENES:
            render(s, args.quality)
    elif args.cmd == "concat":
        concat(args.quality)


if __name__ == "__main__":
    main()
