# GPU 연산과 최적화 07 제작 기준

## 제목

**Softmax는 왜 하나의 Kernel이 될 수 있을까? — Reduction + Elementwise Fusion**

## 길이와 형식

- 90초
- 1080×1920, 30fps, 세로형
- 영상 파일은 무음이며 `tts_script.txt`와 `captions.srt`를 별도로 제공한다.
- 화면 안에도 각 장면의 핵심 설명을 두 줄 자막으로 표시한다.

## 학습 목표

Softmax를 단일 수학 함수가 아니라 `Reduction → Elementwise → Reduction → Elementwise` 계산 구조로 이해한다. 각 논리 단계를 별도 Kernel로 끊으면 중간 Tensor의 global-memory materialization이 생기지만, 필요한 상태와 데이터를 GPU 내부에서 이어가면 하나의 Kernel로 fusion할 수 있음을 설명한다.

## 핵심 주장

1. 안정적인 Softmax는 `MAX → SUBTRACT → EXP → SUM → DIVIDE`로 분해된다.
2. `MAX`와 `SUM`은 여러 값을 각각 작은 상태 `m`, `ℓ`로 축약한다.
3. `m`이 정해진 뒤의 subtract/exp와 `ℓ`이 정해진 뒤의 divide는 원소별 계산이다.
4. Kernel fusion은 논리적 연산을 없애는 것이 아니라 단계 사이의 불필요한 중간 materialization을 피한다.
5. `m`, `ℓ`만으로 최종 출력을 만들 수 있는 것은 아니다. 각 원소 정보가 다시 필요하다.
6. 구현은 원소별 값을 register/shared memory 등에 유지하거나 입력을 다시 읽는 선택을 할 수 있다.

## 정확성 경계

- 모든 Softmax 구현이 언제나 단일 pass 또는 동일한 on-chip 보관 방식을 쓴다고 표현하지 않는다.
- 하나의 Kernel 안에서도 동기화, warp/block reduction, 여러 계산 phase 또는 입력 재읽기가 존재할 수 있다.
- `m`, `ℓ`는 reduction state지만 최종 벡터 출력은 원소별 데이터가 필요하다는 점을 명시한다.
- 텐서 크기와 하드웨어 자원에 따라 register/shared-memory 유지와 재읽기 사이의 선택이 달라질 수 있다.

## 장면별 타임라인

| 시간 | 화면 목표 |
|---|---|
| 00:00–00:07 | 입력 벡터와 하나의 Softmax 박스 |
| 00:07–00:15 | MAX, SUB, EXP, SUM, DIV로 분해 |
| 00:15–00:23 | 별도 Kernel 경계의 STORE/LOAD |
| 00:23–00:30 | MAX가 `m` 상태로 축약 |
| 00:30–00:37 | `xᵢ−m`, exp의 원소별 독립성 |
| 00:37–00:44 | SUM이 `ℓ` 상태로 축약 |
| 00:44–00:51 | 최종 출력에 원소별 정보가 다시 필요 |
| 00:51–00:59 | 하나의 Softmax Kernel 경계 |
| 00:59–01:07 | Thread와 warp reduction 흐름 |
| 01:07–01:15 | Epilogue, Reduction, Softmax 비교 |
| 01:15–01:23 | 유지해야 하는 데이터가 fusion 조건 |
| 01:23–01:30 | keep/compress/reread 선택과 다음 편 연결 |

