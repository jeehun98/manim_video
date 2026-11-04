# 16 — 조건문과 경로의 차이

- 목적·핵심 주장: 조건문과 경로의 차이.
- 앞 장면 입력: 조건문이면 항상 발산할까?
- 확정 구간: 124–134초, 10초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 124–129초 i<32인 32개 Thread의 동일 경로. 129–134초 i<16과 비교해 같은 Warp 안의 경로 차이를 강조.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 스레드별 실행 상태
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

124–129초: 워프 안의 모든 스레드가 같은 조건을 만족한다면 동일한 경로를 실행할 수 있습니다.

129–134초: 중요한 것은 조건문의 존재가 아니라, 같은 워프 안에서 서로 다른 경로가 선택되는지입니다.
