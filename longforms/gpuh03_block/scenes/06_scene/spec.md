# 06 — Block의 Shared Memory

- 목적·핵심 주장: Block의 Shared Memory.
- 앞 장면 입력: 128개의 입력 · 하나의 결과
- 확정 구간: 56–62초, 6초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 56–60초 Block에 귀속된 Shared Memory 영역 등장. 60–62초 __shared__ 소스 대응.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 코드와 공유 배열의 주소
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

56–60초: 이때 사용할 수 있는 것이 공유, Shared Memory입니다.

60–62초: 실제 쿠다 코드를 살펴보겠습니다.
