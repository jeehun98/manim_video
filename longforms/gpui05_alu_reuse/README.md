# GPU 개론 05 — 하나의 회로로 여러 연산을 수행하는 방법

사용자 확정 대본 35문장·종료 시각 기준 175초. 독립 씬 16개. 음원 미제공.

가로 1920×1080 / 세로 1080×1920, 30fps. 무음·전체 문장 자막.

```powershell
python longforms/gpui05_alu_reuse/check_alu.py
python longforms/gpui05_alu_reuse/build.py --preview
python longforms/gpui05_alu_reuse/build.py
python longforms/gpui05_alu_reuse/inspect_frames.py
python longforms/gpui05_alu_reuse/inspect_caption_boundaries.py
python longforms/gpui05_alu_reuse/verify_exports.py
```

개별 씬 수정: `build.py --scene 5 --layout shorts`, 이후 `build.py --resume`으로 결합한다. --resume은 프레임 수만 검사하므로 수정한 씬은 명시적으로 다시 렌더한다. Manim 0.21 / Python 3.12 / FFmpeg / Malgun Gothic.

핵심: 4비트 2의 보수 → XOR·Cin 제어로 가산기 공유 → 별도 비교 판단 → AND/OR → MUX → 고정 배선의 ALU.

A=0101, B=0011에 대해 예시 코드 00 ADD=1000 / 01 SUB=0010 / 10 AND=0001 / 11 OR=0111. 00/01은 같은 산술 경로와 MUX 입력 핀을 공유하며 01일 때 SUB=1이다. ADD와 SUB용 가산기를 두 개 그리지 않는다. 비교 판단 논리는 가산기와 별도이며 signed LT=N XOR V, unsigned LT=NOT Cout인 본 회로의 관례를 사용한다. Cout=1은 A+NOT(B)+1 뺄셈에서 빌림 없음이다. 명령어 체계마다 플래그 관례가 다를 수 있다.

독립 씬 내 가산기 객체를 유지하고 컷 뒤 동일 공통 도형을 재현한다. 제어 변경 시 배선 토폴로지가 유지되는지 실제 Scene 실행 중 assert한다. MUX의 각 후보는 별도 입력 핀에 연결되고 직접 단락하지 않는다. 비선택 경로도 값을 가질 수 있다. DIV는 이 예시 장치에 직접 구현되지 않은 연산이다.

검증 모델: check_alu.py (ADD/SUB 512, 비교 256, ALU/MUX 1024 입력 조합·오버플로 포함).

참고 자료: [Berkeley CS61C adder/subtractor](https://notes.cs61c.org/content/sds-blocks/adder-subtractor/), [Cornell CS3410 ALU](https://www.cs.cornell.edu/courses/cs3410/2019sp/projects/alu/), [ANU ALU lab](https://comp.anu.edu.au/courses/comp2300/labs/02-alu/).

원본 콘티: storyboard_reference.md. 확정 대본: master_script.md / narration.md. 타이밍: timing.json / captions.srt. TTS 원고는 읽지 않을 제목·시각 없이 화면 변화별 빈 줄로 나눈다. 음원이 제공되면 확정 175초 타임라인에 결합한다.
