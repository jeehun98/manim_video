# FlashAttention 01 — Attention은 무엇을 저장하고 있을까?

| 시간 | 내레이션 | 화면 |
|---|---|---|
| 00:00–00:06 | Attention은 Query와 Key의 관계를 계산하고, 그 결과로 Value를 조합합니다. | `Q`, `K`, `V` 입력 카드 |
| 00:06–00:14 | 먼저 각 Query를 모든 Key와 비교해 하나의 점수 행렬 S를 만듭니다. | `S = QKᵀ`, 5×5 score가 셀 단위로 생성 |
| 00:14–00:20 | 입력 길이가 N이라면 이 행렬에는 N 곱하기 N, 즉 N²개의 값이 생깁니다. | 가로·세로 `N` brace, `N² values` |
| 00:20–00:27 | 각 행에 Softmax를 적용하면 점수는 합이 1인 Attention weight가 됩니다. | 한 행씩 선택한 뒤 `P`로 변환 |
| 00:27–00:34 | 이 가중치로 Value들을 섞으면 최종 Attention 출력 O가 만들어집니다. | `P × V = O` |
| 00:34–00:42 | 하지만 최종적으로 필요한 것은 O입니다. 그 O를 만들기까지 N² 크기의 Score S와 Attention P가 중간 결과로 생겼습니다. | `S`, `P`, `O` 데이터 카드. 앞의 두 카드 아래 `N²` |
| 00:42–00:52 | 표준적인 구현은 이런 중간 결과를 HBM에 쓰고, 다음 연산에서 다시 읽어 계산을 이어갑니다. | `QKᵀ → write S → softmax → write P → ×V` |
| 00:52–01:00 | 그렇다면 거대한 Attention 중간 행렬을 전부 저장하지 않고도 같은 출력 O를 만들 수 있을까요? | `S`, `P`는 흐려지고 `O`만 유지 |
| 01:00–01:04 | FlashAttention은 바로 이 문제에서 시작합니다. | `FlashAttention`, 작은 tile 하나 |

## 전체 내레이션

Attention은 Query와 Key의 관계를 계산하고, 그 결과로 Value를 조합합니다.

먼저 각 Query를 모든 Key와 비교해 하나의 점수 행렬 S를 만듭니다.

입력 길이가 N이라면 이 행렬에는 N 곱하기 N, 즉 N²개의 값이 생깁니다.

각 행에 Softmax를 적용하면 점수는 합이 1인 Attention weight가 됩니다.

이 가중치로 Value들을 섞으면 최종 Attention 출력 O가 만들어집니다.

하지만 최종적으로 필요한 것은 O입니다. 그 O를 만들기까지 N² 크기의 Score S와 Attention P가 중간 결과로 생겼습니다.

표준적인 구현은 이런 중간 결과를 HBM에 쓰고, 다음 연산에서 다시 읽어 계산을 이어갑니다.

그렇다면 거대한 Attention 중간 행렬을 전부 저장하지 않고도 같은 출력 O를 만들 수 있을까요?

FlashAttention은 바로 이 문제에서 시작합니다.

