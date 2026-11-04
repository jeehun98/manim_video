# 20 — 함께 실행하는 경로

- 목적·핵심 주장: 함께 실행하는 경로.
- 앞 장면 입력: Thread와 Warp의 역할
- 확정 구간: 159–167초, 8초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 159–167초 같은 Warp에서 공통/서로 다른 경로를 비교하고 전체 구조도·32 Lane 상태로 종료. 후속 예고 없음.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 동일 GPU 지도와 Warp에서 종료. 후속편 예고 없음.
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

159–167초: GPU의 병렬 계산을 이해하려면 스레드가 몇 개 있는지만이 아니라, 이 스레드들이 어떤 명령 경로를 함께 실행하는지도 살펴봐야 합니다.
