# GPU 계층 구조 LEVEL 07 — Shared Memory 상세 영상화 콘티

총 160초 (2분 40초) · 9:16 쇼츠 · 메모리 계층 2편 · CUDA 코드와 하드웨어 구조 연동

이번 편의 핵심은 Shared Memory가 단순히 빠른 메모리가 아니라, 같은 Block의 스레드들이 서로 데이터를 주고받고 반복해서 사용할 수 있게 하는 공간이라는 점이야.

시각화는 세 단계로 발전시키는 것이 좋아.

1. Thread 간 공유: Thread 5가 Thread 6의 데이터를 읽는 과정
2. 동기화: 아직 기록되지 않은 데이터를 읽지 않도록 `__syncthreads()`를 사용하는 과정
3. 데이터 재사용: 행렬곱의 입력 Tile을 Shared Memory에 저장하고 여러 스레드가 반복 사용하는 과정

## 1. 기본 화면 구조

GPU HIERARCHY / LEVEL 07

SHARED MEMORY

CUDA SOURCE

\_\_shared\_\_ float s[128];\
s[t] = A[t];\
\_\_syncthreads();\
B[t] = s[(t + 1) % 128];

구조 개념도. 실제 공유 메모리는 SM의 하드웨어 자원이며, Block 0에 할당된 영역을 논리적으로 구분해 보여주는 장면이야.

### 공통 제작 규칙

- 기존 LEVEL 01\~06의 GPU·SM·Block·Warp·Thread 구조 및 번호 유지
- Register File은 보라색, Shared Memory는 청록색으로 일관되게 표현
- Thread 5는 녹색, Thread 6은 주황색으로 강조해 데이터 이동을 추적
- CUDA 코드 패널은 구조도 아래 또는 옆에 배치하고, 강조하는 코드 줄만 크게 표시
- 코드에 줄 번호를 넣지 않고 화면마다 1\~4줄만 표시
- 코드상의 공유 메모리 배열과 SM의 물리적 Shared Memory를 연결하되, 서로 다른 Block에는 별도의 논리적 배열이 존재하도록 표시

## 2. 기본 CUDA 코드

전반부의 동기화·데이터 공유 설명에 사용할 코드야.

```

__global__ void neighborRead(
    const float* A,
    float* B
) {
    __shared__ float s[128];

    int t = threadIdx.x;

    s[t] = A[t];

    __syncthreads();

    B[t] = s[(t + 1) % 128];
}

// 설명용 실행 조건
// 하나의 Block, 128개 Thread
neighborRead<<<1, 128>>>(d_A, d_B);

```

이 코드는 실제로 동작하는 128개 Thread의 단일 Block 예시야. 입력과 출력 배열은 최소 128개 원소를 가진다고 가정해.

Thread 5는 `s[5]`에 저장하고 `s[6]`을 읽으며, Thread 6은 `s[6]`에 저장하고 `s[7]`을 읽어. 이처럼 쓰는 위치와 읽는 위치가 다르다는 점을 시각화해야 해.

## 3. 시간별 상세 콘티

### SCENE 01 — Register에서 Shared Memory로 (0\~27초)

0\~5초 — Register 복습

LEVEL 06에서 사용한 SM 구조도가 등장해.

각 Thread가 Register File에 할당된 자원을 사용하며 자신의 계산값을 보관하는 모습을 짧게 보여줘.

5\~14초 — 다른 스레드의 데이터가 필요하다면?

Thread 5와 Thread 6을 강조해.

Thread 5가 Thread 6의 계산값을 필요로 하는 상황을 표현하지만, Thread 6의 레지스터를 직접 읽는 연결선에는 제한 표시를 넣어.

이어서 Shared Memory가 SM 내부에 나타나.

14\~19초 — Shared Memory 정의

Block 0에 할당된 Shared Memory 영역을 확대해.

19\~27초 — Register와 Shared Memory 비교

Register

개별 Thread의 계산값 보관

Shared Memory

같은 Block의 스레드 간 데이터 공유·재사용

마지막에는 Register와 Shared Memory를 동시에 보여주되, 카메라의 중심은 Shared Memory에 남겨둬.

### SCENE 02 — CUDA 코드와 Shared Memory 선언 (27\~40초)

27\~29초

코드 패널이 화면 오른쪽에 나타나고, GPU 구조도는 왼쪽에 유지해.

29\~35초

```
__shared__ float s[128];

int t = threadIdx.x;
```

`__shared__`를 강조하면 Shared Memory 영역이 밝아지고, `s[128]`을 강조하면 128개의 원소를 저장할 수 있는 논리적 배열이 나타나도록 해.

35\~40초

```
s[t] = A[t];
```

각 Thread가 Global Memory의 서로 다른 원소를 읽어 Shared Memory의 해당 위치에 저장하는 모습을 보여줘.

화면에는 `A[t] → s[t]`를 표시해.

### SCENE 03 — Thread 5와 Thread 6의 데이터 공유 (40\~54초)

Thread 간 데이터 공유 시뮬레이션

저장읽기

Thread 5

s[5] = A[5]

Thread 6

s[6] = A[6]

Shared Memory

s[0]

s[1]

s[2]

s[3]

s[4]

s[5]

s[6]

s[7]

Thread 5와 Thread 6이 각각 자신의 인덱스 위치에 데이터를 저장

40\~45초 — 각각 다른 위치에 저장

Thread 5가 `s[5]`, Thread 6이 `s[6]`에 저장하는 모습을 보여줘.

45\~49초 — Thread 5가 Thread 6의 값 읽기

Thread 5에서 Shared Memory의 `s[6]`으로 연결선을 이동시켜.

49\~54초 — 공유 가능 범위 설명

Block 0 내부의 여러 Thread가 동일한 배열을 읽고 쓸 수 있다는 점을 강조해.

이때 별도의 Block 1을 흐릿하게 보여주고, Block 0의 Shared Memory에 직접 접근하지 않는다는 것을 함께 나타내도 좋아.

### SCENE 04 — 데이터 준비와 `__syncthreads()` (54\~75초)

이번 편에서 가장 중요하게 제작해야 할 장면 중 하나야.

54\~59초 — 아직 값이 저장되지 않은 상황

Thread 5가 `s[6]`을 읽으려는 상황을 보여줘.

그런데 Thread 6은 아직 `s[6]`에 값을 기록하지 않은 상태로 표시해.

이때 화면에는 `Read before write?`라는 경고 문구를 표시해.

59\~62초 — 동기화 등장

코드에서 `__syncthreads()`를 강조해.

62\~70초 — Block 단위 동기화

128개의 Thread가 동기화 지점에 도달하는 과정을 보여줘. 먼저 도달한 Thread들은 기다리고, 마지막 Thread까지 도달하면 다음 단계가 진행되는 연출이야.

70\~75초 — 안전한 데이터 읽기

모든 Thread가 저장을 마친 뒤 `B[t] = s[(t + 1) % 128];`가 실행되는 모습을 보여줘.

Block 동기화 과정

\_\_syncthreads()

저장 중동기화읽기

Thread 5

저장 완료

Thread 6

저장 진행 중

데이터가 아직 준비되지 않을 수 있음

중요한 점은 `__syncthreads()`를 모든 Thread가 정확히 동시에 같은 명령을 실행하는 장면으로 표현하지 않는 것이야.

먼저 도착한 Thread가 기다리고, 필요한 스레드들이 도착한 후 진행할 수 있다는 것이 정확한 표현이야.

### SCENE 05 — Shared Memory의 진짜 최적화 가치: 데이터 재사용 (75\~113초)

이 장면에서는 앞서 보여준 단순 데이터 교환에서 실제 연산 최적화로 넘어가야 해.

75\~84초 — 단순 공유에서 재사용으로

Thread 5와 Thread 6의 예시를 축소하고, 큰 행렬 A와 B를 화면에 등장시켜.

`Data Sharing → Data Reuse`

84\~92초 — 행렬곱에서 같은 입력값이 반복 사용

출력 행렬 C의 여러 원소를 강조해.

예를 들어 C의 같은 행에 속하는 출력 원소들이 A의 같은 행 데이터를 필요로 한다는 것을 보여줘.

92\~99초 — 입력 데이터를 Shared Memory로 가져오기

Global Memory에 있는 A와 B의 작은 Tile을 선택해 Shared Memory로 이동시키는 모습을 보여줘.

99\~109초 — Tile 재사용

Shared Memory에 로드된 데이터를 여러 Thread가 반복해서 읽어 서로 다른 출력값을 계산하는 모습을 보여줘.

109\~113초 — Global Memory Load 감소

기존 방식과 Tile 재사용 방식을 비교해 중복 데이터 로드가 줄어드는 것을 표현해.

행렬곱의 Tile 재사용

직접 읽기Shared Memory

Global Memory

반복 Global Load

여러 Thread가 각자 필요한 입력을 읽는 접근 방식

이 장면에서는 단순히 Shared Memory가 Global Memory보다 빠르다는 설명보다, 같은 데이터를 여러 번 Global Memory에서 요청하지 않도록 재사용 패턴을 바꾼다는 점에 집중하는 것이 좋아.

실제 CUDA 코드는 전체 GEMM 커널을 길게 보여주기보다는 다음 부분만 발췌하면 충분해.

```
__shared__ float As[T][T];
__shared__ float Bs[T][T];

// 각 Thread가 입력 Tile 일부 로드
As[ty][tx] = A[...];
Bs[ty][tx] = B[...];

__syncthreads();
```

여기의 `...`은 인덱스 계산을 생략한 설명용 코드로 표시하고, 실행 가능한 완성 코드인 것처럼 연출하지 않아야 해.

### SCENE 06 — Shared Memory의 제한된 용량 (113\~123초)

113\~116초

Shared Memory 영역 전체에 `Limited On-Chip Capacity` 문구가 등장해.

116\~123초

하나의 Block이 많은 Shared Memory를 사용하는 상황을 보여줘. SM 내부의 공유 메모리 자원이 더 많이 점유되면서 동시에 상주 가능한 다른 Block의 수가 줄어들 수 있음을 표현해.

6편 Register Pressure와 같은 구조로 연출하면 시리즈의 연결성이 높아져.

### SCENE 07 — Bank Conflict (123\~135초)

이 부분은 시간이 짧기 때문에 Bank의 구조와 충돌 현상만 보여주고 해결 방법은 후속 GPU 최적화 영상으로 남기는 편이 적절해.

123\~126초

Shared Memory를 여러 Bank로 나누어 표시해.

126\~133초

Warp의 서로 다른 Thread가 서로 다른 주소를 요청하지만, 그 주소들이 같은 Bank에 대응되는 상황을 보여줘.

133\~135초

`Bank Conflict` 텍스트가 등장하고 해당 접근이 여러 단계로 처리되는 모습을 보여줘.

Bank Conflict — 개념적 접근 패턴

충돌 없음Bank Conflict

설명용 4-Lane·4-Bank 모형. 실제 일반적인 NVIDIA Shared Memory는 32개 Bank로 구성돼. 동일 주소 브로드캐스트 등은 충돌의 예외야.

이 장면에서 각 Bank를 물리적인 독립 메모리 칩처럼 표현하면 안 돼. Shared Memory의 주소들이 Bank로 나뉘어 접근된다는 개념을 보여주면 충분해.

### SCENE 08 — 최종 정리 (135\~160초)

135\~144초

지금까지 등장한 Shared Memory의 장점과 제약을 나란히 보여줘.

장점

Thread 간 데이터 공유

데이터 재사용

중복 Global Load 감소 가능

제약

제한된 용량

동기화 비용

Bank Conflict

144\~152초

Register와 Shared Memory를 마지막으로 비교해.

Register File은 Thread의 계산값을 유지하는 자원으로, Shared Memory는 Block 내부의 데이터 공유와 재사용을 지원하는 자원으로 강조해.

152\~160초

카메라가 SM에서 GPU 전체로 줌아웃되며, 여러 Block이 각각 자신의 Shared Memory 데이터를 활용해 계산하는 모습을 보여줘.

마지막 화면 문구는 다음과 같이 추천해.

GPU Performance = Computation + Efficient Data Movement

## 4. 제작 시 기술적으로 주의할 사항

| 구분                | 주의할 점                                |
| ----------------- | ------------------------------------ |
| `__shared__`      | 같은 Block이 접근하는 공유 저장 공간              |
| Shared Memory     | SM의 물리 자원이지만 Block별 논리적 데이터 영역은 분리   |
| `__syncthreads()` | Block 단위 배리어와 메모리 가시성 보장             |
| Thread 간 공유       | 다른 Thread의 레지스터를 직접 읽는 것이 아님         |
| Tiling            | Global Memory 요청의 중복을 줄이기 위한 데이터 재사용 |
| Bank Conflict     | 서로 다른 주소가 같은 Bank에 매핑되어 접근이 분할되는 경우  |
| 성능                | Shared Memory 사용만으로 속도 향상을 보장하지 않음   |

특히 54\~75초에서 `__syncthreads()`를 설명할 때는, 모든 스레드가 해당 배리어에 참여하는 정상적인 코드 경로를 전제로 해. 일부 스레드가 배리어에 도달하지 않는 부적절한 분기 구조를 예시로 사용하면 안 돼.

## 5. 최종 제작 우선순위

완성도를 가장 높여야 할 구간은 두 곳이야.

40\~75초 — 공유와 동기화

Thread 5가 `s[5]`에 저장하고, Thread 6이 `s[6]`에 저장한 뒤, 동기화를 거쳐 Thread 5가 `s[6]`을 읽는 흐름이 정확해야 해. 이 과정에서 서로 다른 Thread가 하나의 공유 메모리 배열을 사용하는 이유가 명확해져.

84\~113초 — 행렬곱과 Tiling

같은 입력 데이터가 여러 출력값 계산에 재사용된다는 관계를 먼저 보여준 다음, 해당 데이터를 Shared Memory Tile에 저장해 반복 사용하는 방식으로 발전시켜야 해.

이번 7편의 결론은 Shared Memory는 스레드 간 데이터 교환을 위한 공간이면서, 계산에 필요한 데이터를 반복해서 멀리 가져오는 비용을 줄이기 위한 핵심 자원이라는 것이야.

다음 Global Memory 편에서는 이 데이터가 원래 어디에 저장되어 있고, GPU가 어떻게 읽어오는지를 다루면 메모리 계층의 흐름이 자연스럽게 이어져.