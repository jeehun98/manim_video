# 11막 — 안정적이라는 것은 무엇을 의미할까?

9개 독립 씬, 사용자 음성 실측 323초(5분23초), 가로 1920×1080·30fps 무음 영상. 기존 시각 요소를 재사용해 전체·국소, 방향, 업데이트 조건, 실제 경로, 장기·중간 증폭을 회수한다. 서로 다른 수학적 조건을 하나의 안정성 정의로 묶지 않는다.

렌더: `python longforms/ns11_stability_finale/build.py`. 미리보기: `--preview`. 사용자 실측 `voice_timing.json` 적용 후 `prepare.py`로 문장별 재동기화.

화면 cue마다 빈 줄로 나눈 TTS 70개 문단과 별도 SRT를 제공한다. 음성은 포함하지 않는다. 마지막 질문 이후 자막·진행선까지 암전된다. `math_verification.json`에 요약 통계량·GD 경로·정확한 선형 해 확인을, `verification.json`에 영상 검사를 기록한다.
