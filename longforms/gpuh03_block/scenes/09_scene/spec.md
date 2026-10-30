# 09 — 기록 중인 Thread들

- 목적·핵심 주장: 기록 중인 Thread들.
- 앞 장면 입력: 128개 값의 공동 적재
- 확정 구간: 77–89초, 12초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 77–83초 동기화 전 가능한 진행 상태 예시로 일부 기록 전 표시. 83–89초 Thread 0이 아직 기록 전인 s[64]를 읽으려는 위험.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: Block 전체의 동기화
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

77–79초: 그런데 여기서 문제가 발생합니다.

79–83초: 모든 스레드가 정확히 같은 순간에 데이터를 기록하는 것은 아닙니다.

83–89초: 어떤 스레드가 다른 스레드의 값을 읽으려고 할 때, 해당 값이 아직 기록되지 않았을 수도 있습니다.
