# 내적 LEVEL 10 — Gradient Descent · 시리즈 최종편

사용자 확정38문장과 문장 종료 시각을 적용한169초 영상. L=θ₁²+4θ₂²의 곡면과 등고선에서 기울기(4,8)를 고정하고 단위 이동방향만 회전한다. 내적을 최소화하는 방향에서 음의 기울기를 도출한 뒤 실제 갱신과 학습률의 한계를 확인한다.

세로1080×1920 및 가로1920×1080,30fps. 음원 미제공으로 무음이며 한국어 자막을 포함한다. SRT와 화면 전환별 발음 원고를 별도로 제공한다.

```powershell
python longforms/dot10_gradient_descent/build.py --preview
python longforms/dot10_gradient_descent/build.py
python longforms/dot10_gradient_descent/check_math.py
python longforms/dot10_gradient_descent/check_delivery.py
```

Manim0.21.0, Python3.12, FFmpeg/FFprobe, Malgun Gothic. Text 수식으로 LaTeX를 요구하지 않는다. `--scene 06 --layout shorts`로 개별 씬을 렌더한 뒤 `--concat-only`로 결합한다. `--resume`는 동일 해상도·프레임 수의 씬을 재사용한다. 기존 에피소드용 `scripts/render.py`와 별도로 실행한다.

`manifest.json`의13개 독립 씬과 각 `spec.md`가 주장·대본·실제 길이·화면을 정의한다. `timing.json`은 원본38개 발화 구간이다. `visuals.py`가 3D직교투영·등고선·회전벡터·갱신·회상을 구현하고 `build.py`가 결합과 자막을 처리한다.

3D 곡면의 모든 정점은 z=L(x,y)에서 계산한다. 곡률 차이가 있는 타원형 포물면이다. 높이축은0.15배, 2D기울기 화살표는0.18배로 표시하고 화면에 명시한다. 방향·성분비를 보존한다. 기울기는 파라미터 공간의 벡터이며 3D접평면에서는 δ를(δ₁,δ₂,∇L·δ)로 올린다.

초록 회전 화살표는 단위방향u다. 실제 작은 이동Δθ=εu와 구별하고 DᵤL=∇L·u는 순간 변화율로 표기한다. cosφ와 방향미분도 별도 표기한다. 음의 기울기의 최급강하는 같은 유클리드 이동길이와 국소 일차근사를 기준으로 한다. 실제 손실차는 함수로 다시 계산한다. η=.1이면(1.6,.2),L=2.72; η=.4이면(.4,−2.2),L=19.52다.

126–169초 회상·시리즈 결론은 이번 사용자 대본의 명시적 요청으로 포함했다. LEVEL01–09의 같은 수학 예제를 대표 도형으로 재구성하며 추가 회상·예고·구독유도는 넣지 않는다. 마지막 타이틀은162–169초 유지한다.

결과: `exports/dot10_gradient_descent_169s_shorts_final.mp4`, `exports/dot10_gradient_descent_169s_longform_final.mp4`. 수치 검증은 `qa_math.json`, 영상 메타데이터는 `render_report_both.json`, 전체 재생 검사는 `qa_delivery.json`에 기록한다.
