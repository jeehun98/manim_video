import argparse, os, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EPISODES = {"04": ("episodes/04_irreversibility/scene.py", "Irreversibility"), "03": ("episodes/03_relu_change_magnitude/scene.py", "ReLUChangeMagnitude"), "01": ("episodes/01_relu/scene.py", "ReLUIntroduction"), "02": ("episodes/02_relu_information_loss/scene.py", "ReLUInformationLoss"), "legacy": ("archive/relu_short.py", "ReLUShort")}
def main():
    p = argparse.ArgumentParser()
    p.add_argument("episode", choices=EPISODES)
    p.add_argument("--preview", action="store_true")
    a = p.parse_args()
    source, scene = EPISODES[a.episode]
    env = os.environ.copy()
    env.update(VIDEO_WIDTH="360" if a.preview else "1080", VIDEO_HEIGHT="640" if a.preview else "1920")
    media = ROOT / "media" / a.episode / ("preview" if a.preview else "final")
    subprocess.run([sys.executable, "-m", "manim", "render", source, scene, "--media_dir", str(media)], cwd=ROOT, env=env, check=True)
    latest = max((media / "videos").rglob(scene + ".mp4"), key=lambda p: p.stat().st_mtime)
    output = ROOT / "exports" / (a.episode + ("_preview" if a.preview else "") + ".mp4")
    output.parent.mkdir(exist_ok=True)
    shutil.copy2(latest, output)
    print(f"Export: {output}")
if __name__ == "__main__":
    main()
