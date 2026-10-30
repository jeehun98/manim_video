# 01 — Thread에서 Warp로

- 목적·핵심 주장: Thread에서 Warp로.
- 앞 장면 입력: 같은 GPU·SM 0·Block 0의 Thread 선택
- 확정 구간: 0–8초, 8초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 0–3초 같은 SM·Block의 Thread 1을 선택. 3–8초 동일 Block의 32개 Thread로 시야 확장.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 32개 Thread의 실행 그룹
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

0–3초: GPU에서는 수많은 스레드가 계산을 수행합니다.

3–8초: 그렇다면 이 스레드들은 실제 하드웨어에서 모두 독립적으로 실행될까요?
