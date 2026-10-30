# 18 — Block 내부의 동기화 범위

- 목적·핵심 주장: Block 내부의 동기화 범위.
- 앞 장면 입력: 같은 SM의 실행 자원
- 확정 구간: 148–158초, 10초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 148–152초 Block0의 장벽 범위를 두 Block 지도에서 표시. 152–158초 Block별 독립 Shared 할당, 일반적 __syncthreads()는 다른 Block을 동기화하지 않음.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: Thread · Warp · Block
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

148–152초: 다만 일반적인 블록 내부 동기화 명령은 서로 다른 블록까지 동기화하지는 않습니다.

152–158초: 즉, 블록은 내부적으로 협력할 수 있지만, 다른 블록과는 기본적으로 독립적인 실행 그룹입니다.
