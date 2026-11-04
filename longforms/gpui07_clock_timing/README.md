# GPU 개론 07 — 회로는 언제 값을 갱신할까?

확정31문장·사용자 종료 시각135초. 독립14씬. 가로1920×1080/세로1080×1920,30fps, 무음·전체 원문 자막. 음원 미제공.

```powershell
python longforms/gpui07_clock_timing/check_timing.py
python longforms/gpui07_clock_timing/build.py --preview
python longforms/gpui07_clock_timing/build.py
python longforms/gpui07_clock_timing/inspect_frames.py
python longforms/gpui07_clock_timing/inspect_caption_boundaries.py
python longforms/gpui07_clock_timing/verify_exports.py
```

개별 교체: `build.py --scene 7 --layout shorts`, 이후 `build.py --resume`. resume은 프레임 수만 보므로 변경한 씬은 직접 재렌더한다. 환경은Python3.12/Manim0.21/FFmpeg/Malgun Gothic.

전파 지연→안정 전 기록→안정 여유 확보→DFF→상승 에지·clock-to-Q→주기 제한→계산/저장 역할→동기식 회로→4비트 저장으로 연결한다.

검증 모델 check_timing.py: 1024개4비트 저장/에지 조합, D가 에지 전후 안정된 예시, 에지 뒤 Q변화, 사이 구간 Hold, 이른0/안정후8 기록, 안정 구간 위반시 보장없음, CQ+논리+setup+불확실성 주기 여유. Hold는 별도 조건이며 주기를 늘리는 것만으로 모든 타이밍 문제가 해결된다고 주장하지 않는다. 수치는 개념 시간 단위이고 실측 ns가 아니다.

단일DFF는1비트. 8=1000은4개의 DFF 뱅크로 표시한다. 공통 클럭으로 각기 다른D를 샘플하며 Q의 물리적 변화가 완벽히 동시라는 의미는 아니다. 클럭은저장요소 CLK핀에만 연결하고 ALU에 연결하지 않는다. SR이 D를 연속추종하는것처럼 그리지 않는다. 사용자 도입과마지막질문은유지하되 추가예고제목은넣지않는다.

- [Cornell Stateful Logic](https://www.cs.cornell.edu/courses/cs3410/2025fa/notes/state.html)
- [Cornell Timing Analysis](https://www.csl.cornell.edu/courses/ece2300/pdf/timing-analysis-notes.pdf)

원본: storyboard_reference.md. 확정대본: narration.md/master_script.md. 정확한종료시각: timing.json/captions.srt. TTS원고는 읽지않는제목·시각없이 빈줄로나눈31문단.
