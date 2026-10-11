# 검증 자료

- Ottaviani & Reichenbach, Tensor Rank and Complexity: https://arxiv.org/abs/2004.01492 — rank/border rank and matrix multiplication complexity.
- Christandl et al., Partial Degeneration of Tensors: https://doi.org/10.1137/23M1554898 — degeneration and W tensor constructions.
- Bini, Relations between exact and approximate bilinear algorithms. Applications (1980): https://doi.org/10.1007/BF02575865 — exact/approximate algorithms.

## 이 영상의 직접 검증
verify_math.py checks every W coefficient, the symbolic expansion, interpolation identity, and numeric two-output example. Rank ≥3 follows because the 2-dimensional slice space span([[0,1],[1,0]],[[1,0],[0,0]]) contains only one rank-one direction (det=-α²); a rank-two tensor with full third flattening rank would require two independent rank-one slices. Border rank ≥2 follows from flattening rank 2 (closed minors). These lower bounds are separate from displaying the three-term sum and two-term limit.

P(ε)^⊗k has degree ≤2k and rank ≤2^k at each nonzero evaluation point. Interpolate at 2k+1 distinct nonzero complex points to recover its constant coefficient W^⊗k, giving R(W^⊗k)≤(2k+1)2^k. This is an upper bound, not a claim that ordinary rank powers equal 3^k. No improvement to matrix multiplication's numerical exponent is asserted in this video.

## v2의 기하학 투영
S(t)=(u+tv)^⊗3의 계수 211과221을 선택하면 (t,t²), S(0)은 (0,0)이다. 정규화한 차이 P(t)의 같은 성분은 (1,t)로서 W의 (1,0)에 접근한다. 이는 실제 두 성분의 투영이지만 전체 공간의 거리나 랭크를 2차원 그림만으로 판정하지 않는다. 거듭제곱 상한은 검증 참고 자료에 유지하되 v2 본편에서는 설명하지 않는다.

## v3 집합 개념도
복소수 위 rank≤r 집합 R_r와 폐포를 구분한다. 그림의 원·원판은 실제 대수적 집합의 형상을 나타내지 않는다. target T는 검증된 W와 동형인 특정 예제를 가리킨다. rank≤1 집합은 닫혀 있지만 rank≤2인 2×2×2 텐서 집합은 일반적으로 닫혀 있지 않다. 행렬 rank≤r 집합은 (r+1)차 소행렬식들의 영점집합이므로 닫혀 있다. 개별 항의 발산 가능성은 모든 접근 경로가 반드시 발산한다는 주장이 아니다.

## v4 폐포 설명
닫힌 집합의 정의와 동치인 관점: 집합의 폐포는 집합을 포함하는 가장 작은 닫힌 집합이며, 원래 포함된 점과 빠져 있던 극한점을 모두 포함한다. 유클리드 위상에서 모든 ε>0에 대해 목표점의 ε-근방이 원래 집합과 만나는 것이 폐포 소속의 기준이다. 열린 원판 D의 폐포는 닫힌 원판이다. 텐서 집합을 원판과 동일시하지 않는다.
