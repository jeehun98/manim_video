# 독립 장면 명세

| 클래스 | 시간 | 주장 | 핵심 화면 |
|---|---|---|---|
| CircuitQuestionIntro | 0–26 | 특징의 발견만으로 계산 관계가 정해지지 않는다 | F1–F6·연구형 질문·가능한 두 단계 관계 |
| TranscoderArchitecture | 26–71 | MLP 출력을 CLT 특징으로 근사한다 | 원래 모델·대체 모델·SAE/Transcoder·층별 읽기와 쓰기 |
| AttributionGraphConstruction | 71–99 | 대체 모델의 특정 출력 기여를 추적한다 | 입력·특징·오차·logit·부호·역추적 |
| DallasTexasAustinCircuit | 99–109 | Texas 특징군과 capital 가지가 출력에 기여한다는 가설 | supernode·합류·지름길 |
| InterventionValidation | 109–146 | 원 모델의 개입 결과로 가설을 검증한다 | 다른 모델·같은 답·Dallas 고정·Texas→California·Sacramento |
| ProbingInterventionBridge | 146–166 | 읽을 수 있는 것과 쓰이는 것을 구별해야 한다 | Output→Features→Circuits·읽기/개입 질문 |

여섯 클래스는 해당 구간을 로컬 0초부터 독립 렌더할 수 있다. 전체 Scene은 같은 구현을 순차 실행한다.
음성 실측 대신 제공 발화 종료 시각을 사용한다. 대본은 narration.md, 구간별 발음 원고는 tts_script.txt.
