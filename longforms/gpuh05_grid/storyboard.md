# GPU 계층 구조 LEVEL 05 — Grid 상세 영상화 콘티

총 178초 (2분 58초) · 9:16 쇼츠 · 실제 CUDA 코드 대응 · LEVEL 01\~04와 동일한 시각화 체계

이번 영상의 핵심은 CUDA에서 정의한 Grid의 논리적인 Block 배치와 실제 GPU의 SM에 배치되는 실행 구조가 서로 다르다는 점이야.

특히 기존 4편의 SM 구조도에서 카메라가 GPU 전체로 줌아웃되고, 12개의 Block을 정의한 CUDA 코드가 여러 SM의 실제 실행 작업으로 연결되는 과정을 중심에 두는 게 좋아.

## 1. 시각화의 기본 구성

GPU HIERARCHY / LEVEL 05

GRID

CUDA Grid 0

Logical execution space

B0

B1

B2

B3

B4

B5

B6

B7

B8

B9

B10

B11

하드웨어 자원에 따라 Block 배치

Physical GPU — SM 0\~3

SM 0

Block

SM 1

Block

SM 2

Block

SM 3

Block

CUDA Kernel Launch

vectorAdd<<<12, 128>>>(\
&#x20;   d_A, d_B, d_C, N\
);

기본 화면 구조. 논리적 Grid와 물리적 SM 배치를 구분하며, 코드 패널은 필요한 부분만 크게 표시해.

### 이전 편과 통일할 규칙

- GPU·SM·Block·Warp·Thread의 색상, 번호, 공간적 관계 유지
- Grid는 SM 안에 넣지 않고 실행할 작업 전체를 나타내는 별도의 논리 공간으로 표시
- Block 5를 선택하면 Grid 화면과 SM 배치 화면 모두에서 같은 초록색으로 표시
- CUDA 코드는 줄 번호 없이 테두리와 배경이 있는 패널로 표시
- 필요한 코드 1\~5줄만 발췌해 큰 글자로 강조
- SM 배치 시각화는 설명용 예시이며 실제 스케줄링 순서가 아니라는 표기 유지

## 2. 실제 CUDA 코드

이번 영상의 수치와 정확하게 대응하도록 12 Block × 128 Thread = 1,536 Thread를 고정하는 게 좋아.

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

// Host-side example
int blockSize = 128;
int gridSize = 12;

vectorAdd<<<gridSize, blockSize>>>(
    d_A, d_B, d_C, N
);

```

여기서는 `N = 1536`을 사용하면 1,536개 Thread가 각각 정확히 하나의 원소를 처리하게 돼.

다차원 Grid 장면에서는 별도의 `dim3` 코드 조각을 사용해. 두 예제를 하나의 커널인 것처럼 섞지 않는 것이 중요해.

## 3. 상세 영상화 콘티

### SCENE 01 — SM에서 GPU 전체로 확장 (0\~17초)

0\~5초 — 이전 구조 확장

LEVEL 04의 SM 구조도에서 시작해.

SM 0 안에 Block 0이 배치되어 있고, 그 안의 Warp들이 실행되고 있는 모습을 보여줘.

이어서 SM 1, SM 2, SM 3이 화면에 등장하면서 카메라가 GPU 전체로 줌아웃돼.

5\~12초 — 새로운 질문

화면 왼쪽에 Block 하나가 등장하고, 이어서 다수의 Block이 복제되어 GPU 전체에 실행될 작업을 표현해.

`Grid`라는 큰 외곽선이 이 Block들을 감싸도록 만들어.

12\~17초 — Grid 정의

12개 Block으로 이루어진 하나의 Grid를 보여줘. Grid 화면에는 `Logical Execution Space`를, SM 화면에는 `Physical Execution Hardware`를 표시해.

### SCENE 02 — 12개 Block과 1,536개 Thread (17\~41초)

17\~29초 — 전체 Block 수와 Thread 수

Grid — 12 Blocks

Block 0

Block 1

Block 2

Block 3

Block 4

Block 5

Block 6

Block 7

Block 8

Block 9

Block 10

Block 11

12 Blocks × 128 Threads

### 1,536

각 Block 안의 점 16개는 128개 Thread를 축약하여 표현한 것이야.

29\~34초 — 논리적 Thread와 실제 실행 구분

`1,536 Logical Threads`가 화면 중앙에 나타나.

이후 같은 화면 아래에 제한된 수의 SM을 표시해, 모든 Thread가 동시에 하드웨어에서 실행되는 것은 아니라는 사실을 보여줘.

34\~41초 — Grid와 실행 자원

상단의 Grid는 그대로 유지하고, 아래쪽 SM에 Block이 순차적으로 배치되는 개념적 애니메이션을 보여줘.

### SCENE 03 — CUDA 실행 설정 (41\~59초)

41\~48초 — Kernel Launch

```
int blockSize = 128;
int gridSize = 12;

vectorAdd<<<gridSize, blockSize>>>(
    d_A, d_B, d_C, N
);
```

`<<<gridSize, blockSize>>>`에 하이라이트를 넣어.

48\~54초 — Block당 Thread 수

`blockSize = 128`을 강조하면 하나의 Block 안에 Thread 128개가 나타나.

54\~59초 — Grid의 Block 수

`gridSize = 12`를 강조하면 해당 Block이 12개로 확장돼.

화면에는 실제 코드와 함께 `Grid = 12 Blocks` / `Block = 128 Threads`라는 라벨이 고정되도록 해.

### SCENE 04 — 전체 데이터 인덱스 계산 (59\~93초)

이번 편에서 CUDA 코드와 논리적 Grid가 가장 직접적으로 연결되는 장면이야.

CUDA 인덱스 계산 — Block과 Thread 선택

Block 인덱스

Block 1

Thread 인덱스

Thread 5

CUDA 소스코드

`i = blockIdx.x * blockDim.x + threadIdx.x;`

i = 1 × 128 + 5

# i = 133

이 스레드가 계산하는 데이터 위치: C[133]

59\~64초: 여러 Block 중 하나를 선택하면서 해당 Block의 인덱스가 `blockIdx.x`에 대응된다는 사실을 보여줘.

64\~71초: `blockIdx.x`, `blockDim.x`, `threadIdx.x`를 차례로 강조해.

71\~78초: 화면 중앙에 수식이 등장해.

\\[ i=\text{blockIdx.x}\times\text{blockDim.x}+\text{threadIdx.x} \\]

78\~82초: Block 0, Thread 5를 선택해 전역 인덱스 5가 계산되는 과정을 보여줘.

82\~87초: Block 1, Thread 5로 이동하면서 `1 × 128 + 5 = 133`으로 변경해. 스레드의 Block 내부 번호는 같지만 전체 데이터 위치가 다르다는 점을 강조해.

87\~93초: 전체 Grid의 각 스레드가 서로 다른 원소를 담당할 수 있다는 것을 색상과 연결선으로 보여줘.

### SCENE 05 — Grid의 Block들이 실제 SM에 배치되는 과정 (93\~115초)

여기서부터 화면을 두 영역으로 나누는 게 중요해.

상단에는 Logical Grid, 하단에는 Physical GPU를 두고, Block의 색상과 ID를 정확히 연결해.

Grid → SM 작업 배치

설명용 시뮬레이션

12345

Logical Grid

B0

B1

B2

B3

B4

B5

B6

B7

B8

B9

B10

B11

SM 0

—

SM 1

—

SM 2

—

SM 3

—

4개 SM에 Block 하나씩 상주한다고 가정한 시각화. 실제 하드웨어는 여러 Block이 동시에 상주할 수 있으며 배치 순서는 보장되지 않아.

93\~100초: GPU 전체에 여러 SM이 등장하고, Grid의 Block 중 일부가 각 SM에 배치되는 모습을 보여줘.

100\~104초: SM 내부에 Block이 들어간 뒤 Warp가 실행되는 모습으로 확대해. LEVEL 04에서 사용했던 SM 내부 구조도를 재사용하면 좋아.

104\~108초: 같은 SM에 여러 Block이 상주할 수도 있다는 사실을, 자원 사용량이 적은 Block 두 개가 한 SM에 배치되는 예시로 보여줘.

108\~115초: 더 많은 Block이 있다면 일부가 아직 배치되지 않은 채 남아 있다가, 자원이 확보되었을 때 실행되는 모습을 보여줘.

코드 패널에는 `<<<12, 128>>>`를 작게 유지하고, Grid의 Block 수는 계속 12개로 고정해.

### SCENE 06 — Block의 실행 순서는 보장되지 않는다 (115\~132초)

115\~120초: Grid의 Block 0\~11을 번호순으로 배열하고, 실제 GPU 배치를 설명하는 장면에서는 Block 7, 2, 9 등 서로 다른 번호의 Block이 먼저 실행되는 예시를 보여줘.

120\~126초: 애니메이션을 다시 재생하되 다른 실행 순서를 보여줘.

예를 들어 첫 번째에는 `B0 → B3 → B1`, 두 번째에는 `B5 → B2 → B8`처럼 나타내.

이 순서는 임의의 설명용 시나리오이며, 실제 실행 순서를 예측한 값이 아니라는 것을 표시해.

126\~132초: 서로 다른 실행 순서에서도 모든 Block이 서로 다른 데이터 영역을 처리하므로 결과가 올바르게 만들어지는 모습을 보여줘.

Block 실행 순서가 달라도 결과는 동일

실행 순서 A

B0

B1

B2

B3

서로 겹치지 않는 출력 영역 처리

실행 순서 B

B2

B0

B3

B1

서로 겹치지 않는 출력 영역 처리

여기서는 서로 다른 Block들이 같은 출력 주소에 동기화 없이 기록하는 상황을 예제로 사용하면 안 돼. Block마다 독립적인 출력 데이터 영역을 처리하도록 작성한 커널이라는 조건을 유지해야 해.

### SCENE 07 — 2D Grid와 이미지 처리 (132\~156초)

이 장면에서는 1차원 Grid를 2차원 Grid로 바꾸되, GPU 칩 위에 Block이 2차원 격자로 물리적으로 배열되는 것이 아니라, 데이터 공간의 좌표가 2차원으로 구성되는 것을 강조하자.

132\~140초

1차원으로 배열된 Block들을 2차원 격자로 재배치해.

화면에는 `Grid (x, y)`를 표시하고, 격자의 각 칸이 이미지의 한 영역에 대응되는 것을 보여줘.

140\~148초

이미지를 16×16 픽셀 타일로 나누는 예시를 보여주고, 아래 CUDA 실행 설정을 강조해.

```

dim3 block(16, 16);

dim3 grid(
    (width + 15) / 16,
    (height + 15) / 16
);

imageKernel<<<grid, block>>>(...);

```

148\~150초

`blockIdx.x`, `blockIdx.y`를 선택할 때 이미지의 해당 타일이 강조되도록 만들어.

2D Grid — Block 좌표와 이미지 타일

blockIdx.x

x = 2

blockIdx.y

y = 1

0,0

1,0

2,0

3,0

4,0

0,1

1,1

2,1

3,1

4,1

0,2

1,2

2,2

3,2

4,2

0,3

1,3

2,3

3,3

4,3

선택한 Block (2, 1) → 이미지의 해당 타일

150\~156초

이 격자 좌표는 실제 SM의 물리적 위치가 아니라 데이터 영역을 나누는 논리적 좌표라는 점을 보여줘.

2D Grid 화면 옆에 물리적인 SM 배열을 표시하되 둘 사이에 `Logical ≠ Physical`이라는 문구를 넣으면 좋아.

### SCENE 08 — 전체 실행 계층 정리 (156\~178초)

CUDA 실행 계층과 GPU 하드웨어

논리적인 CUDA 실행 구조

Thread

Block

Grid

하드웨어 실행 구조

Warp

SM

GPU

156\~166초: Thread → Block → Grid의 논리적 구성과 Warp → SM의 하드웨어 실행을 나누어 강조해.

166\~171초: Grid의 Block들이 실제 여러 SM에 배치되며 연산이 처리되는 모습을 보여줘.

171\~178초: CUDA 코드의 실행 설정과 전체 GPU 구조가 동시에 나타나며 종료해.

마지막 문구:

Grid = Logical Workload / SM = Physical Execution Hardware

## 4. 영상화에서 특히 지켜야 할 기술적 기준

| 항목             | 올바른 표현                                            |
| -------------- | ------------------------------------------------- |
| Grid           | 하나의 커널 실행에 속하는 Block 전체의 논리적 공간                   |
| SM             | Block을 배치받아 실제 연산을 처리하는 하드웨어                      |
| `<<<12,128>>>` | 12개의 Block, Block당 128개 Thread                    |
| `blockIdx.x`   | Grid 내 Block의 논리적 인덱스                             |
| `threadIdx.x`  | Block 내 Thread의 논리적 인덱스                           |
| Block 실행 순서    | 인덱스 순서 보장 없음                                      |
| 2D Grid        | 데이터 작업 공간의 논리적 배치                                 |
| Block과 SM      | Block 하나는 하나의 SM에 배치되지만, 한 SM에 여러 Block이 상주할 수 있음 |

## 5. 가장 중요한 두 장면

첫 번째는 64\~93초의 전역 인덱스 계산이야. Grid의 Block과 Thread를 선택할 때 CUDA 코드의 `blockIdx.x`, `threadIdx.x`가 실제 데이터의 인덱스와 대응되는 모습을 정확하게 보여줘야 해.

두 번째는 93\~132초의 SM 배치와 실행 순서야. Grid의 Block ID와 실제 SM의 배치를 분리하고, Block 실행 순서가 보장되지 않더라도 서로 독립적인 출력 영역을 처리하면 정상적인 결과를 얻는다는 점을 시각화해야 해.

이번 편을 완성하면 시리즈의 처음 다섯 편을 통해 Thread → Warp → Block → SM → Grid의 전체 실행 관계를 설명하게 돼. 이후 Register, Shared Memory, Global Memory를 다루는 메모리 계층 시리즈로 자연스럽게 넘어갈 수 있어.