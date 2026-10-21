# 여섯 개의 독립 제작 단위

| 클래스 | 시간 | 주장 | 주요 화면 |
|---|---|---|---|
| FeatureMixingIntro | 0–26 | 관찰한 활성화에서 조합은 직접 보이지 않는다 | 2D 축·다섯 생성 방향·관찰값·빈 잠재 칸 |
| SparseAutoencoderArchitecture | 26–56 | 고정 모델의 활성화를 별도 SAE가 분석한다 | 고정 모델·활성화 복사·Encoder·5 latents·Decoder |
| SparseDictionaryLearning | 56–91 | 희소 제약 아래 여러 입력에 공통 방향을 학습한다 | 비유일 복원·희소 노드·A/B/C의 동일 D 재사용 |
| ReconstructionSparsityTradeoff | 91–111 | 복원과 희소성의 두 목표가 경쟁한다 | 실제 합성점·오차선·잠재 막대·L1 예시 |
| MonosemanticityFindings | 111–131 | 실제 연구에서 해석·개입 가능한 후보가 발견되었다 | 512→4096·문자/형식 예시·원래 모델 개입 |
| InterpretationLimits | 131–171 | 복원·반응만으로 의미와 인과 역할이 확정되지 않는다 | 다른 사전·분할/병합·미검증 후보 그래프 |

모든 단위는 전체 timing.json의 해당 구간을 로컬 0초부터 렌더한다. 전체 Scene은 여섯 단위의 동일 구현을 사용한다. TTS 파일이 없는 상태에서 음성 길이를 실측한 것으로 간주하지 않는다. 사용자가 제공한 종료 시각이 화면 시간의 기준이다.
