# Pruning & Sparsity 01 제작 기준

- 이 편의 유일한 학습 목표는 `작은 Weight를 0으로 만드는 pruning`과 `0이 많은 sparse matrix`의 직관을 만드는 것이다.
- `Sparse = 실제 실행이 빠르다`고 확정하지 않는다. 마지막의 `10× FASTER?`는 다음 편들에서 검증할 질문이다.
- magnitude pruning의 타당성, threshold 선택, 재학습, 정확도 회복은 02편 이후로 미룬다.
- FLOPs와 실행시간의 차이, GPU의 불규칙 접근, sparse storage 형식도 아직 설명하지 않는다.
- 메인 흐름은 `신경망 연결 → 작은 Weight 강조 → 연결 제거 → Dense/Sparse 행렬 → x×0=0 → 90% PRUNED`다.
- 영상은 대본 글자 수에 맞춰 구간별 약 6.5~7.5자/초로 배분한 50초, 1080×1920, 30fps 무음 마스터다. `captions.srt`와 `tts_script.txt`를 별도 제공한다.
