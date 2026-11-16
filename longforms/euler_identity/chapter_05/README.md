# 오일러 항등식 — 5장 · 지수함수가 회전이 되는 순간

- ID: `euler_identity_ch05`
- 확정 길이: 224초, 사용자 제공 49문장 종료 시각.
- 화면: 1920×1080, 60fps, 16:9 전용. 첨부 콘티의 프레임률을 적용한다.
- 상태: 최종 렌더·수학 검증·화면 및 타이밍 검수 완료. 음원 미제공으로 무음·전체 문장 자막.

## 학습 목표

복소수의 작은 수직 변화가 회전으로 수렴하는 이유, 그 회전각이 정확히 θ인 이유, 삼각함수 좌표와의 연결을 이해한다.

## 핵심 결론

e^(iθ)=cosθ+i sinθ는 복소 지수함수와 단위원의 같은 위치를 나타내는 두 표현이다.

## 작업 순서

1. `master_script.md` 확정
2. `scenes.yaml`과 씬별 `spec.md` 작성
3. 씬별 `script.txt`로 TTS 생성 및 길이 기록
4. 씬별 Manim 렌더
5. 씬별 음성 결합
6. 전체 결합과 자막 검수

## 실행

최종 렌더: `py -3.12 longforms/euler_identity/chapter_05/build.py`

대표 씬: `py -3.12 longforms/euler_identity/chapter_05/build.py --preview --scene 8`

결과: `exports/euler_identity_ch05_224s_longform_final.mp4`

18개 독립 씬. 4장의 마지막 프레임으로 시작하고 오일러 공식과 단위원으로 끝난다. 6장 소스·음원은 아직 없다. 기존 장은 30fps이며 이 장은 콘티에 따라 60fps로 제작한다. 전체 합본은 요청 범위가 아니다.

검증: `py -3.12 longforms/euler_identity/chapter_05/verify_math.py`
