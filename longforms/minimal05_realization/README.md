# 05 최소 실현 — 상태가 둘이면 둘 다 필요할까?

확정 대본 154초와 사용자 제공 문장 종료 시각 33개를 사용하는 독립 영상. 16개 씬을 각각 렌더해 세로 9:16과 가로 16:9로 제작한다. 음원 미제공으로 무음 영상이며 자막과 TTS 원고를 제공한다.

## 핵심 시스템

ẋ₁=−x₁+u, ẋ₂=−x₂+u, y=x₁+x₂.
새 좌표 z=x₁+x₂, d=x₁−x₂에서 ż=−z+2u, ḋ=−d, y=z.
따라서 차이는 입력의 영향을 받지 않는 자율 감쇠 상태이며 출력에도 나타나지 않는다. 두 방향은 (1,1)과 (1,−1)로 직교한다.

원래 2상태와 축소 1상태 시스템을 별도 RK4 적분 함수로 계산한다. 출력 곡선을 강제로 같은 좌표로 옮기지 않는다. 초기값 (1.5,.5), z₀=2, 같은 구간별 상수 입력을 사용한다. 일반 초기 상태 네 쌍도 검증한다. data_model.py와 math_verification.json에 행렬 변환, 제어·관측 행렬의 계수, 전달함수 2/(s+1), 독립 적분 오차를 기록한다.

최소 실현은 유한차원 LTI 시스템의 영 초기 상태 입출력 관계를 유지하는 최소 상태 차원이다. 이번 예시에서는 대응 초기값 z₀=x₁₀+x₂₀이면 영 초기 상태가 아니어도 출력이 일치한다. 일반 정의와 예시의 더 강한 성질을 구분한다. 축소 시스템은 제어·관측 가능하고, 비상수 전달함수를 상태 없는 정적 시스템으로 실현할 수 없으므로 최소 차원 1이다.

참고: [MathWorks minreal 공식 문서](https://www.mathworks.com/help/control/ref/dynamicsystem.minreal.html) — 제어 불가능하거나 관측 불가능한 상태 제거 및 최소 실현. 수학적 세부사항은 주어진 예시에서 직접 검증한다.

## 제작과 재현

```powershell
python longforms/minimal05_realization/data_model.py
python longforms/minimal05_realization/build.py --preview
python longforms/minimal05_realization/build.py
python longforms/minimal05_realization/verify_caption_boundaries.py --layout shorts
python longforms/minimal05_realization/verify_caption_boundaries.py --layout longform
```

요구 환경: Python 3.12, Manim 0.21, FFmpeg·FFprobe, Malgun Gothic. LaTeX 없이 Text 기반 수식과 축 표기를 사용한다.

원문: narration.md와 master_script.md. 발음 원고: tts_script.txt. 타이밍: narration_timing.json. 씬별 주장·발화·화면 조건은 scenes/NN/spec.md.
자막은 Manim 내부에서 그리지 않고 최종 concat 이후 단일 ASS 트랙으로 합성한다. 인접 이벤트는 종료 시각과 시작 시각을 같게 두되 중복되지 않도록 한다.

출력: exports/minimal05_154s_shorts_final.mp4 (1080×1920), exports/minimal05_154s_longform_final.mp4 (1920×1080). 각 30fps·154초. 미리보기는 _preview.mp4.

## 완료 상태

두 최종본과 미리보기 완료. 전체 디코딩, 길이·프레임 수, 총198프레임의 자막 경계, 주요 화면 배치 검토 통과. 검증 결과는 verification_final.json, math_verification.json, production_notes.md에 기록.
