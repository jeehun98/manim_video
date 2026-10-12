# 9막 — 증폭과 제어가 개입하는 위치

8개 독립 씬, 사용자 음성 실측 246초(4분6초), 가로 1920×1080·30fps 무음 영상. 55개 문장의 누적 종료 시각에 맞췄으며 화면별 문단으로 분리한다.

미리보기: `python longforms/ns09_amplification_control/build.py --preview --tag timed`
최종: `python longforms/ns09_amplification_control/build.py --tag timed`
실측 ends와 basis를 voice_timing.json에 넣고 prepare.py 실행.

점성과 global norm clipping, 표준화와 잔차 경로를 구별한다. Clipping의 업데이트 상한은 plain SGD에서만 예시하며 다른 optimizer의 후처리 상한으로 확대하지 않는다. 마지막 곡선은 실제 점근안정 선형 모형의 norm이며, 일시적 증폭과 장기적 감소를 구별한다. 모든 모형은 설명용, 전체 NS 해나 실제 네트워크 측정이 아니다. 상세 조건은 spec.md 참조.

최종 산출물: exports/ns09_act09_246s_timed_1080p30.mp4 및 SRT. 7380프레임, 246초, 무음.
