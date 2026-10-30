# GPU 계층 구조 LEVEL 02 — Warp 영상화 콘티

총 167초 (2분 47초) · 9:16 쇼츠 · CUDA 코드와 GPU 실행 구조 대응

이번 편의 핵심은 32개의 Thread가 하나의 Warp를 구성하며, 동일한 명령을 실행할 때와 서로 다른 분기로 나뉠 때 하드웨어에서 어떤 차이가 발생하는지 보여주는 거야.

1편에서 사용한 GPU → SM → Block → Thread 구조도를 그대로 유지하고, 이번에는 Block 내부의 32개 Thread를 하나의 Warp로 강조해.

## 1. 이전 편과 통일할 화면 구성

GPU HIERARCHY / LEVEL 02

WARP

GPU 0 / SM 0 / Block 0

Warp 0

0

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

kernel.cu

CUDA C++

int i = threadIdx.x;\
\
if (i < 16) {\
&#x20;   A[i] \*= 2.0f;\
} else {\
&#x20;   A[i] += 1.0f;\
}

같은 코드 · 서로 다른 Thread · 활성 마스크

실제 영상에서는 GPU 구조 영역이 중심이고, 코드 패널은 필요한 줄만 크게 보여줘. 좌표·색상·Thread 번호는 장면이 바뀌어도 유지.

화면의 고정 규칙

- GPU·SM·Block은 1편과 동일한 좌표와 디자인을 유지.
- Thread 0\~31의 번호는 고정하고, 선택된 Thread의 색상도 유지.
- 코드 패널은 테두리와 어두운 배경을 적용해 명확하게 분리.
- 줄 번호를 표시하지 않고, 해당 장면에 필요한 2\~7줄만 발췌.
- 비활성 Thread는 삭제하지 않고 밝기와 채도만 낮춰 표시.
- 모든 분기 연출에서 실행 순서를 절대적인 하드웨어 사이클 단위로 단정하지 않기.

## 2. 영상 전체에 사용할 실제 CUDA 코드

### A. SIMT 설명용 벡터 덧셈

```

__global__ void vectorAdd(
    const float* A,
    const float* B,
    float* C
) {
    int i = threadIdx.x;

    C[i] = A[i] + B[i];
}

```

하나의 Block에 32개 Thread를 실행하고, 입력·출력 배열에 최소 32개 원소가 있는 예시.

### B. Warp Divergence 설명용 조건문

```

__global__ void branchExample(float* A) {
    int i = threadIdx.x;

    if (i < 16) {
        A[i] = A[i] * 2.0f;
    } else {
        A[i] = A[i] + 1.0f;
    }
}

```

영상에서는 CUDA 커널을 두 개 모두 처음부터 길게 보여주지 않고, 장면에 맞는 코드 조각만 크게 보여주는 게 좋아.

## 3. 시간별 상세 영상화 콘티

### SCENE 01 — Thread에서 Warp로 확장 (0\~17초)

[PPT - Graphics Processing Unit PowerPoint Presentation, free download - ID:1863295](https://images.openai.com/static-rsc-4/iieQBWVVvlTeaJb7HgiLvlQpX-STPYCNpB3tIgM-ypfBhkgwSIbrd6Sf87qIM3sbwY8sAJ0bscdeDHxGiZmxPUH1mj-rM5NlrzXu9vfT_fyWyYb0GvX6iQZ4-bI4fJYhMmqzBKRTuUYEKWJ8Md4U2yq0EE3zYXajuEJ5D7qaXAI?purpose=inline)

0\~8초

1편 마지막의 Thread 강조 화면에서 시작해. 하나의 Thread가 선택되어 있다가, 카메라가 줌아웃되면서 동일한 Block 내부의 다른 Thread가 보이도록 확장해.

아직 Warp를 강조하지 않고, 독립된 실행 문맥들이 실제로 어떻게 실행되는지 질문을 던져.

8\~17초

32개 Thread를 하나의 그룹으로 묶는 외곽선이 등장하고 `Warp 0` 라벨을 붙여.

GPU 구조도 안에서는 Block 내부에 Warp가 표시되지만, Warp가 물리적인 개별 코어처럼 보이지 않도록 그룹 외곽선으로 표현해.

화면 키워드: `32 Threads → 1 Warp` / `Scheduling & Instruction Execution`

### SCENE 02 — Warp와 Lane의 차이 (17\~42초)

Warp 0 — Thread 32개

0

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

Thread의 Warp 내부 번호 = Lane

17\~22초: Warp 내부 32개 스레드를 모두 펼쳐서 표시해. `Thread 0`, `Thread 1`, … `Thread 31` 라벨이 순차적으로 나타나.

22\~29초: 각 Thread의 아래에 0\~31 숫자를 표시하고, 숫자 영역에만 `Lane Index` 라벨을 붙여.

29\~35초: Thread 6을 선택해 확대해. 스레드 자체에는 `Thread`, 위치 번호에는 `Lane 6`을 붙여 두 개념이 다른 실행 단위가 아니라는 사실을 강조해.

35\~42초: 32개 Thread 모두 같은 Warp 외곽선 안에 있으면서 개별 상태를 유지한다는 모습을 보여줘.

이 장면에서는 CUDA 코드를 크게 보여줄 필요가 없어. Lane은 CUDA 소스코드에 등장하는 별도의 실행 객체가 아니라 Warp 내부 번호라는 점이 먼저 이해돼야 하니까.

### SCENE 03 — SIMT와 CUDA 코드 대응 (42\~66초)

SIMT — 같은 명령, 다른 데이터

Warp 0

int i = threadIdx.x;\
\
C[i] = A[i] + B[i];

Thread 0

C[0]

Thread 1

C[1]

Thread 2

C[2]

Thread 31

C[31]

하나의 커널 명령이 여러 스레드의 데이터에 대응

42\~48초: `SIMT`를 중심에 표시하고, 같은 CUDA 커널에서 32개 Thread로 선이 확장되는 애니메이션.

48\~57초: 코드에서 `threadIdx.x`를 강조해 Thread 0, 1, 2, 31이 각각 다른 `i` 값을 갖는다는 것을 보여줘.

57\~66초: `C[i] = A[i] + B[i]`를 하이라이트하고 각 Thread가 대응하는 A/B 원소를 읽고 C 원소를 계산해.

같은 코드 줄을 강조하면서 32개 Thread가 반응하도록 만드는 것이 핵심이야. 각 Thread가 서로 다른 CUDA 소스코드를 갖는 것처럼 표현하지 않아야 해.

### SCENE 04 — 조건문으로 Warp의 실행 경로 분리 (66\~90초)

66\~73초

32개 Thread가 동일한 덧셈을 수행하던 화면에서, 코드 패널이 아래 조건문으로 교체돼.

```
int i = threadIdx.x;

if (i < 16) {
    A[i] *= 2.0f;
} else {
    A[i] += 1.0f;
}
```

73\~79초

조건식 `i < 16`을 크게 확대하고, Warp의 Thread 0\~15에 파란색, 16\~31에 주황색을 부여해.

79\~85초

왼쪽 그룹 위에는 `×2`, 오른쪽 그룹 위에는 `+1`을 표시해. 같은 Warp 안에서 두 종류의 계산이 요구되는 상황을 시각화해.

85\~90초

그룹 둘을 동시에 보여주면서 Warp 내부의 실행 경로가 나뉘었다는 점을 강조해.

이때 두 그룹이 두 개의 독립 Warp가 된 것처럼 외곽선을 분리하지 않아야 해. 동일한 Warp 내부의 분기 상태야.

### SCENE 05 — Warp Divergence와 활성 마스크 (90\~118초)

가장 중요한 시각적 장면이야.

Warp Divergence — 실행 경로별 활성 스레드

곱셈 경로덧셈 경로

0

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

현재 활성 경로

A[i] = A[i] \* 2.0f;

Thread 0–15 활성 · Thread 16–31 비활성

90\~95초: `if` 평가 결과에 따른 두 그룹을 보여주고 `Active Mask` 개념을 시각화해.

95\~102초: 곱셈 명령이 강조될 때 앞의 16개 Thread만 선명하게 표시하고 나머지는 어둡게 처리해.

102\~106초: 덧셈 명령을 강조하면서 반대로 뒤의 16개 Thread만 활성 상태로 바뀌어.

106\~113초: 화면 중앙에 `Warp Divergence`를 표시하고 두 실행 경로를 하나의 Warp가 처리하는 상황을 보여줘.

113\~118초: 동일 Warp 내부에서 여러 경로를 수행할 때 활성 자원이 줄어들 수 있다는 점을 설명해.

여기서는 단순한 시각화를 위해 곱셈 경로 다음에 덧셈 경로를 보여주지만, 실제 하드웨어에서 반드시 그 순서로 실행된다는 뜻은 아니야.

### SCENE 06 — 조건문이 항상 Divergence를 만드는가? (118\~134초)

두 가지 상황을 비교하자.

분기 발산 없음

32개 Thread가 같은 경로 선택

분기 발산 발생

같은 Warp에서 다른 경로 선택

118\~124초: 조건문이 있어도 모든 스레드가 같은 경로로 가는 사례를 표시해.

124\~129초: 32개가 모두 같은 색이 되는 장면과 서로 다른 색으로 나뉘는 장면을 비교해.

129\~134초: `Branch ≠ Divergence`라는 문구를 강조하고, 조건문보다 Warp 내부에서의 경로 차이가 중요하다는 점을 정리해.

### SCENE 07 — Independent Thread Scheduling (134\~150초)

이 구간은 이해를 돕되 과도하게 복잡하게 만들지 않는 게 중요해.

134\~145초: 기존에는 Warp의 스레드들이 하나의 프로그램 카운터를 공유하는 방식으로 설명되던 모델을 간략히 보여주고, Volta 이후에는 스레드별 실행 상태를 더욱 독립적으로 추적한다는 모습을 대비해.

단, 32개 Thread가 완전히 독립적인 명령 발행 장치를 얻은 것처럼 표현하지 않아야 해.

145\~150초: 다시 하나의 Warp 화면으로 돌아와, 활성 스레드를 선택해 명령을 실행하는 구조 자체는 유지된다고 정리해.

추천 화면 문구:

`Independent Thread Scheduling ≠ Independent Instruction Issue`

### SCENE 08 — Thread와 Warp의 차이 정리 (150\~167초)

### Thread

독립적인 실행 문맥

Index · Data · State

### Warp

32개 Thread의 실행 그룹

SIMT · Active Mask

150\~159초: 하나의 Thread를 강조하고 다시 32개의 Thread로 확장해 Warp 외곽선을 표시해.

159\~167초: 같은 Warp라도 Thread들의 실행 경로에 따라 활용 효율이 달라진다는 결론을 시각적으로 보여줘.

최종 화면은 `GPU / SM 0 / Block 0 / Warp 0` 구조도로 돌아가서 종료해. 후속 Block 편에서도 같은 구조도의 위치와 색상을 그대로 사용할 수 있어.

## 4. 제작 시 반드시 유지할 일관성

| 요소           | 1편 Thread             | 2편 Warp                       |
| ------------ | --------------------- | ----------------------------- |
| GPU·SM·Block | 기존 구조도 고정             | 동일 구조도 재사용                    |
| 선택된 Thread   | 번호와 색상 유지             | 같은 번호·색상 유지                   |
| CUDA 코드      | 필요한 코드만 발췌            | 동일한 코드 패널 디자인                 |
| 코드 하이라이트     | `threadIdx.x`, 데이터 접근 | SIMT 명령, 조건문, 분기 경로           |
| Register     | 스레드별 상태와 SM 자원 연결     | 필요할 때만 간략 표시                  |
| 신규 핵심 표현     | Thread Index          | Warp, Lane Index, Active Mask |

### 특히 주의할 기술적 표현

첫째, `threadIdx.x`와 Lane 번호는 항상 같은 것은 아니야. 이번 영상에서는 Block당 32개 Thread를 사용하므로 두 값이 0\~31로 일치하지만, 일반적으로 1차원 Block에서 Lane 번호는 `threadIdx.x % 32`로 구분해.

둘째, Warp Divergence 시각화는 명령 실행 경로의 차이를 보여줘야 해. 두 그룹의 결과가 다르다는 것 자체가 Divergence를 뜻하지는 않아. 같은 Warp의 스레드들이 서로 다른 제어 흐름을 선택한다는 점이 중요해.

셋째, 134\~150초의 Independent Thread Scheduling은 보조 설명으로 유지하자. 이번 편의 주제는 Warp의 기본 실행 모델이지, 아키텍처 세대별 스케줄링 구현 비교가 아니기 때문이야.

## 5. 가장 공들여야 할 장면

90\~113초 — CUDA 조건문과 Active Mask의 동기화

이 부분에서는 코드의 활성 줄, Warp 내부 활성 스레드, 수행할 연산이 동시에 바뀌어야 해.

곱셈 경로 실행

`A[i] = A[i] * 2.0f;`

0

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

16개 스레드 활성

16개 스레드 비활성

이 장면이 성공하면 시청자는 CUDA 소스코드에서 조건문 하나를 추가했을 뿐인데, GPU 내부의 실행 방식이 달라질 수 있다는 사실을 직접 이해하게 돼.

이번 편 전체에서 가장 중요한 연출이자, 이후 GPU 최적화의 Warp Divergence 콘텐츠로도 재활용할 수 있는 장면이야.