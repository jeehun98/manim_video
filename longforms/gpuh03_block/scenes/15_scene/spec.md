# 15 — Shared Memory를 통한 협력

- 목적·핵심 주장: Shared Memory를 통한 협력.
- 앞 장면 입력: Thread 0의 결과 저장
- 확정 구간: 127–135초, 8초. 사용자 문장 종료 시각. 음원 미제공.
- TTS 원문: [script.txt](script.txt).
- 화면·타임라인: 127–131초 네 Warp가 같은 배열에 기록했던 범위를 표시. 131–135초 첫 합산의 연결 예시: Thread0이 기록한 s[0]=1과 Thread64가 기록한 s[64]=65를 Shared Memory에서 읽어 66으로 합침. 결과를 되돌린 실제 실행으로 표현하지 않음.
- 화면 텍스트: GPU/SM0/Block0, 4 Warp·128 Thread, s[128], 현재 stride·부분 합계·대표 실제 값, 코드 발췌.
- 시작·종료: 같은 지도·Block·Warp·Shared 주소를 유지하며 선택·기록·부분 합계만 변화.
- 다음 연결: Block 전체를 한 SM에 배치
- 조건: 한 Block·128 Thread·128 float 입력에 특화. 모든 Thread가 조건문 밖의 장벽에 도달한다. 합산 참여 Thread 수와 총128 Thread 및 장벽 참여 수를 구별한다. 장벽은 동일 하드웨어 사이클 맞춤이 아니며 Warp 도착 순서는 개념도다. 특수 cooperative/cluster 기능은 범위 밖.
- 출처: CUDA Programming Guide — Thread Hierarchy/Shared Memory/Synchronization. README 참고.

## 문장별 시각

127–135초: 여기서 주목할 점은 서로 다른 워프에 속한 스레드들이 같은 공유 메모리를 사용해 하나의 결과를 만들었다는 사실입니다.
