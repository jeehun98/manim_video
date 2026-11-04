# 02 — 128 Thread의 논리 그룹

- 목적·핵심 주장: 128 Thread의 논리 그룹.
- 앞 장면 입력: Warp에서 Block으로
- 확정 구간: 12–23초, 11초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 12–19초 Block 전체 관찰. 19–23초 128 Thread 고정 배치와 launch 설정을 대응.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 4 Warp · 128 Thread
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

12–17초: 블록은 여러 스레드를 하나의 그룹으로 묶는 논리적인 실행 단위입니다.

17–19초: 하나의 블록을 살펴보겠습니다.

19–23초: 이번에는 128개의 스레드로 구성된 블록을 생각해 보겠습니다.
