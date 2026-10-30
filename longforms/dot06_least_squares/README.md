# 내적 LEVEL 06 — 최소제곱과 직교 잔차

사용자 확정 원고와 39개 문장 종료 시각을 적용한 170초 영상.
9:16 쇼츠 1080×1920와 16:9 롱폼 1920×1080, 각각 30fps.
음원 미제공으로 자막이 포함된 무음 영상이다.

## 핵심 설명

두 기준벡터 `(1,0,0)`, `(0,1,0)`로 만드는 결과는 z=0 평면에 놓인다.
목표 `b=(2,3,4)`는 이 평면 밖이므로 정확히 만들 수 없다.
평면 위 최단거리 결과는 `p=(2,3,0)`, 잔차는 `r=b−p=(0,0,4)`다.
잔차는 평면의 모든 방향과 직교한다. 최소 거리 4, 거리 제곱 16이다.

이를 열별 내적으로 묶으면 `Aᵀ(b−Ax)=0`이고, 정규방정식은 `AᵀAx=Aᵀb`다.
이번 예제에서는 열들이 이미 직교정규이므로 축약 QR은 `Q=A`, `R=I₂`다.
`Rx=Qᵀb`를 풀면 최적 계수 `x=(2,3)ᵀ`, 결과 `Ax=(2,3,0)`을 얻는다.

## 제작·실행

대본 → 사용자 제공 종료 시각 → 템플릿 기반 11개 씬 명세 → 화면 → 미리보기 → 최종 렌더.

```powershell
python longforms/dot06_least_squares/build.py --preview
python longforms/dot06_least_squares/build.py
```

사용 환경: Python 3.12, Manim 0.21.0, FFmpeg·FFprobe, Malgun Gothic.
`--layout shorts` 또는 `--layout longform`은 해당 규격만 제작한다.
`--scene 04`는 거리 탐색 씬만 교체한다. 그 뒤 `--concat-only`로 조립한다.
`--resume`은 완성된 동일 규격의 씬을 재사용한다.

## 자료

- `storyboard.md`: 사용자 첨부 콘티 원문
- `master_script.md`, `narration.md`: 확정 원고와 실제 문장 종료 시각
- `tts_script.txt`: 화면 변화 구간별 발음 원고, 시간·제목 없음
- `timing.json`, `captions.srt`: 39개 자막의 0–170초 타이밍
- `manifest.json`, `scenes.yaml`: 11개 독립 씬과 두 영상 규격
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬 계약·TTS·Manim 진입점
- `visuals.py`: 3차원 평면·카메라·거리 탐색·오차 분리·행렬과 축약 QR
- `build.py`: 렌더·자막 합성·concat·프레임 수와 길이 검증

## 정확성·시각 조건

3차원 월드 좌표에 직교투영 카메라를 적용하고 텍스트를 별도 화면 영역에 배치한다.
3차원 거리와 내적은 투영 전 좌표로 계산한다. 따라서 화면상 선분 길이와 실제 거리를 혼동하지 않는다.
직각 표시는 실제 공간의 x/z·y/z 방향으로 정의한 뒤 같은 카메라로 투영한다.
57초에 카메라 고도를 낮춰 수직 관계를 강조하며, 이후 증명 장면에서도 그 시점을 유지한다.
행렬 설명에서는 동일한 도형을 축소해 상단·좌측에 유지한다.

모든 잔차는 후보에서 목표로 향하는 `r=b−Ax`다.
A와 Q는 3×2, R은 2×2, x는 2×1, b는 3×1이다.
Q는 열들이 직교정규인 축약 행렬이며 `QᵀQ=I₂`다.
두 열이 독립인 이번 예제의 최소제곱 계수는 유일하다.
이전 편의 비직교 예제나 Q/R을 가져오지 않는다. 복습·다음 편 예고도 추가하지 않는다.

## 결과

- `exports/dot06_least_squares_170s_shorts_final.mp4`
- `exports/dot06_least_squares_170s_longform_final.mp4`
- 동일 이름의 `.srt`

미리보기는 `_preview` 접미사다. 최종 검증 메타데이터는 `render_report_both.json`이다.
