# GPU 개론 09 — 명령어는 어떻게 회로를 제어할까?

확정 대본 27문장, 총141초. 가로1920×1080 및 세로1080×1920,30fps, 무음·전체 자막. 사용자 제공 문장 종료 시각을 유지한다.

## 학습 목표

입력·연산·쓰기 선택을 명령어 필드로 표현하고, 해독 논리를 통해 실제 데이터 경로의 제어 입력으로 연결하는 과정을 설명한다. 물리적 배선은 고정되고 선택과 연산 기능만 달라진다.

## 교육용 ISA

`OP | RD | RS1 | RS2`, 각각2비트. OP:00 ADD,01 SUB,10 AND,11 OR. R0=00,R1=01,R2=10,R3=11. 저장 데이터는4비트 무부호 정수이며 연산 결과는 하위4비트로 한다. R0는 일반 레지스터로 가정한다. 실제 GPU/CUDA 명령어 규격이 아니다.

`00110110 = ADD R3,R1,R2`: R1=5,R2=3을 읽고 유효한 WE 및 CLK상승에지에서 R3=8로 기록한다. 읽기는 값을 지우지 않는다. `01110110 = SUB R3,R1,R2` 비교에서는WE=0으로 출력2만 달라지고 R3=8을 유지한다.

주소 필드가 선택선으로 직접 연결될 수도 있으며 OP 해석은 고정된 논리 회로에서 수행된다. 쓰기 허용은 실행 시점의 제어 신호이며 8비트 필드 중 특정 비트 하나라고 가정하지 않는다. 마지막 명령어 목록의 `????????`는 미정 자리 표시자다.

## 실행

- `python longforms/gpui09_instruction_control/build.py --preview`
- `python longforms/gpui09_instruction_control/build.py`
- `python longforms/gpui09_instruction_control/check_instruction.py`
- `python longforms/gpui09_instruction_control/inspect_frames.py`
- `python longforms/gpui09_instruction_control/inspect_caption_boundaries.py`
- `python longforms/gpui09_instruction_control/verify_exports.py`

14개의 독립 교체 가능 씬. 대본·시간은 narration.md와 timing.json, 씬별 기준은 scenes/*/spec.md, 상세 콘티는 storyboard_reference.md. 원고 도입·끝 문장은 유지하되 추가 요약·후속 편 타이틀은 넣지 않는다. 단일 자막 객체를 문장 경계에서 교체한다.

기술 참고: [Berkeley 제어 논리](https://notes.cs61c.org/content/datapath/control/), [Berkeley 명령어 해독·데이터 경로](https://notes.cs61c.org/content/datapath/). 실제 RISC-V 형식은 본 영상의 가상8비트 형식과 다르다.
