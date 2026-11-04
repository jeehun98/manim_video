# GPU 개론 10 — 컴퓨터는 어떻게 프로그램을 실행할까?

확정35문장165초,15개독립씬. 가로1920×1080 및 세로1080×1920,30fps,무음·전체자막. 사용자제공종료시각을그대로사용하며음원을별도로받지않았다. 발화자표기로보이는연우는내레이션에포함하지않는다.

## 제작 기준

PC는명령어의주소를저장하는레지스터다. 명령어메모리는그주소의명령어비트열을출력한다.해독회로의제어에따라두독립읽기경로와ALU가동작하고유효한WE·CLK에지에서결과를기록한다. PC갱신도저장동작이므로별도유효갱신시점에일어난다.

교육용슬롯주소는명령어1개당+1이다.실제CPU/GPU의명령어길이·바이트주소증분을일반화하지않는다. 9편의가상8비트ISA재사용:OP|RD|RS1|RS2,각2비트.주소0=00110110(ADD R3,R1,R2),주소1=01111101(SUB R3,R3,R1).초기R1=5,R2=3,R3=0→8→3.

분기는별도예시다.앞의산술프로그램에서R3=0이되었다고하지않는다.분기명령해독·조건판정·목표주소계산후의PC선택을추상화한다.조건거짓이면1→2,참이면1→3.두후보배선은고정되고메모리내용은변하지않는다.산술ISA에분기비트를추가하지않는다.

화면은원고의도입·결론·마지막문장을그대로유지한다.추가NEXT/GPU11예고타이틀은넣지않는다.실행단계애니메이션은논리적설명순서이며사이클수나현대프로세서의파이프라인을단정하지않는다.

## 실행

- `python longforms/gpui10_program_execution/build.py --preview`
- `python longforms/gpui10_program_execution/build.py`
- `python longforms/gpui10_program_execution/check_program.py`
- `python longforms/gpui10_program_execution/inspect_frames.py`
- `python longforms/gpui10_program_execution/inspect_caption_boundaries.py`
- `python longforms/gpui10_program_execution/verify_exports.py`

기술 참고: [Berkeley 명령어인출·데이터경로](https://notes.cs61c.org/content/datapath/), [Berkeley 분기와다음PC선택](https://notes.cs61c.org/content/datapath/b-type/). 교육용형식은실제RISC-VISA와다르다.

단계별 화면은 실행 당시의 피연산자와 선택 결과를 보존해 보여주는 설명용 추적 모델이다. 저장 에지 직후의 모든 조합 회로 과도 상태를 시뮬레이션하는 영상은 아니다.
