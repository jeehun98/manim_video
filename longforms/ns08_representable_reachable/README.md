# 8막 — 좋은 해와 실제 학습 경로

8개 독립 씬, 사용자 음성 실측 251초(4분11초), 가로 1920×1080·30fps 무음 영상. TTS는 화면 cue마다 빈 줄로 분리.

미리보기: `python longforms/ns08_representable_reachable/build.py --preview --tag timed`
최종: `python longforms/ns08_representable_reachable/build.py --tag timed`
실측 누적 종료 시각은 voice_timing.json의 ends와 basis에 기록 후 prepare.py 실행.

유체의 조건 검증과 신경망의 동역학에 의한 해 선택을 구별한다. 비볼록 예시에서는 같은 규칙/서로 다른 초기점의 실제 GD를 계산한다. 두 좋은 해와 암묵적 편향은 f(x)=ax+b, 단일 훈련점(1,1)을 쓰는 부족결정 선형 모델로 검산한다. 두 극한 해의 새로운 입력 반응이 다름을 보여주며 일반화 우열을 주장하지 않는다. GD와 방향별 고정 보정에 의한 선택은 명시적 정규화 없는 특정 모형 결과. 일반 신경망의 보편적 보장으로 해석하지 않는다.

최종 산출물: exports/ns08_act08_251s_timed_1080p30.mp4 및 SRT. 7530프레임, 251초, 무음.
