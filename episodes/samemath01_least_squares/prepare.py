"""Regenerate narration, timing, subtitles, and TTS from the locked script."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "script.json").read_text(encoding="utf-8"))
rows = data["sentences"]
phase_ends = [10, 22, 41, 48, 60, 79, 111, 136, 153, 160]


def stamp(seconds):
    return f"00:{seconds // 60:02}:{seconds % 60:02},000"


timing = []
captions = []
narration = [f"# {data['title']}", "", "사용자 제공 문장 종료 시각 기준 · 160초", ""]
tts_groups = []
group = []
start = 0
for index, (end, sentence) in enumerate(rows, 1):
    assert end > start
    timing.append({"start": start, "end": end, "text": sentence})
    captions.append(f"{index}\n{stamp(start)} --> {stamp(end)}\n{sentence}\n")
    narration.append(f"- {start:03}–{end:03}초: {sentence}")
    group.append(sentence)
    if end in phase_ends:
        tts_groups.append(" ".join(group))
        group = []
    start = end
assert start == 160 and not group
(HERE / "timing.json").write_text(json.dumps({"duration":160,"timing_source":"사용자 제공 문장 종료 시각","sentences":timing}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
(HERE / "captions.srt").write_text("\n".join(captions)+"\n", encoding="utf-8")
(HERE / "narration.md").write_text("\n".join(narration)+"\n", encoding="utf-8")
(HERE / "tts_script.txt").write_text("\n\n".join(tts_groups)+"\n", encoding="utf-8")
