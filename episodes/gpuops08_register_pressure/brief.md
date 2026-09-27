# GPU 연산과 최적화 08 제작 기준

## 제목

**왜 모든 연산을 하나로 합치지 않을까? — Register Pressure**

## 길이와 형식

- 90초
- 1080×1920, 30fps, 세로형
- 무음 영상과 별도 TTS·SRT를 제공한다.
- 모든 장면에 핵심 설명을 두 줄 화면 자막으로 표시한다.

## 학습 목표

Fusion이 중간 materialization을 없애더라도 데이터 자체가 사라지는 것은 아니며, live value를 유지하는 자원 비용이 생긴다는 점을 이해한다. live range 중첩이 register pressure를 높이고, 제한된 SM register file에서 resident warp 수와 latency-hiding 여유에 영향을 줄 수 있음을 연결한다.

## 핵심 주장

1. materialization 제거는 데이터 제거가 아니다.
2. 값은 생성된 시점부터 마지막 사용 시점까지 live 상태다.
3. 동시에 겹치는 live range가 많으면 thread당 register 요구량이 증가할 수 있다.
4. SM의 register file은 유한하며 resident thread/warp가 공유한다.
5. register 요구량 증가는 occupancy를 제한하거나 spill을 유발할 수 있지만, 항상 그렇게 되는 것은 아니다.
6. Fusion은 global-memory traffic 감소와 on-chip resource 비용 사이의 trade-off다.

## 정확성 경계

- register pressure가 증가하면 성능이 반드시 하락한다고 단정하지 않는다.
- occupancy는 register뿐 아니라 shared memory, block 크기, 하드웨어 제한에도 영향을 받는다.
- occupancy가 높을수록 항상 빠르다고 표현하지 않는다. 여기서는 latency hiding의 여유가 줄 수 있다는 관계만 설명한다.
- spill은 가능한 결과로 제시하며 모든 고압력 Kernel에서 발생한다고 표현하지 않는다.

## 장면별 타임라인

| 시간 | 화면 목표 |
|---|---|
| 00:00–00:07 | 이전 Fusion 편 요약 |
| 00:07–00:14 | 모든 Operator를 한 Kernel에 넣는 질문 |
| 00:14–00:22 | 저장하지 않은 값의 위치 질문 |
| 00:22–00:30 | Thread register가 live value로 채워짐 |
| 00:30–00:37 | 겹치는 live range 시각화 |
| 00:37–00:45 | Register Pressure와 spill 가능성 |
| 00:45–00:53 | 유한한 SM Register File |
| 00:53–01:01 | register 요구량과 resident warp 비교 |
| 01:01–01:09 | latency hiding 여유 감소 가능성 |
| 01:09–01:17 | memory traffic과 register pressure 저울 |
| 01:17–01:24 | Fusion 양과 성능의 개념 그래프 |
| 01:24–01:30 | 선택적 경계와 compiler 질문 |

