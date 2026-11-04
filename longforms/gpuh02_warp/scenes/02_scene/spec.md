# 02 — 32개 Thread의 실행 그룹

- 목적·핵심 주장: 32개 Thread의 실행 그룹.
- 앞 장면 입력: Thread에서 Warp로
- 확정 구간: 8–17초, 9초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 8–12초 같은 32개 셀을 Warp 0 외곽선으로 묶음. 12–17초 실행 그룹과 명령 발행을 강조.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: Thread와 Lane
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

8–12초: 엔비디아 GPU에서는 32개의 스레드를 하나의 워프, Warp로 묶어 실행합니다.

12–17초: 워프는 GPU가 스레드들을 스케줄링하고 명령을 실행하는 기본 단위입니다.
