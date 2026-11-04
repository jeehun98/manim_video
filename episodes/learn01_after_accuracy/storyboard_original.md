# 영상화 콘티 — 정답을 모두 맞힌 신경망은 그다음 무엇을 배울까?

총 141초 · 2분 21초 · 16:9 기준 · 과학·수학 모션그래픽

이번 영상은 동일한 신경망이 정확도 100% 이후에도 서로 다른 방향으로 변화할 수 있다는 것을 시각적으로 증명하는 데 집중하자.

첫 번째 움직임에서는 결정경계가 고정된 채 로짓의 크기와 확신도만 변화하고, 두 번째 움직임에서는 결정경계가 움직이지만 훈련 정확도는 유지된다. 두 장면을 같은 좌표계로 보여줘야 차이가 명확해져.

## 전체 시각 디자인

[Classification algorithms: Definition and main models](https://images.openai.com/static-rsc-4/e38t3eDz6ax4Ckdbvoud3Z_TNDbMqJVQys2ET6aOmCyDf3ldA4w_kLs2GP9h7pNyxvfsRoA3qjcrMD5K04eTlE4H5UtmSWQdhF6iqIhj3pmjT9w-DKRpBLNE2y75-5tMTZKYY24gexTG177TwZtVUITF2XorDj0M3DeuBNyqZ9w?purpose=inline)

A. 분류 공간

진한 배경, 청색·청록색 데이터, 주황색 결정경계

[Mathematics Visualizations for Machine Learning | Apatero](https://images.openai.com/static-rsc-4/0AWPuqYscnQA0DMmm25yrU7eIvcUin8o0hlj73pRLfz9itUNUnd73JGsp5u5FzROjKfRSvAWu0wF13sSCOD6c_4jbZLYUBZZ4hpPX5WsaJpqlB7oCwEmdw8YA_Ibftq3DK3SHSFrH9loudZYcpETG6zPjtMlSjDhsMny391s1XU?purpose=inline)

B. 최적화 공간

후반 논문 설명에서 기울기와 파라미터 변화를 표현

색상과 시각적 의미를 영상 전체에서 고정하자.

| 요소    | 색상        | 의미           |
| ----- | --------- | ------------ |
| 파란 점  | `#4DA9FF` | 클래스 A        |
| 청록 점  | `#27D3AF` | 클래스 B        |
| 주황색 선 | `#FFB454` | 결정경계         |
| 보라색   | `#A78BFA` | 로짓·확신도 변화    |
| 녹색    | `#58D68D` | 정확도 100%     |
| 회색    | `#9CA3AF` | 참고 데이터·보조 정보 |

그래프와 수식은 실제 모션그래픽으로 제작하고, AI 영상 생성은 추상적인 도입·전환 장면에만 제한적으로 사용하는 구성이 좋겠어.

## 1막 — 정확도 100%, 그러나 학습은 계속된다

00:00–00:13 · 시청자의 기존 직관을 뒤집는 도입

[Deep Learning - Overfitting](https://images.openai.com/static-rsc-4/CWd3vT861Sp_QVi23zFcPBkcXjMjhXpSEpX5LrTz9B5vjWyegN3QHt1Scf3TXzxnJ6ttVRma0nT99Spcr0JnzjhC-2maiU5nPjb3qUNkSvAHqVKwiG9T0dEwTVMLkLOd6kLFIMRcCLYzMNkN5llREhN6PkIpnWNjAjNdDUXzHMQ?purpose=inline)

컷 01 | 00:00–00:04

“신경망이 훈련 데이터의 정답을 모두 맞혔습니다. 훈련 정확도는 100퍼센트입니다.”

화면 중앙에 훈련 정확도 그래프가 나타난다. 학습 스텝이 증가하면서 곡선이 빠르게 상승해 100%에 도달한다.

곡선이 상단에 고정되고 `TRAIN ACCURACY 100%`가 크게 표시된다.

[Training Dashboard: DataRobot docs](https://images.openai.com/static-rsc-4/nT4kcwHdAs3hJ-53H04SxUlQ2H-hSr6dUZQvAE43KeL9-U0A_8Teyr0a5oxJT83MS2P4cZC0CebxTcqN0eRIjefiMVlFYZtsEQyS3jXmtUCDqNKqnWRilzcto4gMlMnmZCZSYvyyjTgjqOUEYI1vyLLIjDQu1SPdnBWaVZDPg_s?purpose=inline)

컷 02 | 00:04–00:09

“그런데 학습은 아직 끝나지 않았습니다. 손실을 줄일 수 있는 방향이 남아 있기 때문입니다.”

정확도 그래프 아래에 Loss 그래프를 추가한다.

Accuracy는 100%에 고정되지만 Loss는 계속 감소한다. 학습 스텝을 표시하는 세로 커서가 오른쪽으로 움직인다.

자막: Accuracy = 100% / Loss ↓

[TheRouter 弃用 /v1/anthropic/\* 路径：2026 年 9 月 3 日前迁移到 /v1/messages — TheRouter.ai | TheRouter.ai](https://images.openai.com/static-rsc-4/mbLqXPFKDtJmVO2bnf-RYNHPwxCOdxPQjlqQp70Oa2MChirszRqS4oFELBLeNZI2bjZyRbeZRXpx7YlaJHJrwtsk3dIq47olsaWFIonr1lB3ZbLKkKzB9yOEDsOyzVW-BSn2h2Z3fDYsQOH426cLQWDLFyivMJ_BVMYWLlIyHNE?purpose=inline)

컷 03 | 00:09–00:13

“그렇다면 정답을 모두 맞힌 신경망은 그다음 무엇을 배우는 걸까요?”

정확도 그래프가 축소되고 하나의 신경망 파라미터 점으로 변환된다.

점에서 두 개의 궤적이 갈라진다. 하나는 보라색, 하나는 주황색. 아직 의미는 설명하지 않는다.

화면 문구: What changes after 100% accuracy?

## 2막 — 실험 공간을 만든다

00:13–00:23 · 이후 두 실험에서 재사용할 기준 좌표계

[Logistic regression: A deep learning approach.](https://images.openai.com/static-rsc-4/braJxuCE8VPzAiGlBu2qlLeerZrc--GBih57ri9YkEQvlPJXPsK3EWwb49hoD19xWmnnnqW6zfrrAjFfLpwJSAp-INIiipLa0e8xdYyApyM1gqklDq-KnLCdgS2ptGUBYrrL2bFnQEqesS6GzcVgCCCZfSmc1iIS7pEQpZeoAMU?purpose=inline)

컷 04 | 00:13–00:16

“두 종류의 점을 구분하는 분류기를 생각해 보겠습니다.”

검은 화면에 X, Y축이 그려진다. 왼쪽에 파란 점 5개, 오른쪽에 청록색 점 5개가 차례로 나타난다.

점들은 완벽한 직선 형태로 배열하지 않고 약간 불규칙하게 배치한다.

[8  Classification – Intelligence Artificielle](https://images.openai.com/static-rsc-4/yLtliKaNSKjU6YjXfVABHErDMXpc1NVhoSh3vzwTXf84XphFwT3_ZO-rigUV1-4MAsJJms0NJFNcyRRkM-Id_o9fhBWQR5eqfWQk5-fvDf3gxiuA49jE02UGL4LIcFiqNd3lFnWm7kHwBko1d6NHlkfbf6YDcx-RJ0AmGuWmo18?purpose=inline)

컷 05 | 00:16–00:23

“파란 점과 초록 점 사이에 결정경계를 그었습니다. 모든 점이 올바른 쪽에 있으니 훈련 정확도는 100퍼센트입니다.”

두 클래스 사이에 주황색 결정경계가 나타난다.

경계 양쪽에 매우 옅은 청색·청록색 영역을 표시하고, 모든 점에 작은 체크 마크가 순서대로 등장한다.

우측 상단에 `Training Accuracy: 100%`를 고정한다.

이 점들의 좌표와 카메라는 80초까지 유지한다.

## 3막 — 첫 번째 움직임: 정답을 더욱 확신한다

00:23–00:50 · 핵심 시각 실험 A

[Logistic Regression - Practical NLP](https://images.openai.com/static-rsc-4/sRct9ZBlB733GSRhkYJ0zUfMyfGdayWp0rpE6cHtqI9N9ixjAOA5shvAgfmz8jnYbl_K8QMipaNUYTh56zheiH3_g7-HgrNyPKtJTYFR7ZPgDLJofqb8h9LEaRQ65AnjFkpAKahsrBHiE38FM8EVCmTjLSg9bN9OKRzjmNymY4M?purpose=inline)

컷 06 | 00:23–00:30

“이제 첫 번째 변화를 살펴보겠습니다. 분류기가 출력한 점수를 로짓이라고 합니다. 로짓의 부호로 두 클래스를 구분한다고 해보죠.”

오른쪽의 청록색 점 하나를 확대하고 점 옆에 `z = +2`를 표시한다.

왼쪽 파란 점에도 `z = -2`를 표시한다.

화면 아래에 `z > 0 → B`, `z < 0 → A`를 표시한다.

주황색 결정경계 위에는 `z = 0`이 나타난다.

[Neon numbers from 1 to 10 on a black background. Glowing 1,2,3,4,5,6,7,8,9,10 bright purple abstract banner. 3D render](https://images.openai.com/static-rsc-4/wpD8w0L0V_tcEAY_fEwP1DmVWefTR0Bro1pRryfVQqBavvmHhA825Y3d_FqbUyc7niQqfg0bvd_jXYsLhd8Strn0cgQ-mu__lkiX_xJWOjXLJ6aWDYzHoaUJnLBuYDmspvNrM_myJ6gdTUxN7jgBLn_Lw1JN0F7yhgNBLyZiw2uTT6io7jprO90rMIV5OG83?purpose=inline)

컷 07 | 00:30–00:37

“어떤 입력의 로짓이 2였다면, 이를 4나 8로 키워보겠습니다. 음수인 로짓도 같은 비율로 키웁니다.”

점의 위치를 전혀 움직이지 않는다.

오른쪽 점의 숫자만 `+2 → +4 → +8`로 변화한다. 왼쪽 점은 `−2 → −4 → −8`로 변화한다.

화면 상단에는 `z → kz (k > 1)`을 표시한다.

시각적으로는 숫자와 보라색 발광만 증가하고 데이터 위치는 고정한다.

[Plotting the decision boundary of a logistic regression model](https://images.openai.com/static-rsc-4/gZBvn2zWkIpg55qzB2xO_0aJxMqp9gnmlkykp3RMw8bYX1WJ_oWuA4Arz_WEHeVMpUzG_xT6yn9sLmRJMed7adzE8oE8ykHodCXhmI-VjTYTqHQMZB2l9F4LU4oGEjr6uR5NYnECGuoK1USgw-tj4Ccr36nf57NleYGTUVX7Zug?purpose=inline)

컷 08 | 00:37–00:40

“예측 결과는 달라지지 않습니다. 결정경계도 그대로입니다.”

경계선에 잠시 흰색 테두리를 둘러 고정 상태를 강조한다.

`Decision Boundary: Unchanged`

데이터 점과 결정경계 모두 움직이지 않았음을 보여주기 위해 첫 프레임과 마지막 프레임을 빠르게 겹쳐 보여준다.

[The Softmax Function Explained Intuitively for Beginners](https://images.openai.com/static-rsc-4/54e5RqqgMmcmdiDVH_8NF0CDo4qi0ebwGUbrzEkQc0HsxhfHCcv8n_Gahyw2LQgvf4YOniO8bgH_ZOZnvj-jjlW4XrIPapyKGDyB19HZWjEIxiu5UPD41dYUTALzPB_reWe8BlIg2IbwDzcrKtCCUolLZjKxa5YD6sP0LuuIL2c?purpose=inline)

컷 09 | 00:40–00:46

“하지만 소프트맥스가 정답에 부여하는 확률은 높아집니다. 그리고 크로스 엔트로피 손실은 감소합니다.”

기존 그래프 오른쪽에 수치 패널을 등장시킨다.

이진 분류에서 두 클래스의 로짓을 \\([z,0]\\)으로 둔 예시를 사용한다.

z = 2 → 4 → 8

정답 확률: `88.1% → 98.2% → 99.97%`

CE Loss: `0.127 → 0.018 → 0.00034`

위쪽 확률 막대는 늘어나고 아래쪽 Loss 막대는 줄어든다.

[Visualizing the Difference: Why Logistic Regression Outperforms Linear Regression for Classification | by Rohan Bali | Medium](https://images.openai.com/static-rsc-4/KE6LNis6dz7Je5Ostrv8cQZ-xKoX2I221Q3DppFggkHf4-HNrKgLYJhlvrDMDYFzLwuUes8BluQH9ApOHVGIcAr30G2Z4AvPNR9eX3GwQvY7EqQfDlL_E6vzFGJ408IEPBDWEZfr_TFrgvygN7NgN3eEsW9g4ZL3wHR5wOZb0m4?purpose=inline)

컷 10 | 00:46–00:50

“새로운 분류 규칙을 발견하지 않고도 손실을 줄인 것입니다.”

왼쪽에는 변하지 않은 결정경계, 오른쪽에는 감소하는 Loss를 놓는다.

화면 전체에 다음 문구를 표시한다.

Same predictions. Lower loss.

정답 확률 수치는 축소하고 이 문장에 시선을 집중시킨다.

여기서 가장 중요한 제작 조건은 로짓이 커지는 효과를 결정경계의 이동으로 표현하지 않는 것이야. 첫 번째 변화에서는 모든 입력에 동일한 양의 배율을 적용하므로 결정경계와 클래스 예측이 고정돼 있어야 해.

## 4막 — 두 번째 움직임: 결정경계를 바꾼다

00:50–01:11 · 핵심 시각 실험 B

첫 번째 실험의 점 배치를 그대로 유지한 채, 변화시키는 대상만 바꾼다. 이 막에서는 확신도 수치 대신 결정경계 자체의 움직임이 주인공이야.

[When Machine Learning fails — OWNML](https://images.openai.com/static-rsc-4/yDvTaN6p-ih-09--MsOQ829X29tN9m4AQC_6w9MBKRIewzlKxmQ9W_guROQX_neiWKNVFItKlTPi2lKnoqMWMYZvZcjU37_SeLijAdJQO-n-_JKXJAWYPDCNc1KGWYfSHcKkzCUdo_if-dQTJX7hFsyi_PDukIBOiqXTpozrNaI?purpose=inline)

컷 11 | 00:50–00:55

“이번에는 두 번째 변화를 살펴보겠습니다. 결정경계를 조금 회전시켜 보겠습니다.”

실험 A에서 마지막으로 표시된 로짓 수치를 제거한다. 분류 공간만 남긴다.

주황색 결정경계가 중앙의 한 점을 중심으로 시계 방향으로 10\~15도 회전한다.

기존 경계는 회색 점선으로 남기고 새로운 경계를 선명한 주황색으로 표시한다.

화면 문구: Decision Boundary Rotation

[Machine Learning Tutorials - Qiskit Machine Learning 0.9.1](https://images.openai.com/static-rsc-4/ffyJAAUTSdCBfX05DC6RzbUeu72ilBvCmRRIMHaprJUNcql2I66JeonA1Bab-DUZSxB_OeuJFnwqdrN49mbKBsRtw62kBbij-9FwwJiE6swdUvGi3qK5nE-sDaqYngrN531jbORYxEU3aMgJguIu_qExHxnFYMbSkLstZ_-WSJ8?purpose=inline)

컷 12 | 00:55–01:00

“훈련 데이터는 여전히 모두 올바르게 분류됩니다. 정확도는 계속 100퍼센트입니다.”

회전된 경계 양쪽에 있는 훈련 샘플을 차례로 확인한다.

모든 점의 클래스 예측이 그대로 유지되는 것을 강조한다.

`Training Accuracy: 100% → 100%`

이때 정확도 표시를 크게 강조하지만 회전된 경계는 그대로 유지한다.

[From Math to Code: Building Logistic Regression from Scratch (Binary Classification Example) | by Ibrahim Arshad | Medium](https://images.openai.com/static-rsc-4/jqKJoeGW22PWWl9Tv7cp5UDDmmlo2LWxlDQXhW4t9XUrLDsgAVtU74tuAkQtqWtPpgfethjNEh48eCZc6cAYoxydLQ8-4nYtmNLTcT3QQ7KuY4Xc8L2BPe4mAV-OxneGtaSTeAxOF1YOvwHtYrH4ySrpdZBM3wvhU86QQk9MM6Q?purpose=inline)

컷 13 | 01:00–01:06

“하지만 훈련 데이터가 없는 영역에서는 달라집니다. 새로운 입력이 이전과 다른 클래스로 분류될 수 있습니다.”

두 결정경계 사이에 새하얀 물음표 점 하나가 나타난다.

기존 경계 기준으로는 파란색 영역, 회전한 경계 기준으로는 청록색 영역이 되는 위치를 선택한다.

새 점은 움직이지 않지만 예측 클래스가 `A → B`로 변한다.

카메라를 확대하여 입력 자체는 그대로인데 출력만 달라진다는 점을 보여준다.

[Frontera de decisión | Interactive Chaos](https://images.openai.com/static-rsc-4/RAbApkhZwCz6NPa5Gd19tnOmgjFI6MyDXVgI4-CWQ0FdOQ6zfwokHWRJT-N0Ir9_aYc0w1h6n2xKBzGlGOhksrMm10PxV_XPjDHnutb3zj66s44Gn8EGU0wmFVKlPrllKLZCDR49ucHJ9BmRYFIxr6-NuLT_G9tlld7lFci7NnI?purpose=inline)

컷 14 | 01:06–01:11

“같은 훈련 정확도를 유지하면서도 신경망의 예측 함수가 변화한 것입니다.”

화면을 좌우로 분할한다.

왼쪽은 기존 경계, 오른쪽은 회전된 경계.

훈련 점의 위치는 완전히 동일하게 유지한다.

양쪽 모두 `Accuracy 100%`이지만 미지의 샘플만 서로 다른 색으로 나타난다.

Same training accuracy. Different predictions.

## 5막 — 두 움직임을 직접 비교한다

01:11–01:24 · 전체 영상의 시각적 중심

[A Visual Understanding of Logistic Regression | by Reza Bagheri | TDS Archive | Medium](https://images.openai.com/static-rsc-4/zL2JbD53CoS39g9Fpx6Jv-dCEMZqOjIuyBtS2r6nbiQpJ4jiKa-rmHg8vVdKOtt9krXx1fOYXlWCZLf-THuFLzT9hdPDVtsGcXhvvvRHpPYkuBw8axDUf4oBZR1MOMP00qXIHJOj5Js8KkLjYLTPNlvkBKDzUN_KxMOanKtzZX4?purpose=inline)

컷 15 | 01:11–01:20

“여기서 중요한 차이가 나타납니다. 첫 번째 변화는 기존 예측의 확신도를 높입니다. 두 번째 변화는 어떤 입력을 어느 클래스로 구분하는지 바꿀 수 있습니다.”

양쪽에 실험 A와 B를 동시에 재생한다.

왼쪽: 데이터와 결정경계는 정지. `z × 1 → × 2 → × 4`라는 수치 변화와 확률 막대 증가.

오른쪽: 로짓 표시 없음. 주황색 경계가 회전하고 새로운 점의 예측 클래스가 변화.

하단 문구:

- 왼쪽 `Logit Scaling`
- 오른쪽 `Decision Boundary Change`

마지막 2초에는 양쪽 화면을 모두 정지시킨다.

[Функция потерь: как алгоритм понимает, что он ошибся / Хабр](https://images.openai.com/static-rsc-4/ImKHkMuilz3KXG4Bzyznyg1b2a6pye73rn0dVmJfZXYPolZeYFN7AIDshRqdcA7cS8K3fttnmDAnC4nFpm75FlTTiJekAfsVFZiO2dVX95YKvy9p3x7N9qMOJ5F2Fsd2YJsxBW7ulFdimV88gXUqQGGm2b_6xID5pCbWt8bZl_4?purpose=inline)

컷 16 | 01:20–01:24

“그렇다면 실제 경사하강법은 어느 방향을 선택할까요?”

좌우 두 화면이 가운데로 합쳐져 하나의 파라미터 점 \\(\theta\\)가 된다.

주변에 다양한 방향의 작은 화살표가 나타난다.

마지막에는 기울기 방향의 화살표 하나만 남긴다.

화면 문구: Which direction does Gradient Descent follow?

## 6막 — 경사하강법은 무엇을 선택하는가

01:24–01:48 · 직관에서 논문의 발견으로 이동

여기서부터 화면의 배경을 입력 데이터 공간에서 파라미터 공간으로 전환한다. 실제 신경망의 고차원 파라미터 공간을 2차원으로 투영한 개념도로 표현하는 거야.

[File:Gradient Descent Visualization.png - Cornell University Computational Optimization Open Textbook - Optimization Wiki](https://images.openai.com/static-rsc-4/XeyWAPRMY3rCZUCrv7wnqoama3GBhFI-jQDoJpCCXWwReF6-CBDhhM_dnAxRB-Up-VgWUSrtbEaWHvwKd3S_RWPK7Ko0sePs2w6AaKEjf72BZal3tHGwrEaIcpFDwwOeuHKV7FzuiZv2Fz1x-mOfHmERhnDQ1wdX55-9atiEyyg?purpose=inline)

컷 17 | 01:24–01:31

“경사하강법은 일반화에 유리한 방향을 직접 선택하지 않습니다. 현재의 손실을 감소시키는 기울기를 따라 움직입니다.”

2차원 파라미터 공간에 손실의 등고선을 표시한다.

하나의 점 \\(\theta_t\\)에서 손실이 낮아지는 방향으로 화살표가 그려지고, 점이 다음 위치로 이동한다.

화면 하단 수식:

\\[ \theta\_{t+1}=\theta_t-\eta\nabla L \\]

이때 일반화 정확도는 목적함수에 직접 등장하지 않는다는 점을 시각적으로 강조한다.

[ICLR Poster Grokking at the Edge of Numerical Stability](https://images.openai.com/static-rsc-4/dV8_gGjZHDbG8GKT8D2P1qqavLTFs25HojD5ZvhoJmJ878p0oBv_X-dIGpn5nqf1qZ1YUiEtp_WwVzp84O4m43GMrbDtLnGlJ9mMVJJsyeghqmnq76HGKjp1Z-MqWb60nkPinTLynAsLlr7LbLNRmxZwV3Alg-OxRgieMXGSdTA?purpose=inline)

컷 18 | 01:31–01:39

“2025년 발표된 Grokking at the Edge of Numerical Stability 연구는 일부 신경망에서 훈련 데이터를 모두 맞힌 이후, 기울기가 로짓의 크기를 증가시키는 방향에 강하게 정렬되는 현상을 관찰했습니다.”

논문의 제목과 발표 연도를 간결하게 보여준 뒤, 논문 이미지를 화면 좌측 상단으로 축소한다.

화면 중앙에는 파라미터 벡터 \\(\theta\\)와 손실 기울기 방향을 표시한다.

두 방향이 서로 가까워지면서 벡터 사이의 각도가 작아지는 모습을 보여준다.

자막: Gradient alignment with the NLM direction

중요한 것은 모든 기울기가 완전히 같은 방향이 된 것처럼 그리지 않는 거야. 강한 정렬을 나타내되 다른 성분도 남긴다.

[The reason behind moving in the direction opposite to the Gradient | by Praveen R | HackerNoon.com | Medium](https://images.openai.com/static-rsc-4/9JWab4iSV3I-VuwrjTiOI2cv3mxgUEVk9QxfL5XcxmS0bKUKk1b62E0YBFZMxpfU3cONOwXyNp_2-0MQand8CJIBRkKN8GQfwgParGVhUBVW7ZQEnmBekh3bwxtDS6xuAyq9Hgf8tjTl9bRsf0mnc9Zz0LTbSYDoWpcROVI-v2Y?purpose=inline)

컷 19 | 01:39–01:48

“연구진은 이 방향을 Naive Loss Minimization이라고 불렀습니다. 그리고 이러한 성분을 억제했을 때, 실험에서 일반화가 훨씬 빠르게 진행되는 결과를 확인했습니다.”

화면을 둘로 나눈다.

좌측 `Standard Gradient`: 파라미터 방향과 평행한 성분을 포함한 화살표.

우측 `⊥Grad`: 평행 성분을 제거하고 남은 기울기 화살표.

이어 아래에 개념적 테스트 정확도 곡선을 두 개 표시한다. ⊥Grad의 곡선이 더 이른 단계에서 상승한다.

실제 실험값을 재현하지 않는 경우 그래프에 Conceptual Illustration 표시

논문에서 NLM은 예측을 바꾸지 않고 로짓을 스케일링해 손실을 줄이는 성분이며, ⊥Grad는 이러한 방향을 억제하도록 제안된 알고리즘이야.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arXiv



## 7막 — 모든 경계 변화가 좋은 것은 아니다

01:48–02:05 · 논문의 관찰과 일반적인 해석을 구분

[Guide to Support Vector Machine (SVM) Algorithm](https://images.openai.com/static-rsc-4/S6wV-P2rI26_lAld20BysnDcdDFD0EZxhG6SpwYPfAjAxJtS7FKSW8zXNGI8hZ-h8Fktk5bK9qOE8Fz_g23eZU8_VH8VrYNrpQQfBY32v-IVPdekyr3KPQDrgBgEpOxjI-gzODrvDUtd_1aZYP0YZ6ZjKMrywDhADXGowRx5218?purpose=inline)

컷 20 | 01:48–01:54

“물론 결정경계를 변화시키는 모든 움직임이 일반화를 개선하는 것은 아닙니다.”

2막에서 사용했던 분류 공간으로 돌아온다.

동일한 훈련 샘플 사이에 서로 다른 세 개의 결정경계를 차례로 보여준다.

세 경계 모두 훈련 데이터를 올바르게 구분한다. 하지만 점선으로 표시된 미지의 데이터에 대한 예측은 서로 다르다.

자막: Decision Boundary Change ≠ Better Generalization

[Geometric Origins of the Inner Product | Victor Liu's Website](https://images.openai.com/static-rsc-4/tCoZTZjeYu_5Av-rdkB5yf-rUcE4-XMLOg57o5B30RfPatwMN58PleOpcB0_mWNofq_KzMRlXRYk92BU7-CNSXtQCfq1KRUAAzvq3t8_aHY3wfQBhU0MCNTPh1eFm8ejRbTIF_0OuR317Vwl09TgBmszgbsNqUTk6XBi86UkDJg?purpose=inline)

컷 21 | 01:54–02:02

“두 변화가 항상 독립적으로 존재하는 것도 아닙니다. 하지만 이 연구는 중요한 차이를 보여줍니다.”

하나의 기울기 벡터를 두 개의 성분으로 분해한다.

보라색은 파라미터 방향과 평행한 성분, 녹색은 수직 성분.

두 성분이 합쳐져 원래 기울기 벡터가 되는 과정을 보여준다.

좌측 하단에 작은 문구로 `Gradient Decomposition`을 표시한다.

이 그림은 논문에서 사용한 기하학적 분해를 설명하는 것이며, 모든 수직 성분이 일반화 개선에 기여한다는 뜻은 아니라는 점을 유의한다.

[the bug that taught me more about PyTorch than years of using it | Elana Simon](https://images.openai.com/static-rsc-4/i1QG8nUBhBPRvny99ZESGgauByCYQeBjUcnEaGipq03AyRNA81gQcf5fe9Y-PhOawLqwrniuVp05_CCZczyM9oXKC2lyGmbpcIS9LcqNUbTyN5nUvXvH-pSZtIdYbh1Ybc81zMD20LOfanrxzAq_uzWTCi3SH2FTGxJj5Sakvcc?purpose=inline)

컷 22 | 02:02–02:05

“하지만 이 연구는 중요한 차이를 보여줍니다.”

손실 그래프와 테스트 정확도 그래프를 다시 나란히 놓는다.

손실은 계속 감소하고, 테스트 정확도는 한동안 거의 변하지 않는 모습을 보여준다.

두 그래프 가운데에 작은 `≠` 표시를 배치한다.

컷 21과 컷 22의 시간은 실제로 겹치지 않도록 컷 21을 01:54–02:02, 컷 22를 02:02–02:05에 배치하며, 02:02부터 논문 해석에서 최종 결론으로 전환한다.

## 8막 — 결론: 학습은 무엇을 바꾸었는가?

02:05–02:21 · 핵심 질문으로 회귀

[Grokking in loss doesn't necessarily imply grokking in accuracy | Ziming Liu](https://images.openai.com/static-rsc-4/VIKtAvB-Uco04oab5fZe2eFLcqTwH-OfYe-ioCGBFFtNtx-MBtbedBzRejZiw_h5PFdcb7Yw819_ba0iC6esNj88lW5fBowcvnd7wJhrZZhU0k0I_zYHnNDgi-qbsoaogyfv5jA_gDMgU5SdBskBD1Iod66xBZdq4JwDuLNj1_s?purpose=inline)

컷 23 | 02:05–02:11

“훈련 손실이 계속 감소한다는 사실과, 신경망이 새로운 데이터를 더 잘 구분하게 된다는 사실은 같지 않습니다.”

화면 왼쪽에는 손실이 감소하는 곡선, 오른쪽에는 테스트 정확도 곡선.

양쪽 곡선이 동일한 학습 스텝을 따라 움직이지만 서로 다르게 변화한다.

가운데에 `Loss Minimization ≠ Generalization`을 크게 나타낸다.

영상 전체에서 강조해야 할 핵심 문구 중 하나다.

[How to Choose an AI Development Framework — Reinvently](https://images.openai.com/static-rsc-4/-sXPSVKTEVDi5NNHo72-FpLLlfxr1N1cByhZW8tUonSlTXqjTrrxtyzz1ozUua-eza6QPgOrBHdsCLYURcfrWFnDVFNNvr4sUPby02dsYUgC-joy-95A-O7kuo5q5HmuZAevAXCtNmt2fFLDYbwhdWJYXidsOPNcc0TJGrfKbuU?purpose=inline)

컷 24 | 02:11–02:15

“정답을 모두 맞힌 이후에도 신경망은 계속 변합니다.”

도입부에서 등장했던 파라미터 점을 다시 보여준다.

동일한 점에서 출발한 여러 궤적이 서로 다른 방향으로 이어진다.

모든 궤적 위에는 작은 `Training Accuracy = 100%` 표식을 유지한다.

단, 궤적의 색상을 특정한 학습 성능의 우열과 연결하지 않는다.

[HEBB LABS — Human World Model](https://images.openai.com/static-rsc-4/31bOngtN_vHPzBh7Ut584vT_qzaDQQGdqtC9EDqLN0l7Dga77lYs5PyjoH4ZQHZGNvSgOLI-Xy8lRoRNdF5Y5PDrDg02m-R5XNgQlJJXRkLknW9uK-UN31_vddMpnAu79tsypd96xsDX5saW8hjrvHNxNUTbDbMCxIYyNDKaDiE?purpose=inline)

컷 25 | 02:15–02:21

“우리가 물어야 할 것은 얼마나 더 학습했는가가 아니라, 그 학습이 무엇을 바꾸었는가일지도 모릅니다.”

여러 궤적이 천천히 사라지고 하나의 움직이는 점만 남는다.

그 점은 마지막 순간에 멈춘다.

화면 중앙에 최종 질문을 표시한다.

### What did learning actually change?

마지막 1초 동안 모든 그래픽을 제거하고 질문만 남긴 후 검은 화면으로 종료한다.

## 최종 제작용 타임라인

| 구간          | 화면의 중심        | 전달해야 할 핵심           |
| ----------- | ------------- | ------------------- |
| 00:00–00:13 | 정확도와 손실 그래프   | 정확도 100%여도 학습은 계속된다 |
| 00:13–00:23 | 2차원 분류 공간     | 동일한 실험 조건 확립        |
| 00:23–00:50 | 로짓 확대·확률 변화   | 결정경계는 그대로, 손실은 감소   |
| 00:50–01:11 | 결정경계 회전       | 정확도는 그대로, 예측은 변화 가능 |
| 01:11–01:24 | 두 실험의 직접 비교   | 두 변화의 성격 구분         |
| 01:24–01:48 | 기울기·NLM·⊥Grad | 실제 논문의 관찰과 실험       |
| 01:48–02:05 | 경계와 기울기 분해    | 일반화와 단순한 변화를 구별     |
| 02:05–02:21 | 손실과 일반화의 대비   | 학습이 무엇을 바꾸었는가       |

## 제작 시 반드시 지켜야 할 조건

1. 같은 좌표, 같은 점 배치 사용. 첫 번째와 두 번째 실험을 서로 다른 데이터로 보여주면 두 움직임의 차이가 흐려진다.
2. 첫 번째 실험에서 결정경계를 고정. 로짓 스케일링은 입력 공간의 점을 이동시키는 연산이 아니다. 확률과 숫자만 바꾸는 것이 정확하다.
3. 두 번째 실험에서 정확도 100%를 유지. 경계가 기존 훈련 샘플을 넘어가면 영상의 논리가 깨진다.
4. 새 데이터의 예측 변화와 일반화 개선을 동일시하지 않는다. 새로운 점의 참값을 모르면 예측 변화가 좋은지 나쁜지 평가할 수 없다.
5. 논문 그래프와 개념 그래프를 구별한다. 실제 실험 결과를 재현한 그래프가 아니라면 `Conceptual Illustration`을 표시한다.

추가로 정확성을 위해 40\~46초의 확률 계산은 두 클래스 로짓을 \\([z,0]\\)으로 두는 설정으로 통일하자. `z=2,4,8`에서 정답 확률과 Cross-Entropy를 계산하면 콘티의 숫자가 성립해.

## 가장 중요한 연출 제안

이 영상에서 가장 많은 제작 시간을 투자할 부분은 00:23\~01:20의 약 57초라고 생각해.

이 구간에는 설명을 위한 자료를 여러 개 전환하기보다, 동일한 분류 공간을 일종의 시뮬레이터처럼 다루는 게 좋겠어.

특히 01:11부터 양쪽에 두 실험을 동시에 재생하는 장면은 영상 전체의 대표 장면으로 사용할 수 있어.

Logit Scaling

경계 고정 · 확신도 증가

Boundary Change

정확도 유지 · 예측 변화

Same Training Accuracy, Different Changes

이 두 움직임이 한눈에 이해된다면, 후반의 논문 설명에서 NLM이라는 새로운 용어가 등장해도 시청자가 추상적인 개념으로 받아들이지 않을 거야. 이미 눈으로 확인한 현상에 이름을 붙이는 과정이 되니까.

이 구성은 단순한 논문 해설을 넘어 손실함수, 최적화, 일반화 사이의 차이를 하나의 기하학적 실험으로 설명하는 영상이 될 수 있어.