# 19 — Thread와 Warp의 역할

- 목적·핵심 주장: Thread와 Warp의 역할.
- 앞 장면 입력: 명령 실행은 Warp 단위
- 확정 구간: 150–159초, 9초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 150–159초 Thread 6의 Index·Data·State를 같은 셀에서 확인한 뒤 전체 Warp 외곽선으로 확장.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 함께 실행하는 경로
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

150–159초: 결국 스레드는 각자의 데이터와 실행 상태를 가진 논리적인 실행 단위이고, 워프는 이러한 스레드 32개를 묶어 명령을 실행하는 하드웨어 단위입니다.
