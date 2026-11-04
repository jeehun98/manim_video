# 12 — 곱셈 경로 · 16개 활성

- 목적·핵심 주장: 곱셈 경로 · 16개 활성.
- 앞 장면 입력: 참여 Lane을 선택하는 마스크
- 확정 구간: 95–102초, 7초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 95–102초 곱셈 줄과 앞 16개의 활성 상태를 함께 표시. 나머지 16개는 자리를 유지하며 어둡게 표시.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 덧셈 경로 · 16개 활성
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

95–102초: 먼저 곱셈 경로에서는 앞의 16개 스레드가 활성화되고, 나머지 스레드는 해당 경로에서 비활성화됩니다.
