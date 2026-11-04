# 08 — 조건문이 추가되면

- 목적·핵심 주장: 조건문이 추가되면.
- 앞 장면 입력: 같은 명령 · 다른 데이터
- 확정 구간: 66–73초, 7초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 66–70초 공통 경로에서 질문. 70–73초 코드 패널에 if/else를 추가.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 같은 Warp 안의 두 경로
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

66–70초: 그런데 모든 스레드가 항상 같은 명령 경로를 따라야 할까요?

70–73초: 이번에는 코드에 조건문을 추가해 보겠습니다.
