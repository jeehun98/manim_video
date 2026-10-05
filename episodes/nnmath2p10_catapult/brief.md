# 신경망의 수학 2부 10 제작 기준

## 제목과 목표

**Catapult Mechanism — Loss가 폭발했는데 왜 다시 학습될까?**

초기에는 너무 큰 Learning Rate 때문에 Loss가 급격히 상승하지만, 큰 parameter update와 함께 NTK spectrum이 변하고 top eigenvalue가 감소하면서 같은 Learning Rate가 다시 감당 가능한 값이 될 수 있다는 직관을 설명한다.

## 정확성 기준

- Catapult를 모든 큰 Learning Rate에서 발생하는 보편 현상으로 표현하지 않는다.
- 초기 연구가 다룬 large-LR phase와 특정 모델·손실·optimizer 조건에서의 관찰이라는 뉘앙스를 유지한다.
- `critical LR ∝ 1/lambda_max(K)`는 개념적인 안정성 관계로 사용한다.
- loss spike가 top NTK eigenspace에 집중된다는 내용은 후속 관찰 연구의 결과로 표현한다.
- NTK top eigenvalue는 Catapult 동안 의미 있게 진화하며, 대표적인 관찰에서 감소한다.
- Edge of Stability와 Catapult를 같은 현상으로 합치지 않는다.

## 핵심 시각화

- Loss spike 후 recovery하는 곡선을 전반과 결론에서 반복 사용한다.
- current Learning Rate 막대는 고정하고 critical Learning Rate 막대만 길어진다.
- Loss 상승 곡선과 `lambda_max(K)` 하강 곡선을 동시에 보여준다.
- Lazy `K_t ≈ K_0`와 Catapult `K_t ≠ K_0`를 좌우 비교한다.
- Small LR / Catapult regime / Too Large의 세 결과를 분리한다.

총 175초, 1080×1920, 30fps, 무음 마스터.

## 근거 논문

- Lewkowycz et al., *The large learning rate phase of deep learning: the catapult mechanism*, arXiv:2003.02218.
- Meltzer et al., *Catapult Dynamics and Phase Transitions in Quadratic Nets*, arXiv:2301.07737.
- Zhu et al., *Catapults in SGD: spikes in the training loss and their impact on generalization through feature learning*, arXiv:2306.04815.
