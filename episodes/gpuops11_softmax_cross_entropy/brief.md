# GPU 연산과 최적화 11 제작 기준

## 제목과 형식

**Softmax와 Cross Entropy는 한 번의 GPU Kernel로 계산된다**

- 제목은 시선을 끄는 문장으로 사용한다. 본문과 화면에는 **구현·입력 크기·필요한 출력에 따라 하나의 fused kernel 또는 결합된 연산으로 처리할 수 있다**고 명시한다.
- 100초, 세로 1080×1920, 30fps, 무음. TTS 원고와 SRT는 별도 제공.
- 09화의 데이터 이동, 10화의 두 Reduction을 회수한다.

## 학습 목표

정답 클래스 하나에 대한 Cross Entropy loss가 필요할 때 전체 Softmax 확률 Tensor를 중간 출력으로 만들지 않고 logits에서 직접 loss를 계산할 수 있음을 이해한다. 중간 결과 materialization 제거와 안정적인 log-sum-exp 계산을 구분한다.

## 수학 및 정확성 경계

1. 단일 정답 클래스 `y`, 유한하고 비어 있지 않은 logits 벡터 `z`의 한 샘플에 대해 `L = −log p_y = −z_y + log Σⱼ exp(zⱼ)`이다. `m = maxⱼ zⱼ`를 쓰면 `L = −(z_y−m) + log Σⱼ exp(zⱼ−m)`이다.
2. 예시 logits `[2.1, 0.7, −1.2, 3.0]`의 확률은 약 `[0.267, 0.066, 0.010, 0.657]`이며 마지막 클래스의 loss는 약 `0.420`이다. 확률은 반올림값이다.
3. `exp(1000)`은 일반적인 float에서 overflow 위험이 있다. 최대값을 뺀 log-sum-exp는 이 예에서 큰 양의 지수 인수를 피한다. 모든 입력·dtype에 대해 무오류를 보장한다는 주장은 하지 않는다.
4. 전체 확률 벡터가 다른 소비자에게도 필요하면 생략할 수 없다. Label smoothing, soft targets, class weights, backward 저장 상태, 배치 reduction 등은 추가 계산이나 저장을 요구할 수 있다.
5. 수학적 결합은 단일 물리적 GPU kernel launch를 보장하지 않는다. 실제 실행은 구현과 크기, 하드웨어 자원에 따라 단일 kernel 또는 다단계 결합 연산일 수 있다.
6. 10화의 MAX와 SUM Reduction은 여전히 필요하다. 없애는 것은 최종 loss에 불필요한 전체 normalized probability Tensor의 materialization이다.

## 장면별 타임라인

| 종료 | 화면 목표 |
|---|---|
| 10초 | Logits → Softmax → Cross Entropy, 실제 수치 |
| 19초 | 교과서의 두 식과 계산 그래프 |
| 28초 | 전체 p 중 정답 클래스 하나만 사용 |
| 40초 | 대수적 결합과 안정적인 log-sum-exp |
| 50초 | 별도 kernel의 Write p / Read p |
| 60초 | 조건부 fused loss 실행 |
| 69초 | 전편 Softmax 흐름에서 normalize 전체 단계 제거 |
| 78초 | 큰 logits와 안정성 |
| 88초 | 수식 경계와 실행 경계 비교 |
| 100초 | 최종 요약, 단일 kernel 비보장 조건 |

## 싱크 기준

내레이션 길이에 따라 9~12초 구간을 배정했다. 장면 전환 애니메이션은 각 구간 초반 약 1초이며, 이후 화면을 발화 종료 시점까지 유지한다. 실제 TTS 음원의 속도에 맞춰 최종 싱크를 미세 조정할 수 있다.

## 참고 자료

- PyTorch `CrossEntropyLoss`: https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html
- PyTorch `log_softmax` 수치 안정성: https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.log_softmax.html
- NVIDIA cuDNN Softmax 그래프: https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-895/pdf/cuDNN-Developer-Guide.pdf
