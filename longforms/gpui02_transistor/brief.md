# GPU 개론 02 — 제작 기준

- 사용자 대본 28문장·종료 시각 기준 총 142초. 임의 길이 확장·비례 추정 없음.
- 사용자 첨부 상세 콘티를 storyboard_reference.md에 보존한다. 10개 주장 단위 독립 씬.
- 가로 1920×1080, 세로 1080×1920, 30fps. 미리보기 640×360 / 360×640, 15fps.
- 음원 미제공으로 무음·전체 문장 자막. 화면의 영문과 숫자는 원문 표기를 유지하고 발음은 tts_script.txt로 분리한다.
- 배경 #0B1020, 입력 제어 #A78BFA, 데이터·경로 #4299E1, 활성 경로 #34D399, 비활성 #64748B, 전기장 #F59E0B.
- 전류는 경로의 밝기·연결로 표현한다. 이동 입자로 전자의 속도나 방향을 설명하지 않는다. 전하 점의 이동은 단면 내 재분포 모형에만 사용한다.
- n채널 강화형 MOSFET의 단면은 Source·Drain의 n+ 영역, p-type 몸체, 절연막, Gate, 전도 채널을 구별한다. 전자는 절연막을 관통하지 않는다. Body 단자 등 세부 구조는 생략한 개념도다.
- VGS는 Source 기준의 전압이다. Source–Drain 전류 가능성은 VDS>0 조건을 함께 표시한다. Gate에서 Source/Drain으로 전류가 공급되는 식으로 표현하지 않는다.
- CMOS는 pMOS 상단·nMOS 하단이며 공통 Gate 입력과 두 Drain 사이의 출력 노드를 구별한다. 정적 LOW/HIGH 상태에서 켜진 경로는 상보적이며 전원·접지 양쪽을 동시에 ON으로 그리지 않는다.
- 출력 변화는 전파 지연을 확대해 표현한다. 순간적인 충전·방전과 정적 연결을 구분하고, 상시 큰 직류가 흐르는 효과를 넣지 않는다. 입력 신호가 그대로 출력으로 흘러가는 연출을 사용하지 않는다.
- 자막은 초기화한 Text 객체 하나를 문장 경계에서 즉시 교체한다. 1편에서 발생한 중복 표시를 재현하지 않는다. 별도 SRT는 `_captions.srt`로 두어 자동 중복 로드를 피한다.
- 사용자가 명시한 도입 회상과 마지막 질문은 원문대로 유지한다. 추가 복습·예고 문장은 만들지 않는다.

## 기술 참고

- [Toshiba — Structure and Operation of MOSFET](https://toshiba.semicon-storage.com/ap-en/semiconductor/knowledge/e-learning/discrete/chap3/chap3-7.html): 절연 Gate·전기장·반전 채널의 동작.
- [Analog Devices — Transistors](https://wiki.analog.com/university/courses/electronics/text/chapter-8): MOSFET의 구조와 제어 전압 관계.
- [Infineon — What Is a MOSFET?](https://www.infineon.com/technology/mosfets): Gate–Source 전압·CMOS의 상보 소자 구성.
