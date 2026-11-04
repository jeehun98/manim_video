# 16 — Block 전체를 한 SM에 배치

- 목적·핵심 주장: Block 전체를 한 SM에 배치.
- 앞 장면 입력: Shared Memory를 통한 협력
- 확정 구간: 135–143초, 8초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 135–139초 Block을 감싼 GPU·SM 지도 관찰. 139–143초 네 Warp와 Shared 할당을 포함한 Block0 전체를 SM0에 배치.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 같은 SM의 실행 자원
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

135–139초: 그렇다면 블록은 실제 GPU 하드웨어에서 어디에 배치될까요?

139–143초: 쿠다의 블록은 실행될 때 하나의 에스엠에 배치됩니다.
