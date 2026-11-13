"""Render the Gaussian integral short in portrait format."""
import argparse
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
    name = f"gausspi01_short{'_preview' if a.preview else ''}.mp4"
    media = ROOT / "media" / "gausspi01"
    exports = ROOT / "exports"
    exports.mkdir(exist_ok=True)
    subprocess.run([sys.executable, "-m", "manim", "render", str(HERE / "scene3d.py"), "GaussianPi3DShort",
                    "-r", f"{w},{h}", "--fps", "30", "--disable_caching", "--media_dir", str(media), "-o", name], cwd=ROOT, check=True)
    source = next((media / "videos" / "scene3d").rglob(name))
    output = exports / name
    # Manim's partial-movie concat can drift by a frame. Keep the confirmed
    # 177-second script at exactly 5310 frames, including the final held frame.
    normalized = output.with_name(output.stem + "_cfr.mp4")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
                    "-vf", "setpts=N/(30*TB),tpad=stop_mode=clone:stop_duration=0.1",
                    "-frames:v", "5310", "-r", "30", "-fps_mode", "cfr",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
                    str(normalized)], check=True)
    normalized.replace(output)
    print(output)


if __name__ == "__main__":
    main()
