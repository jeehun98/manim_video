# 10막 — 고유값과 일시적 증폭

11개 독립 씬, 사용자 음성 실측 358초(5분58초), 가로 1920×1080·30fps 무음 영상. 화면별 TTS 77개 문단.

미리보기: `python longforms/ns10_non_normal_dynamics/build.py --preview`
최종: `python longforms/ns10_non_normal_dynamics/build.py`
실측 voice_timing.json의 ends/basis 적용 후 prepare.py 실행.

동일한 A=[[-1,10],[0,-1]]의 정확한 해와 P(t)를 계속 사용한다. 선택된 초기 상태의 크기, 고정 시간의 최대 특잇값, 모든 시간의 최대 증폭을 구별한다. 이 예시는 독립 고유벡터 둘이 없는 결함 행렬이므로 고유벡터 두 방향의 분해를 그리지 않는다. 비정규성만으로 증폭을 보장하지 않는다. 유체 리프트업은 횡방향 재배치 개념도, RNN은 고정점 주변의 연속시간 선형화. norm amplitude와 energy squared를 구별한다.

TTS는 화면 cue마다 빈 줄로 나눈 77개 문단이다. 사용자 문장별 누적 종료 시각에 맞춰 화면·자막·애니메이션을 재동기화했다. `math_verification.json`은 정확한 해·특잇값·비정규 반례를 기록한다. `verification.json`은 렌더 후 메타데이터와 화면 검토를 기록한다.
