# Benign Overfitting — 노이즈까지 외웠는데 왜 일반화될까? | 신경망의 수학 2부 11

| 시간 | 내용 |
|---:|---|
| 00:00–00:08 | 고전적 overfitting 그림 |
| 00:08–00:19 | Train error 0, test error small의 역설 |
| 00:19–00:32 | `y_i = x_i^T w* + epsilon_i` |
| 00:32–00:41 | 여러 interpolating solution |
| 00:41–00:51 | 저차원 noise fitting의 왜곡 |
| 00:51–00:59 | 고차원의 수많은 여분 방향 |
| 00:59–01:08 | 하나의 큰 변화 vs 여러 작은 변화 |
| 01:08–01:17 | Data covariance가 중요한 이유 |
| 01:17–01:26 | Covariance spectrum의 head와 tail |
| 01:26–01:38 | Low-variance tail에 noise fitting 분산 |
| 01:38–01:49 | Train interpolation과 test prediction 분리 |
| 01:49–01:59 | 고차원만으로는 부족한 조건 |
| 01:59–02:08 | Solution selection의 중요성 |
| 02:08–02:19 | Minimum-norm interpolator |
| 02:19–02:30 | Gradient descent의 implicit bias |
| 02:30–02:40 | Double Descent와의 구분 |
| 02:40–02:54 | `Interpolation != Bad Generalization` |
