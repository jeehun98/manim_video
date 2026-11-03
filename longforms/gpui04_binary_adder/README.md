# GPU 개론 04 — 논리 게이트는 어떻게 숫자를 더할까?

사용자 확정 원문 35문장과 종료 시각에 맞춘 143초 영상. 독립 교체 가능한 15개 씬.

- 가로 1920×1080, 세로 1080×1920, 30fps. 무음·전체 문장 자막.
- 11₂+01₂=100₂, 1111₂+0001₂=10000₂. 낮은 자리는 오른쪽.
- XOR·AND → 반가산기 → 전가산기 → 리플 캐리 → G/P·캐리 룩어헤드 → 설계 비용.
- 자막은 하나의 Text를 문장 경계에서 교체하며 중첩 페이드를 사용하지 않는다.

```powershell
python longforms/gpui04_binary_adder/check_arithmetic.py
python longforms/gpui04_binary_adder/build.py --preview
python longforms/gpui04_binary_adder/build.py
python longforms/gpui04_binary_adder/inspect_frames.py
python longforms/gpui04_binary_adder/inspect_caption_boundaries.py
```

개별 수정: `build.py --scene 9 --layout shorts`, 이후 `build.py --resume`으로 재결합. --resume은 소스 변경 감지가 없으므로 변경 씬은 명시적으로 렌더한다.

원본 콘티: storyboard_reference.md. 대본·timing.json·captions.srt·씬별 spec.md를 함께 유지한다. 음원 제공 시 확정 타이밍에 맞춰 mux한다.

내용 검토 참고: [UCSD adder notes](https://cseweb.ucsd.edu/classes/wi05/cse140/adder_notes.php), [Rice carry-lookahead](https://www.ece.rice.edu/Courses/422/1996/supafly/adder.html). G=A AND B, P=A XOR B를 사용한다. 애니메이션은 논리적 전파 단계의 정성 모형이며 실측 지연이나 보편적 성능 배율을 뜻하지 않는다. 에너지는 구조·부하·스위칭 등에 따라 달라진다.
