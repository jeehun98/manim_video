"""Render the 9:16 Euler and homology short."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--preview", action="store_true")
    a = p.parse_args()
    w, h = (360, 640) if a.preview else (1080, 1920)
    name = f"euler01_short{'_preview' if a.preview else ''}.mp4"
    media = ROOT / "media" / "euler01"
    exports = ROOT / "exports"
    exports.mkdir(exist_ok=True)
    subprocess.run([sys.executable, "-m", "manim", "render", str(HERE / "scene.py"), "EulerHomologyShort",
                    "-r", f"{w},{h}", "--fps", "30", "--disable_caching", "--media_dir", str(media), "-o", name], cwd=ROOT, check=True)
    source = next(media.rglob(name))
    shutil.copy2(source, exports / name)
    print(exports / name)


if __name__ == "__main__":
    main()
