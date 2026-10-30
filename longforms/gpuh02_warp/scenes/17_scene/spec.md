# 17 — 스레드별 실행 상태

- 목적·핵심 주장: 스레드별 실행 상태.
- 앞 장면 입력: 조건문과 경로의 차이
- 확정 구간: 134–145초, 11초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 134–145초 같은 32개 셀을 유지하며 Volta 이후 Thread별 PC·상태를 개념도로 표시. 독립 명령 발행 장치처럼 그리지 않음.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 명령 실행은 Warp 단위
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

134–145초: 또한 실제 엔비디아 GPU의 실행 방식은 세대에 따라 차이가 있으며, 볼타 이후의 아키텍처에서는 스레드별 실행 상태를 더욱 독립적으로 관리할 수 있습니다.
