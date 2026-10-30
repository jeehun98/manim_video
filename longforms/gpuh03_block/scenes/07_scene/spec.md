# 07 — 코드와 공유 배열의 주소

- 목적·핵심 주장: 코드와 공유 배열의 주소.
- 앞 장면 입력: Block의 Shared Memory
- 확정 구간: 62–73초, 11초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 62–67초 __shared__ float s[128] 강조. 67–73초 Warp별 공동 적재를 보여주며 s[0]=1, s[64]=65 등 대표 주소를 대응.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 128개 값의 공동 적재
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

62–67초: 셰어드 로 선언한 배열은 같은 블록에 속한 스레드들이 함께 사용할 수 있는 메모리 공간입니다.

67–73초: 각 스레드는 자신의 인덱스를 이용해 입력값을 읽고, 공유 메모리의 서로 다른 위치에 저장합니다.
