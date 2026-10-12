# 신경망의 수학 2부 08 제작 기준

## 제목과 목표

**Spectral Bias — 신경망은 왜 낮은 주파수부터 학습할까?**

하나의 복잡한 정답이 통째로 개선된다는 일상적 학습상을 먼저 보여준 뒤, 같은 정답을 주파수 성분으로 분해해 성분별 학습 속도가 다를 수 있음을 발견하게 한다. 현상 소개에서 멈추지 않고 kernel learning dynamics의 고유방향과 고유값으로 속도 차이를 설명한다. 최종 메시지는 `신경망은 정답의 모든 구조를 동등하게 배우지 않는다`이며, `Representable ≠ Equally Learnable`을 그 수학적 귀결로 둔다.

## 정확성 기준

- Spectral Bias는 모든 신경망과 학습 설정에서 동일한 보편 순서가 아니라 자주 관찰되는 경향으로 표현한다.
- learning operator와 eigenvalue 설명은 특정 kernel 또는 선형화된 dynamics 관점으로 제한한다.
- `low frequency = large eigenvalue`를 보편 등식으로 표현하지 않는다. architecture, kernel, data 조건에 따른 spectral structure라고 명시한다.
- 높은 주파수를 늦게 배우는 것과 그 함수를 표현하지 못하는 것을 구분한다.
- 낮은 주파수를 signal, 높은 주파수를 noise와 동일시하지 않는다.
- Fourier Features는 입력 표현을 바꾸는 설계 사례로만 짧게 소개한다.

## 핵심 수식

`cᵢ(t) ≈ cᵢ(0)e^(−λᵢt)`

고유값 `λᵢ`가 클수록 해당 고유방향의 오차 계수 `cᵢ`가 빠르게 감소한다. Fourier 급수는 별도 중심 수식 없이 파동의 분해와 합성 애니메이션으로 설명한다.

## 시각 구성

- 시작부터 복합 target `sin x + 0.3 sin(10x)` 하나만 사용해, 정답 전체가 함께 다듬어진다는 통상적 직관을 먼저 만든다.
- 복합 target을 Low/Mid/High로 물리적으로 분리한 뒤 같은 step에서 성분별 error가 다르게 남는 모습을 보여준다.
- `Loss에는 low frequency를 먼저 배우라는 지시가 없다`는 장면을 넣어, 단순한 coarse-to-fine 설명이 아니라 학습 dynamics의 비중립성으로 전환한다.
- 01:12에 `왜 속도가 다른가?`를 독립 장면으로 제시한다.
- `정답을 분해: Function → Fourier`와 `학습을 분해: Dynamics → Eigenmodes`를 좌우 대칭으로 배치한다.
- `t=0 → t=1`에서 세 error mode의 bar가 λ에 따라 서로 다른 속도로 줄어드는 것을 직접 애니메이션한다.
- Fourier spectrum의 Low/Mid/High와 learning spectrum의 large/medium/small λ를 좌우에서 연결하고, 보편적 등식이 아님을 같은 화면에 명시한다.
- 큰 λ, 중간 λ, 작은 λ를 각각 빠른·중간·느린 error decay와 연결한다.
- high-frequency detail은 low-pass cat 선화와 선명한 선화를 비교해 경계·수염·작은 문자로 표현한다.
- 마지막에는 경로 길이 그림을 사용하지 않고 mode별 eigenvalue와 학습 속도의 spectrum으로 정리한다.
- 모든 장면 전환은 stage 단위로 처리해 이전 파동과 label이 남지 않게 한다.

## 썸네일 기준

- 01:15 프레임의 두 분해 비교 장면을 사용한다.
- `Function → Fourier`와 `Dynamics → Eigenmodes`가 한 화면에 함께 보이게 한다.

## 타임라인

| 구간 | 시간 | 목적 |
|---|---:|---|
| 1 | 00:00–00:06.4 | 하나의 복잡한 target과 질문 |
| 2 | 00:06.4–00:10.1 | 정답 전체가 함께 개선된다는 통상적 학습상 |
| 3 | 00:10.1–00:15.4 | 한 출력만으로는 성분별 속도를 알 수 없음 |
| 4 | 00:15.4–00:22.2 | 하나의 target을 Low/High로 분리 |
| 5 | 00:22.2–00:26.8 | Low/Mid/High Fourier 관점 |
| 6 | 00:26.8–00:35.5 | 같은 step, 다른 성분별 error |
| 7 | 00:35.5–00:42.7 | 발견 뒤 Spectral Bias 명명 |
| 8 | 00:42.7–00:50.5 | Loss에는 학습 순서가 없음 |
| 9 | 00:50.5–00:56.0 | 학습 dynamics는 중립적이지 않음 |
| 10 | 00:56.0–01:01.4 | 관찰과 설명의 분리 |
| 11 | 01:01.4–01:10.0 | learning spectrum 질문 |
| 12 | 01:10.0–01:17.2 | 학습 오차의 eigen-directions |
| 13 | 01:17.2–01:24.3 | eigenvalue와 mode별 학습 강도 |
| 14 | 01:24.3–01:29.9 | 지수적 error decay 수식 |
| 15 | 01:29.9–01:40.5 | frequency-eigenvalue 연결의 조건부 성격 |
| 16 | 01:40.5–01:52.4 | representability와 decay rate 분리 |
| 17 | 01:52.4–02:01.8 | Expressivity와 Learnability 분리 |
| 18 | 02:01.8–02:12.2 | Low=Signal, High=Noise 반박 |
| 19 | 02:12.2–02:21.5 | Fourier Features 사례 |
| 20 | 02:21.5–02:34.0 | learning spectrum으로 결론 |

총 154초. 2부 07의 평균 대본 밀도와 화면 전환 비율을 기준으로, 08의 문단별 글자 수에 따라 장면 시간을 처음부터 재분배한다. 애니메이션 최소 실행 시간만 보정하고 전체 길이는 유지한다. 1080×1920, 30fps, 무음 마스터. 미리보기는 360×640이다.
