"""Allocate the exact narration to the current silent prototype's shot timings.

This is an editorial mapping, not measured speech timing. Rebuild after retiming.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
# The opening title overlaps the first sentence; no extra silent lead-in.
# Each tuple: start, end, first/last script line (one-based), screen state.
CUES = [
    (0, 7.5, 1, 1, "고양이 이미지 등장"),
    (7.5, 10.5, 2, 4, "사람 CAT 등장"),
    (10.5, 14.5, 5, 7, "AI CAT 등장 · 같은 정답"),
    (14.5, 17, 8, 8, "두 CAT 강조 · 같은 이유인가"),
    (17, 19.5, 9, 11, "같은 결과 관찰"),
    (19.5, 20.5, 12, 12, "배경 변화 장면으로 전환"),
    (20.5, 22.5, 13, 14, "배경 색 변화 · 고양이 고정"),
    (22.5, 28, 15, 15, "AI 점수 하락 표현"),
    (28, 33, 16, 16, "판단 변화 질문"),
    (33, 35.5, 17, 17, "세 가지 변형 카드 등장"),
    (35.5, 37, 18, 18, "털 무늬 변형"),
    (37, 38.5, 19, 19, "얼굴 가림"),
    (38.5, 40, 20, 20, "작은 패턴 추가"),
    (40, 45, 21, 22, "변형 카드 비교 · 사람과 AI 반응 차이"),
    (45, 51, 23, 24, "모델·데이터·변형 방식에 따른 차이 · 전환"),
    (51, 54.5, 25, 25, "두 CAT와 미지의 판단 기준 등장"),
    (54.5, 59.5, 26, 26, "같은 정답 아래 물음표"),
    (59.5, 62.5, 27, 28, "판단의 기준 질문 등장"),
    (62.5, 65.5, 29, 29, "알아봤다는 의미 질문으로 전환"),
    (65.5, 68, 30, 31, "무엇을 확인해야 하는가"),
    (68, 72.5, 32, 32, "정답과 사용한 특징 구분"),
    (72.5, 75, 33, 34, "마지막 두 질문으로 전환"),
    (75, 78, 35, 35, "판단을 지탱한 정보 질문"),
    (78, 80, 36, 36, "확인 방법 질문 · 종료"),
]


def stamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def main():
    lines = [x for x in (ROOT / "script.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(lines) == 36, "Script changed; update the cue allocation."
    # Estimate relative speech length from visible characters and punctuation pauses.
    # The measured total is 111s; sentence-level audio alignment is not available.
    weights = []
    for _, _, first, final, _ in CUES:
        text = " ".join(lines[first-1:final])
        weights.append(len(re.sub(r"\s", "", text)) + 3 * len(re.findall(r"[.?!,]", text)))
    total_frames = 111 * 30
    boundaries = [0]
    accum = 0
    for weight in weights:
        accum += weight
        boundaries.append(round(total_frames * accum / sum(weights)))
    covered, blocks, mapping = [], [], [[0, 0]]
    for n, (old_start, old_end, first, final, _) in enumerate(CUES, 1):
        start, end = boundaries[n-1]/30, boundaries[n]/30
        assert start < end <= 111
        covered.extend(range(first, final+1))
        blocks.append(f"{n}\n{stamp(start)} --> {stamp(end)}\n" + "\n".join(lines[first-1:final]))
        mapping.append([old_end, end])
    assert covered == list(range(1, 37))
    (ROOT / "captions.srt").write_text("\n\n".join(blocks)+"\n", encoding="utf-8")
    (ROOT / "timing.json").write_text(json.dumps({
        "duration_seconds": 111,
        "fps": 30,
        "method": "Measured total duration; relative sentence durations estimated from narration text",
        "map": mapping,
    }, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("24 cues; duration 111 seconds; frame-aligned boundaries")


if __name__ == "__main__":
    main()
