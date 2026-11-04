# 03 — Thread와 Lane

- 목적·핵심 주장: Thread와 Lane.
- 앞 장면 입력: 32개 Thread의 실행 그룹
- 확정 구간: 17–29초, 12초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 17–22초 같은 Warp의 번호 0–31을 관찰. 22–27초 Lane 번호를 순차 강조. 27–29초 Lane Index 명명.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 개별 상태 · 같은 Warp
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

17–19초: 하나의 워프를 살펴보겠습니다.

19–22초: 워프는 32개의 스레드로 구성됩니다.

22–27초: 그리고 각 스레드는 워프 안에서 0부터 31까지의 위치를 가집니다.

27–29초: 이 위치를 레인, Lane이라고 부릅니다.
