# 내적 LEVEL 07 — PCA: 정보를 보존하는 방향

사용자 확정 대본과 문장 종료 시각32개를 적용한149초 영상. 같은16개 데이터를 중심화한 뒤, 투영 방향을 바꾸며 재구성 오차 최소화와 분산 최대화의 동치를 보여준다. 공분산행렬과 가장 큰 고윳값의 고유벡터로 첫 번째 주성분을 찾는다.

세로1080×1920 및 가로1920×1080,30fps. 음원 미제공으로 두 영상은 무음이며 한국어 자막이 포함된다. 별도 SRT와 화면 전환별 발음 원고도 제공한다.

```powershell
python longforms/dot07_pca_direction/build.py --preview
python longforms/dot07_pca_direction/build.py
python longforms/dot07_pca_direction/check_math.py
```

Manim0.21.0, Python3.12, FFmpeg/FFprobe, Malgun Gothic. 수식은 Text로 그려 LaTeX 설치를 요구하지 않는다. `--scene 07 --layout shorts`로 개별 씬을 교체한 뒤 `--concat-only`로 결합한다. `--resume`는 완료된 동일 해상도·프레임 수의 씬을 재사용한다.

`manifest.json`의12개 씬은 사용자 문장 경계에서 분리되며 각 `spec.md`에 주장·대본·확정 길이·조건이 있다. `visuals.py`가 두 화면비에 맞춘 공통 도형과 수식을 제공하고 `build.py`가 씬을 렌더·결합·자막 처리한다. `timing.json`은 원본32개 발화 구간이다.

정확성: 중심화 후 점과 축·배율 고정. u만 회전. p=(x·u)u, r=x−p. E+V=T, 분산=V/16=uᵀΣu, Σ=(1/16)Σxxᵀ. 최적 직선의 ±u는 동일한 정사영이다. 표시 수치는 같은 좌표에서 계산한다. 표본분산의 n−1 분모는 사용하지 않는다.

결과: `exports/dot07_pca_direction_149s_shorts_final.mp4`, `exports/dot07_pca_direction_149s_longform_final.mp4`. 검증 자료는 `qa_math.json`, `preview_report_both.json`, `render_report_both.json`.

수치 검증은361개 방향에서 단위길이·잔차 직교성·에너지 보존·분산의 이차형식·±방향의 동일 정사영을 확인한다. 이 데이터의 최적 방향은35°, 최적 오차 제곱합2.1948, 보존 제곱합48.7994, 최대 분산3.04996이다. `check_render.py`는 실제 미리보기의 서로 다른 방향3개에서12개 파란 점의 위치가 고정되어 있는지도 검사한다. 래스터·압축에 따른 중심 차이는 세로0.258px, 가로0.413px였다.
