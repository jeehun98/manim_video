# FlashAttention 05 — FlashAttention은 무엇을 바꾼 걸까?

| 시간 | 내레이션 | 화면 |
|---|---|---|
| 00:00–00:07 | Standard Attention과 FlashAttention은 모두 같은 Query, Key, Value를 입력으로 받습니다. | 좌우에 동일한 Q/K/V |
| 00:07–00:15 | 먼저 전체 Score S를 만들고, Softmax를 적용해 전체 Attention weight P를 계산합니다. | 왼쪽 `QKᵀ→S→softmax→P→PV` |
| 00:15–00:23 | S와 P는 큰 중간 결과로 materialize되고, HBM에 기록됐다가 다음 연산을 위해 다시 읽힙니다. | 왼쪽 S/P HBM WRITE/READ |
| 00:23–00:31 | 같은 Q, K, V를 작은 블록으로 나누고 필요한 tile만 on-chip memory로 가져옵니다. | 오른쪽 Q/K/V tile 이동 |
| 00:31–00:39 | local score를 계산하고 현재 최댓값 m, 지수합 ℓ, Attention output O를 다음 상태로 갱신합니다. | `local score → m,ℓ,O` |
| 00:39–00:47 | 현재 tile의 score와 weight는 상태를 갱신한 뒤 다음 tile로 넘어가기 전에 제거할 수 있습니다. | `create→use→discard`, state 유지 |
| 00:47–00:55 | 왼쪽은 전체 S와 P를 HBM에 남기지만, 오른쪽은 지나간 tile 대신 작은 m, ℓ, O 상태만 유지합니다. | 큰 S/P와 작은 state 비교 |
| 00:55–01:03 | 저장 방식과 계산 순서는 다르지만 두 경로가 만드는 Attention output은 정확히 같습니다. | `O_standard=O_flash` |
| 01:03–01:11 | FlashAttention의 핵심은 답을 바꾸는 것이 아니라 HBM과 on-chip 사이의 데이터 이동을 줄이는 것입니다. | `same math`, `HBM IO↓` |
| 01:11–01:18 | 수식이 같아도 메모리 계층을 고려해 계산 순서와 저장 방식을 바꾸면 실제 실행 비용은 달라질 수 있습니다. | equation→algorithm→memory hierarchy |
| 01:18–01:24 | 같은 답을 계산해도, 계산하는 방법은 같지 않습니다. | 서로 다른 경로가 동일한 O로 합류 |

## 전체 내레이션

Standard Attention과 FlashAttention은 모두 같은 Query, Key, Value를 입력으로 받습니다.

Standard Attention은 먼저 전체 Score S를 만들고, Softmax를 적용해 전체 Attention weight P를 계산합니다.

S와 P는 큰 중간 결과로 materialize되고, HBM에 기록됐다가 다음 연산을 위해 다시 읽힙니다.

FlashAttention은 같은 Q, K, V를 작은 블록으로 나누고 필요한 tile만 on-chip memory로 가져옵니다.

local score를 계산하고 현재 최댓값 m, 지수합 ℓ, Attention output O를 다음 상태로 갱신합니다.

현재 tile의 score와 weight는 상태를 갱신한 뒤 다음 tile로 넘어가기 전에 제거할 수 있습니다.

왼쪽은 전체 S와 P를 HBM에 남기지만, 오른쪽은 지나간 tile 대신 작은 m, ℓ, O 상태만 유지합니다.

저장 방식과 계산 순서는 다르지만 두 경로가 만드는 Attention output은 정확히 같습니다.

FlashAttention의 핵심은 답을 바꾸는 것이 아니라 HBM과 on-chip 사이의 데이터 이동을 줄이는 것입니다.

수식이 같아도 하드웨어의 메모리 계층을 고려해 계산 순서와 저장 방식을 바꾸면 실제 실행 비용은 달라질 수 있습니다.

같은 답을 계산해도, 계산하는 방법은 같지 않습니다.

