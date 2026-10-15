# 계산의 두 얼굴 07 — 같은 신경망인데 실행 그래프는 왜 다를까?

부제: AI Framework와 GPU Execution.

## 학습 목표

연산 그래프(무엇을 계산할지), 실행 계획(커널·배치·자원·순서 선택), 런타임/CUDA Graph(선택된 작업과 의존성의 구성·재사용)를 구분한다. 프레임워크·컴파일러·라이브러리가 여러 구현을 조합·선택하고 입력 조건에 따라 계획을 특수화할 수 있음을 이해한다.

## 제작 기준

- 콘티는 113초 구간과 110–130초 권장 길이를 제공한다. 권장된 특수화 문장과 개념 구분을 포함해 초기 120초로 구성한다. 실제 음원 미제공으로 문장별 시간은 추정이다.
- 1080×1920·30fps, 미리보기 360×640, 무음. 별도 TTS 원고·SRT.
- 8장면 종료 12,27,43,58,73,88,109,120초. 누적 시각 gate 사용.
- 복습·요약과 이후 영상 예고 없음. 프레임워크의 계획 생성과 선택이 주제이며 CUDA Graph는 선택한 작업의 실행 메커니즘으로 한정한다.

## 기술 조건

1. 주 예시 Y=ReLU(XW+b), X[M,K], W[K,N], b[N], Y[M,N]. b는 행 방향 broadcast. 개념적 IR의 출력 shape [M,N], FP32, Layout 후보를 표시한다. 실제 프레임워크 IR의 입력·출력·aliasing·state·metadata 전체를 재현하지 않는다.
2. 계산 그래프 노드와 GPU 커널은 1:1 관계가 아니다. Plan A는 MatMul/Bias/ReLU 세 커널, Plan B는 epilogue를 포함한 fused GEMM 한 커널이 가능한 경우다. 항상 fusion 가능하거나 항상 빠르다는 뜻은 아니다. Plan C는 다른 tile/layout의 커널 선택 후보다.
3. 출력 목표는 실수 수학 및 요구되는 수치 계약 기준이다. 다른 GEMM 구현·fusion·정밀도·반올림이 bitwise 동일함을 보장하지 않는다. 동일한 값의 목표와 동일한 실행 구조를 구별한다.
4. Tile·layout·buffer·register/shared 자원·dependency는 계획 선택 요소다. 프레임워크가 모든 선택을 직접 최적화하는 것은 아니며 컴파일러·커널 라이브러리·휴리스틱·런타임 역할을 포함한 추상화다. 실제 capture/lowering/codegen/선택 순서는 구현마다 다를 수 있다.
5. 분기 장면은 별도 예 Y=f(X)+g(X)이며 원래 ReLU 체인에 독립 분기가 있는 것으로 표현하지 않는다. f,g는 의존성·상태 변경·aliasing 충돌이 없는 독립 작업으로 가정한다. Add는 두 결과 뒤에만 실행한다.
6. 두 stream에서 겹칠 수 있다는 실행 계획이며 stream 개수만으로 실제 concurrency를 보장하지 않는다. 자원·스케줄·동기화·하드웨어 조건에 의존한다. 타임라인은 f/g 각 2, Add 1의 개념 구조이며 실행시간 실측이나 속도 배수 주장이 아니다.
7. CUDA Graph는 kernel·memcpy 등의 작업 노드와 의존성을 정의하고 instantiate한 GraphExec를 반복 launch할 수 있다. 예시는 세 kernel dependency 노드이며 모든 CUDA Graph가 직렬이거나 kernel만 포함한다는 뜻은 아니다. Graph 구성은 직접 API/캡처 등으로 가능하다.
8. CUDA Graph는 신경망 의미를 자동 분석해 최적 커널을 찾아주는 컴파일러와 구분한다. 준비·호스트 제출 비용을 줄일 수 있으나 낮은 수준의 런타임 최적화가 전혀 없다는 주장은 하지 않는다. kernel 실행 자체가 자동으로 빨라지거나 global 중간 저장을 자동 제거한다고 주장하지 않는다.
9. Graph 재사용·update·재캡처의 가능성은 shape·분기·주소·node parameters·호환성 등에 따라 달라진다. 모든 shape 변경이 반드시 재캡처를 요구한다고 단정하지 않는다. 실제 실행에는 API별 제약과 버퍼 수명 조건이 있다.
10. torch.compile은 guard가 기존 컴파일 결과와 맞지 않으면 재컴파일할 수 있고 여러 결과를 캐시할 수 있다. dynamic shape는 여러 입력을 하나의 결과로 처리해 재컴파일을 줄일 수도 있다. 모든 호출·shape 변화가 반드시 재컴파일되는 것은 아니다. 지원되는 설정의 autotuning·측정만 예시로 든다.
11. 같은 계산 그래프에서 비용 모델·선택 규칙·실제 측정으로 후보를 평가할 수 있다. graph node 수나 kernel 수를 성능의 보편적 순위로 사용하지 않는다. 실제 성능 수치는 넣지 않는다.

## 장면

| 시간 | 내용 |
|---|---|
| 0–12 | 같은 식·입력·가중치에서 Plan A/B/C 분기 |
| 12–27 | 연산 그래프의 데이터 의존성과 metadata |
| 27–43 | 세 kernel과 fused GEMM의 다른 노드 대응 |
| 43–58 | Tile·Layout·Buffer·Dependency 등의 계획 선택 |
| 58–73 | 별도 f/g 분기의 직렬/중첩 가능 타임라인 |
| 73–88 | 작업 그래프→Instantiate→GraphExec 반복 launch |
| 88–109 | 비용과 입력 조건, Guard와 캐시/새 계획 |
| 109–120 | 하나의 계산 그래프, 여러 실행 계획 |

## 출처

- [CUDA Graphs Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html): graph 작업·의존성·instantiate·반복 실행.
- [torch.compile 공식 문서](https://docs.pytorch.org/docs/stable/generated/torch.compile): 캐시·guards·백엔드·autotuning.
- [PyTorch Recompilations](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/compile/programming_model.recompilation.html): 조건 변화와 재컴파일.
- [PyTorch Dynamic Shapes](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/torch.compiler_dynamic_shapes.html): 동적 shape와 재사용.

## 검증

계산식·bias broadcast·데이터 의존성, f/g/Add의 위상 순서, 연산 노드/커널/GraphExec 구분을 확인한다. 모든 누적 시각 gate, 미리보기·최종 주요 화면의 겹침·자막·프레임 범위를 검사한다. 실제 프레임워크 컴파일·CUDA 실행·성능과 TTS 발화 싱크는 별도다.

### 2026-10-15 제작 검증 결과

- Manim 0.21.0, FFmpeg, Malgun Gothic 확인. 미리보기와 최종 렌더 완료.
- 최종 1080×1920·30fps 설정·3,600프레임·119.999초, 무음. 목표 120초와 1프레임 이내 차이.
- 미리보기 10/25/41/56/71/86/107/119초 확인. CUDA Graph→Instantiate 연결과 GraphExec 순차 반복 실행 표시를 보완하고 86초 재확인. 최종 71/86/107초 확인.
- 모든 누적 시각 gate 통과. 구체적인 Y=ReLU(XW+b) 예시와 f/g/Add 타임라인 의존성 검산.
- 실제 프레임워크/CUDA 실행·성능과 음원 싱크는 미실시다.

## 122초 사용자 문장 경계 적용 — 현재 기준

- 문장 종료: 6,10,14,18,24,29,34,38,43,48,53,57,61,67,73,79,84,87,93,97,109,115,122초.
- 장면 종료: 10,24,38,53,67,84,109,122초. 120초는 이전 제작 이력이다.
- 전체 배속 없이 Scene.time 누적 목표와 대기를 변경한다. 원고·이동 애니메이션 길이는 유지하며 SRT·timing.json과 대본 구간을 같은 발화 경계로 동기화한다.
- 실제 음원 파일 대조는 미실시다.

### 122초 수정본 검증 결과

미리보기·최종 렌더 완료. 최종 1080×1920·30fps 설정·3,660프레임·121.999초, 무음. 목표 122초와 1프레임 이내 차이. 사용자 제공 23개 문장 종료 시각이 SRT·timing.json과 일치하고 모든 누적 시각 gate 통과. 미리보기 65/82/107초 및 최종 107초 확인. 실제 음원 파일 대조는 미실시.
