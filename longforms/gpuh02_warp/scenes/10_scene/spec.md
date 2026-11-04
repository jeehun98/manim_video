# 10 — 경로가 나뉜 Warp

- 목적·핵심 주장: 경로가 나뉜 Warp.
- 앞 장면 입력: 같은 Warp 안의 두 경로
- 확정 구간: 79–90초, 11초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 79–85초 같은 Warp 안에 ×2와 +1 경로 표시. 85–90초 외곽선은 하나인 채 두 경로를 함께 관찰.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 참여 Lane을 선택하는 마스크
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

79–85초: 이제 워프 안의 스레드 0부터 15까지는 곱셈을, 16부터 31까지는 덧셈을 수행해야 합니다.

85–90초: 문제는 하나의 워프 안에서 서로 다른 명령 경로가 필요하다는 것입니다.
