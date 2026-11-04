# 12 — 128 → 64 부분 합계

- 목적·핵심 주장: 128 → 64 부분 합계.
- 앞 장면 입력: 공유 배열에서 합산 시작
- 확정 구간: 108–115초, 7초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 108–115초 stride64. Thread 0–63이 s[t]+s[t+64]를 계산. 64 부분 합계, 모든 128 Thread가 다음 장벽에 참여.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 64 → 32 → … → 1
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

108–115초: 스레드 0부터 63까지가 각각 다른 위치의 값을 더하면, 64개의 부분 합계가 만들어집니다.
