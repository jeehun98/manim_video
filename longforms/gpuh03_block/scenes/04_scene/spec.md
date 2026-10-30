# 04 — 공유와 동기화

- 목적·핵심 주장: 공유와 동기화.
- 앞 장면 입력: 4 Warp · 128 Thread
- 확정 구간: 34–43초, 9초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 34–38초 고정 Block 관찰. 38–43초 네 Warp에서 하나의 공유 공간으로 연결하는 경로와 동기화 의미.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 128개의 입력 · 하나의 결과
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

34–38초: 그렇다면 스레드들을 하나의 블록으로 묶으면 무엇이 가능해질까요?

38–43초: 가장 중요한 특징 중 하나는 데이터를 공유하고 실행을 동기화할 수 있다는 것입니다.
