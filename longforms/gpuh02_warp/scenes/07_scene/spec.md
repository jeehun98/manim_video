# 07 — 같은 명령 · 다른 데이터

- 목적·핵심 주장: 같은 명령 · 다른 데이터.
- 앞 장면 입력: 코드와 서로 다른 인덱스
- 확정 구간: 57–66초, 9초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 57–61초 Lane 0과 1의 실제 입력·출력 대응. 61–66초 같은 ADD에 모든 Lane이 참여.
- 화면 텍스트: GPU / SM 0 / Block 0 / Warp 0, 고정 Lane 0–31, 관련 코드·마스크.
- 시작·종료: 동일 지도·동일 Lane 좌표에서 현재 선택·경로·참여 마스크만 변경.
- 다음 연결: 조건문이 추가되면
- 조건·과장 방지: 1 Block × 32 Thread 예시. lane와 threadIdx.x가 이 예시에서만 일치. 명령 경로 개념도이며 실제 사이클·명령 발행 순서·성능 배율을 주장하지 않는다. 작은 if는 compiler predication으로 변환될 수 있음.
- 출처: NVIDIA CUDA Programming Guide — SIMT, Independent Thread Scheduling; CUDA Best Practices — control flow. 프로젝트 README 참고.

## 문장별 확정 시각

57–61초: 스레드 0은 0번 원소를, 스레드 1은 1번 원소를 계산합니다.

61–66초: 이렇게 32개의 스레드가 같은 명령을 실행하면서 서로 다른 데이터를 처리합니다.
