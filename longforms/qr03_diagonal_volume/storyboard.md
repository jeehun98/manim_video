# QR 분해 3편 — 상세 영상화 콘티

제목: QR 분해의 대각선에 부피가 숨어 있는 이유 — 행렬식의 기하학

약 110초

9:16 세로 쇼츠

27컷

이번 영상에서 가장 중요한 것은 행렬식이 무엇을 나타내는지와 QR 분해가 그 의미를 어떻게 드러내는지를 구분하는 것이야.

영상 전체를 하나의 단위 정육면체에서 출발하는 연속된 기하학적 실험으로 설계하자.

원래 부피 1 → 행렬 A가 바꾼 부피 → QR로 분리한 높이의 곱

## 1. 제작 기본 설정

### 사용 행렬과 좌표

실제 렌더링에서 벡터와 수식이 일치하도록 다음 행렬을 사용하는 걸 추천해.

\\[ A= \begin{bmatrix} 1&0&1\\\ 1&2&2\\\ 0&0&2 \end{bmatrix} \\]

각 열벡터는

\\[ a_1=(1,1,0),\quad a_2=(0,2,0),\quad a_3=(1,2,2) \\]

이고, QR 분해하면

\\[ Q= \begin{bmatrix} 1/\sqrt2&-1/\sqrt2&0\\\ 1/\sqrt2&1/\sqrt2&0\\\ 0&0&1 \end{bmatrix} \\]

\\[ R= \begin{bmatrix} \sqrt2&\sqrt2&3/\sqrt2\\\ 0&\sqrt2&1/\sqrt2\\\ 0&0&2 \end{bmatrix} \\]

를 얻어.

따라서

\\[ |\det A|=4 \\]

\\[ r\_{11}r\_{22}r\_{33} =\sqrt2\cdot\sqrt2\cdot2=4 \\]

가 일치하지.

실제 내레이션에서는 구체적인 행렬 원소를 모두 읽을 필요 없어. 수학적으로 정확한 애니메이션을 제작하기 위한 내부 기준으로 사용하면 돼.

### 색상과 시각적 의미

| 대상                     | 색상      | 시각적 역할             |
| ---------------------- | ------- | ------------------ |
| 단위 정육면체                | 회색 반투명  | 변환 전 기준 부피         |
| 변환된 평행육면체              | 파란색 반투명 | 행렬 \\(A\\)가 만드는 부피 |
| 밑변 \\(r\_{11}\\)       | 파란색     | 첫 번째 길이            |
| 밑면 수직 높이 \\(r\_{22}\\) | 초록색     | 두 번째 독립 방향의 크기     |
| 공간 수직 높이 \\(r\_{33}\\) | 주황색     | 세 번째 독립 방향의 크기     |
| 비대각 계수                 | 보라색     | 기존 방향으로의 기울어짐      |
| 직교행렬 \\(Q\\)           | 청록색     | 부피를 보존하는 직교변환      |

영상 초기에는 좌표축을 약하게 표시하고, 행렬식과 QR의 관계를 설명할 때만 좌표축과 수식을 밝게 강조한다.

# 2. 컷별 상세 콘티

## A. 행렬식은 왜 부피를 나타낼까? (0\~22초)

[Crafting 3D Experiences with React Three Fiber: Core Concepts and Scene Creation - DEV Community](https://images.openai.com/static-rsc-4/-hfH_XsvRO7d5lp9vmxKbSTZpF8YyafkiAXde55K-DrQR4GCac0BELrJ-m8WrTWdnek8oX9n92u11w4QCyZBUokDWsdr_OyhTlfxEolLpM6-sS8Iv5uTjoyZ9prxQKWP0XQEXbedDj_fOdXg4_FLeDFu94E6Zwud1_ihiYWfaCA?purpose=inline)

컷 01 · 0\~4초

“행렬식은 왜 공간의 넓이나 부피와 연결될까요?”

검은 배경에 3차원 좌표축이 나타난다.

원점에서 각각 길이 1인 세 방향의 벡터가 등장하고, 이 벡터들이 만드는 단위 정육면체가 반투명하게 채워진다.

카메라는 정육면체의 세 면이 모두 보이는 등각투영에 가까운 시점으로 시작한다.

화면: \\(\det A\\) = ?

컷 02 · 4\~7초

“3차원 공간의 단위 정육면체를 생각해 보겠습니다.”

정육면체 내부를 밝은 회색으로 채우고 모서리를 강조한다.

단위 길이를 나타내는 작은 눈금이 세 축에 나타난다.

\\[ V_0=1\times1\times1=1 \\]

[3D Transformation Matrices | Computer Graphics](https://images.openai.com/static-rsc-4/ZTkmNp0ct7k0uKC1A5kW1XEc_yJezKgOUiDUa4POUqeS9bGfLaJ24wxF4Wgld8JaROJOLBd_f4fLGSeBDQpnEaG8qQprw-rruckCo_8KsJ2guFA4Vypky4JX-uvHnVLisq7Jlcawh2iD4AGNB_735UJGnsWvCXHlGBHaUxIriwI?purpose=inline)

컷 03 · 7\~13초

“행렬 A를 적용하면, 세 개의 좌표축은 각각 A의 열벡터 방향으로 변환됩니다.”

표준기저 \\(e_1,e_2,e_3\\)가 각각 \\(a_1,a_2,a_3\\)로 이동하는 애니메이션을 만든다.

정육면체의 모서리와 내부 격자가 동시에 변형된다.

핵심은 세 방향이 서로 독립적으로 움직이는 것처럼 연출하되, 도형 전체에는 동일한 선형변환을 적용하는 것.

\\[ Ae_i=a_i \\]

[Practice Linear Algebra | Brilliant](https://images.openai.com/static-rsc-4/jnPiYR4dKnO_KMxlA3eiOXLUSVr2ibsk-WNhcVvDvq3R6MzUoOhGEMIuwAOQLNnW2Xa_JxhYyxMbJaSgfDoqb-HR9yp11aFHuil1WbB_Nvh4VLxRZcrITRj08euCCw0s_YIDIkvKjvqbye5-C4GgfJSZBAbmr9iWe10Cki7mXok?purpose=inline)

컷 04 · 13\~17초

“그 결과 정육면체는 기울어진 평행육면체가 됩니다.”

변형된 정육면체가 완전한 평행육면체로 고정된다.

변환 전 정육면체를 희미한 윤곽선으로 잠깐 겹쳐 보여준다.

카메라가 평행육면체를 약 20도 회전하며 기울어진 구조를 보여준다.

컷 05 · 17\~22초

“행렬식의 절댓값은 바로 이 변환이 부피를 몇 배로 바꾸었는지를 나타냅니다.”

변환 전후의 부피를 나란히 배치한다.

원래 단위 정육면체에는 `부피 1`, 변환된 평행육면체에는 `부피 4`를 표시한다.

\\[ V=|\det A|\cdot V_0 \\]

\\[ V_0=1\quad\Rightarrow\quad V=|\det A| \\]

부피 배율이 행렬식의 절댓값이라는 점을 명확하게 보여준다.

## B. QR 분해로 부피 변화 분리하기 (22\~43초)

컷 06 · 22\~27초

“그런데 이 부피 변화를 더 단순하게 이해할 방법은 없을까요?”

평행육면체가 중앙에 남아 있고, 표면의 기울어진 모서리를 차례로 강조한다.

화면에는 `길이 · 기울어짐 · 높이`라는 키워드가 나타난다.

이후 복잡해 보이는 도형을 단순하게 해석할 수 있을지 질문을 던진다.

컷 07 · 27\~31초

“행렬 A를 QR 분해해 보겠습니다.”

행렬 \\(A\\)가 중앙에 나타나고 \\(Q\\)와 \\(R\\)로 분리된다.

\\[ \boxed{A=QR} \\]

\\(Q\\)는 청록색, \\(R\\)은 보라색으로 강조한다.

변환된 평행육면체는 배경에 유지한다.

컷 08 · 31\~35초

“A는 직교행렬 Q와 위삼각행렬 R의 곱으로 표현됩니다.”

변환 경로를 화면에 표시한다.

\\[ x\xrightarrow{R}Rx\xrightarrow{Q}QRx \\]

단위 정육면체의 복제본을 사용해 `R 적용 → Q 적용` 순서를 시각화한다.

행렬 곱에서 오른쪽 변환이 먼저 적용된다는 점을 정확하게 보여준다.

[Parallélépipède : définition et explications](https://images.openai.com/static-rsc-4/lxTMJnmgWoJ78Rn1te00tYi8dR4PABwo8JqDCssYEEn9SBYvLBrZSG0TPI3IN8yS3mTsAqKg-CCENypBw_l86vnh0iW2qz8BpCJxJRt3HzHI0ioMRuOwDCwKVoc9QbZEEtCWSJ6pdMJ3hkPELBmXbSzbuKei-Guk9GHX2GAocLk?purpose=inline)

컷 09 · 35\~39초

“여기서 Q는 공간을 회전하거나 반사하는 직교변환입니다.”

\\(R\\)이 만든 평행육면체를 동일한 모양으로 유지한 채 전체를 회전시킨다.

회전 도중 모서리 길이와 각도는 바뀌지 않는다.

이번 예시의 \\(Q\\)는 회전행렬이므로 실제로는 회전만 수행한다. 반사 가능성은 작은 텍스트로 처리한다.

컷 10 · 39\~43초

“이 과정에서는 길이와 각도, 부피가 변하지 않습니다.”

도형의 회전이 진행되는 동안 부피 표시가 `4 → 4`로 유지된다.

\\[ |\det Q|=1 \\]

이후 회전을 되돌려 \\(R\\)이 만든 형태만 화면에 남긴다.

## C. 첫 번째와 두 번째 대각 성분 — 밑변과 넓이 (43\~70초)

이 부분부터 영상의 핵심적인 기하학적 발견이 시작돼.

이제부터는 \\(R\\)의 열벡터를 하나씩 추가하면서 도형을 완성한다.

컷 11 · 43\~47초

“따라서 A가 만들어내는 부피 변화는 R만 살펴보아도 알 수 있습니다.”

원래 평행육면체와 \\(R\\)이 만든 평행육면체를 좌우에 나란히 보여준다.

두 도형은 공간에서의 방향이 다르지만 부피는 동일하다.

화면에는

\\[ |\det A|=|\det R| \\]

를 표시한다.

[Vector Magnitude Calculator - Calculate Length & Norm](https://images.openai.com/static-rsc-4/tAooXYZaSpIXiMtfIi3ec1Qd735YL8oIRrpm6ZSk_9wBsxYmiL-apM7duNYfhP89rHlZCpGXELIXDoT-gc7E-ZbM7SRrGlfsgUijb0GAIztDqOEX1W4FJMLetMuR10y8d1oXb20Vp408GCU338CZ5QDPRFjICiTgnLjxqSxXfM0?purpose=inline)

컷 12 · 47\~51초

“먼저 R의 첫 번째 열벡터입니다.”

도형의 나머지 모서리가 사라지고 첫 번째 열벡터만 남는다.

이 벡터는 첫 번째 좌표축에 놓인다.

\\[ R e_1=(r\_{11},0,0) \\]

컷 13 · 51\~56초

“이 벡터는 첫 번째 좌표축 위에 놓여 있고, 그 길이는 R의 첫 번째 대각 성분의 절댓값입니다.”

벡터에 길이 측정선을 표시한다.

\\[ \\|Re_1\\|=|r\_{11}| \\]

화면의 해당 길이와 행렬 속 \\(r\_{11}\\)이 동시에 밝아지도록 한다.

[Linear Algebra (Part 5): Understanding Planes, Cross Products, and Distance in ℝ³ | by Amit Subhash Chejara | Data Science Collective | Medium](https://images.openai.com/static-rsc-4/a0yncJ_BJrh2yUfnz_sgcgDlIBrXAIqOovJHJs1Rn66uMMlpSBGCq5EnbjMS0JT4NfUH1Bmgbwxx9Z7DSlJr3o_U8ZpBst6zAyUizuCbqezVIBcfP_MDvvMUyBJ2MrIrbkMf7aCXCl5DunfvRvM8hGwvt-5-dLptl3UTJQXQPBM?purpose=inline)

컷 14 · 56\~60초

“두 번째 열벡터를 추가하면 평행사변형이 만들어집니다.”

두 번째 열벡터가 나타난다.

원래 첫 번째 축 방향으로도 성분을 갖고 있으므로, 벡터는 수직이 아니라 기울어진 방향으로 등장한다.

두 벡터가 만드는 평행사변형을 반투명하게 채운다.

컷 15 · 60\~65초

“이때 두 번째 벡터가 첫 번째 방향으로 얼마나 기울어져 있는지는 넓이에 영향을 주지 않습니다.”

평행사변형의 윗변을 좌우로 천천히 이동시킨다.

밑변 길이와 수직 높이는 고정하며, 넓이 표시도 일정하게 유지한다.

\\(r\_{12}\\) 계수를 변화시키는 애니메이션으로 연결하면 좋다.

화면: 기울기 변화 / 넓이 일정

[Área de un paralelogramo - Curriculum Nacional. MINEDUC. Chile.](https://images.openai.com/static-rsc-4/wS1anXbhISG6t6RgQPfSHT_NN0t-RGw_JqVipHsCzLWDDORAe-JCoa-8mgt3sZiA66ErISZ19-eJazkm04zuxHXNoM5vn_LxU8G_2t1fW5yZbTnzpevWP15w8xo-TJ0WGFXoOWHN0yi9PwjYm3Ch6Rwpo2AXcI1HL1Tqy8B8AOU?purpose=inline)

컷 16 · 65\~70초

“넓이를 결정하는 것은 밑변과 수직 높이입니다.”

기울어진 두 번째 벡터 끝에서 밑변이 놓인 직선까지 수직선을 내린다.

수직선에 초록색을 적용하고, \\(r\_{22}\\) 라벨을 표시한다.

\\[ S=|r\_{11}|\cdot|r\_{22}| \\]

여기서는 밑변과 높이가 양수인 길이임을 강조한다.

## D. 세 번째 대각 성분 — 부피의 완성 (70\~93초)

컷 17 · 70\~74초

“그리고 이 높이가 바로 R의 두 번째 대각 성분의 절댓값입니다.”

초록색 높이 \\(r\_{22}\\)를 강조한다.

평행사변형을 잠시 직사각형과 나란히 배치해 밑변과 높이의 곱이 같다는 것을 보여준다.

\\(R\\)의 \\(r\_{22}\\) 위치가 밝아진다.

컷 18 · 74\~78초

“따라서 평행사변형의 넓이는 첫 번째와 두 번째 대각 성분의 절댓값을 곱한 값입니다.”

행렬의 대각선 첫 두 성분을 강조한다.

\\[ S=|r\_{11}r\_{22}| \\]

도형의 전체 면적이 반투명 초록색으로 채워진다.

[Vektorová algebra | Analytická geometrie | Metodika výuky středoškolské matematiky | Přírodovědecká fakulta Masarykovy univerzity](https://images.openai.com/static-rsc-4/ya4ytOMwvPQm0FMNobT0LqrFMCTi-9RwrjXJMPgarUFDqDoCMFbhq81-1DqQeMiHFZpiswpbO4qobxkDf0NRDTlxE0CwcjM9oyO4vEccbHFvRNoYVpdNylVepjhlaUxnVXeQRyImdpkV3OBSrira2hRpxe4XDf1AuU-mcfHhcOA?purpose=inline)

컷 19 · 78\~82초

“이제 세 번째 열벡터를 추가해 보겠습니다.”

카메라가 평면에서 3차원 측면으로 회전한다.

세 번째 벡터가 평면 밖으로 나타나며 기존 평행사변형을 평행육면체로 확장한다.

컷 20 · 82\~87초

“평행육면체의 부피는 밑면의 넓이와 그 평면에서 벗어나는 수직 높이의 곱입니다.”

밑면은 초록색, 수직 높이는 주황색으로 강조한다.

세 번째 벡터 끝에서 밑면으로 수직선을 내린다.

\\[ V=S\cdot h \\]

카메라는 수직 높이를 확인할 수 있도록 약간 측면으로 이동한다.

[Spatprodukt: Herleitung, Berechnen & Beispiel | StudySmarter](https://images.openai.com/static-rsc-4/zKSqM8oFRtceCRa7xrpZv9WrPUNQ06Wji15nA2RJ-LJZHgvKisMTVpl56hKlEbDQPGRic0EU93wCV7k8ThVTFpIdphQWsKgz_qrsZZOkciOKBFOMenjjbxw27zVKVDwPWdKnfUKPLfVFpV3R9qIqQdOkBiDz-FXjdojPm9_A7AM?purpose=inline)

컷 21 · 87\~93초

“세 번째 벡터의 수직 높이는 R의 세 번째 대각 성분의 절댓값입니다.”

\\(R\\)의 세 번째 열에서 평면 안 성분을 흐리게 처리한다.

주황색 수직 성분만 남기고 \\(r\_{33}\\)와 연결한다.

\\[ h=|r\_{33}| \\]

이후 세 대각 성분을 모두 강조한다.

## E. 대각 성분의 곱과 행렬식 (93\~110초)

컷 22 · 93\~97초

“따라서 전체 부피는 R의 세 대각 성분의 절댓값을 곱한 값이 됩니다.”

세 수직 높이를 서로 다른 색으로 강조한다.

\\[ V=|r\_{11}r\_{22}r\_{33}| \\]

밑변 × 높이 × 높이의 대응을 시각적으로 보여준다.

컷 23 · 97\~100초

“R의 대각선 위쪽 계수들은 도형의 기울어진 형태를 바꿀 수 있지만…”

평행육면체의 윗면을 밑면과 평행하게 이동시켜 전단 변형을 보여준다.

\\(r\_{13},r\_{23}\\)을 변화시켜도 수직 높이는 그대로 유지한다.

기울기 변화 ≠ 부피 변화

컷 24 · 100\~103초

“…이 수직 높이들을 바꾸지는 않습니다.”

기울어진 평행육면체에서 수직 높이만 밝게 남긴다.

밑변 길이, 평면 내 수직 높이, 평면 밖 수직 높이를 순서대로 강조한다.

컷 25 · 103\~106초

“결국 A의 행렬식의 절댓값은 R의 대각 성분들의 절댓값을 곱한 값과 같습니다.”

다음 수식을 화면 중앙에 크게 표시한다.

\\[ \boxed{|\det A|=|r\_{11}r\_{22}r\_{33}|} \\]

왼쪽에는 \\(A\\)의 평행육면체, 오른쪽에는 \\(R\\)의 평행육면체를 나란히 표시하고 두 도형의 부피가 일치함을 보여준다.

컷 26 · 106\~109초

“행렬식이 공간의 부피 변화를 나타낸다면, QR 분해는 그 부피 변화가 각각의 독립 방향에서 어떻게 만들어지는지를 보여줍니다.”

처음의 단위 정육면체와 마지막 평행육면체를 겹쳐 보여준다.

이어 세 가지 수직 높이로 부피가 설명되는 과정을 빠르게 재생한다.

컷 27 · 109\~110초 이후 마무리

중앙에 \\(A=QR\\)을 남기고 마지막 문구를 표시한다.

행렬식은 전체 부피를, QR 분해는 그 부피의 기하학적 구성을 보여준다.

## 3. 편집에서 반드시 수정할 부분

위 콘티는 개념 전개를 자세히 분리한 버전이야. 다만 현재 대본은 실제 낭독 속도에 따라 110초보다 길어질 수 있어. 음성 파일의 확정 타임코드가 없다면 위 컷들의 초 단위는 임시 배분으로 보고, 음성과 싱크를 맞출 때 조정해야 해.

특히 영상의 완성도를 좌우할 세 가지가 있어.

첫째, \\(A=QR\\)의 변환 순서를 정확히 보여줘야 해. 벡터에 적용할 때 \\(R\\)이 먼저, \\(Q\\)가 나중이야. \\(Q\\)가 부피를 보존하므로 \\(A\\)와 \\(R\\)의 부피 배율이 같다는 설명도 이 순서를 따라야 자연스러워.

둘째, 평행사변형과 평행육면체에서의 전단 변형을 구분해야 해. 두 번째 열의 첫 방향 성분 \\(r\_{12}\\)는 평행사변형의 기울기를 바꾸고, \\(r\_{13},r\_{23}\\)은 세 번째 벡터의 밑면 내 위치를 바꿔. 이때 대각 성분을 고정하면 부피는 일정하게 유지돼.

셋째, 직교 높이와 대각 성분을 직접 대응시켜야 해. 단순히 대각선을 강조하는 것만으로는 부족해. 공간 속 밑변 길이 \\(r\_{11}\\), 평면 안 수직 높이 \\(r\_{22}\\), 평면 밖 수직 높이 \\(r\_{33}\\)에서 각각 행렬의 해당 위치로 연결선을 이어주는 연출이 가장 효과적이야.

이 영상은 단순한 행렬식 설명에서 끝나지 않고, 왜 QR 분해의 삼각 구조가 부피 계산을 쉽게 만들어 주는지까지 이해시키는 것이 목표야. 행렬식을 배운 사람이 QR 분해를 통해 그 기하학적 의미를 다시 발견하는 경험을 주면 좋겠어.