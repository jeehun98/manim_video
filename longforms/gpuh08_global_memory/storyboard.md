# GPU 계층 구조 LEVEL 08 — Global Memory & Coalescing 상세 영상화 콘티

총 165초 (2분 45초) · 9:16 쇼츠 · CUDA 코드와 GPU 하드웨어 연동 · 메모리 계층 3편

이번 영상에서 가장 중요한 것은 32개 스레드가 동일하게 128바이트를 읽어도, 접근 주소에 따라 필요한 메모리 섹터가 4개에서 32개로 증가하는 과정이야.

기존 6\~7편과 동일한 GPU·SM·Warp·Thread 구조도를 유지하면서, 이번에는 스레드별 데이터 주소를 메모리 섹터와 직접 연결하는 방식으로 제작하는 게 좋아.

## 1. 영상 전체 구성

| 구간        | 내용                      | 핵심 시각화                        |
| --------- | ----------------------- | ----------------------------- |
| 0\~26초    | Global Memory의 위치와 역할   | Register → Shared → Global    |
| 26\~48초   | CUDA 코드와 데이터 이동         | A·B Load → Register → C Store |
| 48\~65초   | Warp의 메모리 접근            | 32 Thread × 4B = 128B         |
| 65\~81초   | 연속 접근                   | 4개의 32B Sector                |
| 81\~109초  | Stride 8 접근             | 32개의 32B Sector               |
| 109\~127초 | Memory Coalescing       | 주소 패턴과 요청 병합                  |
| 127\~149초 | 성능 해석과 Bank Conflict 비교 | 섹터 수 ≠ 실행시간                   |
| 149\~165초 | 전체 구조 정리                | Global Memory와 주소 배치          |

## 2. 메인 화면 구조

GPU HIERARCHY / LEVEL 08

GLOBAL MEMORY

CUDA SOURCE

float a = A[i];\
float b = B[i];\
C[i] = a + b;

기본 구조도. 실제 Global Memory Load는 캐시에 의해 처리될 수도 있으므로 모든 요청이 반드시 DRAM까지 이동하는 모습으로 표현하지 않아야 해.

### 시리즈 공통 제작 기준

- 기존 GPU → SM → Block → Warp → Thread 구조와 색상 유지
- Register는 보라색, Shared Memory는 청록색, Global Memory는 황금색으로 구분
- 이번 편의 핵심인 메모리 섹터는 별도 격자로 확대
- Lane 0\~31과 접근 주소의 대응이 유지되도록 애니메이션 제작
- CUDA 코드는 필요한 부분만 노출하고, 관련 스레드와 메모리 주소를 같은 색상으로 강조
- `128B 유효 데이터`, `32B Sector`, `섹터 기준 처리량`을 서로 다른 라벨로 표시
- 섹터 수는 실제 DRAM 요청 횟수나 실행시간으로 직접 치환하지 않음

## 3. CUDA 코드 구성

기본 데이터 이동에는 기존 Vector Addition 커널을 활용해.

```

__global__ void vectorAdd(
    const float* A,
    const float* B,
    float* C,
    int N
) {
    int i = blockIdx.x * blockDim.x
          + threadIdx.x;

    if (i < N) {
        float a = A[i];
        float b = B[i];
        C[i] = a + b;
    }
}

```

Memory Coalescing 비교에는 별도의 두 Load 패턴을 보여줘.

연속 접근

```
float x = A[i];
```

Stride 8 접근

```
float x = A[i * 8];
```

두 번째는 첫 번째 코드를 그대로 실행한 결과가 아니라 메모리 주소 접근 패턴을 비교하기 위한 별도 예시야.

## 4. 시간별 상세 콘티

### SCENE 01 — Register와 Shared Memory에서 Global Memory로 (0\~26초)

0\~8초 — 이전 메모리 계층 복습

SM 내부를 확대해 Register File과 Shared Memory를 차례로 강조해.

- Register: 스레드의 계산값
- Shared Memory: Block 내부 데이터 공유

8\~15초 — 대규모 데이터는 어디에 저장될까?

카메라가 SM 바깥으로 줌아웃되고, GPU 전체와 디바이스 메모리 영역이 등장해.

`Global Memory`가 GPU의 대규모 데이터 저장 공간으로 표시돼.

15\~21초 — 여러 SM에서 접근

SM 0\~3에서 Global Memory에 존재하는 동일한 대규모 배열을 참조하는 연결선을 보여줘.

21\~26초 — 용량과 접근 지연

Register·Shared·Global을 비교하면서 Global Memory의 상대적으로 큰 용량과 높은 접근 지연을 강조해.

GPU 메모리 계층 — 개념적 비교

| Register      | 스레드 계산값        | 매우 작은 용량   |
| ------------- | -------------- | ---------- |
| Shared Memory | Block 데이터 공유   | 제한된 온칩 용량  |
| Global Memory | GPU 전체 대규모 데이터 | 상대적으로 큰 용량 |

### SCENE 02 — CUDA 코드에서 Global Memory가 사용되는 방법 (26\~48초)

26\~34초 — 두 배열 읽기

코드 패널에서 다음 두 줄을 강조해.

```
float a = A[i];
float b = B[i];
```

Global Memory의 A·B 배열에서 해당 스레드의 데이터가 읽혀 계산에 사용되는 모습을 보여줘.

34\~41초 — 덧셈과 출력

`C[i] = a + b;`를 강조해.

읽어온 값이 연산에 사용되고 결과가 Global Memory의 C 배열에 저장되는 흐름을 보여줘.

41\~48초 — Load → Compute → Store

Global Memory

A[i], B[i]

Compute

Registers / ALU

Global Memory

C[i]

화면에서 값이 Register에 남을 수 있다는 점을 표현하되, 모든 지역 변수에 고정적인 Register 하나씩을 배정하지는 않아야 해.

### SCENE 03 — Warp의 32개 Thread가 데이터를 읽는다면? (48\~65초)

48\~56초

다시 Warp 0을 확대해. 32개 Lane이 일렬로 배열되고 각 Lane에 하나의 4B Load 명령을 표시해.

56\~60초

`Warp = 32 Threads`가 등장해.

60\~65초

`32 × 4B = 128B`라는 식이 나타나.

이후의 모든 비교 장면에서 유효 데이터 128B를 고정하는 것이 중요해.

Warp 0 — 32개의 float32 읽기

L0

4B

L1

4B

L2

4B

L3

4B

L4

4B

L5

4B

L6

4B

L7

4B

L8

4B

L9

4B

L10

4B

L11

4B

L12

4B

L13

4B

L14

4B

L15

4B

L16

4B

L17

4B

L18

4B

L19

4B

L20

4B

L21

4B

L22

4B

L23

4B

L24

4B

L25

4B

L26

4B

L27

4B

L28

4B

L29

4B

L30

4B

L31

4B

## 32 × 4B = 128B

### SCENE 04 — 연속 주소 접근: 4개의 Sector (65\~81초)

이 장면은 다음 Stride 8 비교의 기준이 되므로, 주소 격자의 크기와 배열 구조를 고정한 상태에서 접근 패턴만 바꾸는 것이 좋아.

65\~70초 — 연속 주소

화면 위쪽에는 Lane 0\~31, 아래쪽에는 Global Memory 배열 A를 배치해.

Lane 0은 `A[0]`, Lane 1은 `A[1]`, 마지막 Lane 31은 `A[31]`을 읽어.

각 Lane에서 해당 배열 주소로 연결선을 그려줘.

70\~76초 — 128바이트의 연속 영역

32개 원소를 8개씩 묶어 네 그룹으로 표시해.

각 원소가 4바이트이므로 한 그룹은 32바이트야.

76\~81초 — Sector 4개

네 그룹을 각각 하나의 32B Sector로 강조하고, 코드 패널에는 `float x = A[i];`를 보여줘.

Coalesced Access — Stride 1

4 Sectors

Sector 0

0

1

2

3

4

5

6

7

32B

Sector 1

8

9

10

11

12

13

14

15

32B

Sector 2

16

17

18

19

20

21

22

23

32B

Sector 3

24

25

26

27

28

29

30

31

32B

유효 데이터 128B

4 × 32B = 128B

이 수치는 배열의 시작 주소가 적절하게 정렬된 상황을 전제로 해. 정렬 상태가 다르면 연속된 접근도 더 많은 섹터를 필요로 할 수 있어.

### SCENE 05 — Stride 8: 32개의 Sector (81\~109초)

이번 영상에서 가장 시각적인 효과가 강해야 하는 구간이야.

81\~86초 — 코드 변경

코드 패널에서 `A[i]`를 `A[i * 8]`로 바꿔.

Lane 수와 Thread당 읽는 데이터 크기는 그대로 유지해.

86\~92초 — 같은 128바이트

Lane 0\~31이 각각 4바이트씩 요청하는 모습을 유지해.

다만 배열에서 선택되는 원소의 위치가 8칸씩 벌어져.

92\~100초 — 서로 다른 섹터

Lane 0은 A[0], Lane 1은 A[8], Lane 2는 A[16]에 접근하는 식이야.

32바이트 섹터 하나에는 float32 원소 8개가 들어가므로, 각 Lane이 서로 다른 섹터에 접근하는 모습이 나타나.

100\~103초 — 4개에서 32개로 증가

기존 연속 접근 화면과 Stride 8 화면을 나란히 배치해.

103\~109초 — 섹터 기준 요청량 비교

메모리 접근 패턴 비교

Stride 1Stride 8

32B Sector 주소 맵

S0

S1

S2

S3

S4

S5

S6

S7

S8

S9

S10

S11

S12

S13

S14

S15

S16

S17

S18

S19

S20

S21

S22

S23

S24

S25

S26

S27

S28

S29

S30

S31

파란색은 Warp에서 적어도 하나의 원소를 요청한 섹터

유효 데이터

## 128B

접근 섹터

## 4개

섹터 기준

## 128B

기준 주소가 32B 경계에 정렬된 32개 활성 Lane의 float32 읽기 예시야. 섹터 기준 수치이며 실제 DRAM 전송량을 그대로 뜻하지 않아.

최종 화면 비교는 다음처럼 명확하게 표현해.

| 조건         | 연속 접근 | Stride 8 |
| ---------- | ----- | -------- |
| 활성 Lane    | 32개   | 32개      |
| Lane당 요청   | 4B    | 4B       |
| 유효 데이터     | 128B  | 128B     |
| 필요한 섹터     | 4개    | 32개      |
| 섹터 기준 데이터량 | 128B  | 1,024B   |

화면의 숫자가 128B에서 1,024B로 바뀌는 순간에도 유효 데이터 128B는 변하지 않는다는 표시가 남아 있어야 해.

### SCENE 06 — Memory Coalescing의 의미 (109\~127초)

109\~117초

화면에 `Memory Coalescing`을 크게 표시해.

이전의 32개 Lane과 주소 맵을 다시 불러오고, Warp의 주소 요청이 필요한 섹터 단위로 처리되는 모습을 보여줘.

여기서 모든 메모리 요청이 반드시 하나의 트랜잭션으로 합쳐지는 것처럼 표현하면 안 돼.

117\~122초

두 접근 방식이 같은 연산량과 같은 유효 데이터량을 가진다는 점을 강조해.

122\~127초

주소 패턴에 따라 필요한 메모리 섹터 수가 달라진다는 결론을 강조해.

화면 문구:

Same Useful Data, Different Memory Traffic

추가로 흥미로운 장면을 넣고 싶다면, Lane이 데이터를 요청하는 순서를 뒤섞더라도 접근 주소들이 동일한 네 개 섹터 안에 모여 있으면 네 개 섹터로 처리될 수 있다는 모습을 짧게 보여줘. 즉, Coalescing의 핵심은 Lane 번호가 반드시 오름차순 주소에 대응하는 것이 아니라 요청 주소들이 얼마나 적은 섹터에 모여 있는가라는 점이야.

### SCENE 07 — 섹터 수가 8배면 성능도 8배 차이 날까? (127\~137초)

127\~132초

연속 접근의 4 Sector와 Stride 8의 32 Sector를 나란히 보여줘.

그 아래에 다음 문구를 표시해.

`8× Sector Footprint ≠ 8× Execution Time`

132\~137초

GPU 메모리 구조에서 L1 Cache, L2 Cache, Device DRAM을 차례로 강조해.

캐시 적중 여부, 메모리 대역폭, 다른 연산에 의해 실제 실행시간이 영향을 받는다는 사실을 전달해.

여기서는 추정 실행시간 그래프를 만들지 않는 편이 좋아. 대신 섹터 수와 실행시간이 서로 다른 성능 지표라는 것을 명확하게 전달해.

### SCENE 08 — Bank Conflict와 Memory Coalescing 비교 (137\~149초)

앞선 LEVEL 07과 연결되는 장면이야.

137\~143초

화면을 좌우로 나눠.

왼쪽에는 Shared Memory와 Bank Conflict, 오른쪽에는 Global Memory와 Memory Coalescing을 보여줘.

143\~149초

두 현상의 차이를 메모리 구조에 직접 대응시켜.

Bank Conflict

Shared Memory

서로 다른 주소가 같은 Bank에 집중

Coalescing

Global Memory

요청 주소가 여러 Sector에 분산

두 그림 모두 원리를 축약한 모형이야. Bank Conflict는 Bank 접근 경합, Coalescing은 필요한 전역 메모리 섹터 수에 관한 개념이야.

이 비교가 좋은 이유는, 둘 다 Warp의 스레드들이 어떤 주소에 접근하는가와 관련 있지만 그 주소를 처리하는 하드웨어 구조가 서로 다르다는 것을 보여주기 때문이야.

### SCENE 09 — 최종 정리 (149\~165초)

149\~158초

카메라가 Sector 확대 화면에서 다시 GPU 전체로 돌아와.

Global Memory와 SM들을 연결하고, 각 SM의 Warp에서 전역 메모리로 주소 요청이 발생하는 모습을 보여줘.

이번에는 일부 요청이 연속된 주소에 모여 있고, 다른 일부는 흩어져 있는 모습을 보여줘.

158\~165초

전체 GPU 구조 위에 마지막 문구를 띄워.

Global Memory — Address Pattern Matters

그리고 바로 아래에:

`Same Computation · Different Memory Efficiency`

마지막 장면에서도 Global Memory가 메인 하드웨어 주제라는 점을 유지해. Memory Coalescing은 그 공간을 효율적으로 사용하는 핵심 원리로 배치하면 돼.

## 5. 영상의 정확성을 위한 체크포인트

| 항목                | 주의 사항                            |
| ----------------- | -------------------------------- |
| Global Memory     | GPU 전체에서 접근할 수 있는 논리적 주소 공간      |
| Device DRAM       | 일반적인 Global Memory 데이터의 물리 저장 공간 |
| 32B Sector        | 이 영상에서 사용할 NVIDIA GPU 메모리 접근 모델  |
| 4 Sector          | 32개 Lane의 정렬된 연속 float32 접근 예시   |
| 32 Sector         | 32개 Lane의 Stride 8 float32 접근 예시 |
| 1,024B            | 32개의 32B 섹터에 해당하는 데이터량           |
| Memory Coalescing | Warp 주소들을 필요한 메모리 접근으로 묶어 처리     |
| 성능                | 섹터 수와 실제 실행시간은 일대일로 비례하지 않음      |

특히 한 가지는 반드시 지켜야 해.

Stride 8에서 접근하는 주소들이 1,024바이트 전체에 퍼져 있다는 것과 실제로 1,024바이트 모두가 연산에 사용된다는 것은 달라.

실제 사용하는 데이터는 128바이트이고, 필요한 섹터가 32개라는 것이 정확한 설명이야.

## 6. 최종 제작 우선순위

이번 편에서는 세 구간의 완성도가 가장 중요해.

첫 번째: 26\~48초 — 데이터 이동

CUDA 코드의 `A[i]`, `B[i]`, `C[i]`를 실제 Global Memory와 연결해. 처음부터 Memory Coalescing으로 넘어가지 않고 Global Memory의 기본적인 역할을 명확하게 소개해야 해.

두 번째: 65\~109초 — 핵심 비교

32개의 Lane, 유효 데이터 128바이트, 32바이트 Sector라는 조건을 고정하고 접근 주소만 바꾸었을 때 필요한 섹터 수가 4개에서 32개로 달라지는 과정을 정확하게 시각화해.

세 번째: 137\~149초 — Bank Conflict와 비교

앞선 7편의 Shared Memory 개념과 연결하되, 서로 다른 하드웨어 메커니즘임을 구분해야 해.

이렇게 구성하면 8편은 Global Memory의 기본적인 역할을 설명하면서도, 메모리 주소 접근 패턴이 GPU 성능에 영향을 주는 이유를 하나의 구체적인 실험으로 보여주는 영상이 돼.