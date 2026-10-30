# 05 — 128개의 입력 · 하나의 결과

- 목적·핵심 주장: 128개의 입력 · 하나의 결과.
- 앞 장면 입력: 공유와 동기화
- 확정 구간: 43–56초, 13초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 43–48초 input[t]=t+1의 128개 입력. 48–51초 각 Thread가 자기 위치를 담당. 51–56초 output[0] 하나가 필요함을 강조.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: Block의 Shared Memory
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

43–45초: 간단한 계산을 살펴보겠습니다.

45–48초: 128개의 숫자를 모두 더하려고 합니다.

48–51초: 각 스레드가 숫자 하나씩을 읽는 것은 어렵지 않습니다.

51–56초: 하지만 최종 합계 하나를 만들려면 서로 다른 스레드가 읽어온 값들을 합쳐야 합니다.
