# QR 분해 2편 — 상세 영상화 콘티

영상 제목: 왜 R의 아래쪽은 모두 0일까? — QR 분해의 숨겨진 구조

98초

9:16 세로 영상

25개 컷

이번 영상의 핵심은 3차원 벡터의 직교 관계가 행렬 \\(R\\)의 0으로 기록되는 과정이야.

단순히 수식과 벡터 그림을 번갈아 보여주는 것이 아니라, 공간에서 발생하는 기하학적 관계가 행렬의 각 원소로 연결되도록 설계하자.

## 1. 제작 기준

시각적 구성

[Orthogonality and The Gram-Schmidt Process. | by Benjamin Vanous | Medium](https://images.openai.com/static-rsc-4/mDIdZbRt_66Dni6oxh8GKb8Z4v4xCOPojwxA7AoPe-UnW32_hoo3-jIJ7o4cmmEy32QI_tFbp-RW20pDv8uN94I81qQHHxYSO9U4Ypye0HDMDZuQEWUQO04XmhzW5tvDsayumF_jVj2_tJBJoIv36i9KszHBJ8msdfVctIEWdrU?purpose=inline)

좌측: 벡터 공간

벡터, 직교 방향, 투영, 부분공간

[Upper Triangular matrix](https://images.openai.com/static-rsc-4/YIPqs2xtmvntD9u6TSLH3Ga18-ksgEv6bgSTGEqLK2_-TdcY35c5WH6yjKKMxES2MI0EbwZpMdXYaD1hD4fla27o0RxsBoU0PbBbpQ1gSD6goa79JJvZe3gZKC0l9f4t34qGkwYCa4x-sw2749a3rrc1rKM9esinBTMhUhVR6f4?purpose=inline)

우측: 행렬 표현

내적 계수, 행렬의 열, 0이 되는 위치

영상의 대부분은 공간과 행렬을 연결해 보여주고, 기하학적 발견이 중요한 순간에는 벡터 공간을 전체 화면으로 확대한다.

### 벡터 및 색상

| 대상                | 색상       | 역할            |
| ----------------- | -------- | ------------- |
| \\(a_1,a_2,a_3\\) | 흰색 계열    | 원래 벡터         |
| \\(q_1\\)         | 파란색      | 첫 번째 직교 기준    |
| \\(q_2\\)         | 초록색      | 두 번째 직교 기준    |
| \\(q_3\\)         | 주황색      | 세 번째 직교 기준    |
| 투영 성분             | 보라색      | 내적으로 측정한 계수   |
| 0이 되는 계수          | 붉은색 → 회색 | 직교성으로 제거되는 성분 |

실제 영상에 사용할 벡터는 다음으로 설정하자.

\\[ a_1=(1,1,0),\quad a_2=(0,2,0),\quad a_3=(1,2,2) \\]

이에 대응하는 직교 기저와 위삼각행렬은

\\[ Q= \begin{bmatrix} \frac1{\sqrt2}&-\frac1{\sqrt2}&0\\\ \frac1{\sqrt2}&\frac1{\sqrt2}&0\\\ 0&0&1 \end{bmatrix} \\]

\\[ R= \begin{bmatrix} \sqrt2&\sqrt2&\frac3{\sqrt2}\\\ 0&\sqrt2&\frac1{\sqrt2}\\\ 0&0&2 \end{bmatrix} \\]

이 예시는 \\(R\\)의 대각선 위쪽 성분이 모두 0이 아니기 때문에 위삼각 구조에서 반드시 0이어야 하는 위치와 우연히 0이 되는 위치를 혼동하지 않게 해준다.

## 2. 상세 컷별 콘티

### A. 왜 R에는 0이 존재할까? (0\~21초)

컷 01 · 0\~4초

“QR 분해에서 행렬 R은 왜 대각선 아래쪽이 모두 0일까요?”

검은 배경 중앙에 \\(A=QR\\)이 나타난다. 카메라가 \\(R\\)을 확대하면 3×3 위삼각행렬이 펼쳐진다.

\\[ R=\begin{bmatrix}r\_{11}&r\_{12}&r\_{13}\\\\\color{red}{0}&r\_{22}&r\_{23}\\\\\color{red}{0}&\color{red}{0}&r\_{33}\end{bmatrix} \\]

0 세 개가 순서대로 붉게 발광하고 마지막에 물음표가 나타난다.

컷 02 · 4\~10초

“이것은 단순히 계산하기 편하도록 정해 놓은 형태가 아닙니다. 벡터들이 공간을 구성하는 방식과 관련이 있습니다.”

오른쪽의 행렬이 축소되고 왼쪽에 3차원 좌표 공간이 나타난다.

행렬의 각 열에서 공간으로 얇은 연결선을 뻗게 한다. 마지막에는 공간 속 세 벡터에 시선을 집중시킨다.

화면 문구: 숫자의 구조 ↔ 공간의 구조

[Medium](https://images.openai.com/static-rsc-4/F51CTL2fj3IfzfnC9AMhYdcPmysRTSWAvhcxlmPHE74YwTo6qOZJR2GdWOVhemCXYwJrf6YQ25sOwn-iPIJRquF0dC_9X6bmGXXSseFql5u8dkpNfgWcTs90uYYIizasNevYJk081Ab5fNv_Cfrz80DU7905Nih3tQnxYpU6kaY?purpose=inline)

컷 03 · 10\~14초

“세 개의 선형독립 벡터를 열로 가진 행렬 A를 생각해 보겠습니다.”

원점에서 시작하는 세 개의 벡터 \\(a_1,a_2,a_3\\)를 등장시킨다.

화면 한쪽에 행렬을 나타내고, 각 열과 벡터를 순서대로 연결한다.

\\[ A=[a_1\ a_2\ a_3] \\]

카메라는 세 번째 벡터가 평면 밖으로 향한다는 사실이 보이도록 약간 위에서 내려다보는 각도를 유지한다.

[Orthogonal and Orthonormal Vectors – LearnDataSci](https://images.openai.com/static-rsc-4/hPIkqPkXLUEEk3WPrjTIlWCAi4CHxR74DNMJh3W43ZqYfxEoIeMWJsUhonh9lEufrYLjuS6F7bMX6JUmKr-UA4GgqF7KGOEgJDUs_YMJxSkUHluQ-RgF71TQP5zDLMvwFA7JZ_PJ08RYfP7lOuThOr7HAfvrTwXlzazbbAz4Sj0?purpose=inline)

컷 04 · 14\~21초

“이 벡터들을 순서대로 직교화하면, 서로 수직이고 길이가 1인 세 방향, 큐 원, 큐 투, 큐 쓰리를 얻습니다.”

원래 벡터의 투명도를 낮추고 직교 기준 \\(q_1,q_2,q_3\\)를 순서대로 등장시킨다.

각 방향에는 해당 색상을 적용하고 직각 기호를 짧게 표시한다.

\\[ Q=[q_1\ q_2\ q_3],\quad Q^TQ=I \\]

직교화 전체를 다시 설명하지 않고 결과만 보여준다.

### B. 첫 번째 열 아래에 0이 생기는 이유 (21\~41초)

이 부분이 첫 번째 핵심 장면이야. 단순히 \\(q_2,q_3\\)가 수직이라고 말하는 것으로 끝내지 말고, 내적을 계산했을 때 행렬의 해당 원소가 실제 0이 되는 모습을 보여주자.

컷 05 · 21\~25초

“첫 번째 벡터 에이 원은 큐 원 방향만으로 표현할 수 있습니다.”

\\(a_1\\)과 \\(q_1\\)만 밝게 남긴다. 두 벡터가 정확히 같은 방향에 있다는 사실을 보여준다.

\\[ a_1=r\_{11}q_1 \\]

\\(q_1\\)을 \\(r\_{11}\\)배 확장하면 원래 \\(a_1\\)이 재구성된다.

컷 06 · 25\~27초

“그런데 왜 큐 투와 큐 쓰리의 계수는 0일까요?”

\\(q_2,q_3\\)가 다시 등장한다. 오른쪽에는 첫 번째 열의 계수 세 개를 보여준다.

\\[ \begin{bmatrix}r\_{11}\\\\?\\\\?\end{bmatrix} \\]

물음표 두 개를 강조한다.

[12.3: O produto Dot - Global](https://images.openai.com/static-rsc-4/OhcbVPCQVQsyoJ_3I1PlRvKMq84Zmqr6Yrqevr85PrTzNcJ9FREBbDDVa7_wwevCZRsDYN9JWC5mrK16Vx0r08YmXQyKVkdIUPLRGykK43gcTdExBW0ZfJ3cnH5wReMzLP6-E4PXmNKqAbdJJpEWb2NOAySBDFO4l8s_FBcA620?purpose=inline)

컷 07 · 27\~30초

“두 방향 모두 첫 번째 벡터에 수직이기 때문입니다.”

\\(a_1\\)과 \\(q_2\\), \\(a_1\\)과 \\(q_3\\) 사이의 수직 관계를 차례로 보여준다.

\\[ a_1\perp q_2,\qquad a_1\perp q_3 \\]

가능하면 시선을 각각의 벡터 쌍에 맞춰 카메라를 짧게 회전한다.

컷 08 · 30\~36초

“직교하는 단위벡터를 기준으로 할 때, 각 방향의 계수는 원래 벡터와의 내적으로 구할 수 있습니다.”

우측에 다음 공식을 표시한다.

\\[ r\_{ij}=q_i^Ta_j \\]

공간 속 \\(a_1\\)을 \\(q_2\\)축에 투영한다. 투영 벡터의 길이가 0임을 표시한다.

이어 같은 과정을 \\(q_3\\)축에 적용한다.

표시: 투영 길이 = 0

컷 09 · 36\~41초

“수직인 두 벡터의 내적은 0이므로, 첫 번째 열의 아래쪽 두 계수는 0이 됩니다.”

두 내적 결과가 행렬의 첫 번째 열로 이동한다.

\\[ r\_{21}=q_2^Ta_1=0 \\]

\\[ r\_{31}=q_3^Ta_1=0 \\]

\\[ R=\begin{bmatrix}r\_{11}&?&?\\\\\color{red}{0}&?&?\\\\\color{red}{0}&?&?\end{bmatrix} \\]

0이 들어간 순간만 짧은 강조 효과를 적용한다.

### C. 두 번째 열, 그리고 위삼각행렬의 완성 (41\~65초)

컷 10 · 41\~43초

“이번에는 두 번째 벡터를 보겠습니다.”

공간의 강조가 \\(a_1\\)에서 \\(a_2\\)로 이동한다. 행렬에서도 첫 번째 열은 회색으로 낮추고 두 번째 열만 강조한다.

[Скалярное произведение и разложение в ряд Фурье | Солнечные электростанции](https://images.openai.com/static-rsc-4/p5ADVR_YnrayipIiWWm1GU61xCD2Cq23tpXekv1cjLGdyRE8_pM5Wazl7-9GL2PVIji9hSQ4-ZAtEgb6MdL--wyNPwVi46Jn_Xd0MJD_IaAkqIYzAjfLSwDHnc6VHebajuS2vGpKaL9zKyxm4zIoM5EtTj0m7zZpkZFssUYJysc?purpose=inline)

컷 11 · 43\~47초

“두 번째 벡터는 큐 원과 큐 투의 선형결합으로 표현됩니다.”

\\(q_1\\) 방향 성분과 \\(q_2\\) 방향 성분을 머리-꼬리 방식으로 연결한다. 합성 결과가 \\(a_2\\)와 일치하도록 한다.

\\[ a_2=r\_{12}q_1+r\_{22}q_2 \\]

두 계수 \\(r\_{12},r\_{22}\\)를 오른쪽 행렬의 두 번째 열에 표시한다.

[Gradient Surgery for Multi-Task Learning](https://images.openai.com/static-rsc-4/Sfarxyfj2UFVM1OdIlQzjsEp1-EEzobdT8uJRLsGuSEu_G4Q1USowbrzXPS4ADoUbKrN7JH1PTXobam5K7YhunnlfULQk8igIz2FlCVj9bgiAuGk_PMn9tsyGYJk7QBBA1Qaa_KQeAsy2YjxUmpLV-v9095XgDFs0cqcUJHKqfw?purpose=inline)

컷 12 · 47\~53초

“세 번째 방향 큐 쓰리는 처음 두 벡터가 만드는 평면에 수직이므로, 두 번째 벡터와의 내적도 0입니다.”

\\(a_1,a_2\\)가 만드는 반투명 평면을 표시한다.

\\(q_3\\)가 이 평면에 수직으로 서 있다. \\(a_2\\)를 \\(q_3\\) 방향에 투영하면 길이가 0이 되는 모습을 보여준다.

\\[ r\_{32}=q_3^Ta_2=0 \\]

두 번째 열의 마지막 칸이 0으로 바뀐다.

컷 13 · 53\~57초

“반면 세 번째 벡터는 세 방향 모두의 성분을 가질 수 있습니다.”

평면 위에 \\(a_3\\)가 등장하고 평면 안의 두 방향 성분과 평면 밖의 방향 성분을 분리한다.

\\[ a_3=r\_{13}q_1+r\_{23}q_2+r\_{33}q_3 \\]

각 성분을 파란색·초록색·주황색으로 구분한다.

컷 14 · 57\~61초

“이제 각 벡터를 표현하는 계수들을 열 순서대로 모아보겠습니다.”

공간을 왼쪽으로 축소하고 오른쪽에 \\(R\\)을 크게 표시한다.

첫 번째 벡터 계수가 첫 열, 두 번째 벡터 계수가 둘째 열, 세 번째 벡터 계수가 셋째 열에 차례로 들어간다.

애니메이션 순서: 첫 열 → 둘째 열 → 셋째 열

컷 15 · 61\~65초

“대각선 아래쪽이 모두 0인 위삼각행렬 R이 만들어집니다.”

완성된 행렬을 중앙에 크게 배치한다.

\\[ R=\begin{bmatrix}r\_{11}&r\_{12}&r\_{13}\\\\\color{red}{0}&r\_{22}&r\_{23}\\\\\color{red}{0}&\color{red}{0}&r\_{33}\end{bmatrix} \\]

대각선 아래 0들을 한 번에 강조한다. 나머지 계수는 유지하고, 아래쪽의 0에만 밝은 테두리를 적용한다.

### D. 더 깊은 구조 — 부분공간의 보존 (65\~87초)

이 구간이 2편의 차별화 지점이야.

직교한 벡터들이 특정 계수를 0으로 만든다는 설명에서 끝내지 않고, QR 분해가 벡터들의 순서에 따라 만들어지는 부분공간을 유지한다는 사실까지 보여준다.

컷 16 · 65\~67초

“여기에는 더 중요한 구조가 숨어 있습니다.”

행렬을 화면 위로 축소하고 공간 속 원래 벡터들을 다시 등장시킨다. 화면 중앙에 `무엇이 그대로 유지될까?`를 짧게 표시한다.

[2.5: Linear Independence - Mathematics LibreTexts](https://images.openai.com/static-rsc-4/dvT-zwCgTKDZrppXMdH0NIwfO0dOh1WNGsfHVaWqA8nCqrSiumtNNQKAR0H_RXxFxTgSo8jucmvLltPgrc0s2pwBidFQCdvbZm8iZaWU9TMSJsVUZc1oOyO-f_Pkb7UtwM8QMCFM9LKlvK1ePk0wskLu5O2wG1fA9qHI2VRFf20?purpose=inline)

컷 17 · 67\~71초

“첫 번째 원래 벡터가 만드는 직선은 큐 원이 만드는 직선과 같습니다.”

먼저 \\(a_1\\)을 보여주고, 같은 방향의 \\(q_1\\)을 겹쳐 배치한다.

두 벡터를 따라 무한히 뻗는 하나의 직선을 표시한다.

\\[ \operatorname{span}(a_1)=\operatorname{span}(q_1) \\]

벡터 길이는 다르지만 동일한 직선을 만든다는 점을 강조한다.

[Can Gnuplot Made by Lazarus Plot 3D surface along with its orthogonal line in Julia? - General Usage - Julia Programming Language](https://images.openai.com/static-rsc-4/_n_wDf0Ty5o1WiHkbU90aRj2x13gNL5Q2TRx_a8SxI-BQQw5C9CG2-xmM1AdzIer5QPmSAgwrVWwUqlPV3gF9QAd3EGowlw2P6apr7cQMMLJaW1f9307QkDNIYfMfmOa6PgEEtKUnNGR0U4KxIBsEgaLGJkag_YUbRnBONWOMsU?purpose=inline)

컷 18 · 71\~76초

“처음 두 벡터가 만드는 평면도 큐 원과 큐 투가 만드는 평면과 같습니다.”

원래 \\(a_1,a_2\\)가 만드는 평면을 보여준다.

두 벡터를 반투명하게 처리한 뒤 \\(q_1,q_2\\)를 강조한다. 반투명 평면은 그대로 유지된다.

\\[ \operatorname{span}(a_1,a_2) = \operatorname{span}(q_1,q_2) \\]

벡터는 달라졌지만 공간은 바뀌지 않았다는 사실이 눈에 들어오도록 한다.

컷 19 · 76\~79초

“세 번째 벡터까지 포함해도 마찬가지입니다.”

\\(a_3\\)와 \\(q_3\\)가 평면 밖으로 등장한다.

공간 전체에 반투명 3차원 격자를 확장시켜 두 벡터 집합 모두 같은 3차원 공간을 생성한다는 사실을 표현한다.

컷 20 · 79\~83초

“QR 분해는 원래 벡터들이 순서대로 만들어가는 부분공간을 보존하면서…”

아래의 세 단계가 순서대로 나타난다.

첫 벡터

\\(V_1=\operatorname{span}(q_1)\\)

첫 두 벡터

\\(V_2=\operatorname{span}(q_1,q_2)\\)

세 벡터

\\(V_3=\operatorname{span}(q_1,q_2,q_3)\\)

직선 → 평면 → 공간으로 확장되는 애니메이션을 함께 보여준다.

컷 21 · 83\~87초

“…그 공간의 기준을 직교하는 방향들로 바꿉니다.”

원래 벡터 집합과 직교 기저 집합을 좌우로 배치한다.

\\[ \\{a_1,a_2,a_3\\} \\]

원래 기준

\\[ \\{q_1,q_2,q_3\\} \\]

직교 기준

두 집합 아래에 동일한 공간을 나타내는 반투명 기하학적 도형을 배치한다.

### E. 결론 — 공간의 수직성이 행렬의 0이 된다 (87\~98초)

컷 22 · 87\~91초

“따라서 R의 아래쪽에 나타나는 0들은 우연한 계산 결과가 아닙니다.”

화면에 \\(R\\)을 다시 확대한다.

대각선 아래의 0들이 차례로 깜빡이며 좌측 공간의 해당 직교 관계로 연결된다.

\\[ r\_{21}=0,\quad r\_{31}=0,\quad r\_{32}=0 \\]

컷 23 · 91\~94초

“뒤에 만들어진 직교 방향이 앞의 벡터들이 만드는 공간에 수직이라는 사실이…”

공간에서 \\(q_3\\)를 강조하고, \\(a_1,a_2\\)가 만드는 평면과 직각임을 표시한다.

이어 \\(q_2\\)가 \\(a_1\\)과 수직이라는 사실을 보여준다.

컷 24 · 94\~96초

“…행렬에 그대로 나타난 것입니다.”

벡터 공간이 행렬 뒤로 희미하게 사라지고, 내적이 0이라는 사실과 행렬의 0이 겹쳐진다.

\\[ q_i^Ta_j=0\qquad(i>j) \\]

컷 25 · 96\~98초

최종적으로 \\(A=QR\\)을 중앙에 남긴다.

\\[ A=QR \\]

위삼각 구조는 공간의 직교 관계를 기록한다.

## 3. 영상에서 사용할 핵심 수식

영상 전체에 많은 공식을 배치할 필요는 없어. 아래 네 가지 관계만 장면에 맞게 등장시키면 충분해.

① 직교 기저

\\[ Q^TQ=I \\]

서로 다른 \\(q_i\\)가 수직이고 각각 길이가 1이라는 성질.

② 계수의 의미

\\[ r\_{ij}=q_i^Ta_j \\]

\\(R\\)의 각 원소는 원래 벡터와 직교 기준 방향의 내적이다.

③ 위삼각 구조

\\[ i>j\quad\Rightarrow\quad r\_{ij}=0 \\]

앞 벡터는 뒤에 만들어진 직교 방향에 성분을 갖지 않는다.

④ 부분공간 보존

\\[ \operatorname{span}(a_1,\ldots,a_k)=\operatorname{span}(q_1,\ldots,q_k) \\]

원래 벡터와 직교 기저가 순서대로 생성하는 부분공간이 일치한다.

## 4. 제작에서 가장 중요한 세 가지

첫째, 행렬의 0과 벡터의 수직 관계를 실제로 연결해야 해. 예를 들어 \\(q_3\\)와 \\(a_2\\)의 내적이 0인 순간, 화면 반대편의 \\(r\_{32}\\)가 0으로 변하도록 만드는 거야. 관객은 위삼각행렬이 암기할 형태가 아니라 계산에서 필연적으로 등장하는 구조라는 것을 이해할 수 있어.

둘째, 부분공간 보존 장면에서는 벡터가 변해도 공간은 그대로라는 사실을 강조해야 해. 원래 두 벡터가 만드는 평면과 직교한 두 벡터가 만드는 평면을 동일하게 유지하고, 그 위에 벡터만 교체되는 연출이 효과적이야.

셋째, QR 분해를 단순한 회전으로 표현하지 않는 것이 중요해. \\(Q\\)는 직교 기저를 나타내지만, QR 분해가 원래 각 벡터를 하나의 공통 회전으로 \\(q_i\\)에 대응시키는 것은 아니야. 원래 벡터들의 선형결합 관계를 \\(R\\)에 남기면서 기준을 바꾸는 과정이 핵심이지.

최종적으로 이 영상에서 관객이 발견해야 할 사실은 하나야.

행렬 \\(R\\)의 0은 수학자가 임의로 정한 빈칸이 아니라, 공간에서 서로 수직인 방향들이 남긴 흔적이라는 것.