# GPU 계층 구조 LEVEL 01 — Thread 영상화 콘티

총 152초 (2분 32초) · 9:16 쇼츠 · 실제 CUDA 코드 대응형

이번 영상의 핵심은 스레드의 논리적 위치, 실행 상태, 데이터 처리 과정이 CUDA 코드와 어떻게 대응되는지 보여주는 거야.

단순히 코드가 옆에 표시되는 수준을 넘어서, 특정 코드가 강조되면 해당 Thread와 데이터가 반응하도록 구성하는 것을 추천해.

## 1. 전체 화면 디자인

GPU HIERARCHY / LEVEL 01

THREAD

vector_add.cu

CUDA C++

\_\_global\_\_ void vectorAdd(...) {\
&#x20; int i = threadIdx.x;\
\
&#x20; float a = A[i];\
&#x20; float b = B[i];\
&#x20; float sum = a + b;\
&#x20; C[i] = sum;\
}

현재 선택된 Thread 1의 계산

&#x20;A[1] = 2&#x20;

&#x20;B[1] = 20&#x20;

C[1] = 22

구성 예시: 위쪽은 GPU 구조와 데이터, 가운데는 실제 CUDA 소스코드, 아래는 선택된 스레드의 계산 결과. 장면에 따라 GPU 영역을 크게 확장하고 코드를 축소할 수 있어.

영상 내내 같은 코드를 사용하되, 실제 개념에 맞게 하이라이트를 이동시키는 게 좋아.

## 2. 영상 전체에 사용할 CUDA 코드

```

#include <cuda_runtime.h>

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

        float sum = a + b;

        C[i] = sum;
    }
}

// Host-side launch example
int threadsPerBlock = 4;
int blocksPerGrid =
    (N + threadsPerBlock - 1) / threadsPerBlock;

vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(
    d_A, d_B, d_C, N
);

```

설명용 코드 발췌. 커널 실행 부분은 호스트 함수 안에서 호출하며, `d_A`, `d_B`, `d_C`는 미리 할당하고 데이터를 준비한 GPU 메모리 포인터야. Block당 4개 Thread 설정은 시각화를 위한 것이고, 일반적인 성능 최적화 설정은 아니야.

코드 화면에서는 다음 세 부분을 특히 강조하자.

- `__global__`: GPU 커널의 정의
- `threadIdx.x`: Block 내부의 스레드 인덱스
- `A[i]`, `B[i]`, `sum`, `C[i]`: 스레드의 데이터 처리

후반부에는 `blockIdx.x * blockDim.x`를 추가로 강조해 Block 내부 좌표와 전체 데이터 인덱스가 달라지는 것을 보여주는 거야.

## 3. 초 단위 상세 콘티

### SCENE 01 — GPU에서 Thread 하나까지 확대 (0\~16초)

0\~8초 · 문제 제기

나레이션 1\~3문장

[Towards Microarchitectural Design of Nvidia GPUs — \[Part 1\] | by Dung Le | Distributed Knowledge | Medium](https://images.openai.com/static-rsc-4/fSwaNGO4RRtTjftCBlP4EkDWxbQlvHoZN2azbU9fyj0UAyV-jox1BEGeBR0W_KQpkduN_OohjyE2r5tL9gNmMLHfP62l9mSUnAgrC2XybFO-MhUF8qfvfSlIectVW7eNyzh9WF0y44yc82CHBkHVCaJaUvnSrWX73AI5I9AXohI?purpose=inline)

GPU 칩 전체를 보여준 뒤, 수많은 계산을 상징하는 작은 점들이 동시에 활성화돼. 카메라가 점차 한 영역으로 들어가면서 하나의 Thread를 나타내는 작은 실행 문맥에 집중해.

화면 텍스트: `GPU → Thread`

8\~16초 · Thread의 정의

실행 단위 설명

Thread를 하나의 작은 카드로 표시하고, 그 안에 `Instruction`, `Index`, `State`라는 세 요소를 보여줘.

단, 실제 독립된 물리 코어를 하나씩 가지고 있는 것처럼 표현하지 않아야 해. 이 카드는 논리적 실행 문맥의 시각화야.

코드: 아직 등장시키지 않음. 하드웨어 개념만 먼저 소개.

### SCENE 02 — 벡터 덧셈의 수학적 구조 (16\~36초)

16\~29초 · 입력 배열과 결과

A

1

2

3

4

B

10

20

30

40

C

11

22

33

44

A와 B 배열이 등장하고, 같은 열의 숫자들이 더해져 C 배열로 이동하는 애니메이션을 보여줘.

화면에는 다음 수식을 함께 표시해.

\\[ C_i=A_i+B_i \\]

29\~36초 · CPU에서 CUDA로 전환

CPU 예시

for (int i=0;\
&#x20;    i\<N; ++i) {\
&#x20;C[i]=A[i]+B[i];\
}

CUDA 커널

int i =\
&#x20;threadIdx.x;\
C[i]=A[i]+B[i];

CPU 코드는 반복문으로 원소 인덱스를 바꾸는 예시, CUDA 코드는 서로 다른 스레드 인덱스를 이용하는 예시로 제시해.

CPU도 병렬화할 수 있으므로 CPU는 항상 순차 실행한다는 식으로 설명하지 않는 게 좋아.

### SCENE 03 — CUDA 코드와 Thread 인덱스 연결 (36\~70초)

이 구간이 영상 전체에서 가장 중요한 장면이야.

코드 ↔ Thread 시각화

Thread를 선택해 보기

Thread 0idx = 0

Thread 1idx = 1

Thread 2idx = 2

Thread 3idx = 3

CUDA 코드의 실행 값

threadIdx.x = 1

i = 0 × 4 + 1 = 1

C[1] = A[1] + B[1]

## 2 + 20 = 22

36\~48초: GPU 커널 소스가 나타나고 `__global__`에 밑줄이 그어져. `threadIdx.x`에 초점을 옮기면서 하나의 Block이 화면 왼쪽에 등장해.

48\~62초: 네 Thread를 각각 0, 1, 2, 3으로 표시하고, 각 Thread에서 A와 B의 같은 번호 원소로 연결선을 그어. 계산 결과가 C의 대응 위치에 나타나게 해.

62\~70초: 네 Thread가 같은 CUDA 코드의 서로 다른 실행 인스턴스라는 점을 보여줘. 소스코드 하나에서 네 개의 Thread로 연결되는 시각적 연출이 핵심이야.

화면 문구: `Same Kernel · Different Thread Index · Different Data`

### SCENE 04 — 스레드 내부의 실행 과정 (70\~99초)

이 장면에서는 카메라가 Thread 1을 선택해 확대하는 연출이 좋아.

Thread 1 내부 실행

i = 1

1234

현재 실행 단계 — Load A

float a = A[i];

A[1]에서 값 읽기

## a = 2

영상에선 이 네 단계를 자동으로 진행시키면 돼.

| 시간      | 코드 하이라이트            | GPU 내부 표현                     |
| ------- | ------------------- | ----------------------------- |
| 70\~77초 | `A[i]`, `B[i]`      | 입력값을 읽어오는 모습                  |
| 77\~81초 | `float sum = a + b` | Thread 1의 중간값이 바뀜             |
| 81\~92초 | 지역 변수와 연산 부분        | SM의 Register 자원과 Thread 상태 연결 |
| 92\~99초 | `sum`, `C[i]`       | 레지스터 할당과 코드상 변수의 차이 설명        |

Register는 스레드 카드의 물리적 내부 메모리처럼 그리지 않는 게 중요해. SM의 Register File에서 실행 중인 스레드가 자원을 할당받는 모습으로 표현하고, 컴파일러에 따라 실제 레지스터 사용량이 결정된다고 주석을 넣자.

또한 위 코드는 이해를 돕기 위한 소스 수준의 실행 순서야. 실제 기계 명령은 컴파일러 최적화로 합쳐지거나 재배치될 수 있어.

### SCENE 05 — 스레드는 하나의 원소만 계산할까? (99\~109초)

화면을 두 개로 분할해.

원소 하나

int i = threadIdx.x;\
C[i] = A[i] + B[i];

Thread 0 → C[0]

여러 원소

for (int j = t;\
&#x20;    j < N; j += S)\
&#x20; C[j] = A[j]+B[j];

Thread 0 → C[0], C[4], …

오른쪽 예시는 총 4개 Thread일 때 `t=threadIdx.x`, `S=blockDim.x`인 단일 Block 예시야.

왼쪽에서는 하나의 Thread와 하나의 데이터가 연결되고, 오른쪽에서는 동일한 Thread가 여러 인덱스를 순서대로 처리해.

강조 문구: `Thread ≠ One Arithmetic Operation`

이 장면은 10초 정도이므로 루프 코드 전체를 읽히기보다는, 같은 Thread에 여러 데이터가 연결되는 모습을 중심으로 연출하는 게 좋아.

### SCENE 06 — Thread의 논리적 위치 (109\~140초)

후반부의 핵심은 `threadIdx.x`와 전역 데이터 인덱스가 다르다는 사실이야.

Block 내부의 인덱스와 전역 데이터 인덱스

Block 0Block 1

Block 0t0t1t2t3

Block 1t0t1t2t3

각 Block에서 threadIdx.x = 2인 스레드

i = 1 × 4 + 2 = 6

`C[{Number(block)*4+2}]` 위치 처리

109\~121초: 두 개의 Block을 나란히 놓고, 각 Block에 `Thread 0~3`을 표시해. 두 Block 모두 `threadIdx.x = 2`를 가진 스레드가 있다는 사실을 강조해.

121\~128초: 코드에 다음 줄을 확대해.

```
int i = blockIdx.x * blockDim.x
      + threadIdx.x;
```

Block 0의 Thread 2는 전역 인덱스 2, Block 1의 Thread 2는 전역 인덱스 6에 대응시켜.

128\~134초: 이번에는 2차원 Block 예시로 전환해. 4×4 격자의 각 칸에 `(x,y)` 좌표를 표시하고 `threadIdx.x`, `threadIdx.y`로 행렬의 열과 행을 선택하는 모습을 보여줘.

134\~140초: 격자의 좌표가 물리적 GPU 칩 위의 실제 위치를 의미하는 건 아니라는 점을 명시해.

화면 문구: Logical Coordinates ≠ Physical Hardware Position

### SCENE 07 — Thread의 정의를 하나의 화면으로 정리 (140\~152초)

### Thread

Index

자신의 논리적 위치

State

독립적인 실행 상태

Work

주어진 명령과 데이터 처리

하나의 Thread가 여러 Thread로 복제되는 듯한 연출을 사용한 뒤, 모두 같은 CUDA 커널을 가리키는 선으로 연결해.

마지막 화면은 Block 안의 여러 Thread가 각기 다른 인덱스를 가진 상태로 종료하면 좋아. 다음 편에서 이 Thread들이 Warp 단위로 실행되는 모습을 소개할 때 같은 화면을 재활용할 수 있어.

## 4. 영상 제작에서 꼭 지킬 기술적 기준

| 표현                | 주의할 부분                                          |
| ----------------- | ----------------------------------------------- |
| Thread는 논리적 실행 단위 | Thread마다 별도 CUDA Core가 존재하는 것처럼 묘사하지 않기         |
| 4개 Thread 예시      | 실제 Warp는 32개 Lane이므로, 4개 Thread는 교육용 축소 예시임을 표시 |
| Register          | 소스코드 변수와 물리적 레지스터를 무조건 일대일 대응시키지 않기             |
| Block 내부 인덱스      | `threadIdx.x`와 전역 데이터 인덱스 `i`를 구분               |
| 스레드의 독립성          | 논리적인 실행 상태의 독립성과 물리적인 명령 실행의 독립성을 구분            |

## 5. 제작용 권장 레이어 구성

이 영상은 코드와 구조를 따로 만든 뒤 합성하는 방식이 관리하기 좋아.

- GPU 레이어: Thread, Block, 인덱스 라벨, 메모리 접근, 상태 변화
- CUDA 코드 레이어: 실제 소스코드, 줄 번호, 활성 줄 하이라이트
- 데이터 레이어: A/B/C 배열, 선택 원소, 중간값, 계산 결과
- 설명 레이어: 핵심 개념, 수식, 논리적 좌표와 물리적 구조의 구분

특히 모든 장면에 코드를 계속 크게 표시할 필요는 없어. 36\~70초와 109\~140초에서는 코드를 분명히 읽을 수 있도록 배치하고, 70\~99초에서는 스레드 내부의 데이터 흐름을 더 크게 보여주는 편이 효과적이야.

영상의 차별점은 CUDA 문법 자체가 아니라 소스코드의 한 표현이 GPU의 논리적 실행과 어떻게 대응되는지를 실제 값의 변화로 보여주는 것이야. 이것이 앞으로 Warp, Block, SM 편에서도 일관되게 사용할 시각적 문법이 될 수 있어.