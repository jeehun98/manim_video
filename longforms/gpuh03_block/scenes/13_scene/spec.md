# 13 — 64 → 32 → … → 1

- 목적·핵심 주장: 64 → 32 → … → 1.
- 앞 장면 입력: 128 → 64 부분 합계
- 확정 구간: 115–123초, 8초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 115–119초 stride32·16. 119–123초 stride8·4·2·1. 각 단계 뒤 Block 장벽. Shared Memory의 앞부분만 부분 합계로 남고 Thread 수는 계속128.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: Thread 0의 결과 저장
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

115–119초: 다음 단계에서는 32개, 그다음에는 16개로 줄어듭니다.

119–123초: 이 과정을 반복하면 마지막에는 하나의 합계가 남습니다.
