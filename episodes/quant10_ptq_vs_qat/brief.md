# Quantization 시리즈 10편 제작 기준

- 이 편의 유일한 대비는 `학습 완료 후 quantize하는 PTQ vs 학습 중 quantization 효과를 경험하는 QAT`다.
- PTQ는 전체 학습을 처음부터 반복하지 않는 장점을 보여주되, calibration이나 짧은 보정 절차가 전혀 없다고 단정하지 않는다.
- PTQ 장면은 quantization error가 원래 FP 학습 이후에 유입되어 모델이 학습 중 사전 적응하지 못했다는 점을 강조한다.
- QAT 장면은 학습 가능한 FP master weight를 유지하면서 forward에 simulated/fake quantization 효과를 넣고 loss를 통해 FP weight를 업데이트하는 구조로 표현한다.
- QAT가 quantization error 자체를 없앤다고 표현하지 않는다. 오차가 존재하는 환경에서도 목적함수가 작아지도록 파라미터가 적응할 기회를 준다고 설명한다.
- 실제 weight 이동 예시는 개념적 시각화이며 weight가 반드시 grid point 위로 이동한다는 뜻이 아니다.
- Straight-Through Estimator, fake quantization 구현 세부, calibration 방식, GPTQ, AWQ, 특정 프레임워크는 제외한다.
- 다음 편 예고 없이 `Quantization 오차를 학습 중 경험했는가`라는 기준으로 독립적으로 마무리한다.
- 영상은 60초, 1080×1920, 30fps, 무음 마스터다.
