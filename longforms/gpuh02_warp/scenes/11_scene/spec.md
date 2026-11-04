# 11 — 참여 Lane을 선택하는 마스크

- 목적·핵심 주장: 참여 Lane을 선택하는 마스크.
- 앞 장면 입력: 경로가 나뉜 Warp
- 확정 구간: 90–95초, 5초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 90–95초 현재 명령의 참여 Lane과 Active Mask 연결.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 곱셈 경로 · 16개 활성
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

90–95초: GPU는 각 경로를 실행할 때 해당 경로에 참여하는 스레드만 활성화할 수 있습니다.
