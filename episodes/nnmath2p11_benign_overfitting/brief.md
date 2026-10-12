# 제작 기준 — Benign Overfitting

## 핵심 질문

`Training noise까지 정확히 interpolation했는데도 왜 prediction error가 작을 수 있는가?`

## 핵심 결론

- `Interpolation != Bad Generalization`.
- 단순히 parameter 수가 많은 것이 아니라 data covariance spectrum과 effective rank가 중요하다.
- 대표적인 엄밀한 결과는 고차원 linear regression의 minimum-norm interpolator를 다룬다.
- noise fitting이 prediction에 영향이 작은 많은 방향에 분산될 수 있다는 기하학적 직관을 사용한다.
- 아무 interpolating solution이나 좋은 것이 아니며 solution selection과 implicit bias가 중요하다.

## 정확성 제약

- `고차원이면 자동으로 benign` 또는 `noise는 항상 low-variance 방향에 저장된다`로 단정하지 않는다.
- covariance eigenvalue tail, sample size, signal, effective rank에 대한 조건부 현상으로 표현한다.
- 신경망 일반에서 동일 mechanism이 증명되었다고 말하지 않고, deep learning이 던진 현상을 linear regression에서 분석한 결과로 범위를 분명히 한다.
- Double Descent와 연결되지만 개념을 동일시하지 않는다.

## 시각 언어

- 세로 9:16, 어두운 배경, 기존 2부의 cyan/purple/yellow/mint/pink palette.
- 2D 왜곡과 고차원 분산을 대비하고, 중반 이후에는 동일 covariance spectrum을 반복 사용한다.
- 엄밀한 effective-rank 식을 나열하기보다 head/tail 구조와 minimum-norm solution 기하를 핵심 시각화로 사용한다.

## 근거

- Bartlett, Long, Lugosi, Tsigler, *Benign Overfitting in Linear Regression*, PNAS 2020, DOI `10.1073/pnas.1907378117`.
- 논문의 핵심 범위: minimum-norm interpolating prediction rule, covariance의 두 effective-rank 개념, prediction에 중요하지 않은 parameter-space 방향의 수가 sample 수보다 훨씬 많아야 함.
