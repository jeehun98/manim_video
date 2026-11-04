# GPU 계층 구조 LEVEL 04 — SM 상세 영상화 콘티

총 178초 (2분 58초) · 9:16 쇼츠 · GPU 하드웨어 중심 + 실제 CUDA 코드 대응

이번 편은 앞선 세 편과 성격이 조금 달라.

Thread, Warp, Block은 CUDA 프로그램의 실행 구조를 중심으로 설명했다면, SM은 그 실행 구조를 실제 하드웨어가 어떻게 처리하는지 보여주는 편이야.

따라서 이번 영상에서 가장 중요한 장면은 Warp 0이 메모리 접근을 기다리는 사이, Warp Scheduler가 준비된 Warp 1의 명령을 실행하는 과정이야.

## 1. 화면의 기본 구조

GPU HIERARCHY / LEVEL 04

SM

CUDA 코드 · 필요한 부분만 발췌

float x = A[i];\
float y = x \* 2.0f;\
B[i] = y;

이 그림은 개념적 관계도야. 실제 SM에서는 스케줄러와 실행 유닛이 여러 개일 수 있고, Register File과 Shared Memory의 물리적 배치는 아키텍처마다 달라.

### 이전 편과 동일하게 유지할 제작 규칙

- GPU → SM → Block → Warp → Thread 구조도의 위치, 색상, 번호 유지
- 이번에는 SM 외곽선을 가장 강하게 강조하고 내부 자원을 단계적으로 공개
- 선택된 Warp 0의 파란색, 대기 상태의 주황색, 실제 명령 발행 상태의 녹색을 일관되게 사용
- CUDA 코드 패널은 테두리와 배경을 분리하고 줄 번호 없이 필요한 1\~5줄만 표시
- 코드 강조와 GPU의 명령 실행 상태가 동시에 변하도록 연출
- 메모리 대기와 스케줄러의 명령 발행을 별도 상태로 구분

## 2. 실제 CUDA 코드

이번 영상은 다음 하나의 커널을 계속 활용하는 방식이 좋아.

```

__global__ void compute(
    const float* A,
    float* B,
    int N
) {
    int i = blockIdx.x * blockDim.x
          + threadIdx.x;

    if (i < N) {
        float x = A[i];
        float y = x * 2.0f;
        B[i] = y;
    }
}

// Host-side launch, inside a function
int blockSize = 128;
int gridSize = (N + blockSize - 1) / blockSize;

compute<<<gridSize, blockSize>>>(
    d_A, d_B, N
);

```

실제 메모리 대기를 보여주는 장면에서는 `float x = A[i]`와 `float y = x * 2.0f`만 강조해.

다만 이 코드가 실행될 때 반드시 긴 메모리 대기가 발생하는 것은 아니야. 캐시에 데이터가 존재할 수도 있고, 컴파일러가 곱셈을 다른 명령 형태로 최적화할 수도 있어. 따라서 영상의 대기 장면은 메모리 지연이 발생한 상황을 가정한 예시라고 명시하면 정확해.

## 3. 초 단위 상세 콘티

### SCENE 01 — 실제 실행 공간인 SM 등장 (0\~19초)

0\~5초

3편에서 사용한 Block 0 구조로 시작해. 128 Thread, 4 Warp를 그대로 보여주면서 논리적인 실행 구조를 상기시켜.

5\~13초

카메라가 줌아웃하면서 Block을 감싸는 SM의 외곽선이 등장해.

화면 중앙에 `Streaming Multiprocessor (SM)` 라벨이 나타나고, 기존 Block 0이 SM 0 안으로 들어가는 애니메이션을 보여줘.

13\~19초

SM 외곽선이 강조되고 내부의 Warp Scheduler, Register File, Execution Units, Shared Memory가 희미하게 표시돼.

화면 핵심 문구: `CUDA Block → Physical SM`

### SCENE 02 — SM 내부 자원과 Block 배치 (19\~42초)

19\~29초 — SM 내부 구조

각 하드웨어 자원을 하나씩 강조해.

| 하드웨어               | 역할             |
| ------------------ | -------------- |
| Warp Scheduler     | 실행할 명령 선택 및 발행 |
| Execution Units    | 산술·메모리 명령 처리   |
| Register File      | 스레드들의 값과 상태 보관 |
| Shared Memory / L1 | 데이터 공유·캐싱      |

29\~38초 — Block 하나가 SM 하나에 배치

Block 0의 네 Warp를 SM 0 내부에 펼치고, Warp Scheduler와 Execution Units까지 연결해.

공유 메모리는 Block 소유처럼 표현하되 실제 저장 자원은 SM 안에 위치하도록 표시해.

38\~42초 — 여러 Block 상주

SM 0 안에 Block 1이 추가되는 모습을 보여줘. 단, Block 1이 항상 배치될 수 있는 것처럼 표현하지 않고 자원이 허용하는 경우임을 나타내.

화면 보조 문구: `Multiple resident blocks — subject to resource limits`

### SCENE 03 — Warp Scheduler와 CUDA 코드 (42\~66초)

42\~52초 — Scheduler 확대

Warp Scheduler로 줌인하고, Warp 0\~3에서 준비된 명령이 스케줄러로 연결되는 모습을 보여줘.

스케줄러는 Ready 상태인 Warp에서 발행 가능한 명령을 선택한다는 사실을 강조해.

52\~60초 — CUDA 코드 등장

```
float x = A[i];
float y = x * 2.0f;
B[i] = y;
```

코드의 세 줄을 각각 Load → Compute → Store로 시각적으로 연결해.

60\~66초 — 데이터 의존성

`float x = A[i]`에서 읽어온 값 `x`가 다음 곱셈에 필요하다는 점을 강조해.

Load A[i]

Compute x × 2

Store B[i]

다음 명령은 필요한 데이터가 준비되어야 진행 가능

### SCENE 04 — 메모리 대기로 Warp가 멈추는 순간 (66\~82초)

66\~70초

Warp 0이 `A[i]`에 대한 Load 명령을 발행해.

메모리 계층 쪽으로 데이터 요청이 이동하는 모습을 보여줘.

70\~74초

요청한 데이터가 아직 도착하지 않은 상황을 연출해. `x`를 필요로 하는 곱셈이 실행되지 못하고 기다리는 모습을 강조해.

74\~78초

Warp 0을 주황색 대기 상태로 바꿔.

다른 Warp들은 SM 내부에서 그대로 존재하도록 유지해. SM 전체가 정지한 것처럼 화면을 멈추지 않아야 해.

78\~82초

Warp 0 위에 `Waiting for Data`를 표시한 채 Warp Scheduler를 다시 강조해.

### SCENE 05 — Latency Hiding: 다른 Warp의 명령 실행 (82\~103초)

이번 편에서 가장 중요한 장면이야.

Warp Scheduler 실행 시뮬레이션

개념적 동작

1

2

3

4

Warp 0

명령 발행

Warp 1

발행 가능

Warp 2

발행 가능

Warp 3

발행 가능

현재 강조되는 CUDA 코드

float x = A[i];

Warp 0이 메모리 Load 명령을 발행

82\~86초: Warp 0이 대기하는 동안 Warp Scheduler가 준비된 Warp 1을 선택해.

86\~90초: Warp 1에 녹색 강조가 들어가고, 실행 유닛 쪽으로 명령이 전달돼. 이후 Warp 2도 선택되는 모습을 보여줘.

90\~95초: Warp 0의 메모리 데이터가 도착하고, 데이터 의존성이 해결돼. Warp 0이 다시 발행 가능한 상태가 된 다음 계산을 진행해.

95\~103초: 화면에 `Latency Hiding`을 표시하고, Warp 0의 메모리 대기 구간 동안 다른 Warp의 명령이 발행되었다는 사실을 타임라인으로 정리해.

개념적 명령 발행 타임라인

여기서 중요한 것은 Warp 자체를 CPU 스레드처럼 저장·복원하는 문맥 교환으로 표현하지 않는 것이야.

상주 Warp의 실행 상태는 이미 하드웨어에 유지되고 있어. 스케줄러는 준비된 Warp의 명령을 선택해 발행할 수 있기 때문에 이러한 지연 숨기기가 가능해.

### SCENE 06 — Occupancy와 SM의 자원 제한 (103\~140초)

103\~108초 — Warp가 많으면 더 빠를까?

SM 내부에 Warp가 추가되는 모습을 보여주고, 많을수록 언제나 좋은지 질문을 던져.

108\~119초 — 하드웨어 자원 제한

SM 내부의 Register File과 Shared Memory를 크게 보여줘.

각 Block이 상주할 때마다 필요한 레지스터와 Shared Memory 자원을 점유하는 모습을 표현해.

SM 자원 사용과 상주 Block 수

Block별 자원 사용 적음

Block 0

Block 1

Block 2

Block 3

상주 Block 4개

Block별 자원 사용 많음

Block 0

다른 Block은 자원 대기

상주 Block 1개

자원 사용량에 따라 상주 가능한 Block 수가 달라질 수 있다는 개념적 예시. 실제 배치 수는 스레드 수와 하드웨어 한계에도 영향을 받아.

119\~130초 — Occupancy 정의

SM 내부의 Warp 수를 Occupancy 측정값으로 전환해.

\\[ \text{Occupancy} =\frac{\text{상주 Warp 수}}{\text{최대 상주 Warp 수}} \\]

가상 SM — 최대 32개 Warp 상주

설명용 수치

16 / 32 Warp

## 50%

130\~140초 — 높은 Occupancy가 항상 빠른 것은 아님

Occupancy 50%와 100%인 두 경우를 비교하되, 성능이 반드시 2배가 되는 것은 아니라고 표시해.

`Higher Occupancy ≠ Higher Performance`

이때 하드웨어 실행 시간이 반드시 같다고 단정하지 말고, 성능이 단조롭게 증가하지 않을 수 있다는 사실만 보여줘.

### SCENE 07 — CUDA 코드에서 SM을 직접 지정할 수 있을까? (140\~154초)

140\~142초

카메라가 SM 전체 구조에서 CUDA 소스코드 패널로 이동해.

142\~149초

다음 실행 구문을 크게 표시해.

```
int blockSize = 128;
int gridSize = (N + blockSize - 1) / blockSize;

compute<<<gridSize, blockSize>>>(
    d_A, d_B, N
);
```

`gridSize`와 `blockSize`가 각각 Block 수와 Block당 Thread 수를 결정한다는 점을 표시해.

반면 코드에는 일반적인 커널 실행 설정으로 SM 번호를 직접 지정하는 인자가 없다는 점을 보여줘.

149\~154초

여러 Block이 GPU의 여러 SM으로 배치되는 장면을 보여줘.

각 Block은 하나의 SM에 배치되지만, 일반적인 커널에서는 GPU가 배치할 SM을 결정한다는 사실을 강조해.

여기서는 프로그램의 `blockIdx.x`를 물리적 SM 번호처럼 사용하지 않도록 주의해야 해.

### SCENE 08 — Thread → Warp → Block → SM 정리 (154\~178초)

Thread

Warp

Block

SM

154\~162초: 기존 Thread → Warp → Block 구조를 차례로 강조하고, 마지막에 SM 외곽선이 강조되는 모습을 보여줘.

162\~169초: Block의 Warp들이 SM의 실행 자원을 활용해 명령을 발행하고 처리하는 모습을 다시 짧게 보여줘.

169\~178초: 여러 Warp가 서로 다른 상태에 있지만 SM 전체에서는 명령 발행이 이어지는 장면으로 마무리해.

최종 화면에는 다음 문구를 남겨.

SM — Warp Scheduling · Execution · Latency Hiding

이렇게 하면 마지막 장면이 독립적으로 완결되면서도, 이후 GPU 전체 구조로 확장하는 영상과 자연스럽게 이어져.

## 4. 제작 과정에서 주의할 기술적 사항

| 항목             | 정확한 표현                                |
| -------------- | ------------------------------------- |
| SM             | CUDA의 논리적 단위가 아닌 실제 하드웨어 실행 장치        |
| Warp Scheduler | 실행 가능한 Warp의 발행 가능한 명령을 선택            |
| Latency Hiding | 다른 Warp의 작업으로 지연 구간의 유휴 시간을 줄임        |
| Register File  | SM의 제한된 하드웨어 자원                       |
| Occupancy      | SM 최대 상주 Warp 수에 대한 실제 상주 Warp 수의 비율  |
| Block 배치       | 일반적인 CUDA 커널에서 특정 SM 직접 지정 불가         |
| 명령 실행          | 스케줄러의 명령 발행과 실제 연산 완료는 서로 다른 시점일 수 있음 |

기술적으로 특히 중요한 두 가지는 다음과 같아.

첫째, Warp 0이 대기한다고 해서 Warp 0 자체가 SM 밖으로 나갔다가 다시 들어오는 것은 아니야. 상주 Warp의 상태는 유지된 채 발행 가능한 다른 Warp의 명령을 선택하는 거야.

둘째, 높은 Occupancy와 높은 실행 성능은 같은 개념이 아니야. 이번 영상에서 Occupancy는 실행 가능한 작업을 얼마나 확보할 수 있는지 이해하기 위한 지표로 설명하고, 성능 최적화 자체는 별도 영상에서 다루는 게 좋아.

## 5. 제작 우선순위

가장 완성도를 높여야 할 구간은 66\~103초야.

이 구간에서 다음 세 가지가 정확하게 연결되어야 해.

CUDA 코드

`float x = A[i];` → `float y = x * 2.0f;`

SM 내부

Warp 0 Load 발행 → 데이터 대기 → Warp 1 명령 발행 → Warp 0 재개

시간축

Warp 0의 대기 구간과 다른 Warp의 실행 구간이 겹쳐 나타남

이 장면이 정확히 구현되면 시청자는 GPU가 메모리 지연을 없애는 것이 아니라, 다른 작업을 실행해 그 지연을 숨긴다는 차이를 이해할 수 있어.

그것이 이번 SM 편에서 전달해야 할 가장 중요한 개념이야.