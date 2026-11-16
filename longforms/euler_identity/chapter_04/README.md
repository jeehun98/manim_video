# 오일러 항등식 — 4장 · e, 반복 곱셈에서 연속적인 변화로

- ID: `euler_identity_ch04`
- 확정 길이: 202초, 사용자 제공 46문장 종료 시각.
- 화면: 1920×1080, 30fps, 16:9 전용. 기존 장과 같은 프레임률.
- 상태: 최종 렌더·검수 완료. 음원 미제공으로 무음·전체 문장 자막.

## 학습 목표

반복 곱셈에서 실수 지수로 확장하고, e^x의 변화율과 작은 비례 변화의 극한을 이해한다.

## 핵심 결론

현재 값에 비례하는 작은 변화를 잘게 나누어 반복하면 e^x가 된다. 그 변화의 방향을 i로 돌렸을 때의 결과는 질문으로 남긴다.

## 작업 순서

1. `master_script.md` 확정
2. `scenes.yaml`과 씬별 `spec.md` 작성
3. 씬별 `script.txt`로 TTS 생성 및 길이 기록
4. 씬별 Manim 렌더
5. 씬별 음성 결합
6. 전체 결합과 자막 검수

## 실행

최종 렌더: `py -3.12 longforms/euler_identity/chapter_04/build.py`

대표 씬: `py -3.12 longforms/euler_identity/chapter_04/build.py --preview --scene 8`

결과: `exports/euler_identity_ch04_202s_longform_final.mp4`

16개 독립 씬. 마지막은 복소평면과 e^(iθ)다. 사용자 원문에 포함된 연결 문장은 그대로 유지한다. 5장 소스·음원은 아직 없다.

수학 검증: `py -3.12 longforms/euler_identity/chapter_04/verify_math.py`
