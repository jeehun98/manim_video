# GPU 계층 구조 LEVEL 11 — 최종 통합편 상세 영상화 콘티

총 191초 (3분 11초) · 9:16 세로 영상 · LEVEL 01\~10 통합 · 벡터 덧셈 CUDA 커널

이번 영상의 핵심은 하나의 CUDA 코드가 GPU의 논리적 실행 구조, 실제 연산 하드웨어, 메모리 계층과 어떻게 연결되는지 보여주는 거야.

기존 10편에서 설명한 개념을 순서대로 다시 소개하기보다는, `C[i] = A[i] + B[i]`라는 하나의 연산을 끝까지 추적하는 방식이 더 적합해.

## 1. 전체 영상 구성

| 시간        | 구간                | 핵심 화면                                   |
| --------- | ----------------- | --------------------------------------- |
| 0\~18초    | 시리즈 구조 총정리        | 실행 계층 + 메모리 계층                          |
| 18\~53초   | CUDA의 논리적 실행 구조   | Grid → Block → Warp → Thread            |
| 53\~81초   | 실제 하드웨어 실행        | SM · Warp Scheduler · Register · Shared |
| 81\~115초  | 데이터 읽기와 저장        | Global Memory · L1/L2 · DRAM            |
| 115\~133초 | 하나의 계산과 대규모 병렬 실행 | 여러 Thread의 벡터 덧셈                        |
| 133\~151초 | 자원과 데이터 이동의 제약    | Occupancy · Memory Access               |
| 151\~191초 | 전체 연결 및 시리즈 마무리   | 논리적 실행 → 물리적 연산 → 데이터 공급                |

## 2. 영상의 공통 기준

### 실제 코드

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
        C[i] = A[i] + B[i];
    }
}

int blockSize = 128;
int gridSize = (N + blockSize - 1) / blockSize;

vectorAdd<<<gridSize, blockSize>>>(A, B, C, N);

```

영상의 모든 장면은 이 커널을 기준으로 구성해.

시각화 예시는 `N = 512`, `blockSize = 128`, `gridSize = 4`로 설정하면 좋아. 따라서 4개 Block, 각 Block의 128개 Thread, 각 Block의 4개 Warp, 총 512개 Thread가 돼.

단, 이는 이해를 위한 축소된 실행 예시이고 실제 GPU의 SM 개수와 실행 동시성을 그대로 나타내지는 않아.

### 공통 색상과 공간 구분

| 요소                   | 색상       | 표현 방식              |
| -------------------- | -------- | ------------------ |
| Grid                 | 흰색 또는 회색 | 커널 전체 외곽선          |
| Block                | 파란색      | 128 Thread의 논리적 집합 |
| Warp                 | 보라색      | 32 Thread 묶음       |
| Thread               | 청록색      | 개별 계산 담당           |
| SM                   | 진한 파란색   | 실제 연산 하드웨어         |
| Register             | 연보라색     | Thread별 계산값        |
| Shared Memory        | 녹색       | Block 내부 공유 데이터    |
| L1 / L2 Cache        | 하늘색      | 캐시 저장 계층           |
| Global Memory / DRAM | 주황색      | 배열 A·B·C의 데이터      |
| Memory Controller    | 금색       | DRAM 접근 제어         |

가장 중요한 연출 규칙: Grid·Block·Warp·Thread는 논리적 실행 구조이고, SM은 물리적 하드웨어라는 점을 모든 장면에서 유지해야 해. Block을 SM 내부에 배치하는 장면은 실제로는 논리적인 Block의 자원이 SM에 할당되어 실행되는 것을 나타내.

## 3. 메인 통합 시각화

하나의 CUDA 커널이 사용하는 GPU 구조

최종 구조도의 하드웨어 측면. CUDA Grid·Block·Warp·Thread는 위의 SM 구조와 별도로 등장한 뒤 실행 매핑으로 연결해.

이 구조도를 영상 전체에서 일관되게 유지하고, 해당 타임코드에 필요한 부분만 확대하거나 강조하는 방식이 좋아. 특히 50초 이후에는 새로운 구조도를 계속 교체하기보다 동일한 그림에서 카메라를 이동시켜야 시청자가 위치 관계를 잃지 않아.

## 4. 시간별 상세 영상화 콘티

### SCENE 01 — 지금까지 살펴본 GPU의 계층 (0\~18초)

0\~4초 — 시리즈 회상

GPU 전체 구조도가 중앙에 등장해. 내부 하드웨어를 모두 흐리게 두고 `GPU Hierarchy`라는 문구를 보여줘.

4\~8초 — 실행 단위 복습

Grid의 외곽선 → Block 네 개 → Warp → Thread 순서로 확대해.

별도의 계층도에서는 `Grid → Block → Warp → Thread`라는 논리적 포함 관계를 표시해.

SM은 논리적 포함 계층에 넣지 말고 `Physical Execution Hardware`로 옆에 구분해.

8\~13초 — 메모리 계층 복습

Register File, Shared Memory, Global Memory, L1/L2, DRAM을 순서대로 강조해.

Global Memory를 DRAM·캐시와 단순한 부모·자식 포함 관계로 표현하지 않아야 해.

13\~18초 — 모든 구조가 하나의 코드로 수렴

흩어져 있던 계층 라벨이 화면 바깥으로 이동하고, 중앙에 CUDA 코드가 등장해.

`One CUDA Kernel → GPU Execution`

### SCENE 02 — 벡터 덧셈 코드 (18\~26초)

18\~21초

배열 A, B, C를 세 줄의 수평 셀로 표시해. A와 B의 동일한 인덱스에 있는 원소를 더해 C에 저장하는 모습을 애니메이션으로 보여줘.

Vector Addition — 개념 예시

1

2

3

4

B[i]

5

6

7

8

6

8

10

12

C[i] = A[i] + B[i]

21\~26초

CUDA 코드의 `C[i] = A[i] + B[i];` 부분을 강조해.

이 코드를 영상의 중심 앵커로 계속 사용하면 돼.

### SCENE 03 — Grid, Block, Warp, Thread (26\~53초)

26\~29초 — Kernel Launch

```
int blockSize = 128;
int gridSize = 4;
vectorAdd<<<gridSize, blockSize>>>(A, B, C, 512);
```

Launch 구성에서 `gridSize=4`, `blockSize=128`을 각각 강조해.

29\~35초 — Grid → Block

하나의 Grid 안에 Block 0\~3을 표시해. 각 Block이 128 Thread를 가진다는 라벨을 붙여.

35\~43초 — Block → Warp

Block 0을 확대하고 128개의 Thread 셀을 32개씩 묶어 Warp 0\~3으로 구분해.

Block 0 — 128 Threads / 4 Warps

Warp 0

Warp 1

Warp 2

Warp 3

32 Threads × 4 Warps = 128 Threads. 이 네 묶음은 Block의 논리적인 스레드 구성이지 SM 안의 고정된 네 개 연산 장치를 의미하는 것은 아니야.

43\~50초 — Thread 인덱스로 배열 위치 계산

```
int i = blockIdx.x * blockDim.x
      + threadIdx.x;
```

Block 1, Thread 5를 선택해.

`i = 1 × 128 + 5 = 133`

배열 A[133], B[133], C[133]을 동시에 강조해서 인덱스가 실제 데이터 주소 선택과 연결된다는 점을 보여줘.

50\~53초 — 논리적 실행 구조 정리

`Grid / Block / Warp / Thread = Logical Execution Structure`

이 문구를 보여주면서 화면 오른쪽에 실제 GPU SM들이 대기하는 장면으로 전환해.

### SCENE 04 — 논리적 Block은 실제 어디에서 실행될까? (53\~72초)

이 구간은 앞서 보여준 논리적 Grid 구조를 실제 GPU의 SM에 연결하는 장면이야.

53\~56초 — 질문 전환

왼쪽에는 `Grid = 4 Blocks`, 오른쪽에는 여러 SM이 배치된 GPU를 보여줘.

논리적 Block이 아직 어느 SM에도 연결되지 않은 상태로 시작해.

56\~59초 — SM 등장

GPU 칩 안의 SM 0\~3을 강조해.

여기서 SM은 CUDA 코드로 정의한 Block의 하위 단위가 아니라 실제 명령을 실행하는 물리적 하드웨어라는 것을 표시해.

59\~67초 — Block 배치 및 Warp 스케줄링

Block 0이 SM 0에, Block 1이 SM 1에 배치되는 하나의 가능한 실행 예시를 보여줘.

이어서 Block 0 내부의 Warp 0\~3이 SM 0의 Warp Scheduler와 연결되도록 해.

논리적인 Block과 물리적인 SM의 매핑

각 Block이 서로 다른 SM에 배치되는 하나의 예시야. 실제 배치 순서나 SM별 Block 수는 보장되지 않으며, 한 SM에 여러 Block이 동시에 상주할 수도 있어.

67\~72초 — 실제 명령 실행

SM 0의 Warp Scheduler에서 Warp 0의 명령을 선택하는 모습을 보여줘.

명령이 SM의 실행 유닛으로 전달되고 선택된 Warp의 활성 Lane에서 연산이 수행되는 장면으로 이어가.

화면 문구:

`Warp Scheduling → SM Execution Units`

### SCENE 05 — Register와 Shared Memory의 위치 (72\~81초)

72\~76초 — Register

스레드에서 사용하는 인덱스 `i`, 읽어온 값, 중간 계산값이 레지스터에 보관될 수 있음을 보여줘.

SM의 Register File을 확대하고, 선택한 스레드에 할당된 레지스터를 강조해.

단, CUDA 소스 코드의 모든 변수가 반드시 레지스터에 존재한다고 묘사하지는 않아야 해.

76\~81초 — Shared Memory

SM 내부의 Shared Memory 영역을 강조해.

여기서는 `vectorAdd` 코드와 Shared Memory 사이에 실제 데이터 이동 화살표를 연결하지 않는 것이 중요해.

현재 코드에는 `__shared__`가 없으므로, Shared Memory는 이번 커널에서 필수적으로 사용되는 데이터 경로가 아니야.

화면 문구:

`Shared Memory — Optional, Block-level Cooperation`

### SCENE 06 — 배열 A·B는 어디에 있을까? (81\~95초)

81\~85초 — SM 내부에서 GPU 메모리로 전환

SM을 확대했던 카메라가 GPU 전체로 줌아웃해.

Register와 Shared Memory는 SM 안쪽에 남고, 아래쪽에 `Global Memory` 공간을 표시해.

85\~89초 — 배열 A·B·C 배치

Global Memory 주소 공간에 배열 A, B, C를 표시해.

선택된 Thread가 담당하는 `A[133]`, `B[133]`, `C[133]`을 강조해.

89\~95초 — Global Load 요청

코드에 다음 부분을 표시해.

```
C[i] = A[i] + B[i];
```

A와 B에 대한 읽기 요청을 각각 다른 색상의 데이터 토큰으로 표현해.

이 요청들은 실제로 캐시와 메모리 시스템을 통해 처리될 수 있다는 점을 보여줘.

### SCENE 07 — L1·L2 Cache와 DRAM의 데이터 공급 (95\~115초)

이번 구간은 9편과 10편의 내용을 같은 실행 흐름 안에서 연결하는 장면이야.

95\~100초 — Cache Hit

A의 데이터는 L1에 있는 경우, B의 데이터는 L1에 없지만 L2에 있는 경우를 예시로 구성해.

두 데이터가 각각 다른 캐시에서 공급되는 모습을 보여줘.

100\~105초 — Cache Miss와 DRAM 접근

캐시 어디에도 없는 다른 데이터 요청을 추가해 Memory Controller를 거쳐 DRAM에 접근하는 경로를 보여줘.

이때 벡터 덧셈 코드에서 실제로 A와 B 외에 새로운 세 번째 Load가 발생하는 것처럼 묘사하면 안 돼. 같은 Load 요청의 다른 가능한 상황으로 화면을 전환해.

105\~111초 — 계산과 Store

A와 B의 값이 준비되면 선택된 스레드가 덧셈을 수행하고 C에 저장하는 모습을 보여줘.

111\~115초 — 쓰기 경로

`C[i]`의 Store 요청이 메모리 시스템으로 전달되는 장면을 보여주고, 나중에 데이터가 DRAM에 반영될 수 있다는 점을 암시해.

한 Thread의 벡터 덧셈 흐름

예시 i = 133

LoadAddStore

A[133]

4

B[133]

7

SM Arithmetic Unit

4 + 7 = 11

C[133] = 11

A[133]과 B[133] 값을 메모리 시스템에서 읽음

이 예시는 개별 Thread의 논리적인 계산 순서를 보여주는 거야. 실제 GPU 하드웨어에서는 여러 Warp와 다수의 메모리 요청이 겹쳐 진행돼.

### SCENE 08 — 하나의 코드, 수많은 계산 (115\~133초)

115\~117초 — 시점 전환

선택된 Thread 하나의 실행을 마친 뒤 화면을 잠깐 정지시켜.

117\~125초 — 모든 Thread로 계산 확장

선택된 Thread의 `C[133] = A[133] + B[133]` 연산을 다른 Thread들로 확장해.

`C[0]`, `C[1]`, `C[2]` … `C[511]`이 각자의 입력 원소를 사용해 계산되는 모습을 보여줘.

512개의 셀을 모두 세밀하게 표시하기보다는, Block별로 128개씩 영역을 나누고 결과가 채워지는 애니메이션이 좋아.

125\~133초 — 논리 구조와 물리적 실행 결합

Grid의 4개 Block이 SM에 배치되고, Warp가 스케줄링되며, 데이터는 메모리 계층을 통해 공급되는 전체 화면을 보여줘.

여기서는 모든 스레드가 정확히 같은 순간에 실행된다는 인상을 주지 않도록, 여러 Warp가 시간에 따라 선택되고 실행되는 움직임으로 표현해.

### SCENE 09 — 스레드가 많으면 무조건 빠를까? (133\~151초)

133\~139초 — 질문과 반전

SM 안에 많은 Block을 배치하려는 장면을 보여줘.

처음에는 SM 안에 Block이 계속 들어갈 것처럼 표현하다가, Register File과 Shared Memory의 자원 사용량이 표시되면서 배치 가능한 수에 제한이 생기는 모습을 보여줘.

139\~145초 — 하드웨어 자원 제약

Register 사용량이 작은 경우와 큰 경우를 비교해.

같은 128 Thread Block이라도 레지스터 사용량이 증가하면 해당 SM에 동시에 상주할 수 있는 Block 수가 줄어들 수 있음을 보여줘.

Shared Memory 사용량도 별도의 제약 요소로 표시해.

145\~151초 — 메모리 접근 패턴

Warp 0이 Global Memory의 연속된 주소를 읽는 경우와 큰 간격의 주소를 읽는 경우를 비교해.

8편에서 다룬 Memory Coalescing 장면을 짧게 재사용하면 좋아.

GPU 성능을 제약하는 두 가지 예시

Resource Limits

Register / Shared 사용량이 Block 상주 수를 제한

Memory Traffic

주소 패턴이 메모리 요청과 데이터 이동에 영향

성능 비교 수치를 임의로 표시하지 않는 게 중요해. 이 구간은 최적화 결과가 아니라 하드웨어의 구조가 성능에 제약을 만든다는 점만 설명하면 충분해.

### SCENE 10 — GPU 계산의 세 가지 질문 (151\~163초)

151\~156초

코드 전체를 다시 등장시켜.

`C[i] = A[i] + B[i]`

화면 아래에는 세 가지 질문이 차례로 나타나게 해.

156\~163초

하나의 CUDA 커널을 이해하는 세 가지 질문

Who?

어떤 Thread가 계산하는가

Where?

어느 SM에서 실행되는가

From Where?

데이터는 어디서 공급되는가

이 세 질문은 시리즈 전체를 요약하는 핵심 문구로 활용할 수 있어.

### SCENE 11 — 최종 구조 정리 (163\~183초)

163\~169초 — Logical Execution Structure

Grid → Block → Warp → Thread를 구조도 안에서 순서대로 강조해.

`Logical Execution Hierarchy`

이후 SM과 연결해 물리적 실행 하드웨어의 역할을 분리해.

169\~178초 — Hardware & Memory Hierarchy

SM 내부의 Execution Units, Register File, Shared Memory, L1 Cache를 보여줘.

카메라가 아래로 이동하면서 L2 Cache, Memory Controller, DRAM까지 연결해.

이 장면에서는 Register·Shared·Global이 프로그래밍 관점의 메모리 공간이고, Cache·Controller·DRAM은 물리적인 데이터 공급 하드웨어라는 이전 영상의 구분을 유지해야 해.

178\~183초 — 전체 통합

코드의 커널 호출부터 Thread별 계산, SM 배치, 메모리 시스템까지 하나의 화면에 연결해.

CUDA Kernel → GPU Execution

Kernel Launch

`<<<gridSize, blockSize>>>`

Logical

Grid

Block

Warp

Thread

Physical

SM

Execution Units

Register / Shared

Memory System

L1 / L2 · Controller · DRAM

왼쪽은 논리적 스레드 조직, 오른쪽은 실제 실행 및 메모리 하드웨어를 나타내는 별도 관점이야. 위아래로 동일하게 중첩된 물리적 포함 관계는 아니야.

### SCENE 12 — 마무리 및 GPU 최적화로 연결 (183\~191초)

183\~191초

화면 중앙에 `C[i] = A[i] + B[i]`를 다시 표시해.

왼쪽에는 Thread와 Block의 배치, 오른쪽에는 SM과 메모리 시스템을 보여줘.

마지막에는 다음 문구를 순서대로 표시해.

계산을 어디에 배치할 것인가?

데이터를 어떻게 이동시킬 것인가?

이어서 시리즈 전체 제목을 화면 중앙에 표시하면서 마무리해.

`GPU HIERARCHY — COMPLETE`

마지막 프레임에서는 전체 GPU 계층 구조도를 유지하는 것이 좋아. GPU 최적화라는 다음 질문을 던지는 동시에, 이번 시리즈의 구조적 설명이 완결되었다는 인상을 남길 수 있어.

## 5. 기술적 정확성 검토

| 항목                           | 주의해야 할 표현                                      |
| ---------------------------- | ---------------------------------------------- |
| Grid → Block → Warp → Thread | CUDA의 논리적 조직 구조                                |
| SM                           | 물리적인 실행 장치로, Block과 같은 논리 계층에 속하지 않음           |
| Block 배치                     | SM에 할당되지만 배치 순서나 특정 SM은 보장되지 않음                |
| Warp Scheduler               | 실행 가능한 Warp의 명령을 선택함. 모든 Warp를 동시에 실행하는 것은 아님  |
| Register                     | 컴파일러가 배치하는 저장 자원. 소스 코드의 모든 변수에 1:1 대응하지 않음    |
| Shared Memory                | 벡터 덧셈 예제에서는 사용하지 않음                            |
| Global Memory                | CUDA의 논리적 메모리 공간                               |
| L1 / L2 Cache                | 데이터 공급을 위한 하드웨어 캐시. 모든 Load가 반드시 L1을 거치는 것은 아님 |
| DRAM                         | 캐시에 없는 데이터를 공급할 수 있는 물리적 저장 장치                 |
| Store                        | 저장 요청과 실제 DRAM 반영이 반드시 같은 시점에 일어나는 것은 아님       |

## 6. 최종 제작 방향

이번 마지막 편은 개념이 많지만, 새로운 화면 요소를 계속 추가하기보다 동일한 벡터 덧셈 커널과 동일한 GPU 구조도를 유지하면서 카메라의 시점을 바꾸는 방식이 가장 적합해.

특히 26\~53초의 논리적 실행 구조, 53\~81초의 물리적 하드웨어, 81\~115초의 메모리 계층을 하나의 연속적인 공간처럼 연결하면 시리즈 전체의 개념이 자연스럽게 정리될 거야.

그리고 151\~183초에는 앞선 열 편에서 설명한 구조가 결국 세 가지 질문으로 수렴한다는 점을 보여줘.

누가 계산하는가, 어디에서 실행되는가, 데이터는 어디에서 오는가.

이 세 가지가 마지막 통합편의 중심 메시지야.