"""Add the fixed equation and timed narration captions to the rendered short."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
STYLES = r"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Header,Malgun Gothic,40,&H00E5D2B6,&H00FFFFFF,&H00190E09,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,56,56,104,1
Style: Equation,Malgun Gothic,65,&H00FFF4EB,&H00FFFFFF,&H00190E09,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,45,45,160,1
Style: Caption,Malgun Gothic,47,&H00F9F6F2,&H00FFFFFF,&H00191009,&H00000000,0,0,0,0,100,100,0,0,1,0.65,0,5,86,86,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def stamp(seconds):
    return f"0:{seconds // 60:02d}:{seconds % 60:02d}.00"


def dialogue(start, end, style, text):
    return f"Dialogue: 0,{stamp(start)},{stamp(end)},{style},,0,0,0,,{text}\n"


def overlays(data, core_preview):
    start, end = 0, data["duration"]
    if core_preview:
        start = data["scene_boundaries"][4]
        end = data["scene_boundaries"][6]
    length = end - start
    script = STYLES
    script += dialogue(0, length, "Header", "같은 해를 나타내는 두 표현")
    script += dialogue(0, length, "Equation", r"{\c&H00F7CE56&}x² = 2{\c&H00BCE267&}   ⇔   {\c&H00FFA4B9&}x = ±√2")
    for cue in data["captions"]:
        left, right = max(start, cue["start"]), min(end, cue["end"])
        if left < right:
            script += dialogue(left-start, right-start, "Caption", r"{\pos(540,1652)}"+cue["text"])
    return script


def finish(source, output, core_preview=False):
    source, output = source.resolve(), output.resolve()
    data = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
    output.parent.mkdir(exist_ok=True, parents=True)
    # Keep the Manim frame in proportion and leave a dedicated caption band.
    filters = (
        "setpts=N/(30*TB),scale=iw*0.8:ih*0.8,"
        "pad=iw*5/4:ih*5/4:(ow-iw)/2:oh*0.035:0x090E19,"
        "drawbox=x=iw*0.08:y=ih*0.136:w=iw*0.84:h=2:color=0x31415C:t=fill,"
        "drawbox=x=iw*0.055:y=ih*0.791:w=iw*0.89:h=ih*0.137:color=0x111B2B:t=fill,"
        "ass=overlay.ass"
    )
    with tempfile.TemporaryDirectory(prefix="sqrt01-overlay-", dir=output.parent) as directory:
        work = Path(directory)
        (work / "overlay.ass").write_text(overlays(data, core_preview), encoding="utf-8")
        rendered = work / "captioned.mp4"
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
             "-vf", filters, "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264",
             "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-an",
             "-movflags", "+faststart", str(rendered)],
            cwd=work, check=True,
        )
        rendered.replace(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--core-preview", action="store_true")
    args = parser.parse_args()
    finish(args.source, args.output, args.core_preview)
