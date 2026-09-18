# Activation Function Series

GPU 연산 시리즈 1화: **수식 하나가 GPU에서 실행되기까지** (145초, 한국어 내레이션 포함).
대본·타이밍·실행 안내는 [GPU 01](episodes/gpu01_formula_to_gpu/narration.md)을 참고하세요.
`python scripts/render.py gpu01 --preview` 또는 `python scripts/render.py gpu01`로 렌더합니다.
공통 시각 컴포넌트는 `gpu_series/`에 분리되어 있습니다.

GPU 2화 **Warp란 무엇인가** (164초, 무음): [대본](episodes/gpu02_warp/narration.md), [구성 안내](episodes/gpu02_warp/brief.md).
`python scripts/render.py gpu02` → `exports/gpu02.mp4`.

GPU 3화 **같은 계산, 다른 메모리 접근** (175초, 무음): [대본](episodes/gpu03_memory_access/narration.md), [구성 안내](episodes/gpu03_memory_access/brief.md).
`python scripts/render.py gpu03` → `exports/gpu03.mp4`. TTS 텍스트는 영어·수식을 한글 발음으로 표기합니다.

Manim 세로형 수학 Shorts. 1080 × 1920, 30fps, 어두운 배경과 원소별 파스텔 색상.
렌더는 음성·음악 없는 마스터로 생성합니다. 보존한 기존 GPU 01 MP4에는 한국어 내레이션이 포함되어 있습니다. LaTeX는 필요 없습니다.

## 에피소드

| ID | 주제 | 길이 | 소스·대본 | 결과물 |
| --- | --- | --- | --- | --- |
| 01 | ReLU 소개 | 38초 | `episodes/01_relu/` | `exports/01.mp4` |
| 02 | ReLU — Information Loss #1 | 42초 | `episodes/02_relu_information_loss/` | `exports/02.mp4` |
| 03 | ReLU — Beyond the count | 40초 | `episodes/03_relu_change_magnitude/` | `exports/03.mp4` |
| 04 | Irreversibility — Beyond Information Loss | 100초 | `episodes/04_irreversibility/` | `exports/04.mp4` |
| 05 | Information Guides Optimization | 100초 | `episodes/05_computation_simplification/` | `exports/05.mp4` |
| 06 | Sigmoid 01 — 위치에 따라 달라지는 압축 | 70초 | `episodes/06_sigmoid_intro/` | `exports/06.mp4` |
| 07 | Sigmoid 02 — 기울기로 읽는 압축률 | 100초 | `episodes/07_sigmoid_derivative/` | `exports/07.mp4` |
| 08 | Sigmoid 03 — 포화와 작아지는 학습 신호 | 100초 | `episodes/08_sigmoid_saturation/` | `exports/08.mp4` |
| 09 | Sigmoid 04 — 값에서 분포로 | 100초 | `episodes/09_sigmoid_distribution/` | `exports/09.mp4` |
| 10 | Sigmoid 05 — 누적확률이라는 새 좌표 | 137초 | `episodes/10_sigmoid_cdf/` | `exports/10.mp4` |
| 11 | Sigmoid 06 — 한계와 선택의 이유 | 150초 | `episodes/11_sigmoid_finale/` | `exports/11.mp4` |
| 12 | Softmax 01 — 점수에서 분포로 | 90초 | `episodes/12_softmax_intro/` | `exports/12.mp4` |
| 13 | Softmax 02 — 숫자가 달라도 결과가 같은 이유 | 84초 | `episodes/13_softmax_shift/` | `exports/13.mp4` |
| 14 | Softmax 03 — 차이가 비율이 되는 이유 | 80초 | `episodes/14_softmax_ratio/` | `exports/14.mp4` |
| 15 | Softmax 04 — Temperature로 분포 조절하기 | 108초 | `episodes/15_softmax_temperature/` | `exports/15.mp4` |
| 16 | Softmax 05 — 서로 연결된 출력과 자코비안 | 119초 | `episodes/16_softmax_jacobian/` | `exports/16.mp4` |
| 17 | Softmax 06 — 두 입력의 Softmax와 Sigmoid | 124초 | `episodes/17_softmax_sigmoid/` | `exports/17.mp4` |
| 18 | Softmax 07 — Smooth Max의 기울기 | 176초 | `episodes/18_softmax_lse/` | `exports/18.mp4` |
| 19 | Softmax 08 — 분포의 집중도를 읽는 Entropy | 166초 | `episodes/19_softmax_entropy/` | `exports/19.mp4` |
| 20 | Softmax 09 — Attention의 비중을 결정하는 함수 (완결) | 152초 | `episodes/20_softmax_attention_finale/` | `exports/20.mp4` |
| legacy | 초기 프로토타입 | 10초 | `archive/relu_short.py` | `exports/legacy.mp4` |

## 실행

```powershell
python -m pip install -r requirements.txt
python scripts/render.py 20 --preview
python scripts/render.py 20
python scripts/render.py 19 --preview
python scripts/render.py 19
python scripts/render.py 18 --preview
python scripts/render.py 18
python scripts/render.py 17 --preview
python scripts/render.py 17
python scripts/render.py 16 --preview
python scripts/render.py 16
python scripts/render.py 15 --preview
python scripts/render.py 15
python scripts/render.py 14 --preview
python scripts/render.py 14
python scripts/render.py 13 --preview
python scripts/render.py 13
python scripts/render.py 12 --preview
python scripts/render.py 12
python scripts/render.py 11 --preview
python scripts/render.py 11
python scripts/render.py 10 --preview
python scripts/render.py 10
python scripts/render.py 09 --preview
python scripts/render.py 09
python scripts/render.py 08 --preview
python scripts/render.py 08
python scripts/render.py 07 --preview
python scripts/render.py 07
python scripts/render.py 06 --preview
python scripts/render.py 06
python scripts/render.py 05 --preview
python scripts/render.py 05
python scripts/render.py 04 --preview
python scripts/render.py 04
python scripts/render.py 03 --preview
python scripts/render.py 03
python scripts/render.py 02 --preview
python scripts/render.py 02
python scripts/render.py 01
python scripts/render.py legacy
```

미리보기는 360 × 640이며 `exports/02_preview.mp4`처럼 별도 저장됩니다.
렌더 스크립트는 실행 위치와 무관하게 프로젝트 루트를 기준으로 동작합니다.

## 폴더 규칙

- `episodes/<번호>_<주제>/`: scene.py, narration.md, 필요하면 brief.md.
- `archive/`: 보존하는 초기 프로토타입.
- `scripts/`: 공통 렌더 도구.
- `exports/`: 공유·편집용 MP4. Git 제외.
- `media/<ID>/`: 재생성 가능한 렌더 캐시. 기존 media 결과도 보존.

새 에피소드는 scripts/render.py의 EPISODES에 등록합니다.
각 에피소드 소스는 독립적으로 동작하며 공통 해상도 환경변수를 지원합니다.
02편은 벡터 → 억제 비율 → 분포 → 음수 확률 → 같은 개수, 다른 크기로 이어집니다.
Zeroed Ratio는 정보 손실 자체가 아닌 단순 억제 지표입니다.

## TTS 편집용 타이밍

13편부터 짧은 질문·연결 문장은 2~3.5초 내에 전환하고, 문장 길이와 시각적 설명량에 따라 시간을 배분합니다. 전환 시간은 각 구간에 포함합니다. 실제 음성 미제공 시 발화 길이를 추정하며, 타임코드 대본과 SRT를 함께 제공합니다.

- GPU 04: `episodes/gpu04_memory_spaces/scene.py` → `python scripts/render.py gpu04` → `exports/gpu04.mp4` (174초, 무음)

- GPU 05: `episodes/gpu05_naive_gemm/scene.py` → `python scripts/render.py gpu05` → `exports/gpu05.mp4` (174초, 무음)

- GPU 06: `episodes/gpu06_tiled_gemm/scene.py` → `python scripts/render.py gpu06` → `exports/gpu06.mp4` (174초, 무음)

- GPU 07: `episodes/gpu07_tile_size/scene.py` → `python scripts/render.py gpu07` → `exports/gpu07.mp4` (174초, 무음)

- GPU 08: `episodes/gpu08_register_occupancy/scene.py` → `python scripts/render.py gpu08` → `exports/gpu08.mp4` (174초, 무음)

- GPU 09: `episodes/gpu09_bank_conflict/scene.py` → `python scripts/render.py gpu09` → `exports/gpu09.mp4` (174초, 무음)

## 선형대수학 시리즈

- LA 01 **행렬은 관계를 기록한다** — 154초, 1080×1920, 30fps, 무음. 세 대상 사이의 방향 있는 연결이 행렬의 각 칸으로 정리되는 과정.
- [대본](episodes/la01_matrix_relations/narration.md) · [제작 의도와 시리즈 구상](episodes/la01_matrix_relations/brief.md)
- `python scripts/render.py la01 --preview` → `exports/la01_preview.mp4`
- `python scripts/render.py la01` → `exports/la01.mp4`
- 이전 공간 변환 버전 영상·대본: `archive/la01_space_version/`. 다음 편 예고: 행렬과 벡터의 곱.
