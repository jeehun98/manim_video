# 03 — 4 Warp · 128 Thread

- 목적·핵심 주장: 4 Warp · 128 Thread.
- 앞 장면 입력: 128 Thread의 논리 그룹
- 확정 구간: 23–34초, 11초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 23–28초 4×32=128. 28–34초 일반적인 크기 선택 64·128·256을 코드 패널에서 비교. 현재 reduction kernel은 128 고정이라는 조건을 표시.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 공유와 동기화
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

23–28초: 워프 하나는 32개의 스레드로 구성되므로, 이 블록에는 네 개의 워프가 포함됩니다.

28–34초: 블록의 크기는 쿠다 커널을 실행할 때 지정할 수 있으며, 반드시 128개의 스레드로 구성되어야 하는 것은 아닙니다.
