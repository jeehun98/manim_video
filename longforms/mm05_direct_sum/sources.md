# 수학 검증 자료

- Alman & Vassilevska Williams, *Limits on All Known (and Some Unknown) Approaches to Matrix Multiplication*, Theorem 3.1: https://people.csail.mit.edu/virgi/matmultlimits.pdf
- Schönhage, *Partial and Total Matrix Multiplication*: https://epubs.siam.org/doi/10.1137/0210032
- Christandl et al., *Border rank non-additivity for higher order tensors*: https://arxiv.org/abs/2007.05458

복소수 위 정사각 행렬곱 q개, 각 크기 m≥2, 직합 보더 랭크≤R, R>q이면 q m^ω≤R. 영상은 q=3 동일 크기 사례로 제한한다. 반복 구조는 직합의 텐서곱 분배 및 행렬곱 텐서의 결합으로 q^k개의 크기 m^k 행렬곱을 포함하고, 보더 랭크≤R^k이다. 이는 정리의 직관이지 증명 전체가 아니다.

직합의 랭크 비가법성은 일반 텐서에 관한 명제이며 여기의 세 행렬곱에 대한 엄격한 절약을 주장하지 않는다. 2차원 대각 블록은 삼차 텐서의 세 그룹 분리를 축약한 개념도이다.

- 정확한 랭크의 일반 비가법성: Shitov, *Counterexamples to Strassen’s direct sum conjecture*: https://arxiv.org/abs/1712.08660

## v2 수치 검증

D=세 개의 2×2 행렬곱 직합. D²에는 9개의4×4, D³에는27개의8×8 계산 관계가 있다. verify_math.py는 2차와3차의 전체 비영 계수 지지집합을 비교한다. 정확한 Strassen 분해 세 개로 R(D)≤21 및 보더 랭크≤21을 확보한다. 점근적 합 부등식에 대입하면3·2^ω≤21, ω≤log₂7≈2.807. 이는 기존 상한의 재현이며 이 직합에서r<21의 존재를 주장하지 않는다.
