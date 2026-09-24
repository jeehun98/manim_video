# EML 시리즈 제작 기준

- 논문: Andrzej Odrzywołek, *All elementary functions from a single binary operator*, arXiv:2603.21852 (2026).
- 핵심 primitive: `EML(x,y)=exp(x)−ln(y)`와 상수 `1`.
- 이 시리즈에서 “하나”는 표현 문법의 primitive가 하나라는 뜻이다. 계산량, 메모리 이동, 지연 시간 또는 실제 구현의 명령 수가 자동으로 줄어든다는 뜻으로 사용하지 않는다.
- 화면의 EML 노드는 아래 두 입력 포트와 위 출력 포트를 유지한다. 이후 모든 식은 동일 노드의 binary expression tree로 확장한다.
- 색 의미: x/exp 경로는 파랑, y/log 경로는 분홍, 상수 1과 소거는 초록, EML 및 합성 결과는 금색.
- 1편의 핵심 match cut은 `여러 operator → EML 하나`와 `EML(x,1) tree → exp 복원` 두 장면이다.
- 도입에서 primitive 축소의 이점은 구현 규칙·dispatch·표현 graph를 통일하는 관점으로 설명한다. EML 표현이 실제 하드웨어 면적, 연산량 또는 실행 시간을 자동으로 줄인다고 말하지 않는다.
- 결말의 초점은 exp 자체가 아니라 `깊이 1의 첫 tree → 동일 노드를 반복한 더 깊은 tree`로 이동한다.

## 재사용 컴포넌트

`episodes/eml_series/visuals.py`

- `OperatorChip`: 계산기 연산자 타일.
- `EMLNode`: 안정적인 두 입력/한 출력 anchor를 가진 primitive 노드.
- `ExpressionTree`: `("EML", left, right)` 중첩 튜플을 동일 노드의 tree로 렌더링.
