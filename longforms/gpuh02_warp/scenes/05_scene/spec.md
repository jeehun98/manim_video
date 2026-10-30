# 05 — SIMT 실행 모델

- 목적·핵심 주장: SIMT 실행 모델.
- 앞 장면 입력: 개별 상태 · 같은 Warp
- 확정 구간: 42–48초, 6초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 42–46초 SIMT와 전체 Lane의 공통 명령 반응. 46–48초 동일 벡터 덧셈 소스로 연결.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 코드와 서로 다른 인덱스
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

42–46초: 이러한 실행 모델을 SIMT, Single Instruction, Multiple Threads라고 합니다.

46–48초: 실제 쿠다 코드를 살펴보겠습니다.
