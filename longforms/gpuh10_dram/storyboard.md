# GPU 계층 구조 LEVEL 10 — Memory Controller & DRAM 상세 영상화 콘티

총 164초 (2분 44초) · 9:16 쇼츠 · GPU 메모리 계층 5편 · CUDA 코드와 실제 하드웨어 대응

이번 영상의 핵심은 CUDA 프로그램의 Global Memory 주소가 실제 DRAM의 물리적인 저장 위치와 어떻게 연결되고, Memory Controller가 그 접근을 어떻게 처리하는지 보여주는 거야.

앞선 9편에서는 L1·L2 Cache를 설명했으므로, 이번에는 카메라가 캐시 아래의 메모리 시스템까지 확장되는 구조로 이어가면 좋아.

## 1. 전체 영상 구성

| 시간        | 장면                     | 핵심 시각화                            |
| --------- | ---------------------- | --------------------------------- |
| 0\~23초    | Global Memory와 DRAM 구분 | 논리적 주소 공간 vs 물리 저장 장치             |
| 23\~51초   | Memory Controller의 위치  | SM → Cache → Controller → DRAM    |
| 51\~81초   | CUDA Load의 실제 데이터 흐름   | Cache Miss 이후 DRAM Read           |
| 81\~116초  | DRAM 내부 구조             | Bank, Row, Column, Row Activation |
| 116\~141초 | GDDR와 HBM              | 서로 다른 DRAM 패키징·인터페이스              |
| 141\~164초 | 전체 구조 정리               | 주소 공간·캐시·컨트롤러·물리 메모리              |

## 2. 메인 화면 구성

이번 편에서는 기존 LEVEL 01\~09의 GPU 구조도를 그대로 확장하면서, GPU 칩 내부와 칩 외부의 메모리 장치를 공간적으로 구분하는 것이 중요해.

GPU HIERARCHY / LEVEL 10

DRAM

계층 관계를 보여주는 개념도. 실제 GPU의 컨트롤러 수, L2 분할 구조 및 DRAM 칩의 배치는 아키텍처와 패키징에 따라 달라져. 특히 HBM은 GPU 다이와 같은 패키지에 배치될 수도 있어.

### 이전 영상과 통일할 연출 규칙

- SM은 파란색, L1·L2 Cache는 보라색 계열, Memory Controller는 주황색, DRAM은 금색 계열로 구분
- 실제 물리 장치는 GPU 칩/패키지 구조에 맞춰 배치하고, Global Memory는 논리적 주소 공간이라는 별도의 오버레이로 표현
- Load 요청은 실선, 요청이 돌아오는 데이터 경로는 다른 색상의 실선으로 구분
- Cache Hit / Miss의 처리는 이전 9편의 화면 구조와 연결
- CUDA 코드는 관련된 1\~4줄만 노출하고 줄 번호는 사용하지 않음
- DRAM 내부의 Row·Bank 시각화는 실제 셀 배열의 정확한 물리 배치가 아닌 설명용 모형으로 처리

## 3. CUDA 코드

이번 편에서도 기존 `vectorAdd`와 유사한 커널을 사용하면 시리즈의 통일성이 좋아.

```

__global__ void readData(
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

이 코드는 Global Memory Load와 Store를 설명하기 위한 예시야.

`float x = A[i];`에 집중하면서, 해당 Load가 Cache Miss를 일으켜 DRAM까지 도달하는 상황을 가정하면 돼. 실제 컴파일된 명령 하나가 반드시 단일 DRAM 요청 하나에 대응하는 것은 아니야.

## 4. 시간별 상세 영상화 콘티

### SCENE 01 — Global Memory와 DRAM은 같은 개념일까? (0\~23초)

0\~5초 — Global Memory 복습

기존 8편에서 사용한 Global Memory 구조도를 불러와.

SM 0\~3이 하나의 대규모 배열 A를 접근하는 장면을 보여줘.

5\~15초 — 논리적 주소와 물리 저장 공간

화면을 두 부분으로 나눠.

왼쪽에는 CUDA 프로그램이 보는 `Global Memory Address Space`와 배열 A를 표시해.

오른쪽에는 GPU의 실제 DRAM 칩을 표시해.

15\~23초 — 두 개념 연결

Global Memory 주소 공간의 특정 위치가 실제 DRAM의 물리적 저장 공간으로 연결되는 개념적인 매핑 애니메이션을 보여줘.

Global Memory

CUDA가 사용하는 논리적 주소 공간

A[0], A[1], A[2] ...

Device DRAM

데이터를 실제로 저장하는 하드웨어

Bank / Row / Column

Logical Address Space ≠ Physical Storage Device

여기서는 CUDA의 가상 주소에서 물리적 DRAM으로 이어지는 내부 변환 과정을 하나의 단순한 화살표로 처리하고, `A[i]`가 곧바로 DRAM Row·Column 번호라고 오해하게 만들지 않는 것이 좋아.

### SCENE 02 — Memory Controller는 GPU의 어디에 있을까? (23\~51초)

이 장면에서는 기존의 `SM → L1/L2 → DRAM` 그림 사이에 Memory Controller를 추가하는 것이 핵심이야.

23\~30초 — 캐시 아래의 하드웨어 공개

SM 0에서 발생한 메모리 요청을 화살표로 표시해.

L1 Cache와 L2 Cache를 지나 DRAM 쪽으로 요청이 향하는 모습에서 카메라를 멈춰.

30\~40초 — Cache Miss와 Memory Controller 등장

L1과 L2에 요청 데이터가 존재하지 않는 예시를 보여줘.

기존 구조도에서 L2와 DRAM 사이의 경로가 확대되고, `Memory Controller`가 새롭게 등장해.

40\~45초 — 메모리 컨트롤러의 위치

메모리 컨트롤러는 GPU의 메모리 시스템에서 DRAM에 대한 접근을 조정하는 하드웨어로 표시해.

45\~51초 — 컨트롤러의 역할

`Read Scheduling`, `Write Scheduling`, `DRAM Timing`이라는 세 개의 기능을 차례로 강조해.

Memory Controller의 세 가지 역할

Read

데이터 읽기

Write

데이터 쓰기

Timing

DRAM 동작 조정

실제 DRAM 접근 시점과 요청 처리 순서는 여러 대기 요청과 하드웨어 제약에 의해 달라질 수 있어. 따라서 모든 메모리 요청이 반드시 발생한 순서대로 DRAM에서 처리된다고 표현하지 않아야 해.

### SCENE 03 — CUDA Load가 DRAM에 도달하는 과정 (51\~81초)

이번 편에서 가장 중요한 실행 시각화 장면이야.

하나의 CUDA Load를 중심으로 메모리 요청이 내려가는 방향과 읽어온 데이터가 돌아오는 방향을 분리해서 보여줘.

51\~58초 — 실제 코드와 Thread 선택

코드 패널에 다음 부분을 표시해.

```
float x = A[i];
B[i] = x * 2.0f;
```

Warp 0 내부의 선택된 Thread를 강조하고, `A[i]`의 값을 요청하는 상황을 보여줘.

58\~63초 — Cache Miss 발생

L1과 L2에 해당 데이터가 존재하지 않는 상태를 표시해.

요청이 DRAM 접근이 필요한 상태로 바뀌어.

63\~71초 — Controller가 DRAM 읽기 처리

Memory Controller가 요청을 받아 필요한 DRAM 읽기 작업을 진행해.

71\~76초 — 데이터 반환

읽어온 데이터가 DRAM에서 메모리 시스템을 거쳐 SM으로 전달돼.

76\~81초 — 계산 재개

데이터가 준비되면 `x * 2.0f` 계산이 진행되는 모습을 보여줘.

CUDA Global Load 흐름

캐시 미스 예시

1

2

3

4

5

SM / Warp Load

L1 / L2 Cache

Memory Controller

Device DRAM

Load 요청

SM에서 A[i]에 대한 Global Load 발생

이 시뮬레이션은 한 메모리 요청의 대표적인 흐름을 간략화한 것이야. 실제 GPU에서는 다른 Warp의 명령 실행과 여러 메모리 요청이 겹쳐 진행될 수 있어.

### SCENE 04 — DRAM 내부의 Bank, Row, Column (81\~116초)

이번 장면에서는 DRAM을 단순히 데이터를 쌓아둔 배열로 보여주는 것에서 벗어나, 물리적인 접근 절차가 있는 저장 장치임을 보여주는 것이 핵심이야.

81\~86초 — Memory Controller의 역할 확장

컨트롤러를 확대하면서 DRAM 내부 구조를 드러내.

86\~94초 — 여러 Bank와 Row·Column

DRAM을 Bank 0\~3으로 나누고, 각 Bank 안에는 Row와 Column으로 이루어진 데이터 격자를 표시해.

94\~100초 — Row 활성화

Bank 0에서 원하는 Row가 선택되고 활성화되는 모습을 보여줘.

그다음 선택된 Row의 Column에서 데이터가 읽히는 개념적 과정을 표시해.

100\~105초 — 이미 활성화된 Row와 다른 Row

같은 Bank에서 이미 열려 있는 Row의 데이터에 접근하는 경우와 다른 Row에 접근하기 위해 전환이 필요한 경우를 비교해.

105\~110초 — Controller의 타이밍 관리

요청 처리 과정에서 `ACTIVATE`, `READ`, `PRECHARGE` 등의 명령이 관련된다는 점을 보여줘.

110\~116초 — 접근 상태에 따른 지연 차이

같은 데이터 크기를 읽어도 Row 상태에 따라 필요한 DRAM 명령과 지연이 달라질 수 있다는 점을 정리해.

DRAM Bank — Row 접근 시뮬레이션

열린 Row 접근다른 Row 접근

Bank 0 · Row Buffer 상태

요청한 Row가 이미 활성화된 상태

개념적 DRAM 명령

READ

이미 Row가 열려 있는지에 따른 단순화된 예시. 실제 DRAM 명령 순서 및 타이밍은 현재 Bank 상태, 선행 명령과 메모리 종류에 따라 달라져.

영상에서는 이 두 조건을 Row Buffer Hit / Row Conflict로 표시하면 이해하기 좋아.

다만 한 Bank에 여러 Row가 동시에 모두 열린 상태처럼 묘사하지 않아야 해.

### SCENE 05 — GDDR와 HBM의 물리적 구조 비교 (116\~141초)

이 장면에서는 GDDR와 HBM을 단순한 빠른 메모리와 느린 메모리의 비교로 만들지 않는 게 중요해.

둘 다 DRAM이지만, 메모리 칩의 구성과 GPU에 연결되는 인터페이스의 구조가 다르다는 점이 핵심이야.

116\~120초 — DRAM의 종류 소개

GPU 메모리 시스템을 다시 보여주고, Device DRAM 영역이 GDDR와 HBM이라는 두 가지 구현 예시로 나뉘는 애니메이션을 보여줘.

120\~129초 — GDDR

GPU 프로세서 주변에 여러 개의 메모리 칩이 배치된 그래픽카드 기판을 보여줘.

GPU에서 메모리 칩으로 연결되는 배선과 메모리 인터페이스를 강조해.

129\~136초 — HBM

여러 개의 DRAM 다이를 수직으로 적층한 HBM 스택을 보여줘.

스택과 GPU가 가까이 배치되고 넓은 인터페이스로 연결되는 모습을 표현해.

136\~141초 — 두 방식의 공통점

두 방식 모두 Global Memory의 데이터를 저장하는 물리적 DRAM 기술임을 강조해.

[Обзор видеокарты Yeston GeForce RTX 3060 «Шесть Стражников» 12G (12 ГБ)](https://images.openai.com/static-rsc-4/vTXNKkmrJphI2C8_zfRWLmjI0-Mw8yDNEgG-hKUexuE83Tt85l-97gxl_xlbSyyKnADdFvP8Css4eLb9l3bfVZODnrUmfW6_OPTopZ1Wx22t7YmQgA1hrUM8e70v6lcOG9pEK6gbbm437H1v8ZRDvgJGIRW9OXyxspsUpnFZc_A?purpose=inline)

GDDR

GPU 주변의 개별 메모리 칩과 고속 인터페이스

[HBM 공정 ② — TSV 심화: 에칭·라이너·구리필·CMP](https://images.openai.com/static-rsc-4/OLXji8fNk3Xs-GVMYtfFXUHUVMMNijf8cfd1sBQ06ijxbDgzTQ0BArxSDryrL4akVlv8CWKyrYrbUKvIMtiB9wKnZpzWIRqFHodRygZf1TdE_7rGwzp45azkkbqH94wsE3oh7Qoy_Req23vUQiFdshHGT7YR057s4ALFUZg-rG4?purpose=inline)

HBM

수직 적층 메모리 다이와 넓은 데이터 인터페이스

제품 이미지나 기술 도식은 실제 참고 자료로 활용하고, 최종 영상에서는 이전 GPU 구조도와 동일한 스타일의 단순화된 3D 도형으로 재구성하는 편을 추천해.

### SCENE 06 — 논리적 주소 공간과 물리 하드웨어의 최종 연결 (141\~164초)

141\~149초 — Global Memory vs DRAM

화면을 좌우로 나누어 CUDA 프로그램이 인식하는 주소 공간과 데이터를 저장하는 DRAM 하드웨어를 비교해.

`Global Memory = Logical Address Space`

`Device DRAM = Physical Storage`

149\~153초 — Memory Controller

두 개념 사이를 연결하는 Memory Controller의 역할을 강조해.

단, Global Memory 주소가 Memory Controller에서 처음으로 물리 주소로 변환된다는 식으로 표현하지 말고, 주소 변환을 포함한 GPU 메모리 시스템이 물리적 접근을 처리한다는 수준으로 유지해.

153\~157초 — 캐시 아래의 하드웨어

SM, L1, L2, Memory Controller, DRAM이 한 화면에 나타나고 실제 데이터 경로를 다시 보여줘.

157\~164초 — 최종 마무리

카메라가 GPU 전체로 줌아웃되고 이번 영상에서 추가된 두 요소를 강조해.

Memory Controller — DRAM Access Control

DRAM — Physical Data Storage

GPU 메모리 계층 — 최종 개념도

CUDA Global Memory Address

SM / L1 Cache

L2 Cache / Memory Fabric

Memory Controller

Device DRAM — GDDR / HBM

캐시 미스가 발생해 DRAM 접근이 필요한 상황의 단순화된 경로. Global Memory 주소 자체는 물리 장치가 아니라 프로그래밍 관점의 메모리 공간이야.

## 5. 제작 시 주의할 기술적 사항

| 요소                | 정확한 표현                                   |
| ----------------- | ---------------------------------------- |
| Global Memory     | CUDA가 접근하는 논리적 메모리 주소 공간                 |
| Device DRAM       | 전역 메모리 데이터를 실제로 저장하는 일반적인 물리 장치          |
| Memory Controller | DRAM 읽기·쓰기 및 타이밍을 관리하는 하드웨어              |
| Cache Miss        | 요청 데이터가 캐시에 없어 하위 계층 접근이 필요한 상황          |
| DRAM Bank         | 물리적 DRAM에서 접근을 구성하는 단위                   |
| Row Activation    | 필요한 Row를 읽기 위해 활성화하는 과정                  |
| Row Buffer Hit    | 필요한 Row가 이미 활성화되어 있는 경우                  |
| GDDR / HBM        | 서로 다른 DRAM 인터페이스·패키징 기술                  |
| Load와 DRAM 요청     | CUDA Load 하나가 반드시 DRAM 명령 하나에 대응하는 것은 아님 |

## 6. 최종 제작 우선순위

이번 10편은 다음 세 장면의 완성도를 높이는 것이 중요해.

첫 번째: 0\~23초 — Global Memory와 DRAM의 구분. 기존 영상에서 Global Memory를 물리적인 메모리 장치처럼 그렸다면, 이번 편에서는 그것이 프로그래밍 관점의 주소 공간이라는 사실을 더 명확히 보여줘야 해.

두 번째: 51\~81초 — CUDA Load에서 DRAM까지의 경로. 실제 CUDA 코드의 `A[i]`를 기준으로 메모리 요청과 데이터 반환 경로가 연결돼야 해.

세 번째: 86\~116초 — Memory Controller와 DRAM Bank. 단순한 주소 전달이 아니라 Row 활성화와 DRAM 타이밍 조정이라는 실제 역할이 존재한다는 점을 보여줘야 해.

이렇게 구성하면 10편은 Global Memory, L1·L2 Cache, Memory Controller, DRAM의 관계를 완성하면서 CUDA의 논리적 메모리 공간이 물리적인 GPU 메모리 하드웨어와 어떻게 연결되는지 설명하는 영상이 돼.

다음 마지막 11편에서는 실행 구조와 메모리 계층을 하나의 CUDA 커널로 연결하여 전체 시리즈를 마무리하면 좋아.