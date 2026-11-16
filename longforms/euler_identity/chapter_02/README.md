# 오일러 항등식 — 2장 · π, 모든 원에서 발견되는 하나의 비율

- ID: `euler_identity_ch02`
- 확정 길이: 142초, 사용자 제공 35문장 종료 시각.
- 화면: 1920×1080, 30fps, 16:9 전용.
- 상태: 최종 렌더·검수 완료. 음원 미제공으로 무음·전체 문장 자막.

## 학습 목표

원의 비율 C/d=π에서 라디안 θ=s/r, 단위원의 좌표 (cosθ,sinθ)로 이어지는 관계를 이해한다.

## 핵심 결론

회전의 크기를 각도 하나로 나타내고, 그 각도로 원 위의 두 좌표를 계산할 수 있다.

## 작업 순서

1. `master_script.md` 확정
2. `scenes.yaml`과 씬별 `spec.md` 작성
3. 씬별 `script.txt`로 TTS 생성 및 길이 기록
4. 씬별 Manim 렌더
5. 씬별 음성 결합
6. 전체 결합과 자막 검수

## 실행

최종 렌더: `py -3.12 longforms/euler_identity/chapter_02/build.py`

대표 씬 검수: `py -3.12 longforms/euler_identity/chapter_02/build.py --preview --scene 11`

결과: `exports/euler_identity_ch02_142s_longform_final.mp4`

13개 독립 씬. 0장의 자막·폰트·타이밍·렌더 도구를 재사용한다. CircleRatioVisual, RadianCircleVisual, UnitCircleVisual은 이 장의 공통 기하 객체다. 원 위의 점·호·성분·숫자 표시를 하나의 각도에서 계산한다.

1장 마지막의 원·π와 같은 배치로 시작하고, 마지막에는 원·좌표축·i²=−1을 남긴다. 3장 소스나 음원은 아직 없다. 사용자 원문에 포함된 앞 장 언급과 연결 문장은 그대로 유지한다.
