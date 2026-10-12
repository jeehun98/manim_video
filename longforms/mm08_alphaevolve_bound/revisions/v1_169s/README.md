# 8막 — AI는 더 좋은 행렬곱 상한을 어떻게 찾았을까?

현재 본편 8막. 7막 레이저 방법에서 이어져, 같은 수학적 증명 체계 안에서 선택을 최적화하는 과정을 설명한다. 기존 AlphaTensor 편은 mm08_alphatensor_game에 이전안으로 보존한다.

7개 독립 씬. 임시 169초·1920×1080·30fps·무음. 실제 TTS 길이는 미확정이며 현재 콘티 시간은 화면 검토용이다. tts_script.txt는 읽을 문장만 발화 구간별 빈 줄로 나눈다. 실측 종료 시각을 받으면 화면·자막을 동기화한다. captions.srt는 임시 씬 제목 카드다.

핵심 흐름: 같은 텐서의 다른 선택 → 크기·개수·손실을 반영한 평가 → 조합 손실 분석의 최적화 → 재구성·경사 기반 최적화·AlphaEvolve 코드 개선 → 엄밀 검증 → ω<2.371177.

선택 A·B와 지형은 개념도이며 실제 연구 데이터가 아니다. 논문의 수치 인증은 독립 재현하지 않았다. AI가 새 레이저 방법이나 직접적인 행렬곱 분해 공식을 발명했다고 말하지 않는다. 실행 속도 개선과 이론적 지수 상한 개선을 구분한다.

실행:
- `python longforms/mm08_alphaevolve_bound/build.py --preview`
- `python longforms/mm08_alphaevolve_bound/build.py`

출력: exports/mm08_alphaevolve_bound_169s_1080p30.mp4

[전체 대본](master_script.md) · [TTS](tts_script.txt) · [출처와 범위](sources.md)

렌더 검증 완료: 1920×1080·30fps·5,070프레임·169초·오디오 없음. 개념도, 기여 구분, 실제 상한 숫자와 9막 연결 화면을 확인했다.
