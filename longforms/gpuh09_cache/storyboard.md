# GPU 계층 구조 LEVEL 09 — L1 & L2 Cache 상세 영상화 콘티

총 169초 (2분 49초) · 9:16 쇼츠 · GPU 메모리 계층 4편 · CUDA 코드와 하드웨어 구조 연동

이번 편은 앞선 메모리 영상들과 조금 다르게 구성하는 게 좋아.

Register, Shared Memory, Global Memory를 크기순으로 나열하고 그 사이에 L1·L2 Cache를 추가하는 방식은 오해를 만들 수 있어.

따라서 영상의 핵심을 두 종류의 관계를 구분하는 것으로 잡자.

- CUDA 메모리 공간: Register, Shared Memory, Global Memory — 데이터의 소유·접근 범위
- 하드웨어 캐시 계층: L1, L2 — 메모리 요청을 처리하고 데이터를 재사용하는 구조

특히 이번 편에서는 Shared Memory와 L1이 물리적으로 통합될 수 있으면서도 서로 다른 역할을 수행한다는 것을 정확히 시각화해야 해.

## 1. 전체 영상 구성

| 시간        | 장면                         | 핵심 시각화                              |
| --------- | -------------------------- | ----------------------------------- |
| 0\~21초    | 두 관점의 구분                   | Memory Space vs Cache Hierarchy     |
| 21\~45초   | 세 메모리 공간과 캐시               | Register / Shared / Global과 L1 / L2 |
| 45\~57초   | GPU 내부 캐시 위치               | SM별 L1, GPU 공유 L2                   |
| 57\~94초   | CUDA Load 및 Cache Hit/Miss | L1 → L2 → DRAM                      |
| 94\~132초  | Shared Memory와 L1 관계       | 통합 온칩 자원, 별도 관리 방식                  |
| 132\~144초 | L2의 독립적인 역할                | 여러 SM의 데이터 접근                       |
| 144\~169초 | 전체 구조 정리                   | 논리적 공간과 물리적 접근 경로                   |

## 2. 메인 화면 설계

이번에는 CUDA 메모리 공간과 캐시를 같은 계층의 상자로 쌓지 않는 것이 중요해.

GPU HIERARCHY / LEVEL 09

CACHE

CUDA Memory Spaces

Register

Thread

Shared

Block

Global

GPU-wide

Hardware Caches

L1 Cache

SM-local

L2 Cache

Shared across SMs

Global Load

L1

L2

DRAM

메모리 공간과 캐시 계층을 서로 다른 축으로 보여주는 기본 화면. 오른쪽의 접근 경로는 L1 캐싱을 사용하는 일반적인 Global Load 예시야.

### 시리즈 공통 시각 규칙

- 기존 LEVEL 01\~08의 GPU, SM, Block, Warp, Thread의 식별 색상·위치 유지
- Register File 보라색, Shared Memory 청록색, Global Memory 황금색 유지
- L1은 파란색, L2는 진한 파란색 계열로 구분
- CUDA 소스코드는 테두리와 배경이 분리된 패널로 표시하고 줄 번호는 사용하지 않음
- Cache Hit는 초록색, Cache Miss는 주황색으로 표현
- 실제 Load 요청의 예시와 일반적인 메모리 공간 구조를 혼동하지 않도록 라벨 표시
- 캐시에 데이터를 저장하는 동작을 사용자가 명시적으로 제어하는 Shared Memory 코드와 구분

## 3. CUDA 코드

이번 편에서는 가장 짧은 Global Memory Load를 중심으로 설명하는 것이 좋아.

```

__global__ void readArray(
    const float* A,
    float* B,
    int N
) {
    int i = blockIdx.x * blockDim.x
          + threadIdx.x;

    if (i < N) {
        float x = A[i];
        B[i] = x * 2.0f;
    }
}

```

실제 영상의 57\~94초에서는 전체 커널을 보여주기보다 다음 부분만 강조해.

```
float x = A[i];
```

이 Load가 캐시 계층에서 어떻게 처리되는지 보여주는 거야.

단, 같은 코드가 항상 L1에 캐시된다는 의미는 아니야. 캐시 정책, 실제 캐시 내용, 아키텍처에 따라 경로가 달라질 수 있다는 점을 영상 중반에서 명확하게 다루면 돼.

## 4. 시간별 상세 콘티

### SCENE 01 — L1·L2는 어디에 속하는가? (0\~21초)

0\~4초 — 이전 메모리 공간 복습

기존 6\~8편의 메모리 구조도를 불러와.

SM 안의 Register File, Shared Memory, GPU의 Global Memory 영역을 차례로 강조해.

4\~9초 — L1·L2 등장

L1과 L2를 기존 메모리 구조도 위에 표시하되, 처음에는 위치를 확정하지 않고 두 개의 카드로 등장시켜.

`L1 Cache?` `L2 Cache?`

시청자가 이 둘이 Shared와 Global 중 어디에 포함되는지 질문하도록 만들면 좋아.

9\~13초 — 두 가지 분류 기준 제시

화면을 좌우로 분할해.

`CUDA Memory Spaces`와 `Hardware Cache Hierarchy`라는 별도 제목을 보여줘.

13\~21초 — 분류 구조 정리

왼쪽에는 Register·Shared·Global을, 오른쪽에는 L1·L2를 배치해.

앞서 보여준 하나의 수직 계층도가 두 개의 분류 체계로 나뉘는 애니메이션을 사용해.

### SCENE 02 — 메모리 공간과 캐시의 역할 (21\~45초)

21\~28초

Register를 강조하면 개별 Thread의 계산값, Shared를 강조하면 Block 내부의 협력, Global을 강조하면 여러 SM에서 접근하는 배열이 나타나도록 구성해.

28\~34초

Global Memory 안에 큰 배열 A·B·C가 등장하고, 서로 다른 SM이 배열을 참조하는 모습을 보여줘.

34\~37초

L1·L2 카드에 다시 초점을 맞춰.

37\~45초

Global Memory의 배열 A를 읽는 작업과 그 데이터의 복사본이 캐시에 유지되는 상황을 개념적으로 보여줘.

Global Memory 안에 L1·L2 주소 공간이 존재하는 것처럼 상자를 중첩하지 않는 게 중요해.

화면 문구:

Memory Space ≠ Cache Hierarchy

### SCENE 03 — L1·L2의 물리적 위치 (45\~57초)

GPU 내부의 L1 / L2 배치

45\~53초: SM마다 L1을 강조해. 하나의 SM에서 L1이 빛나면 다른 SM의 L1과는 별도의 영역임을 보여줘.

53\~57초: GPU 공용 L2가 한꺼번에 강조되며 여러 SM에서 선이 연결되도록 해.

### SCENE 04 — CUDA Load와 Cache Hit / Miss (57\~94초)

이 구간은 코드의 동일한 `A[i]` 접근이라도 데이터가 어디에 존재하느냐에 따라 공급 경로가 달라질 수 있다는 사실을 보여주는 장면이야.

57\~64초 — CUDA 코드 연결

`float x = A[i];`가 강조되고, 선택된 Warp의 Load 요청이 L1 Cache로 향하는 모습을 보여줘.

64\~70초 — L1 Cache Hit

L1에 필요한 데이터가 있는 경우에는 바로 해당 캐시에서 데이터를 공급하는 모습을 보여줘.

70\~78초 — L1 Cache Miss

같은 데이터가 L1에 없는 가상의 상황으로 변경해. 요청이 더 아래의 L2로 전달되는 모습을 표시해.

78\~84초 — L2 Hit 또는 DRAM 접근

L2에 있다면 그곳에서 데이터가 공급되고, L2에도 없다면 디바이스 DRAM으로 접근하는 경로를 보여줘.

84\~94초 — 캐시 정책에 따른 경로 차이

GPU 구조도에 `Cache policy / architecture dependent`라는 보조 문구를 표시해.

이 장면에서는 L1을 거치지 않는 Global Load 경로도 존재할 수 있음을 짧게 보여줘.

Global Load 경로 시뮬레이션

개념적 예시

L1 Hit

L2 Hit

Cache Miss

L1 미사용

`float x = A[i];`

L1 Cache

Hit

L2 Cache

미접근

Device DRAM

미접근

SM의 L1 Cache에서 데이터 공급

연출 주의: 화면의 상자는 요청 경로를 이해하기 위한 모형이야. 캐시 Hit 여부가 결정되는 모든 하드웨어 내부 단계를 정확한 시간 순서로 나타낸 것은 아니야.

### SCENE 05 — Shared Memory와 L1은 어떤 관계일까? (94\~132초)

이 부분이 이번 영상의 개념적 핵심이야. 앞서 시청자가 가질 수 있었던 \*\*“L1은 Shared Memory 안에 있는 걸까?”\*\*라는 의문을 해결해야 해.

94\~100초 — 구조적 질문

SM 하나를 확대하고 Shared Memory와 L1 Cache를 다시 강조해.

기존의 단순 메모리 공간 그림을 접은 뒤, 물리적 하드웨어 관점으로 전환해.

100\~106초 — 통합 온칩 자원

일부 NVIDIA 아키텍처에서 Unified L1 / Shared Memory 자원의 일부가 Shared Memory, 나머지가 L1 Cache로 활용될 수 있다는 것을 표시해.

SM 내부의 통합 온칩 자원 — 개념도

구성 A구성 B구성 C

Unified On-Chip Storage

Shared

L1

온칩 저장 자원을 서로 다른 기능에 배분하는 관계를 나타낸 비례 모형

25:75, 50:50, 75:25는 개념적인 배분 예시일 뿐 실제 GPU의 지원 구성이나 용량 비율이 아니야. 아키텍처별 고정 영역과 설정 제한은 다를 수 있어.

106\~111초 — 같은 자원과 같은 주소 공간은 다르다

하나의 외곽선 안에 Shared Memory와 L1 Cache가 존재하지만 각자 독립된 라벨과 접근 경로를 유지하도록 해.

이 장면에서 두 영역 사이에 데이터가 자동으로 자유롭게 왕복하는 연출은 피해야 해.

111\~118초 — Shared Memory는 코드에서 명시적으로 관리

```
__shared__ float s[128];

s[threadIdx.x] = A[i];
```

`__shared__`가 강조되면 SM의 Shared Memory 영역이 밝아지도록 만들어.

코드에서 해당 배열에 직접 쓰고 읽는다는 점을 강조해.

118\~123초 — L1은 하드웨어가 관리

```
float x = A[i];
```

이 코드에서 L1 Cache의 데이터 적재 및 교체는 일반적으로 하드웨어가 관리한다는 점을 보여줘.

123\~132초 — 두 메모리의 역할 비교

| Shared Memory          | L1 Cache                    |
| ---------------------- | --------------------------- |
| CUDA 코드에서 명시적으로 사용     | 일반적으로 하드웨어가 자동 관리           |
| 같은 Block의 스레드 간 공유     | 해당 SM의 캐시 가능한 접근 지원         |
| 프로그램의 데이터 배치·동기화 필요    | Cache Hit / Miss에 따라 데이터 공급 |
| 일부 GPU에서 L1과 물리적 자원 공유 | 일부 GPU에서 Shared와 물리적 자원 공유  |

화면 최종 문구:

Shared Hardware Resources ≠ Same Memory Space

### SCENE 06 — L2 Cache는 왜 별도로 존재할까? (132\~144초)

132\~137초

GPU 전체 화면으로 줌아웃해.

SM 0과 SM 1에서 발생하는 메모리 요청이 공용 L2 Cache로 연결되는 모습을 보여줘.

137\~144초

SM 0이 사용했던 데이터가 L2에 남아 있는 상황을 가정해.

SM 1이 동일한 데이터 주소를 요청했을 때 DRAM에 다시 접근하지 않고 L2에서 공급받는 과정을 연출해.

여러 SM이 공유하는 L2 Cache

동일 데이터가 L2에 남아 있어 재사용되는 경우를 보여주는 설명용 예시야. 서로 다른 SM의 L1 Cache가 직접 같은 공간을 공유한다는 의미는 아니야.

### SCENE 07 — 최종 정리 (144\~169초)

144\~151초 — 메모리 공간 관점

Register·Shared·Global을 차례로 강조하고, 각 공간의 사용 주체와 접근 범위를 짧게 표시해.

151\~158초 — 캐시 계층 관점

같은 GPU 하드웨어 그림에서 L1·L2 Cache를 강조해.

Global Memory의 Load가 캐시의 도움으로 더 가까운 저장 자원에서 공급될 수 있다는 구조를 보여줘.

158\~169초 — 두 관점을 통합

GPU 메모리 구조 — 두 가지 관점

Memory Spaces

Register

Shared Memory

Global Memory

데이터의 저장·접근 범위

Cache Hierarchy

L1 Cache

L2 Cache

Device DRAM

데이터 공급·재사용 경로

Memory Spaces ≠ Hardware Cache Hierarchy

마지막에는 두 분류가 서로 독립적이면서도 실제 GPU의 동일한 메모리 시스템 안에서 연결된다는 점을 전달하면 돼.

## 5. 반드시 지켜야 할 기술적 표현

| 개념             | 정확한 영상 표현                                   |
| -------------- | ------------------------------------------- |
| Global Memory  | 대용량 논리적 주소 공간이며 실제 데이터는 일반적으로 디바이스 DRAM에 저장 |
| L1 Cache       | SM에 가까운 하드웨어 캐시                             |
| L2 Cache       | 여러 SM이 공유하는 하드웨어 캐시                         |
| Cache Hit      | 요청한 데이터가 해당 캐시에 존재                          |
| Cache Miss     | 해당 캐시에 데이터가 없어 더 아래 계층의 처리가 필요              |
| Shared Memory  | CUDA에서 명시적으로 사용하는 Block 단위 공유 저장 공간         |
| L1 / Shared 통합 | 일부 아키텍처에서 온칩 자원 공유, 동일한 주소 공간이라는 의미는 아님     |
| 캐시 경로          | 명령과 캐시 정책에 따라 달라질 수 있음                      |

## 6. 영상 제작의 핵심 우선순위

첫 번째: 0\~45초 — 두 가지 분류 기준 확립

L1·L2가 Shared Memory나 Global Memory에 포함되는 별도의 CUDA 주소 공간이 아니라는 사실을 명확히 보여줘야 해. 이 부분이 잘 만들어지면 뒤의 설명을 이해하기 쉬워져.

두 번째: 57\~94초 — 동일한 CUDA Load의 서로 다른 경로

`float x = A[i]`라는 동일한 코드가 Cache Hit / Miss 및 정책에 따라 다른 데이터 공급 경로를 활용할 수 있다는 점을 보여줘. 코드와 하드웨어의 연결이 이 구간의 핵심이야.

세 번째: 94\~132초 — Shared Memory와 L1의 물리적 관계

일부 GPU에서 같은 온칩 자원을 공유한다는 사실과, 두 공간의 프로그래밍·관리 방식이 다르다는 사실을 분리해서 보여줘.

이번 9편은 새로운 캐시 두 개를 단순히 소개하는 영상이 아니라, CUDA의 논리적 메모리 공간과 GPU의 물리적 데이터 공급 구조를 정확히 연결하는 편이 되어야 해.