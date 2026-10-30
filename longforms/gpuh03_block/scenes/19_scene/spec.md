# 19 — Thread · Warp · Block

- 목적·핵심 주장: Thread · Warp · Block.
- 앞 장면 입력: Block 내부의 동기화 범위
- 확정 구간: 158–169초, 11초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 158–169초 동일 구조에서 Thread1→Warp0→Block0 차례로 강조. 개별 계산·명령 실행 그룹·협력 범위를 대응.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: 협력으로 만든 하나의 결과
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

158–169초: 결국 스레드는 각자의 명령과 데이터를 처리하고, 워프는 32개의 스레드를 묶어 명령을 실행하며, 블록은 여러 스레드가 데이터를 공유하고 동기화하며 협력할 수 있는 단위입니다.
