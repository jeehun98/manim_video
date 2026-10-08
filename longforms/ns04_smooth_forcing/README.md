# 4막 — 원하는 모양이면 충분할까?

기존 3막을 분리해 재구성한 직관 중심 영상. 7개 독립 씬, 실측 161초, 가로형 1920×1080 30fps 무음 영상. 사용자 제공 30개 문장의 누적 종료 시각에 화면과 자막을 맞췄다. 수식 항별 분석 대신 영역 축소, 속도 화살표, 역방향 설계와 균형을 보여준다.

- 대본: master_script.md / TTS: tts_script.txt (화면 cue마다 빈 줄)
- 미리보기: python longforms/ns04_smooth_forcing/build.py --preview
- 최종본: python longforms/ns04_smooth_forcing/build.py --tag timed
- 씬 교체: build.py --scene N 후 build.py --concat-only
- 실측: voice_timing.json에 basis와 문장별 누적 종료 시각 ends를 넣고 prepare.py 실행.
- 최종 영상: exports/ns04_act04_161s_timed_1080p30.mp4

모형과 논문이 제시한 구성을 구별한다. 고속 영역의 축소를 물질 부피 압축으로 설명하지 않는다. 작은 합만으로 외력의 매끄러움이 증명된다고 하지 않는다. 발표와 공식 평가를 구별하며 sources.md에 원 출처를 보관한다.
