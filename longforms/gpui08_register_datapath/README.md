# GPU 개론 08 — 저장된 값은 어떻게 다시 계산에 사용될까?

사용자 확정 대본 31문장, 153초. 가로 1920×1080 및 세로 1080×1920, 30fps. 음원 미제공으로 무음이며 자막은 영상에 포함한다.

14개의 독립 씬으로 레지스터 구성, MUX 입력 선택, ALU 재사용, 두 읽기 경로와 결과 기록을 설명한다. 전체 대본과 확정 시각은 narration.md 및 timing.json, 씬별 기준은 scenes/*/spec.md에 있다.

실행: `python longforms/gpui08_register_datapath/build.py --preview` 후 `python longforms/gpui08_register_datapath/build.py`.

검증: check_datapath.py, inspect_frames.py, inspect_caption_boundaries.py, verify_exports.py.

4비트 교육용 모델이며 부호 없는 수를 사용한다. 5+3=8을 저장한 뒤 8+2=10을 계산할 때 WE=0이므로 저장된 8은 유지된다. 읽기는 값을 지우지 않으며 쓰기는 대상 선택·쓰기 허용·클럭 상승 에지가 필요하다. Datapath는 ALU, 레지스터 및 선택·전달 연결을 포함하는 구조로 표현한다.

기술 참고: [Berkeley State Elements](https://notes.cs61c.org/content/datapath/elements/), [UCSD register file](https://cseweb.ucsd.edu/classes/su19/cse141L-a/lab2.html).
