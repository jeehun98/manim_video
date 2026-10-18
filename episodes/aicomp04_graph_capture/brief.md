# AI 컴파일러 04 — 파이썬 신경망은 어떻게 계산 그래프가 될까?

## 제작 상태

사용자 확정 콘티 10장면·21개 발화 구간·152초로 화면을 제작한다. 실제 음원은 미제공이다. approved_segments.txt에 사용자 발음 원문을 보존하고 prepare.py로 대본·TTS·SRT·timing.json을 생성한다. 발음 원고에 있던 종료 시각은 타이밍 자료로 옮기고 원고에는 읽을 문장만 남긴다. scene.py의 렌더 ID는 aicomp04다. 앞 영상 복습·후속 예고 없이 독립적으로 완결한다.

## 중심 질문과 개념

컴파일러는 프로그램의 어떤 부분을 어떻게 포착하는가? 코드의 문법 구조보다 **실제 값 계산과 연산 기록의 차이 → 값에 의존하는 분기 → 포착 범위가 나뉘는 이유**를 발견하게 한다. AST·SSA·IR 정의 강의로 확장하지 않는다. 정확성은 예시의 조건과 짧은 화면 표기로 지키며 도구 이름을 나열하지 않는다.

## 공통 코드와 분기 예시

```python
def forward(x, W, b):
    h = x @ W
    z = h + b
    return torch.relu(z)
```

분기 장면에서는 별도 변형임을 알리고 다음 코드를 사용한다.

```python
def forward(x, W, b):
    y = x @ W
    if y.sum() > 0:
        y = torch.relu(y)
    return y + b
```

분기 예시의 편향 덧셈은 ReLU 이후다. 도입의 `ReLU(XW+b)`와 같은 계산으로 표시하지 않는다. X[M,K], W[K,N], b[N]으로 shape가 성립한다.

## 장면 구성

| 구간 | 화면 | 전달할 발견 |
|---|---|---|
| 도입 | 짧은 Python 코드와 GPU 사이에 질문 | Python 전체를 그대로 GPU 코드로 옮기는가? |
| 1 | h·z 값의 사용을 MatMul → Add → ReLU로 연결 | 연산과 값의 관계를 포착 |
| 2 | 실제 실행은 원소→계산값, Symbolic Tracing 예시는 Proxy x→연산 기록→그래프 | 숫자를 계산하는 것과 구조를 기록하는 것은 다름 |
| 3 | 분기 코드에 y.sum()>0 강조, 양수/비양수 두 입력 사례 | 실제 값이 경로를 결정 |
| 3 후반 | 포착 구간 A, Python 분기, 이후 포착 구간 B의 경계 | 포착 방식이 처리하지 못하는 동작에서 중단 가능 |
| 4 | A 실행 → Python 분기 처리 → 후속 구간 실행, 전체 프로그램 테두리는 유지 | Graph Break가 항상 실행 실패는 아님 |
| 4 보충 | 지원되는 명시적 조건 연산을 별도 작은 도식으로 표시 | 모든 컴파일러에서 분기가 불가능한 것은 아님 |
| 결론 | 전체 프로그램 테두리와 그 안의 포착된 그래프 영역 비교 | 원래 프로그램과 한 번에 분석하는 범위는 다를 수 있음 |

## 기술·연출 조건

사용자 확정 콘티의 장면 배정은 다음과 같다. 06~08에 총 41초를 둔다. 한 장면 안의 주요 화면 변화는 사용자 발화 종료 시각에 맞춘다.

| 장면 | 시작–종료 | 길이 | 화면 |
|---|---|---|---|
| 01 | 0–6초 | 6초 | Python 함수 전체의 경계와 질문 |
| 02 | 6–26초 | 20초 | 코드·수식에서 연산과 값 연결로 |
| 03 | 26–34초 | 8초 | 데이터 의존성과 Graph Capture 이름 |
| 04 | 34–64초 | 30초 | 실제 값 계산과 FX Proxy의 연산 기록 비교 |
| 05 | 64–74초 | 10초 | FX Symbolic Tracing과 TorchDynamo 구분 |
| 06 | 74–89초 | 15초 | 데이터 의존 분기와 실제 값에 따른 경로 |
| 07 | 89–100초 | 11초 | Graph Break와 포착 범위 분할 |
| 08 | 100–115초 | 15초 | 포착·컴파일을 먼저 제시하고 Runtime Execution으로 화면 전환 |
| 09 | 115–131초 | 16초 | fullgraph 설정 구분과 torch.cond 가능성 |
| 10 | 131–152초 | 21초 | 전체 프로그램의 경계와 포착 범위 비교 |

반드시 다르게 보여줄 세 쌍: **FX Symbolic Tracing / TorchDynamo**, **Graph Capture / Runtime Execution**, **Graph Break / Execution Failure**. FX에만 Proxy를 연결하고, 값 토큰은 Runtime Execution에서만 분기를 선택한다. 분할 개념도에서는 가능한 경로를 표시하되 실제 실행 예시에서는 sum=+2의 True 경로만 강조한다. 포착과 실행은 이해를 위한 별도 화면이며 JIT에서는 호출 과정에서 이어질 수 있다고 주석을 둔다.

1. Graph Capture는 계산을 컴파일러가 다룰 표현으로 얻는 넓은 개념이며 Tracing은 한 접근이다. FX symbolic_trace, Dynamo의 Python 바이트코드 해석, 실제 입력 기반 tracing, 명시적 그래프 구성은 서로 다른 방법이다. 한 도구가 모든 방식을 동시에 수행하는 파이프라인으로 합치지 않는다.
2. FX의 Proxy는 연산을 기록하는 대리 객체다. ‘Shape만 가진 텐서’ 또는 FakeTensor와 동일하다고 그리지 않는다. Proxy에 shape 정보가 자동으로 항상 구체적으로 들어 있다고 보장하지 않는다. 화면에는 ‘Symbolic Tracing 예시 · 입력 원소 계산 대신 연산 기록’을 표시한다. 속성·상수 등은 포착 중 실제로 처리될 수 있으므로 어떤 계산도 전혀 하지 않는다고 단정하지 않는다.
3. 조건 `y.sum()>0`의 True/False는 텐서 원소에 의존한다. 텐서 크기에 따른 Python 분기·정적 설정에 따른 분기를 모두 같은 제약으로 일반화하지 않는다.
4. Graph Break 설명은 torch.compile/TorchDynamo의 부분 포착 예시다. 전통적 FX symbolic_trace의 Proxy에 따른 분기 오류를 그대로 ‘부분 그래프 실행 후 재개’로 설명하지 않는다. 장면 사이 ‘다른 포착 방식의 예’ 표기로 도구 전환을 명확히 한다.
5. `fullgraph=False`에서 이미 얻은 그래프를 컴파일하고 지원하지 않는 코드를 일반 Python으로 실행한 뒤 포착을 재개할 수 있다. 모든 중단에서 항상 복구·성공하는 것은 아니며 `fullgraph=True` 등 단일 그래프 요구에서는 오류가 가능하다. 음성에서는 설정 이름 대신 개념을 짧게 설명한다.
6. A: MatMul·Reduce, Python: 조건 판단, B: 선택된 경로의 연산·Add는 개념도다. 비교 연산 포함 위치·분할 개수·재개 위치·후속 그래프 구성은 구현과 설정에 따라 다르다. 실제 포착 결과나 실행 로그로 제시하지 않는다. 양쪽 경로가 조건 없이 모두 실행되는 그림도 피한다.
7. `torch.cond` 같은 지원되는 명시적 제어 흐름으로 동적 분기를 그래프에 표현할 수 있다. 지원·제약이 있으며 임의 Python if를 무조건 대체할 수 있다고 설명하지 않는다. 이름은 보조 화면 표기로 두고 상세 사용법은 생략한다.
8. 넓은 포착 범위는 연산 간 분석 기회를 늘릴 수 있으나 항상 빠르다는 보장은 없다. Graph Break 제거를 곧 정확성 향상이나 성능 보장으로 표현하지 않는다.

## 확인한 공식 자료

- [PyTorch FX](https://docs.pytorch.org/docs/stable/fx.html): Proxy를 이용한 symbolic tracing, 데이터 의존 제어 흐름의 한계.
- [Dynamo Core Concepts](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/compile/programming_model.dynamo_core_concepts.html): Python 바이트코드 해석, 기본 설정에서 부분 그래프 컴파일과 일반 Python 실행·포착 재개.
- [Common Graph Breaks](https://docs.pytorch.org/docs/main/user_guide/torch_compiler/compile/programming_model.common_graph_breaks.html): 데이터 의존 분기와 명시적 조건 연산.
- [torch.compile Programming Model](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/compile/programming_model.html): 부분 포착·단일 그래프 설정 구분.

## 검증

대본과 TTS의 발화 내용을 대조하고, 1편 최종 발음 원고와 분량을 비교한다. 숫자·영문은 대본과 화면에 유지하며 발음 원고에만 한국어로 적는다. 실제 시각은 추정하지 않는다.

- 이전 19구간 초안을 사용자 확정 21구간·152초 대본으로 대체한다. 문장 종료 시각은 6,17,26,34,38,45,52,60,64,74,80,89,96,100,110,115,123,131,136,143,152초다.

## 출력과 검증 기준

- 미리보기 360×640, 최종 1080×1920, 30fps, 기본 무음. 음원 합성·mux는 하지 않는다.
- Scene.time 누적 gate로 발화 종료 시각에 맞추며 초과 시 오류를 발생시킨다. 전체 배속으로 길이를 맞추지 않는다.
- 영상에는 짧은 핵심 자막을, 별도 SRT에는 전체 발화를 둔다. 긴 발화의 SRT 내부 경계는 문자량 기준으로 배분하며 사용자 종료 시각은 유지한다. 음원 기반 정렬 결과는 아니다.
- 실행: `python scripts/render.py aicomp04 --preview`, `python scripts/render.py aicomp04`.

## 제작 검증 결과

- Manim 0.21.0·FFmpeg·Malgun Gothic 확인. 미리보기·최종 렌더 완료, 모든 누적 발화 시간 gate 통과.
- 최종 1080×1920·30fps·4,560프레임·152.000초. 미리보기 360×640·30fps·4,560프레임, 컨테이너 약151.997초로 1프레임 이내. 오디오 스트림 없음.
- 6초 간격 미리보기 접촉 시트, 57·107·120·126초 개별 프레임, 최종 94·107·148초를 확인했다. 주요 도형·자막 겹침과 프레임 밖 잘림 없음.
- FX Proxy 연산 기록과 Dynamo 포착 예시를 별도 화면으로 구분했다. 포착·컴파일 화면에서 Runtime Execution으로 전환한 후 실제 입력의 True 경로만 강조함을 확인했다. Graph Break와 실행 실패도 별도 메시지로 구분했다.
- 사용자 원문과 TTS 21구간 일치, 읽지 않을 타임코드 제거, SRT에 21개 종료 시각 모두 포함, 10개 장면 종료와 최종152초 확인. Python 구문 검사·git diff --check 통과.
- 실제 음원과 발화 싱크 대조는 미실시다. SRT 발화 내부 분할은 문자량 기준이다. 그래프 분할도는 실제 torch.compile 실행 출력이 아닌 개념도다.
