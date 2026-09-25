# Quantization 09 — 왜 Weight보다 Activation이 더 까다로울까?

| 시간 | 내레이션 | 화면 |
|---|---|---|
| 00:00–00:07 | Weight와 activation은 둘 다 숫자 배열이지만 성격은 완전히 다릅니다. Weight는 멈춰 있고 activation은 입력마다 바뀝니다. | 고정 행렬과 계속 변하는 벡터의 분할 화면 |
| 00:07–00:15 | 학습이 끝난 weight는 inference 동안 거의 고정되므로 전체 분포와 범위를 모델 실행 전에 분석할 수 있습니다. | Weight 행렬, histogram, `−2.1~1.8` |
| 00:15–00:23 | 그래서 scale을 미리 정하고 INT8이나 INT4로 저장해 여러 입력에서 같은 quantized weight를 재사용할 수 있습니다. | Weight quantization 준비 파이프라인과 재사용 |
| 00:23–00:34 | Activation은 입력 데이터와 이전 layer의 결과에 따라 매번 새로 만들어집니다. 같은 layer에서도 범위가 `−1~1`, `−5~7`, `−0.3~12`로 달라질 수 있습니다. | 입력 A/B/C와 계속 바뀌는 histogram |
| 00:34–00:43 | 하나의 고정 scale을 좁게 잡으면 큰 activation이 잘리고, 넓게 잡으면 작은 activation이 사용하는 격자가 성겨집니다. | 좁은 범위의 clipping과 넓은 범위의 coarse grid |
| 00:43–00:50 | 따라서 weight는 미리 분석하고 scale을 정하기 상대적으로 쉽지만 activation은 실행 중 변하는 분포까지 고려해야 합니다. | Weight/Activation 비교 카드 |
| 00:50–00:56 | 이 때문에 큰 weight는 INT4로 줄이고 activation은 FP16으로 유지하는 weight-only quantization도 사용됩니다. | LLM layer의 `Weight INT4 / Activation FP16` |
| 00:56–01:00 | 그렇다면 activation scale은 미리 고정할까요, 실행 중 계산할까요? 다음에는 Static과 Dynamic Quantization을 비교합니다. | Static/Dynamic 선택 카드 |

## 전체 내레이션

Quantization할 때 weight와 activation은 겉보기에는 둘 다 숫자 배열입니다. 하지만 실제로는 둘의 성격이 완전히 다릅니다. Weight는 같은 값이 멈춰 있고 activation은 입력마다 계속 바뀝니다.

학습이 끝난 weight는 inference 동안 거의 고정됩니다. 따라서 전체 값의 분포와 최솟값, 최댓값을 모델을 실행하기 전부터 미리 분석할 수 있습니다.

그래서 weight는 적절한 scale을 미리 정하고 INT8이나 INT4 형태로 저장해둘 수 있습니다. 한 번 변환한 quantized weight는 여러 입력을 처리할 때 계속 재사용됩니다.

하지만 activation은 입력 데이터와 이전 layer의 결과에 따라 실행할 때마다 새로 만들어집니다. 같은 layer에서도 Input A는 마이너스 1부터 1, Input B는 마이너스 5부터 7, Input C는 마이너스 0.3부터 12처럼 범위와 분포가 달라질 수 있습니다.

Activation에 하나의 고정 scale을 사용하면 모든 입력에 잘 맞지 않을 수 있습니다. 범위를 좁게 잡으면 큰 activation이 표현 범위 밖에서 잘리고, 넓게 잡으면 작은 activation이 사용하는 격자가 성겨져 표현이 거칠어집니다.

그래서 weight quantization은 값을 미리 분석하고 scale을 정하기 상대적으로 쉽지만, activation quantization은 실행 중 계속 변하는 분포까지 고려해야 해서 더 까다롭습니다.

이 때문에 실제 LLM에서는 큰 weight matrix만 INT4로 줄이고 activation은 FP16으로 유지하는 weight-only quantization 방식도 사용됩니다.

그렇다면 activation의 scale은 실행 전에 미리 고정해야 할까요, 아니면 입력이 들어올 때마다 새로 계산해야 할까요? 다음 영상에서는 Static Quantization과 Dynamic Quantization을 비교하겠습니다.
