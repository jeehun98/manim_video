# QR 1편 — 벡터는 어떻게 새로운 공간을 만드는가?

- 사용자 확정 대본·문장 종료 시각 기준 95초, 24개 독립 교체 가능 컷.
- 쇼츠: 1080×1920 / 가로 롱폼: 1920×1080, 각 30fps.
- 음원 미제공. 무음·화면 자막 영상, SRT 별도 제공.
- 3D 좌표 모델을 직교 투영한다. 투영 제거 중 카메라 고정, 관찰 구간에서만 시점 이동.
- 도입 종속 사례 a₃=(1,3,0) / 본 계산 a₃=(1,1,2).
- 기본 실행은 두 화면비 렌더·결합. --resume은 길이·fps가 검증된 컷을 재사용한다.

## 실행

```powershell
python longforms/qr01_new_directions/build.py --preview
python longforms/qr01_new_directions/build.py
python longforms/qr01_new_directions/build.py --layout shorts --scene 11
```

출력: exports/qr01_new_directions_95s_shorts_final.mp4 및 exports/qr01_new_directions_95s_longform_final.mp4.

## 자료

storyboard.md는 사용자 콘티 원문이다. narration.md·master_script.md·tts_script.txt는 확정 원고, timing.json·captions.srt는 20개 문장 종료 시각이다. scenes.yaml·manifest.json 및 각 spec.md는 24개 컷의 인덱스다. visuals.py는 공통 기하학, build.py는 컷별 렌더·프레임 수 검증·결합을 구현한다.

컷별 script.txt에 걸쳐 있는 문장은 전체 timing.json 기준으로 한 번만 발화한다. 컷별 script.txt를 개별 합성해 중복 발화하지 않는다. 실제 음원 싱크는 음원 미제공으로 미검증이다.

## 최종 검증 (2026-10-25)

두 최종본 모두 95.000초, 30fps, 2,850프레임 확인. 세로 1080×1920, 가로 1920×1080. 각 17개 대표 시각의 프레임을 검수했다. A=QR·QᵀQ=I·양의 대각·문장 타임라인 연속성 수치 검증 통과. verification.json, math_verification.json 및 qa/contact_*.jpg 참조. 차원 비교 컷의 문구는 벡터 이동과 함께 변경되도록 최종 수정했다.
