# GPU 개론 06 — 논리 게이트는 어떻게 값을 기억할까?

사용자 확정29문장·종료 시각 기준140초. 독립 씬14개. 가로1920×1080 / 세로1080×1920,30fps. 음원 미제공으로 무음·전체 문장 자막.

```powershell
python longforms/gpui06_sr_latch/check_latch.py
python longforms/gpui06_sr_latch/build.py --preview
python longforms/gpui06_sr_latch/build.py
python longforms/gpui06_sr_latch/inspect_frames.py
python longforms/gpui06_sr_latch/inspect_caption_boundaries.py
python longforms/gpui06_sr_latch/verify_exports.py
```

특정 씬: `build.py --scene 7 --layout shorts`, 이후 `build.py --resume`. resume은 소스 변경 감지가 없으므로 수정 씬은 명시적으로 재렌더한다. Manim0.21 / Python3.12 / FFmpeg / Malgun Gothic.

핵심 흐름: 연속 계산의 중간 결과→ALU재사용의 저장 필요성→조합논리 한계→Feedback→교차 NOR→같은 입력의 두 안정 상태→SR Latch→갱신 시점 질문.

위 게이트 Q=NOT(R OR Qbar), 아래 게이트 Qbar=NOT(S OR Q). S펄스는 Qbar0을 먼저 만들고 Q1로 안정한다. R펄스는 Q0을 먼저 만들고 Qbar1로 안정한다. 전파 중은 지연 순서를 나타내는 모형이며 안정 상태에서 두 식을 검사한다. R=S=0에서 기존 상태가 유지된다. R=S=1은 시연하지 않는다. 교차 피드백선은 브리지로 비접합을 표시한다. 회로 전원이 공급되고 정상 동작하는 조건의 휘발성 기억이다.

검증: 합법 전환6개·길이6의 입력열1458개, 두 안정식 및 Hold 검증. 제어 시 고정 배선 좌표 검사. 일반 되먹임만으로 안정 기억을 보장하지 않는다. ALU 재사용의 결과 버스와 래치 내부 피드백은 서로 다른 구조다. SR입력을 D입력으로 바꾸는 것처럼 표현하지 않는다.

원문은 storyboard_reference.md. 확정 대본은 master_script.md/narration.md, 시각은 timing.json/captions.srt. TTS는 제목·시각 없이 빈 줄 구분. 사용자가 제공한 도입과 마지막 문장을 유지하고 GPU07 제목이나 추가 예고는 삽입하지 않는다.

근거: [Cornell Stateful Logic](https://www.cs.cornell.edu/courses/cs3410/2025fa/notes/state.html), [Cornell state lecture](https://www.cs.cornell.edu/courses/cs3410/2025sp/lectures/07-state-notes.pdf).
