# QR 분해 1편 — 상세 영상화 콘티

제목: 벡터는 어떻게 새로운 공간을 만드는가? — QR 분해의 기하학

총 95초

9:16 세로 쇼츠 · 24개 장면 · 3D 벡터 애니메이션 중심

기존 내레이션과 타임코드는 유지하고, 장면 전환·카메라·벡터 좌표·수식·애니메이션 동작을 구체화한 제작 콘티야.

## 1. 영상의 시각적 핵심

이번 영상은 단순한 Gram–Schmidt 공식 설명이 아니라 벡터가 기존 공간에 기여하는 새로운 방향을 찾아가는 과정을 보여줘야 해.

영상 내내 같은 3차원 좌표 공간을 사용하고, 벡터의 변화가 기하학적으로 연결되도록 구성하자.

벡터 및 색상 규칙

파란색

첫 번째 벡터 / q₁

초록색

두 번째 벡터 / q₂

주황색

세 번째 벡터 / q₃

보라색

투영 성분 / 기존 공간

원래 벡터는 실선 화살표, 투영 성분은 점선, 생성된 부분공간은 반투명 면으로 구분한다.

실제 계산 예시는 다음으로 통일하는 것이 좋아.

\\[ a_1=(1,1,0),\quad a_2=(0,2,0),\quad a_3=(1,1,2) \\]

이 세 벡터는 선형독립이고, \\(q_1,q_2\\)는 원래 좌표축과 기울어진 방향을 갖게 돼.

\\[ q_1=\frac{1}{\sqrt 2}(1,1,0) \\]

\\[ q_2=\frac{1}{\sqrt 2}(-1,1,0),\qquad q_3=(0,0,1) \\]

\\[ R=\begin{bmatrix} \sqrt2&\sqrt2&\sqrt2\\\ 0&\sqrt2&0\\\ 0&0&2 \end{bmatrix} \\]

수치와 좌표를 전부 내레이션에 넣지는 않고, 실제 애니메이션의 위치와 벡터의 변화가 수학적으로 일치하도록 하는 제작 기준으로 사용하자.

## 2. 상세 타임라인 콘티

### 장면 A — 벡터 개수와 차원의 차이 (0\~30초)

[Koordinaten eines Vektors - Vektoren einfach erklärt | Prüfungshefte Wiki](https://images.openai.com/static-rsc-4/b1uLWd_Ms2k9zdJr6J3oHPTl00XaKNShhHurG7zLo-fswMo2tDyPQlBrJs2_LyQ_KYKcMOFoUq2z4CgmruqqhPVenTo7wBJmmlFzntzfsUO7983D4NqJHIXUN98RLFK0BLOUR-Pauvy0X_FDqjL_IZBh71wBxnm5TmXIlfQYKBk?purpose=inline)

컷 01 · 0\~3초

“벡터가 세 개 있으면, 반드시 3차원 공간을 만들 수 있을까요?”

검은 배경의 3차원 좌표축에 파란 벡터 한 개가 등장한다. 이어 초록색, 주황색 벡터가 차례로 나타난다. 카메라는 정면보다 약간 위에서 비스듬히 내려다보며 시작한다.

화면 문구: 벡터 3개 = 3차원?

[Vector Equations — Linear Algebra, Geometry, and Computation](https://images.openai.com/static-rsc-4/vgzR741uoP73SLhIuFnkr8Oo56gIXLsGfIzBXuUCnOuLWcDBn5CcjMXQYZ7ObO0N5exD3tR4OlSGXDwsxOaKqo9BrMOMDYPEg6PJF5X7A9xJhlRI_jYKvmOLzXwd_nHfkQLxV5wFsgnsOMsde7cuCu9T9x2jVHyW0Ns47PUQopM?purpose=inline)

컷 02 · 3\~8초

“첫 번째 벡터가 있습니다. 이 벡터에 여러 숫자를 곱하면 하나의 직선을 만들 수 있습니다.”

첫 벡터만 남기고 나머지는 사라진다. 벡터 길이가 0.5배, 1배, 2배로 바뀌고 반대 방향에도 나타난다. 화살표 끝들의 궤적이 하나의 무한한 직선으로 확장된다.

\\(\operatorname{span}(a_1)\\)

[5.11.1.4: Finite Dimensional Spaces - Mathematics LibreTexts](https://images.openai.com/static-rsc-4/Hte3gZpEJN6Z7EiH2pCPI2lCSlKSapdqU5XVKoA_PXGSA2_sTls-ALoEAX5isDK4n_11MhhS0CibxQiygzCBfG3yCcUbwFfP5YlQQ5KeNlK3TWH5kJjJlvcnphTeCHuZCAd7X95csbblifb-0RRH8bhkMU6dudztUk_KlUtnyj4?purpose=inline)

컷 03 · 8\~12초

초록 벡터가 나타나고, 파란 벡터와 평행하지 않은 방향으로 뻗는다. 두 벡터가 만드는 평행사변형이 반복적으로 확대되며 평면으로 확장된다.

컷 04 · 12\~16초

카메라를 평면의 위쪽에서 비스듬하게 회전시켜, 두 벡터가 같은 평면에 속한다는 사실을 보여준다. 반투명 평면 위에 작은 좌표 격자가 나타난다.

\\(\operatorname{span}(a_1,a_2)\\)

컷 05 · 16\~19초

“그렇다면 세 번째 벡터는 어떨까요?”

주황색 세 번째 벡터가 위쪽에서 나타나 기존 평면을 향해 이동한다. 관객에게 3차원 방향이 등장할 것 같은 기대감을 준다.

[Linear Independence — Linear Algebra, Geometry, and Computation](https://images.openai.com/static-rsc-4/wcv7cwoH4a9W1xeTh9AIIDBJhnLmgU9O-yNw-TlSYIKhX_2JdHJAp4J-RamxNd6zm4B3hhqc2lOhhA7tQD13v0CDSutNR5uG487zKUUZa9HbJyJCoX6FYYMozF1yGvxjl9LcRcEf5Tkf9qcrQr4oG5zRcm0l2BtarznJ3QgeA6c?purpose=inline)

컷 06 · 19\~24초

세 번째 벡터가 평면 위에 정확히 눕는다. 화면에 \\(a_3=a_1+a_2\\)를 짧게 표시하고, 평면 위의 합성 벡터 경로를 점선으로 그려 보여준다.

이 장면은 도입 전용 종속 벡터 예시이며, 본 계산 예시와 구분한다.

컷 07 · 24\~30초

“중요한 것은 벡터의 개수가 아니라, 기존 벡터들로 표현할 수 없는 새로운 방향이 존재하는가입니다.”

화면을 좌우로 나눈다. 왼쪽은 세 벡터가 평면 안에 있는 상태, 오른쪽은 세 번째 벡터가 평면 밖으로 뻗은 상태.

왼쪽: 차원 2

오른쪽: 차원 3

### 장면 B — 새로운 방향을 분리하는 과정 (30\~56초)

컷 08 · 30\~34초

“그렇다면 새로운 방향만 따로 찾아낼 수 있을까요?”

기존 시각화를 축소한 뒤 첫 번째와 두 번째 벡터만 화면 중앙으로 확대한다. 이번에는 선형독립인 제작 기준 벡터 \\(a_1=(1,1,0)\\), \\(a_2=(0,2,0)\\)를 사용한다.

화면 문구: 기존 방향 / 새로운 방향

[What normalize() does (and why Three.js raycasting needs it) - DEV Community](https://images.openai.com/static-rsc-4/mlgycCe_EFf-aJwOBojXcvpTx70UV_Go7w6SfQKMi2rCSmN6HBDB6Lc7HDkt1i3pxiCyBlogVKMSsEMmNB50zF4oTY_Ffep7pFOCRbDDFTGeSblVmxA33jYpMzo5F-EfwMBfR7eDRzrZEzJg7aA-ACJkuOz6xg0u5txZ3YpBt2U?purpose=inline)

컷 09 · 34\~38초

파란 벡터 \\(a_1\\)이 방향을 유지하면서 길이 1로 줄어들고 \\(q_1\\) 라벨로 교체된다. 원래의 방향이 그대로 유지된다는 점을 강조한다.

\\[ q_1=\frac{a_1}{\\|a_1\\|} \\]

컷 10 · 38\~40초

“이제 두 번째 벡터를 살펴보겠습니다.”

초록 벡터 \\(a_2\\)만 밝아지고 \\(q_1\\)은 어둡게 유지된다. 카메라가 평면에 거의 수직인 방향으로 이동해 2D 투영이 명료하게 보이도록 한다.

[Epsilons, no. 4: The Gram-Schmidt process](https://images.openai.com/static-rsc-4/-9NTmbR-EbtA_aeW2QkQc_Mx678El8WL2wIJlUdlMpNnOkxJjA9tULU_mHpZMBJjr780Kkyp7q2RHLMSCgkDeIiyhVbw53vmeHqwW_ghZVGKOnXilcU_O27_PxyA-iG1OmDm1sWmouwvxg5b6RmEXtKBFgX0dtTSaw4Ve9PrVIQ?purpose=inline)

컷 11 · 40\~45초

초록 벡터 끝에서 파란 기준축으로 수직선을 내린다. 원점에서 투영점까지 보라색 점선 벡터, 투영점에서 원래 벡터 끝까지 초록색 수직 성분을 표시한다.

\\[ a_2=(q_1^Ta_2)q_1+u_2 \\]

직각 표시를 투영점에 추가한다.

컷 12 · 45\~51초

“큐 원 방향으로 투영한 성분을 제거하면…”

보라색 투영 성분이 점차 사라진다. 동시에 초록 수직 성분을 평행이동시켜 원점에서 시작하는 벡터로 표시한다. 이때 원래 벡터 \\(a_2\\)는 반투명하게 남겨 차이를 비교한다.

\\[ u_2=a_2-(q_1^Ta_2)q_1 \\]

[QR Decomposition - 공돌이의 수학정리노트 (Angelo's Math Notes)](https://images.openai.com/static-rsc-4/rG-Nw3IggGjx_Y4MRPVLG5Te_2MaM2CUBOCpue4NLVOJ12RX11usX2hwM6ar6shSeZwix40-9jr6RMKzLdy8gBo_CtbQB1WCdoNQ2LK-y8clIFHnIAamfnS4OIHHaCOK-0Zgyb9ym-eyoCi-O3RVuJ4GtgVjvhigVumijg4WI80?purpose=inline)

컷 13 · 51\~56초

초록 수직 벡터의 길이가 1이 되도록 조정되면서 \\(q_2\\)가 된다. \\(q_1\\)과 \\(q_2\\) 사이에 직각 표시를 남긴다.

\\[ q_2=\frac{u_2}{\\|u_2\\|} \\]

화면 문구: 새로운 독립 방향 발견

### 장면 C — 평면 밖의 새로운 방향 발견 (56\~71초)

[Geometric Control and Structure-at-Infinity Control for Disturbance Rejection and Fault Compensation Regarding Buck Converter-Based LED Driver](https://images.openai.com/static-rsc-4/iDgQz5h5ATNLu1L1YNWW0eWSIHfyiN5057iaYrRJgPfni-zUni6tRH_leRFDm1iBA9F9-A8FMUpa4gXikI2MTZ6gL4cKTv6Ej7eYSVhon92Qw2rgvALoprKtgInE2_KZOb-Ul23TcbUFvB7_ewHST2h6rSzbjB-niPa2IwyHaok?purpose=inline)

컷 14 · 56\~59초

“이제 세 번째 벡터를 추가해 보겠습니다.”

카메라가 2D 평면에서 서서히 기울어지며 3D 공간을 보여준다. \\(q_1,q_2\\)가 만드는 평면을 반투명하게 표시하고, 주황색 \\(a_3=(1,1,2)\\)가 평면 밖으로 등장한다.

이때 세 번째 벡터는 평면에서 수직으로만 향하는 것이 아니라, 평면 위 성분과 평면 밖 성분을 동시에 가진다는 점을 보여준다.

[Gradient Surgery for Multi-Task Learning](https://images.openai.com/static-rsc-4/Sfarxyfj2UFVM1OdIlQzjsEp1-EEzobdT8uJRLsGuSEu_G4Q1USowbrzXPS4ADoUbKrN7JH1PTXobam5K7YhunnlfULQk8igIz2FlCVj9bgiAuGk_PMn9tsyGYJk7QBBA1Qaa_KQeAsy2YjxUmpLV-v9095XgDFs0cqcUJHKqfw?purpose=inline)

컷 15 · 59\~62초

“이번에는 기존의 두 방향에 대한 투영 성분을 모두 제거합니다.”

\\(a_3\\)의 끝점에서 \\(q_1,q_2\\)가 만드는 평면으로 점선을 내려 수직 투영한다.

평면 위 투영 벡터를 보라색으로 강조한다.

\\[ p_3=(q_1^Ta_3)q_1+(q_2^Ta_3)q_2 \\]

화면에서는 수식을 작은 크기로 표현하고, 평면 위 성분과 수직 성분의 분리를 우선한다.

컷 16 · 62\~65초

“남은 벡터가 0이 아니라면, 기존 평면에 수직인 새로운 방향…”

평면 위 투영 성분이 사라진다. 투영점에서 원래 끝점까지의 주황색 수직 성분만 남긴 뒤, 이를 원점으로 평행이동한다.

\\[ u_3=a_3-p_3 \\]

카메라는 수직 성분의 방향이 기존 평면 밖을 향한다는 사실이 드러나도록 측면으로 이동한다.

[Orthogonal and Orthonormal Vectors – LearnDataSci](https://images.openai.com/static-rsc-4/hPIkqPkXLUEEk3WPrjTIlWCAi4CHxR74DNMJh3W43ZqYfxEoIeMWJsUhonh9lEufrYLjuS6F7bMX6JUmKr-UA4GgqF7KGOEgJDUs_YMJxSkUHluQ-RgF71TQP5zDLMvwFA7JZ_PJ08RYfP7lOuThOr7HAfvrTwXlzazbbAz4Sj0?purpose=inline)

컷 17 · 65\~67초

“…큐 쓰리를 얻을 수 있습니다.”

\\(u_3\\)의 길이를 1로 정규화하고 \\(q_3\\)라고 표시한다.

\\[ q_3=\frac{u_3}{\\|u_3\\|} \\]

화면 하단에 작게 `기존 평면에 수직인 방향`을 표시한다.

컷 18 · 67\~71초

“이렇게 만들어진 세 방향은 서로 직교하며, 각각 길이가 1입니다.”

\\(q_1,q_2,q_3\\)를 한 화면에 배치한다. 세 벡터의 길이가 동일하게 보이도록 하고 서로 직교하는 기준 방향임을 표시한다.

\\[ Q^TQ=I \\]

수식과 함께 세 방향 사이의 직각 관계를 차례로 강조한다.

### 장면 D — 공간의 기하학에서 행렬 분해로 (71\~85초)

이 구간은 영상에서 가장 중요한 전환이야. 앞에서 발견한 새로운 기준 방향이 단순히 독립적으로 존재하는 게 아니라, 원래 벡터들을 다시 만드는 데 사용될 수 있다는 사실을 보여줘야 해.

컷 19 · 71\~76초

“그리고 원래 벡터들은 이 직교하는 방향들의 선형결합으로 다시 표현할 수 있습니다.”

화면을 좌우로 나눈다.

왼쪽에는 원래 벡터 \\(a_1,a_2,a_3\\), 오른쪽에는 직교 기준 \\(q_1,q_2,q_3\\)를 표시한다.

오른쪽에서 \\(q_1,q_2,q_3\\)를 각각 확대·축소한 후 머리와 꼬리를 이어 원래 벡터들을 재구성한다.

\\[ \begin{aligned} a_1&=\sqrt2q_1\\\ a_2&=\sqrt2q_1+\sqrt2q_2\\\ a_3&=\sqrt2q_1+2q_3 \end{aligned} \\]

실제 화면에서는 세 식을 동시에 보여주지 않고, 한 벡터씩 재구성할 때 해당 계수만 표시한다.

컷 20 · 76\~79초

“직교하는 기준 방향들을 모은 행렬이 큐…”

원래 공간의 \\(q_1,q_2,q_3\\)를 각각 행렬의 열에 대응시키는 연결선을 그린다.

\\[ Q=\begin{bmatrix}|&|&|\\\q_1&q_2&q_3\\\\|&|&|\end{bmatrix} \\]

공간 속 화살표는 화면 한쪽에 축소해 유지하고, 그와 연결된 행렬의 열을 같은 색으로 강조한다.

컷 21 · 79\~82초

“원래 벡터들을 그 기준으로 표현한 계수들을 모은 행렬이 알입니다.”

앞서 원래 벡터를 재구성할 때 사용한 계수들을 표 형태로 정렬해 \\(R\\)을 구성한다.

\\[ R=\begin{bmatrix} \sqrt2&\sqrt2&\sqrt2\\\ 0&\sqrt2&0\\\ 0&0&2 \end{bmatrix} \\]

열 하나를 선택하면 해당 열의 계수가 공간 속 \\(q_1,q_2,q_3\\)에 적용되고 원래 \\(a_i\\)가 재구성되는 짧은 애니메이션을 사용한다.

컷 22 · 82\~85초

“바로 에이 이퀄 큐 알. QR 분해입니다.”

앞의 벡터와 계수 표현들이 정리되면서 중앙에 크게 나타난다.

\\[ \boxed{A=QR} \\]

원래 벡터

직교 기저 × 조합 계수

이 순간에만 배경의 복잡한 좌표 격자를 최소화해 공식이 명확하게 보이도록 한다.

### 장면 E — QR 분해의 의미 (85\~95초)

컷 23 · 85\~89초

“QR 분해는 단순히 벡터를 수직으로 만드는 계산이 아닙니다.”

\\(Q\\)의 벡터들만 강조하는 화면에서 다시 원래 \\(A\\)의 벡터들을 함께 보여준다.

원래 벡터를 구성하는 각각의 기준 방향 성분이 색상으로 구분되어 나타난다.

화면 문구: 직교화 그 이상의 의미

컷 24 · 89\~95초

“각 벡터가 기존 공간에서 얼마나 설명될 수 있고, 무엇을 새롭게 추가하는지 드러내는 과정입니다.”

첫 번째 벡터의 직선, 두 번째 벡터의 평면, 세 번째 벡터의 공간 확장이 한 번에 재생된다.

각 단계에서 기존 공간에 포함되는 성분은 투명해지고 새롭게 추가되는 직교 성분만 밝게 강조한다.

마지막 1초에는 완성된 직교 기저와 다음 문구를 남긴다.

QR 분해 — 공간에 새롭게 추가되는 방향을 찾아내다

## 3. 제작 시 반드시 지켜야 할 수학적·시각적 기준

| 항목   | 제작 기준                                               |
| ---- | --------------------------------------------------- |
| 카메라  | 투영 연산 시 관찰 방향을 안정적으로 유지해 수직 관계가 왜곡되지 않도록 한다         |
| 벡터   | 위치 이동과 벡터의 길이 변경을 구별한다. 평행이동은 벡터 자체의 방향·크기를 바꾸지 않는다 |
| 부분공간 | 원점을 지나는 직선·평면으로 표현한다                                |
| 직교화  | 기존 공간에 대한 투영을 제거한 잔여 벡터로 새로운 방향을 만든다                |
| 정규화  | 잔여 벡터가 0이 아닌 경우에만 수행한다                              |
| 색상   | 원래 벡터와 정규화된 기저의 대응이 유지되도록 한다                        |
| 행렬   | 마지막 \\(A,Q,R\\)은 영상에 실제로 표시된 벡터들과 수학적으로 일치해야 한다     |

특히 카메라 연출에서 2D와 3D의 차이를 분명하게 보여주면 좋아. 평면을 정면으로만 바라보면 3차원에서의 수직 높이나 새로운 방향의 의미가 잘 전달되지 않으므로, 3차원 성분이 등장하는 순간에는 카메라를 회전시키는 게 효과적이야.

## 4. 영상 제작을 위한 장면 우선순위

가장 중요한 장면: 컷 11\~13

두 번째 벡터의 기존 방향 성분을 제거하면서 새로운 직교 방향을 발견하는 과정.

가장 시각적인 장면: 컷 15\~17

평면에 포함되는 성분이 사라지고 평면 밖의 수직 방향만 남는 과정.

가장 개념적으로 중요한 장면: 컷 19\~22

직교 기저의 조합으로 원래 벡터들을 복원하고, 그 과정이 \\(A=QR\\)로 표현되는 장면.

영상 전체에서 가장 피해야 할 연출은 원래 벡터들이 단순히 회전해서 직교 벡터로 변하는 모습이야. 그런 연출은 Gram–Schmidt의 실제 의미를 잘못 전달할 수 있어.

반대로 기존 공간에 대한 투영을 제거하고 잔여 성분을 독립적인 방향으로 찾아내는 과정을 일관되게 보여주면, QR 분해의 기하학적 의미가 정확하게 전달될 거야.