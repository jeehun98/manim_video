# 01 — Warp에서 Block으로

- 목적·핵심 주장: Warp에서 Block으로.
- 앞 장면 입력: 같은 GPU/SM0/Block0의 Warp0
- 확정 구간: 0–12초, 12초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 0–5초 Warp 0의 동일한 32 Lane 보기. 5–10초 Warp 0을 축소해 Warp 1·2·3이 있는 같은 Block으로 확장. 10–12초 Block 외곽선 강조.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 128 Thread의 논리 그룹
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

0–5초: GPU에서는 32개의 스레드가 하나의 워프로 묶여 명령을 실행합니다.

5–10초: 그렇다면 서로 다른 워프에 속한 스레드들이 하나의 계산을 함께 수행하려면 어떻게 해야 할까요?

10–12초: 여기서 등장하는 것이 블록입니다.
