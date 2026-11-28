"""Render independent unity clips and join them on the frame grid."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))


def verify(path, seconds, dimensions, fps, *, assembled=False):
    report = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ]))
    video, = report["streams"]
    assert video["codec_type"] == "video", path
    assert (video["width"], video["height"]) == dimensions, path
    assert video["r_frame_rate"] == f"{fps}/1", path
    assert int(video["nb_frames"]) == seconds * fps, path
    drift = abs(float(report["format"]["duration"]) - seconds)
    assert drift < 1 / fps, path
    exact = video["avg_frame_rate"] == f"{fps}/1" and drift < 0.001
    if assembled:
        assert exact, path
    return exact


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--scene", nargs="+", choices=[s["id"] for s in DATA["scenes"]])
    args = parser.parse_args()
    mode = "preview" if args.preview else "final"
    dimensions = (360, 640) if args.preview else (1080, 1920)
    fps = 15 if args.preview else 60
    files = [HERE / name for name in ("build.py", "scene.py", "timing.json")]
    files.extend(ROOT / name for name in (
        "longforms/qcs01_speed/direction.py", "longforms/qcs01_speed/layouts.py",
        "quantum_series/shared/theme.py", "quantum_series/shared/components.py",
    ))
    digest = hashlib.sha256(b"".join(file.read_bytes() for file in files)).hexdigest()[:16]
    cache = ROOT / "media" / "unity01" / mode / digest
    cache.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, QCS_LAYOUT="shorts", QCS_PREVIEW=str(int(args.preview)),
               QCS_AUDIT_DIR=str(cache / "audit"), PYTHONIOENCODING="utf-8")
    tex_bin = ROOT / ".tools/TinyTeX/TinyTeX/bin/windows"
    if tex_bin.is_dir():
        env["PATH"] = str(tex_bin) + os.pathsep + env.get("PATH", "")
    scenes = [s for s in DATA["scenes"] if not args.scene or s["id"] in args.scene]
    clips = [cache / (s["class"] + ".mp4") for s in scenes]
    missing = [s["class"] for s, clip in zip(scenes, clips) if not clip.exists()]
    if missing:
        subprocess.run([
            sys.executable, "-m", "manim", "render", str(HERE / "scene.py"), *missing,
            "--media_dir", str(cache), "--verbosity", "WARNING", "--progress_bar", "none",
        ], cwd=ROOT, env=env, check=True)
        for name in missing:
            rendered, = (cache / "videos").rglob(name + ".mp4")
            rendered.replace(cache / (name + ".mp4"))
    exact_clips = []
    for scene, clip in zip(scenes, clips):
        exact_clips.append(verify(clip, scene["end"] - scene["start"], dimensions, fps))
        audit = json.loads((cache / "audit" / (scene["id"] + ".json")).read_text())
        expected = [s["start"] for s in DATA["sentences"] if scene["start"] <= s["start"] < scene["end"]]
        times = [row["at"] for row in audit if row["at"] < scene["end"]-.001]
        assert len(times) == len(expected) and all(abs(a-b) < 1/fps for a, b in zip(times, expected)), audit
    if args.scene:
        print(cache)
        return

    manifest = cache / "concat.txt"
    manifest.write_text("".join(f"file '{clip.name}'\n" for clip in clips), encoding="utf-8")
    output = ROOT / "exports" / ("unity01_preview.mp4" if args.preview else "unity01.mp4")
    output.parent.mkdir(exist_ok=True)
    staged = cache / "assembled.mp4"
    codec = ["-c", "copy"]
    if not all(exact_clips):
        # Manim's concatenation can introduce sub-frame timestamp drift at cuts.
        codec = ["-vf", f"settb=1/{fps},setpts=N", "-r", str(fps), "-fps_mode", "cfr",
                 "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(manifest), *codec, "-movflags", "+faststart", str(staged)], check=True)
    verify(staged, DATA["duration"], dimensions, fps, assembled=True)
    staged.replace(output)
    print(f"Export: {output}")


if __name__ == "__main__":
    main()
