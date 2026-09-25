# Quantization 10 — PTQ와 QAT는 무엇이 다를까?

| 시간 | 내레이션 | 화면 |
|---|---|---|
| 00:00–00:08 | 같은 Quantization도 언제 적용하느냐에 따라 달라집니다. 학습이 끝난 뒤 줄이는 PTQ와 학습 중부터 오차를 고려하는 QAT가 있습니다. | 학습 완료 모델에서 PTQ/QAT 두 갈래 분기 |
| 00:08–00:17 | PTQ는 이미 학습된 FP 모델을 나중에 quantized 모델로 바꿉니다. 전체 학습을 처음부터 다시 하지 않아도 된다는 것이 장점입니다. | `Trained FP Model → Quantize → INT8/INT4` |
| 00:17–00:27 | 하지만 값을 격자에 맞추며 생긴 Quantization Error는 원래 학습에서 고려되지 않았습니다. | 원래 점이 격자로 이동하고 원위치는 ghost로 남음 |
| 00:27–00:39 | QAT는 학습 중 fake quantization을 forward에 넣습니다. 그 오차를 포함한 loss로 학습 가능한 FP weight를 업데이트합니다. | FP weight, fake quant, forward, loss, backward, update loop |
| 00:39–00:49 | 반복 학습을 통해 오차를 없애는 것이 아니라, 그 오차가 있어도 loss가 작아지도록 FP weight 위치를 조정합니다. | 초기 weight와 QAT 후 weight의 grid 적응 비교 |
| 00:49–00:58 | PTQ는 적용이 빠르지만 사전 적응이 없고, QAT는 추가 학습이 필요한 대신 Quantization 환경에 적응할 기회를 줍니다. | PTQ/QAT 비교 카드와 핵심 질문 |
| 00:58–01:00 | PTQ는 나중에 줄이고, QAT는 Quantization 오차와 함께 학습합니다. | 예고 없는 독립형 결론 |

## 전체 내레이션

같은 Quantization이라도 언제 적용하느냐에 따라 두 가지 방식으로 나눌 수 있습니다. 학습이 끝난 뒤 줄이는 PTQ와 학습할 때부터 Quantization 오차를 고려하는 QAT입니다.

PTQ, Post-Training Quantization은 이미 학습이 끝난 FP 모델을 나중에 INT8이나 INT4 모델로 바꾸는 방식입니다. 전체 학습을 처음부터 다시 하지 않아도 된다는 것이 큰 장점입니다.

하지만 Quantization을 적용하면 원래 weight와 activation이 가장 가까운 격자로 이동하면서 작은 오차가 생깁니다. 문제는 모델이 원래 학습 과정에서는 이 Quantization Error를 고려하지 않았다는 점입니다.

QAT, Quantization-Aware Training은 학습 루프 안에 Quantization 효과를 넣습니다. 학습 가능한 FP weight를 fake quantization해 forward에서 오차를 경험하고, 그 결과의 loss를 이용해 FP weight를 업데이트합니다.

이 과정을 반복하면 모델은 Quantization Error를 완전히 없애는 것이 아니라, 그 오차가 존재하는 상태에서도 loss가 작아지도록 weight의 위치를 조금씩 조정할 수 있습니다.

정리하면 PTQ는 완성된 모델에 빠르게 적용할 수 있지만 Quantization Error에 사전 적응하지 않습니다. QAT는 추가 학습이 필요하지만 모델이 Quantization 환경을 학습 중 경험하고 그 오차에 적응할 기회를 줍니다.

둘의 가장 큰 차이는 Quantization 오차를 학습 과정에서 경험했는가입니다. PTQ는 학습이 끝난 뒤 줄이고, QAT는 Quantization 오차와 함께 학습합니다.
