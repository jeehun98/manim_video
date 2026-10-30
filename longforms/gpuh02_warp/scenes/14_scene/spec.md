# 14 — Warp Divergence

- 목적·핵심 주장: Warp Divergence.
- 앞 장면 입력: 덧셈 경로 · 16개 활성
- 확정 구간: 106–118초, 12초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 106–113초 두 마스크를 같은 Warp에서 번갈아 관찰. 113–118초 여러 경로와 명령별 활성 참여량의 관계. 실측 속도 배율은 주장하지 않음.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 조건문이면 항상 발산할까?
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

106–113초: 이처럼 하나의 워프에 속한 스레드들이 서로 다른 실행 경로로 나뉘는 현상을 Warp Divergence, 워프 분기 발산이라고 합니다.

113–118초: 분기 발산이 발생하면 여러 경로를 처리해야 하므로 실행 효율이 떨어질 수 있습니다.
