# 7막 — 가장 제한적인 모드와 업데이트

10개 독립 씬, 사용자 음성 실측 343초(5분43초), 가로 1920×1080·30fps 무음 영상. 71개 문장의 누적 종료 시각에 맞췄다. 화면 cue마다 TTS를 빈 줄로 분리한다.

실행: `python longforms/ns07_update_stability/build.py --preview --tag timed` 및 `python longforms/ns07_update_stability/build.py --tag timed`. 실측 ends와 basis를 voice_timing.json에 기록 후 prepare.py 실행.

확산: 1D 등간격 중앙차분과 Forward Euler, 주기 경계 모드 예시. 신경망: 고정 양의 정부호 이차 손실의 GD. 비증폭과 감쇠를 구별하고 실제 NS 특이점과 수치 불안정을 구별한다. 비균일 격자의 정확한 제한, 이류 CFL, 암시적/국소 적분, 실제 비볼록 최적화는 별도다. 단순한 계산 예시이며 실제 신경망 실측이 아니다.

최종 산출물: `exports/ns07_act07_343s_timed_1080p30.mp4`, 동일 이름 SRT. 10290프레임, 343초, 무음.
