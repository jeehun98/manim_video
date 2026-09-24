# EML 04 제작 기준

- 시리즈에서 직접 구성한 `exp`, `ln`, `+`만 복습 문장에 포함한다. `×`는 논문이 포함하는 이후 연산 세계의 배경 기호다.
- 핵심 morph는 같은 `EMLNode` 객체 12개를 유지한 채 위치와 연결선만 바꾸어 exp(1 node), ln(3 nodes), add(9 nodes)를 만드는 장면이다.
- 동일 primitive가 모든 계산을 같은 비용으로 만든다는 뜻이 아니다. topology, node count, depth와 실행 환경은 별도다.
- NAND 비교는 functional completeness라는 구조적 아이디어에 한정한다. EML을 디지털 NAND와 하드웨어적으로 동일시하지 않는다.
- 마지막 질문은 `복잡성은 부품의 종류에서 오는가, 조합에서 오는가?`이다.
