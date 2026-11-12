# GPU 개론3부 마무리 · 하나의 명령어에서 병렬 실행까지

독립마무리/롱폼에필로그. 원본11~15단순합본이아님. 확정28문장141초·13씬,가로/세로1080p30·자막포함·무음.

`python longforms/gpui_part3_epilogue/build.py --preview`

`python longforms/gpui_part3_epilogue/build.py`

`python longforms/gpui_part3_epilogue/verify_exports.py`

shared_components.py는기존13/14/15편검수된시각요소와15편연산모델을재사용한다.

메인예시LOAD R1,[100]→ADD R3,R1,R2→STORE R3,[102],Memory100=5,R2=3,결과R3=Memory102=8. 병렬ALU별도예시SUB R6,R4,R5에서R4=9,R5=2,R6=7. Forwarding별도ADD→SUB예시는R5=2/R4결과6으로구별. 두화면비공통애니메이션과별도배치. 새회로는기존Core동일좌표에누적·확대/축소. 2비트FSM은다중사이클설계의제어이며파이프라인확장후에는단계별제어로조직변경(하나의전역상태가한단계만활성화하는구조를그대로유지하지않음). 4단계설명→5단계IF/ID/EX/MEM/WB정리는개념적단계세분화. 독립명령메모리/데이터접근경로가정. 파이프라인동작이Load의미준비값을ADD에공급한다고표현하지않음. Stall은PC/IFID유지·IDEX버블,A진행. Forwarding은준비된값만전달,단일ALU시간재사용. 다중ALU는이미준비된두독립명령에대한자원확장,인출/해독/스케줄러문제완성주장없음. 읽기4/쓰기2포트는교육용설계선택. 파이프라인과다중ALU를구별. ALU증가그림은확장가능성개념도이지실제GPU구조가아님. 원문28문장141초보존,회고/다음질문은사용자명시요청으로포함하며추가예고/엔드카드없음. 음원미제공으로무음.