# 17 — 같은 SM의 실행 자원

- 목적·핵심 주장: 같은 SM의 실행 자원.
- 앞 장면 입력: Block 전체를 한 SM에 배치
- 확정 구간: 143–148초, 5초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 143–148초 동일 SM0의 Warp Scheduler·Register File·Shared Memory 자원을 연결. 특정 사이클·스케줄을 주장하지 않음.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: Block 내부의 동기화 범위
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

143–148초: 같은 블록의 워프들은 해당 에스엠의 실행 자원과 공유 메모리를 사용합니다.
