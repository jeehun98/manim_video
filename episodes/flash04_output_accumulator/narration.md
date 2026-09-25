# FlashAttention 04 — Attention 출력도 바로 누적할 수 있을까?

| 시간 | 내레이션 | 화면 |
|---|---|---|
| 00:00–00:07 | score 전체를 저장하지 않고도 현재 최댓값 m과 누적 지수합 ℓ을 블록마다 갱신할 수 있었습니다. | score block이 지나가고 `m`, `ℓ` 유지 |
| 00:07–00:14 | 하지만 Attention의 목적은 Softmax 가중치로 Value를 섞어 최종 출력 O를 만드는 것입니다. | `weights × V → O` |
| 00:14–00:23 | 첫 번째 Key block의 score를 계산할 때, 그 위치에 대응하는 Value block도 함께 가져옵니다. | `QᵢK₁ᵀ → scores₁`, `V₁` |
| 00:23–00:32 | 현재 score의 지수 가중치와 V₁을 곱해 지금까지의 Attention 출력을 만듭니다. | `m=3`, `ℓ=1.503`, `O=2.399` |
| 00:32–00:41 | 새 score에서 더 큰 값 5가 나타나면 m과 ℓ을 새로운 기준으로 갱신합니다. | `K₂,V₂`, `m:3→5`, `ℓ:1.503→1.621` |
| 00:41–00:51 | 이전 output이 가진 weight mass를 새 최댓값 기준으로 줄이고, 새 block의 Value 기여를 더해 다시 정규화합니다. | old O mass rescale + new V₂ mass → `O=5.910` |
| 00:51–01:00 | 같은 갱신을 반복하면 지나간 score와 Softmax weight를 남기지 않고 m, ℓ, O 세 상태만 유지할 수 있습니다. | K/V tile이 사라지고 `m=5`, `ℓ=2.014`, `O=5.741` 유지 |
| 01:00–01:08 | 모든 score와 Softmax weight를 먼저 만든 경우와 block-wise로 갱신한 마지막 출력 O는 같습니다. | Standard와 Block-wise 모두 `O=5.741` |
| 01:08–01:15 | Score S와 Attention P 전체를 HBM에 저장하지 않고도 tile과 작은 상태만으로 같은 O를 만들 수 있습니다. | S/P에 X, `tiles → m,ℓ,O → O` |
| 01:15–01:20 | 마지막에는 HBM 왕복과 on-chip tile 계산을 나란히 놓고 FlashAttention이 실제로 줄인 것을 정리합니다. | `HBM ↔ On-chip`, `IO ?` |

## 전체 내레이션

score 전체를 저장하지 않고도 현재 최댓값 m과 누적 지수합 ℓ을 블록마다 갱신할 수 있었습니다.

하지만 Attention의 목적은 Softmax 가중치로 Value를 섞어 최종 출력 O를 만드는 것입니다.

첫 번째 Key block의 score를 계산할 때, 그 위치에 대응하는 Value block도 함께 가져옵니다.

현재 score의 지수 가중치와 V₁을 곱해 지금까지의 Attention 출력을 만듭니다.

새 score에서 더 큰 값 5가 나타나면 m과 ℓ을 새로운 기준으로 갱신합니다.

이전 output이 가진 weight mass를 새 최댓값 기준으로 줄이고, 새 block의 Value 기여를 더해 다시 정규화합니다.

같은 갱신을 반복하면 지나간 score와 Softmax weight를 남기지 않고 m, ℓ, O 세 상태만 유지할 수 있습니다.

모든 score와 Softmax weight를 먼저 만든 경우와 block-wise로 갱신한 마지막 출력 O는 같습니다.

Score S와 Attention P 전체를 HBM에 저장하지 않고도 tile과 작은 상태만으로 같은 O를 만들 수 있습니다.

마지막에는 HBM 왕복과 on-chip tile 계산을 나란히 놓고 FlashAttention이 실제로 줄인 것을 정리합니다.

