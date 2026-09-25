# Quantization 시리즈 8편 제작 기준

- 이 편의 유일한 구조는 `실수 행렬곱 → 정수 행렬곱 + scale 복원`이다.
- zero point를 생략한 단순한 대칭형 quantization 예시를 사용한다. 완전한 affine GEMM 전개는 이 편에서 다루지 않는다.
- 예시는 `s_w=s_x=0.02`로 고정한다.
- `Q_w=[[21,−40],[8,31]]`, `Q_x=[27,−14]ᵀ`이며 정수 GEMM 결과는 `[1127,−218]ᵀ`다.
- 결합 scale은 `s_ws_x=.0004`, 복원 결과는 `[.4508,−.0872]ᵀ`다.
- 원래 행렬의 정확한 결과는 `[.4536,−.0846]ᵀ`이므로 등호가 아니라 근사 기호로 비교한다.
- 근사 오차는 integer GEMM 자체가 아니라 W와 X를 quantize할 때 유입됐다는 점을 명확히 한다.
- 파이프라인은 `Q_w,Q_x → Integer GEMM → Accumulator → Scale → Ŷ`로 표현한다.
- accumulator는 다음 편의 질문으로만 제시하며 INT32가 필요한 이유는 설명하지 않는다.
- requantization, bias, per-channel scale, Tensor Core 내부 구현은 제외한다.
- 영상은 60초, 1080×1920, 30fps, 무음 마스터다.
