# 18 — 명령 실행은 Warp 단위

- 목적·핵심 주장: 명령 실행은 Warp 단위.
- 앞 장면 입력: 스레드별 실행 상태
- 확정 구간: 145–150초, 5초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 145–150초 Warp 외곽선과 활성 마스크를 강조. 개별 상태와 Warp 명령 실행을 구분.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: Thread와 Warp의 역할
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

145–150초: 하지만 워프 단위의 명령 실행과 활성 스레드의 개념은 여전히 중요합니다.
