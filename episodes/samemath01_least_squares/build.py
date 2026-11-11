"""Render the two aspect-ratio versions of the same 160 s Manim scene."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--aspect", choices=("short", "long", "both"), default="both")
    args = parser.parse_args()
    dimensions = {"short": (360, 640) if args.preview else (1080, 1920),
                  "long": (640, 360) if args.preview else (1920, 1080)}
    targets = dimensions if args.aspect == "both" else {args.aspect: dimensions[args.aspect]}
    exports = ROOT / "exports"
    exports.mkdir(exist_ok=True)
    for aspect, (width, height) in targets.items():
        scene = "SameMathShort" if aspect == "short" else "SameMathLong"
        command = [sys.executable, "-m", "manim", "render", str(HERE / "scene.py"), scene,
                   "-r", f"{width},{height}", "--fps", "30", "--disable_caching",
                   "--media_dir", str(ROOT / "media" / "samemath01"),
                   "-o", f"samemath01_{aspect}{'_preview' if args.preview else ''}.mp4"]
        subprocess.run(command, cwd=ROOT, check=True)
        result = next((ROOT / "media" / "samemath01").rglob(command[-1]))
        destination = exports / command[-1]
        destination.write_bytes(result.read_bytes())
        print(destination)


if __name__ == "__main__":
    main()
