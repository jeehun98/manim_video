# Activation Function Series · ReLU

## 38-second introduction

```powershell
python -m manim render activation_relu.py ReLUIntroduction
```

Output: `media/videos/activation_relu/1920p30/ReLUIntroduction.mp4`.
1080×1920 portrait, 30 fps. Silent visual master with optional narration in `narration_relu.md`.

The six connected sections introduce the name and formula (4 s), transform a
column vector element by element (10 s), carry its colors into graph samples
(8 s), show selective suppression with OFF/PASS regions (9 s), briefly highlight
the kink and name nonlinearity (3 s), and return to the vector and graph (4 s).
Negative input markers rise from the faint identity reference to the zero-output
branch; positive markers pulse in place. Section budgets, colors, values, and
reusable text and column-vector helpers are in `activation_relu.py`.

The source uses Arial text for mathematical notation, so LaTeX is not required.
To adapt to another activation, update the function, formula, explanatory text,
and graph geometry together. For a smaller preview, change `config.pixel_width`
and `config.pixel_height` in the source; these explicit settings take precedence
over CLI resolution flags in the installed Manim version.

## Original 10-second short

검은 배경과 cyan 네온 라인으로 음수 입력이 ReLU를 거쳐 0이 되는 과정을 표현합니다.

## 실행

```powershell
python -m pip install -r requirements.txt
python -m manim render relu_short.py ReLUShort
```

기본 출력: `media/videos/relu_short/1920p30/ReLUShort.mp4`

- 1080×1920, 9:16, 30 fps, 정확히 10초
- 제목 → 입력 −3 → ReLU → 0으로 변환 → 출력 → 정의와 결론
- 외부 이미지, LaTeX, 유료 영상 생성 도구 없이 렌더링
- 음성 및 음악 없는 영상으로, Resolve/After Effects에서 후반 작업 가능

빠른 미리보기는 `python -m manim render -r 360,640 relu_short.py ReLUShort`를 사용합니다.
`-ql`과 같은 품질 프리셋은 해상도와 프레임률을 덮어쓸 수 있으므로 최종 렌더에서는 생략합니다.

스타일과 배치는 `relu_short.py`의 색상 상수, `label`, `neon` 및 장면 좌표에서 수정할 수 있습니다.

python.exe -m pip install --upgrade pip       
pip install -U manim
