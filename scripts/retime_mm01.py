"""Timing import completed. Use narration_timing.json as the timing source."""
from pathlib import Path
import json
p=Path(__file__).resolve().parents[1]/"longforms/mm01_cubic_question"
r=json.loads((p/"narration_timing.json").read_text(encoding="utf-8"))
assert len(r)==34 and r[-1]["end"]==142
print("User timestamps preserved: 34 intervals, 142 seconds")
