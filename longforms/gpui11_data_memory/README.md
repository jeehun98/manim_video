# GPU 개론 11 — 레지스터에 없는 데이터는 어떻게 계산할까?

확정37문장174초,14개 독립 씬. 가로1920×1080/세로1080×1920,30fps. 음원 미제공으로 무음이며 원문 자막을 영상에 포함한다.

## 목표

레지스터에 미리 들어 있지 않은 값을 데이터 메모리에서 읽고, ALU로 계산한 결과를 다시 저장할 수 있도록 기존 프로세서의 연결을 확장한다. 빠르게 만드는 최적화보다 실행 가능한 프로그램의 범위를 넓히는 기능적 확장이다.

## 예시와 정확성

Memory[100]=5,Memory[101]=3,Memory[102]=0. LOAD R1,[100] → LOAD R2,[101] → ADD R3,R1,R2 → STORE R3,[102]. 두 Load는 순차 실행하며 결과 Memory[102]=8,원래100/101값과R1/R2/R3는유지된다.

주소와 데이터는 구분한다. 주소100/101/102는 별도 주소 경로에서 표현하며 이 편에서는 주소 계산을 상세히 구현하지 않는다. 명령어는 교육용 사람이 읽는 표기이며 이전8비트 산술 형식에 주소100을 담는 인코딩을 만들지 않는다. 데이터·주소의 비트폭은 단정하지 않는다.

쓰기 MUX는 ALU와 메모리의 독립 결과 후보 중 하나를 고른다. 실제 레지스터 기록은 목적지·RegWE·응답유효·갱신에지 조건이 필요하다. Store는 레지스터→메모리WriteData이며 MemWE가유효할때지정주소만갱신한다. Store중RegWE=0. 주소변화만으로쓰지않는다.

명령어메모리와데이터메모리는역할구분을위해그리며반드시물리적으로분리된장치라는주장이아니다. 마지막구간은데이터응답이준비되지않은동안목적지등을유지해야한다는문제를제시한다. 구체적인사이클수·지연수치는정하지않는다.

## 실행

- `python longforms/gpui11_data_memory/build.py --preview`
- `python longforms/gpui11_data_memory/build.py`
- `python longforms/gpui11_data_memory/check_memory.py`
- `python longforms/gpui11_data_memory/inspect_frames.py`
- `python longforms/gpui11_data_memory/inspect_caption_boundaries.py`
- `python longforms/gpui11_data_memory/verify_exports.py`

사용자원문도입·마지막문장은보존하되별도GPU12예고제목은넣지않는다. 대본·발음원고·타이밍·씬명세는각파일에기록한다.

기술 참고: [Berkeley Load/Store 데이터 경로](https://notes.cs61c.org/content/datapath/load-store/), [Berkeley 상태 요소와 쓰기 제어](https://notes.cs61c.org/content/datapath/elements/).
