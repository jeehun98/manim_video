# 오일러 항등식 — 3장 · i, 허수와 회전

- ID: `euler_identity_ch03`
- 확정 길이: 171초, 사용자 제공 40문장 종료 시각.
- 화면: 1920×1080, 30fps, 16:9 전용. 기존 장과 동일한 프레임률.
- 상태: 최종 렌더·검수 완료. 음원 미제공으로 무음·전체 문장 자막.

## 학습 목표

i²=−1이라는 대수적 규칙과 복소평면의 반시계 90° 회전이 어떻게 연결되는지 이해한다.

## 핵심 결론

i(a+bi)=−b+ai이므로 i의 곱셈은 (a,b)를 (−b,a)로 보낸다.

## 작업 순서

1. `master_script.md` 확정
2. `scenes.yaml`과 씬별 `spec.md` 작성
3. 씬별 `script.txt`로 TTS 생성 및 길이 기록
4. 씬별 Manim 렌더
5. 씬별 음성 결합
6. 전체 결합과 자막 검수

## 실행

최종 렌더: `py -3.12 longforms/euler_identity/chapter_03/build.py`

대표 씬 검수: `py -3.12 longforms/euler_identity/chapter_03/build.py --preview --scene 11`

결과: `exports/euler_identity_ch03_171s_longform_final.mp4`

14개 독립 씬. 2장의 단위원과 0장의 자막·타이밍을 재사용한다. 2장의 마지막 프레임으로 시작하고 e·지수곡선으로 마친다. 4장 소스·음원은 아직 없다. 사용자 원문에 포함된 앞 장 언급과 연결 문장은 그대로 유지한다.

회전 수학 검증: `py -3.12 longforms/euler_identity/chapter_03/verify_rotation.py`
