# 10 — Block 전체의 동기화

- 목적·핵심 주장: Block 전체의 동기화.
- 앞 장면 입력: 기록 중인 Thread들
- 확정 구간: 89–102초, 13초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 89–92초 __syncthreads() 등장. 92–97초 Warp 도착 순서는 설명용으로 제시하고 모든 128 Thread가 장벽에 참여. 97–102초 장벽 해제와 기록 가시성.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 공유 배열에서 합산 시작
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

89–92초: 이 문제를 해결하기 위해 사용하는 것이 싱크 스레드 입니다.

92–97초: 이 명령을 만나면 같은 블록의 스레드들은 동기화 지점에 도달할 때까지 기다립니다.

97–102초: 그리고 동기화 이전의 메모리 기록을 다른 스레드들이 올바르게 확인할 수 있도록 보장합니다.
