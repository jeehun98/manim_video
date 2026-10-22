# SVD 1막 — 서로 다른 입력을 행렬은 구별할 수 있을까?

- 현재본: 2026-10-22 사용자 제공 내레이션·문장 종료 시각과 상세 콘티 기준.
- 길이: 정확히 133초. 16개 독립 씬, 26개 문장 구간.
- 최종 영상: 1920×1080, 30fps. 미리보기: 854×480, 15fps.
- 음원 미제공: 영상은 무음이며 내레이션 자막을 포함한다. SRT도 별도 제공한다.
- 대본: [narration.md](narration.md), 발음용 [tts_script.txt](tts_script.txt).
- [사용자 콘티 원문](storyboard_source.md), [문장 시각](timing.json), [씬 인덱스](manifest.json).

## 제작 기준

관찰자는 출력만 본다. 입력 공간 공개는 시청자에게만 제공되는 실험 정보다. 입력 A는 파랑, B는 주황으로 양쪽에 유지한다. 두 좌표계의 단위는 동일하게 1.65이며, 카메라 배율은 고정한다.

A_s=diag(1,s), x_A=(0,0), x_B=(cosθ,sinθ), y_B=(cosθ,s sinθ)로 매 프레임 실제 계산한다. 화면 크기 때문에 겹쳐 보이는 0.001과 수학적으로 같은 좌표인 0을 구분한다. 확대 상자는 별도 척도임을 표시하며 실제 거리 0.001을 명시한다. 배율 0에서는 같은 x좌표의 세로 방향 입력들만 같은 출력으로 모인다. 115초에 s=0.1로 복귀했음을 표시한다. 출력 궤적은 그리지 않는다.

사용자 내레이션과 종료 시각을 그대로 적용한다. 마지막은 방향별 반응의 지도라는 현재 실험의 질문으로 끝내며, 후속 영상 안내 문구는 넣지 않는다. 이전 5막·15씬 초안의 1막과는 다른 현재 제작본이다.

## 실행

프로젝트 루트에서 Manim 0.21.0, FFmpeg 9.0.1, PyAV, Malgun Gothic 확인 후:

```powershell
python longforms/svd01_distinguish_inputs/build.py --preview
python longforms/svd01_distinguish_inputs/build.py
```

씬 하나만 교체한 뒤 결합:

```powershell
python longforms/svd01_distinguish_inputs/build.py --scene 10
python longforms/svd01_distinguish_inputs/build.py --concat-only
```

기본 동시 렌더 수 3. `--jobs 1`로 순차 실행할 수 있다. 모든 독립 씬은 공통 scene_engine.py의 절대시간 상태를 재현한다. 정규화는 동일 fps와 사용자 지정 프레임 수를 맞추는 용도이며 속도 변경을 하지 않는다. 최종 concat 후 길이·프레임 수·해상도를 검사한다.

출력: exports/svd01_distinguish_inputs_133s_1080p30.mp4 및 같은 이름의 .srt. 실제 음원 확보 후 mux할 수 있으며, 음성이 들어간 완성본으로 표기하지 않는다.

## 렌더 검증 결과

2026-10-22 최종본 생성 및 전체 디코딩 검사 완료: 133초, 1920×1080, 30fps, 3,990프레임. 미리보기 133초, 854×480, 15fps, 1,995프레임. 26개 사용자 문장 경계 및 주요 계산 사례 검증. 최종 결합 영상의 14개 시점에서 화면·자막을 확인했다. [검사 기록](qa/report.json), [최종 화면 모음](qa/final_contact_sheet.jpg).
