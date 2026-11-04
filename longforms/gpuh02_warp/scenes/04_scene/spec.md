# 04 — 개별 상태 · 같은 Warp

- 목적·핵심 주장: 개별 상태 · 같은 Warp.
- 앞 장면 입력: Thread와 Lane
- 확정 구간: 29–42초, 13초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 29–35초 같은 셀 6을 선택해 Thread 6과 Lane 6을 대응. 35–42초 개별 데이터·상태와 하나의 Warp 외곽선 유지.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: SIMT 실행 모델
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

29–35초: 즉, 스레드는 명령을 실행하는 논리적인 단위이고, 레인은 워프 안에서 해당 스레드를 구분하는 번호입니다.

35–42초: 이 스레드들은 각자 다른 데이터와 실행 상태를 가지지만, 워프 단위로 명령을 실행합니다.
