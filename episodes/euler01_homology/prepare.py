"""Generate narration and caption assets from the supplied sentence endpoints."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "script.json").read_text(encoding="utf-8"))
rows = data["sentences"]
group_ends = {21, 56, 77, 92, 117, 144, 157, 173}


def stamp(t):
    return f"00:{t // 60:02}:{t % 60:02},000"


timing = []
captions = []
narration = [f"# {data['title']}", "", "사용자 제공 문장 종료 시각 기준 · 173초", ""]
groups = []
group = []
start = 0
for i, (end, sentence) in enumerate(rows, 1):
    assert end > start
    timing.append({"start": start, "end": end, "text": sentence})
    captions.append(f"{i}\n{stamp(start)} --> {stamp(end)}\n{sentence}\n")
    narration.append(f"- {start:03}–{end:03}초: {sentence}")
    group.append(sentence)
    if end in group_ends:
        groups.append(" ".join(group))
        group = []
    start = end
assert start == 173 and len(rows) == 39 and not group
(HERE / "timing.json").write_text(json.dumps({"duration": 173, "timing_source": data["timing_source"], "sentences": timing}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(HERE / "captions.srt").write_text("\n".join(captions) + "\n", encoding="utf-8")
(HERE / "narration.md").write_text("\n".join(narration) + "\n", encoding="utf-8")
(HERE / "tts_script.txt").write_text("\n\n".join(groups) + "\n", encoding="utf-8")
