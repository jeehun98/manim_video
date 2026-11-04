# 독립 제작 단위

| 클래스 | 시간 | 주장 | 주요 화면 |
|---|---|---|---|
| ProbeIntroduction | 0–21 | 내부 정보의 존재와 실제 사용은 다른 질문 | 영어 문장·cats·Frozen Transformer·h |
| LinearProbeTraining | 21–61 | 별도 분류기로 선형 판독 가능성을 조사 | h의 두 갈래·별도 Probe 학습·학습 밖 평가 |
| AmnesicIntervention | 61–94 | 판독 방향을 줄이고 모델의 나머지 계산을 비교 | Number→POS·2D 투영·INLP·동일 가중치 |
| BehaviorComparison | 94–129 | 예측 변화와 목표 정보의 인과 효과는 구별 | 가상 분포 A/B·겹친 다른 정보·교란 |
| EvidenceLevels | 129–155 | 판독·개입·경로의 세 질문에 각각 근거가 필요 | 세 병렬 패널·가설과 검증 결합 |
| PatterningValidationBridge | 155–175 | 학습 유도는 내부 형성과 기능도 확인해야 함 | 데이터 재가중·새 학습·회로 가설·관찰/개입 |

전체 클래스와 여섯 독립 클래스가 같은 화면 구현을 공유한다. 독립 Scene은 해당 구간을 로컬 0초부터 렌더한다. 길이는 사용자 발화 시각 기준이며 실측 TTS 길이로 표기하지 않는다.
