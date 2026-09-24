# Activation Function Series

## FlashAttention — 계산보다 데이터를 움직이는 방법

- FlashAttention 01 **Attention은 무엇을 저장하고 있을까?** — 64초, 1080×1920, 30fps, 무음. 표준적인 materialized Attention이 `S = QKᵀ`, `P = softmax(S)`의 `N × N` 중간 결과를 만들고 HBM에 쓰고 읽는 흐름을 보여준 뒤, 같은 출력 `O`를 유지하면서 저장을 피할 수 있는지 묻습니다.
- [대본](episodes/flash01_attention_storage/narration.md) · [제작 기준](episodes/flash01_attention_storage/brief.md)
- `python scripts/render.py flash01 --preview` → `exports/flash01_preview.mp4`
- `python scripts/render.py flash01` → `exports/flash01.mp4`

## EML — 하나의 primitive로 만드는 계산

- EML 01 **과학용 계산기의 연산자를 하나만 남긴다면?** — 50초, 1080×1920, 30fps, 무음. primitive 축소가 표현 규칙과 연산 graph를 통일하는 이유를 살펴보고, 실제 실행 효율과 구분한 뒤 `EML(x,1)=eˣ`를 첫 tree로 구성합니다.
- [대본](episodes/eml01_single_operator/narration.md) · [시리즈 제작 기준](episodes/eml01_single_operator/brief.md)
- `python scripts/render.py eml01 --preview` → `exports/eml01_preview.mp4`
- `python scripts/render.py eml01` → `exports/eml01.mp4`
- EML 02 **같은 연산자를 연결해서 로그 만들기** — 60초. 동일한 EML 노드 세 개를 아래에서 위로 평가해 `ln x`가 남는 과정을 보여줍니다.
- [2편 대본](episodes/eml02_log_tree/narration.md) · [2편 제작 기준](episodes/eml02_log_tree/brief.md)
- `python scripts/render.py eml02 --preview` → `exports/eml02_preview.mp4`
- `python scripts/render.py eml02` → `exports/eml02.mp4`
- EML 03 **덧셈도 기본 연산자가 아니라면?** — 66초. `1 Add node`와 직접 탐색된 `9 EML nodes · depth 8` graph를 비교해 표현 통일과 실행 최적화를 구분합니다.
- [3편 대본](episodes/eml03_addition_graph/narration.md) · [3편 제작 기준](episodes/eml03_addition_graph/brief.md)
- `python scripts/render.py eml03 --preview` → `exports/eml03_preview.mp4`
- `python scripts/render.py eml03` → `exports/eml03.mp4`
- EML 04 **하나의 연산자로 계산한다는 것은 무엇일까?** — 72초 완결편. 동일한 EML 블록을 exp·ln·add topology로 재배치하며 primitive의 표현력과 실행 효율을 구분합니다.
- [완결편 대본](episodes/eml04_primitive_finale/narration.md) · [완결편 제작 기준](episodes/eml04_primitive_finale/brief.md)
- `python scripts/render.py eml04 --preview` → `exports/eml04_preview.mp4`
- `python scripts/render.py eml04` → `exports/eml04.mp4`

## SVD — 네 가지 관점

한국어 화면 자막을 포함한 세로 1080×1920, 30fps 무음 마스터 네 편입니다. 각 MP4와 같은 이름의 SRT가 `exports/`에 있습니다.

| ID | 제목 | 길이 | 대본 | 영상 |
|---|---|---|---|---|
| svd01 | 최적의 망각 | 115초 | [대본](episodes/svd01_optimal_forgetting/narration.md) | [MP4](exports/svd01.mp4) |
| svd02 | 차이의 생존율 | 99초 | [대본](episodes/svd02_difference_survival/narration.md) | [MP4](exports/svd02.mp4) |
| svd03 | 방향별 감도 지도 | 100초 | [대본](episodes/svd03_sensitivity_map/narration.md) | [MP4](exports/svd03.mp4) |
| svd04 | 입력에게 던지는 독립적인 질문 | 100초 | [대본](episodes/svd04_independent_questions/narration.md) | [MP4](exports/svd04.mp4) |
| svd05 | 타원을 훑어 찾는 두 값 | 85초 | [대본](episodes/svd05_ellipse_extrema/narration.md) | [MP4](exports/svd05.mp4) |
| svd06 | Condition Number: 방향의 불균형 | 60초 | [대본](episodes/svd06_condition_number/narration.md) | [MP4](exports/svd06.mp4) |
| svd07 | 역행렬이 오차를 키우는 이유 | 60초 | [대본](episodes/svd07_inverse_error/narration.md) | [MP4](exports/svd07.mp4) |
| svd08 | 방정식은 거의 같은데, 답은 왜 다를까? | 69초 | [대본](episodes/svd08_near_parallel_lines/narration.md) | [MP4](exports/svd08.mp4) |
| svd09 | 행렬이 한 방향을 완전히 잃는 순간 | 60초 | [대본](episodes/svd09_singular_matrix/narration.md) | [MP4](exports/svd09.mp4) |

[시리즈 제작 안내와 수학적 기준](episodes/svd_series/README.md). `python scripts/render.py svd01`로 렌더합니다. 나머지도 같은 방식이며 `--preview`를 추가하면 360×640 미리보기를 생성합니다.

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

- LA 01 **행렬은 관계를 기록한다** — 130초, 1080×1920, 30fps, 무음. 세 대상 사이의 방향 있는 연결이 행렬의 각 칸으로 정리되는 과정.
- [대본](episodes/la01_matrix_relations/narration.md) · [제작 의도와 시리즈 구상](episodes/la01_matrix_relations/brief.md)
- `python scripts/render.py la01 --preview` → `exports/la01_preview.mp4`
- `python scripts/render.py la01` → `exports/la01.mp4`
- 이전 공간 변환 버전 영상·대본: `archive/la01_space_version/`. 다음 편 예고: 행렬과 벡터의 곱.

- LA 02 **기여를 모으면 결과가 된다** — 90초, 1080×1920, 30fps, 무음. 여러 출발점의 가중 기여를 목적지별로 합산합니다.
- [2편 대본](episodes/la02_matrix_vector_product/narration.md) · [구성 및 수학 확인](episodes/la02_matrix_vector_product/brief.md)
- `python scripts/render.py la02` → `exports/la02.mp4` (`--preview`는 별도 미리보기).

- LA 03 **경로를 잇고, 기여를 모은다** — 100초, 1080×1920, 30fps, 무음. 두 단계 경로의 곱과 합을 통해 A²와 행렬곱을 설명합니다.
- [3편 대본](episodes/la03_matrix_paths/narration.md) · [구성 및 수학 확인](episodes/la03_matrix_paths/brief.md)
- `python scripts/render.py la03` → `exports/la03.mp4` (`--preview`는 별도 미리보기).

## 화면 표기와 TTS 표기

영상의 화면 문구, 자막(SRT), narration.md에서는 숫자·영어·수식을 원래 표기 그대로 사용합니다(예: `0.8`, `A²`, `k`, `BA`). `영 점 팔`, `에이 제곱`, `케이` 같은 한글 발음 표기는 `tts_script.txt`에만 사용합니다. 자연스러운 한국어 서수 표현(첫 번째, 두 번째 등)은 유지합니다.

- LA 04 **반복하면 어떤 패턴이 남을까?** — 110초, 1080×1920, 30fps, 무음. 반복 계산의 크기와 비율을 비교하며 고유벡터·고유값을 예고합니다.
- [4편 대본](episodes/la04_repeated_patterns/narration.md) · [구성 및 수학 확인](episodes/la04_repeated_patterns/brief.md)
- `python scripts/render.py la04` → `exports/la04.mp4` (`--preview`는 별도 미리보기).

- LA 05 **같은 입력, 다른 패턴별 배율** — 99초, 1080×1920, 30fps, 무음. 섞인 두 고유패턴을 서로 다르게 조절하고 다시 합치는 과정을 보여줍니다.
- [5편 대본](episodes/la05_pattern_filter/narration.md) · [구성 및 수학 확인](episodes/la05_pattern_filter/brief.md)
- `python scripts/render.py la05` → `exports/la05.mp4` (`--preview`는 별도 미리보기).

- LA 06 **행렬이 지우는 차이** — 100초, 1080×1920, 30fps, 무음. 두 입력이 같은 출력으로 겹치는 과정에서 영공간을 설명합니다.
- [6편 대본](episodes/la06_nullspace/narration.md) · [구성 및 수학 확인](episodes/la06_nullspace/brief.md)
- `python scripts/render.py la06` → `exports/la06.mp4` (`--preview`는 별도 미리보기).

- LA 07 **벡터가 늘면 자유도도 늘까?** — 108초, 1080×1920, 30fps, 무음. 계수의 중복과 상쇄 관계를 통해 자유도·선형독립·표현의 유일성을 설명합니다.
- [7편 대본](episodes/la07_independence/narration.md) · [구성 및 수학 확인](episodes/la07_independence/brief.md)
- `python scripts/render.py la07` → `exports/la07.mp4` (`--preview`는 별도 미리보기).

- LA 08 **Rank: 실제로 남는 자유도** — 107초, 1080×1920, 30fps, 무음. 같은 2×2 행렬의 Rank 1·2를 출력 공간으로 비교합니다.
- [8편 대본](episodes/la08_rank/narration.md) · [구성 및 수학 확인](episodes/la08_rank/brief.md)
- `python scripts/render.py la08` → `exports/la08.mp4` (`--preview`는 별도 미리보기).

- LA 09 **방향과 조합으로 나누어 기록하기** — 112초, 1080×1920, 30fps, 무음. Rank 분해 A=BC로 독립적인 방향과 열의 조합을 분리합니다.
- [9편 대본](episodes/la09_rank_factorization/narration.md) · [구성 및 수학 확인](episodes/la09_rank_factorization/brief.md)
- `python scripts/render.py la09` → `exports/la09.mp4` (`--preview`는 별도 미리보기).

- LA 10 **SVD: 관계를 채널로 나누어 보기** — 109초, 1080×1920, 30fps, 무음. 반투명 채널 레이어로 입력 패턴·전달 강도·출력 패턴을 분리합니다.
- [10편 대본](episodes/la10_svd_channels/narration.md) · [구성 및 수학 확인](episodes/la10_svd_channels/brief.md)
- `python scripts/render.py la10` → `exports/la10.mp4`
