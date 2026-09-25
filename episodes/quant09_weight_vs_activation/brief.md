# Quantization 시리즈 9편 제작 기준

- 이 편의 유일한 대비는 `고정된 weight vs 입력에 따라 변하는 activation`이다.
- Weight는 학습 완료 후 inference 동안 거의 고정된다는 전제에서 offline으로 전체 분포와 범위를 분석할 수 있음을 보여준다.
- Activation은 입력과 이전 layer 출력에 의존하므로 같은 layer에서도 실행마다 분포와 범위가 달라질 수 있음을 애니메이션으로 보여준다.
- 고정 activation scale의 어려움은 두 가지로 한정한다: 범위를 좁게 잡았을 때 clipping, 넓게 잡았을 때 coarse resolution.
- Weight-only 예시는 `Weight INT4 / Activation FP16`으로 표현한다. 실제 kernel의 dequantization이나 혼합 precision 계산 경로는 다루지 않는다.
- Weight quantization이 항상 무손실이거나 쉽다는 뜻이 아니라, scale을 사전에 정하고 재사용하기가 상대적으로 쉽다는 의미로 제한한다.
- SmoothQuant, activation outlier의 원인, calibration dataset, AWQ, GPTQ, KV cache quantization은 제외한다.
- 마지막에는 activation scale을 미리 고정하는 Static과 실행 중 계산하는 Dynamic의 질문만 제시한다.
- 영상은 60초, 1080×1920, 30fps, 무음 마스터다.
