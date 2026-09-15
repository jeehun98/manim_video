# Activation Function Series

Manim 세로형 수학 Shorts. 1080 × 1920, 30fps, 어두운 배경과 원소별 파스텔 색상.
영상은 음성·음악 없는 마스터이며 LaTeX는 필요 없습니다.

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
| legacy | 초기 프로토타입 | 10초 | `archive/relu_short.py` | `exports/legacy.mp4` |

## 실행

```powershell
python -m pip install -r requirements.txt
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
