# GPU 계층 구조 LEVEL 06 — Register 상세 영상화 콘티

총 175초 (2분 55초) · 9:16 쇼츠 · GPU 메모리 계층 1편 · 실제 CUDA 코드 대응

이번 영상의 핵심은 스레드가 계산에 사용하는 값이 SM의 Register File에 보관될 수 있으며, 이 저장 자원의 사용량이 GPU의 병렬 실행 규모에 영향을 준다는 사실이야.

앞선 1\~5편이 실행 구조를 확장했다면, 이번에는 동일한 GPU 구조도를 유지하면서 SM 내부의 메모리 자원으로 카메라를 이동시키는 방식이 좋아.

## 1. 전체 영상 구성

| 시간        | 장면                   | 핵심 내용                       |
| --------- | -------------------- | --------------------------- |
| 0\~21초    | 실행 계층 → 메모리 계층       | 기존 구조도에서 Register로 시점 전환    |
| 21\~55초   | CUDA 코드와 중간값         | 변수, Load, Compute, Store    |
| 55\~69초   | Register File의 실제 위치 | Thread와 SM의 레지스터 자원 연결      |
| 69\~95초   | 제한된 레지스터 용량          | 128 Thread × 32/64 Register |
| 95\~114초  | Register Pressure    | 상주 Block·Warp 수와 Occupancy  |
| 114\~137초 | Register Spilling    | Register → Local Memory     |
| 137\~158초 | 빠른 저장 공간의 역설         | 사용량과 병렬 실행 사이의 균형           |
| 158\~175초 | 최종 구조 정리             | 메모리와 실행 구조의 연결              |

## 2. 영상 화면의 기본 레이아웃

GPU HIERARCHY / LEVEL 06

REGISTER

CUDA SOURCE / 현재 강조 코드

float a = A[i];\
float b = B[i];\
float sum = a + b;\
C[i] = sum;

이번 편에서도 GPU 구조도가 메인이고 코드가 보조 화면이야. Register는 Thread 카드 내부의 물리적 메모리가 아니라 SM의 자원으로 표시해.

### 기존 영상과 통일할 연출 규칙

- Thread, Warp, Block, SM의 위치와 식별 색상 유지
- Register File은 보라색, 데이터가 실제 계산에 사용되는 순간은 초록색으로 강조
- CUDA 코드 패널은 어두운 배경과 테두리, 큰 글자, 줄 번호 없음
- 한 번에 필요한 코드 1\~5줄만 표시
- 선택된 Thread의 번호가 입력 데이터, 계산 결과, 레지스터 자원 강조까지 이어지도록 연결
- Register Pressure는 SM의 자원 점유 변화로, Spilling은 추가 메모리 접근으로 별도 표현

## 3. 전체 CUDA 예시 코드

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

        float sum = a + b;

        C[i] = sum;
    }
}

```

이 코드는 지역 변수가 레지스터에 저장될 수 있다는 설명용 예시야. 실제로 몇 개의 레지스터가 배정되고 어떤 값이 남는지는 컴파일 결과에 따라 달라져.

특히 뒤에서 등장하는 스레드당 32개·64개 레지스터 사용 예시는 이 단순한 벡터 덧셈 커널의 실제 사용량이 아니라, 자원 제한을 설명하기 위한 가상의 별도 상황으로 표시해야 해.

## 4. 시간별 상세 콘티

### SCENE 01 — 실행 구조에서 메모리 계층으로 (0\~21초)

0\~9초 — 앞선 실행 계층 정리

GPU 전체 구조에서 Thread → Warp → Block → SM → Grid를 차례로 강조해.

처음부터 구조도를 새로 만들지 말고, 이전 5편에서 실제로 사용했던 모델을 그대로 불러와.

9\~18초 — 관점 전환

SM 내부의 한 Thread를 선택해 확대해. 해당 Thread가 계산하는 도중 두 입력값과 중간 결과가 등장하도록 표현해.

화면에 두 질문을 순차적으로 표시해.

`Where does computation happen?`

`Where are intermediate values stored?`

이어서 `Execution Hierarchy → Memory Hierarchy` 전환 텍스트를 보여줘.

18\~21초 — Register 등장

SM 내부의 Register File 영역을 보라색으로 강조하고 나머지 실행 구조는 희미하게 유지해.

카메라는 Thread에서 물리적으로 SM 내부의 Register File로 이동해야 해.

### SCENE 02 — CUDA 코드의 지역 변수와 중간 결과 (21\~55초)

이번 구간에서는 코드와 데이터 흐름이 정확하게 대응되어야 해.

CUDA 코드와 스레드의 계산

1234

입력 배열 A에서 데이터 읽기

float a = A[i];

## a = 3

값 3, 4, 7은 시각화를 위한 예시. 소스코드의 지역 변수와 실제 물리 레지스터 할당이 일대일로 같다는 뜻은 아니야.

21\~27초: Register의 기능을 먼저 설명하고, 선택한 Thread 하나가 입력값을 처리하는 모습을 보여줘.

27\~32초: 실제 CUDA 소스코드 패널이 등장해. `float a`, `float b`, `float sum`을 각각 표시해.

32\~41초: `A[i]`, `B[i]`에서 값이 읽혀 Thread의 계산 상태에 들어오고, 덧셈 결과가 만들어지는 모습을 보여줘.

41\~46초: `a`, `b`, `sum`이 중간값을 나타내는 소스코드 변수라는 사실을 강조해. 이 값들이 레지스터에 보관될 수 있다는 설명과 연결해.

46\~55초: 소스코드 변수와 물리 레지스터의 대응이 컴파일러에 의해 결정된다는 점을 표현해.

추천 연출은 `CUDA Source → Compiler → Register Allocation`의 세 단계 구조야.

`a`, `b`, `sum`이라는 세 변수를 무조건 세 개의 Register 슬롯에 하나씩 연결하지 않아야 해.

### SCENE 03 — Register는 실제로 어디에 존재할까? (55\~69초)

이 구간은 1편에서 등장했던 Thread의 실행 상태와 4편에서 등장했던 SM의 물리적 구조를 연결하는 장면이야.

55\~59초 — 위치에 관한 질문

Thread 내부에 표시했던 `a`, `b`, `sum`이라는 값들을 다시 보여줘.

카메라가 Thread 카드 바깥으로 이동하면서 `SM 0`의 전체 하드웨어 구조가 나타나.

59\~64초 — Register File 강조

SM 안의 Register File이 보라색으로 강조되고, 선택한 Thread의 레지스터 할당 영역이 밝아져.

64\~69초 — 여러 Thread의 자원 할당

하나의 Thread뿐 아니라 여러 Thread가 같은 SM의 레지스터 파일 자원을 사용하지만, 서로의 레지스터 값을 임의로 직접 접근하는 것은 아니라는 점을 표현해.

SM Register File — Thread별 자원 할당

Thread별 레지스터 할당을 표현한 개념도. 실제 레지스터 파일의 물리적 주소와 저장 배열을 나타내는 것은 아니야.

### SCENE 04 — 제한된 Register File (69\~95초)

이번에는 레지스터가 빠르다는 사실보다 한정된 자원이라는 사실이 중심이야.

69\~75초

SM의 Register File 영역에 `Limited Capacity`를 표시해. 여러 Block이 이 자원을 공유해야 한다는 상황을 보여줘.

75\~85초

128개 Thread로 구성된 Block을 등장시켜.

각 Thread에 레지스터 32개가 배정되는 가상 상황에서 계산식을 표시해.

\\[ 128\times32=4096 \\]

85\~91초

동일한 Block에서 스레드당 레지스터 사용량이 64개로 증가하는 상황을 보여줘.

\\[ 128\times64=8192 \\]

91\~95초

128개 Thread는 그대로 유지되지만 Block이 필요로 하는 총 레지스터 수가 두 배가 됐다는 점을 강조해.

동일한 Block, 서로 다른 Register 사용량

32 Registers / Thread64 Registers / Thread

Block의 Thread 수

# 128

Block의 레지스터 요구량

# 4,096

레지스터 사용량 비교

64개/Thread인 경우, 32개/Thread보다 두 배의 레지스터가 필요

중요한 것은 이 두 설정이 실제 CUDA 지역 변수 몇 개의 차이만으로 반드시 만들어지는 것이 아니라는 점이야. 영상에서는 컴파일된 커널의 스레드당 레지스터 요구량이 달라졌다는 가상 비교로 명확히 표시해.

### SCENE 05 — Register Pressure와 Occupancy (95\~114초)

이 장면에서는 4편의 SM, Warp Scheduler, Occupancy 구조도를 재사용하는 것이 가장 좋아.

95\~102초

레지스터 사용량이 적을 때에는 SM에 여러 Block이 들어가는 모습을 보여줘.

레지스터 사용량을 늘리면 한 Block의 자원 요구량이 커지고, 결과적으로 동시에 상주 가능한 Block 수가 줄어들 수 있다는 것을 나타내.

102\~108초

`Register Pressure`가 나타나고, 화면의 Block 수와 상주 Warp 수가 감소하는 모습을 보여줘.

108\~114초

SM 내부 Warp Scheduler로 카메라를 이동시켜.

데이터를 기다리는 Warp가 있을 때 다른 준비된 Warp가 충분하지 않으면 명령을 발행할 기회가 줄어들 수 있다는 것을 보여줘.

Register Pressure → Occupancy → Latency Hiding

여기서는 실제 속도가 무조건 감소한다는 그래프를 만들지 않는 게 좋아. Register Pressure가 증가해도 다른 병목이나 코드 구조에 따라 실제 성능은 달라질 수 있기 때문이야.

### SCENE 06 — Register Spilling: 저장 공간이 부족하다면? (114\~137초)

이 장면에서는 Register Pressure와 Register Spilling을 별개 개념으로 보여줘야 해.

Register Pressure는 레지스터에 대한 요구가 높아지는 상황이고, Spilling은 컴파일러가 일부 값을 레지스터에 유지하지 않고 메모리에 저장하는 상황이야. 레지스터 사용량이 많다고 반드시 Spilling이 발생하는 것은 아니야.

114\~121초

Register File 안에서 값을 보관하기 어려운 상황을 가정하고, 컴파일러가 일부 값을 메모리로 옮겨 저장하는 경로를 등장시켜.

121\~127초

`Register Spilling`이라는 용어를 표시하고 `Local Memory`를 강조해.

127\~133초

Local Memory가 SM 내부의 Register File과 같은 종류의 온칩 저장 공간이 아니라는 것을 보여줘.

GPU의 L1/L2 캐시를 거쳐 디바이스 메모리 계층으로 연결되는 경로를 간략히 표현해.

133\~137초

Spill Store와 Spill Load라는 추가적인 메모리 명령이 발생할 수 있다는 점을 보여줘.

Register Spilling — 추가 메모리 접근

이 장면에선 CUDA 원본 코드에 존재하지 않는 `Spill Load / Store`를 컴파일된 명령의 개념적 표현으로 보여줘. 소스코드에 직접 작성한 명령인 것처럼 표시하지 않아야 해.

### SCENE 07 — 레지스터를 많이 쓰는 것이 좋은가? (137\~158초)

137\~143초

화면을 둘로 나눠 레지스터를 적게 사용하는 커널과 많이 사용하는 커널을 비교해.

한쪽에는 레지스터 부족으로 추가 메모리 접근이 발생할 수 있는 상황, 다른 쪽에는 레지스터 사용량 때문에 상주 Warp 수가 줄어들 수 있는 상황을 보여줘.

143\~150초

각 상황의 장점과 제약을 대비해.

| 레지스터 활용  | 장점               | 가능한 제약          |
| -------- | ---------------- | --------------- |
| 충분한 레지스터 | 중간값을 빠르게 유지      | 상주 Warp 수 감소    |
| 제한된 레지스터 | 더 많은 Warp 상주 가능성 | 추가 메모리 접근 발생 가능 |

150\~158초

두 상황 중 어느 쪽이 항상 빠르다고 단정하지 않고, `Register Usage ↔ Parallelism`이라는 문구를 중심에 두어 균형 관계를 표현해.

여기서는 레지스터 사용량만으로 성능을 결정할 수 없다는 것이 가장 중요해.

### SCENE 08 — 실행 구조와 메모리 계층 연결 (158\~175초)

마지막은 지금까지 다룬 GPU 계층 구조를 다시 보여주는 장면이야.

158\~166초

SM 안의 Register File을 강조하고, 실행 중인 Thread들이 이 자원을 사용하며 계산하는 모습을 보여줘.

카메라가 멀어지면서 SM에 여러 Block과 Warp가 상주하는 전체 구조가 다시 나타나.

166\~175초

코드, 중간값, Register File, Warp Scheduler가 한 화면에 나타나게 해.

Register가 연결하는 두 가지 구조

Execution Hierarchy

Thread · Warp · Block · SM

Memory Hierarchy

Register · Shared · Cache · DRAM

Memory Resources Affect Parallel Execution

이 화면은 쇼츠의 독립적인 결론이면서, 다음 Shared Memory 편으로도 이어질 수 있어.

## 5. 코드와 연출을 연결할 때의 체크포인트

| CUDA 코드·개념               | 화면에 반드시 보여줄 것          |
| ------------------------ | ---------------------- |
| `float a = A[i]`         | 입력값 읽기와 스레드별 계산 상태     |
| `float sum = a + b`      | 입력값을 이용한 중간 결과         |
| 지역 변수                    | 컴파일러가 물리 레지스터 사용을 결정   |
| SM Register File         | 여러 스레드의 레지스터 자원 할당     |
| 32 → 64 Registers/Thread | Block당 레지스터 요구량 2배     |
| Register Pressure        | 제한된 SM 자원과 상주 Warp 수   |
| Register Spilling        | 추가적인 Local Memory 접근   |
| Occupancy                | 레지스터 사용량과 병렬 실행 규모의 관계 |

추가로 제작 단계에서 실제 컴파일 결과를 보여주는 짧은 오버레이를 넣는 것도 좋아. CUDA 코드 패널이 이번 영상의 보조 주제이기 때문에, 단순히 설명하는 것보다 컴파일러가 레지스터 사용량을 결정한다는 사실을 직접 연결할 수 있어.

예를 들어 다음 명령을 자료 화면으로 활용할 수 있어.

```
nvcc -Xptxas=-v register_example.cu -o register_example
```

컴파일 로그에서는 실제로 확인한 `Used N registers` 값을 표시하고, Spilling이 발생한 사례를 보여줄 때도 실제 컴파일 결과에서 확인된 수치만 사용해야 해.

## 6. 가장 중요한 제작 포인트

이번 6편은 다음 세 장면의 완성도에 집중하는 것이 좋아.

첫 번째는 41\~69초. CUDA의 지역 변수가 Thread의 계산에 사용되지만 물리 레지스터와 반드시 일대일로 대응하지 않는다는 사실을 보여주는 구간이야.

두 번째는 75\~114초. 128개 Thread에서 레지스터 요구량이 늘어나는 장면을 SM의 한정된 자원과 상주 Warp 수 변화로 연결해야 해.

세 번째는 114\~137초. Register Spilling을 단순히 메모리가 부족한 화면으로 표현하지 말고, 기존 계산에 없었던 추가적인 메모리 접근이 발생하는 현상으로 표현해야 해.

이렇게 만들면 6편은 단순한 메모리 소개가 아니라 GPU에서 가장 빠른 저장 공간조차 잘못 사용하면 병렬 실행에 제약을 줄 수 있다는 구조적 특징을 설명하는 영상이 돼.

그리고 7편에서는 개인 스레드가 주로 사용하는 Register와 달리, 같은 Block의 여러 Thread가 협력해 사용하는 Shared Memory로 자연스럽게 시야를 확장할 수 있어.