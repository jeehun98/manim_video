# 5막 — 전체와 국소에서 활성값 이상치로

유체 설명에 첫 58초를 배정하고 신경망의 활성값과 양자화로 연결한다. 10개 독립 씬, 실측 249초(4분9초), 1920×1080 30fps 무음 영상. 사용자 제공 51개 문장의 누적 종료 시각에 화면과 자막을 맞췄다. 수식 분해 대신 공간 집중, 행렬의 큰 값, 같은 눈금의 공유와 크기 보상을 보여준다.

- 준비: python longforms/ns05_activation_outliers/prepare.py
- 미리보기: python longforms/ns05_activation_outliers/build.py --preview
- 최종본: python longforms/ns05_activation_outliers/build.py --tag timed
- 씬 교체: build.py --scene N 후 build.py --concat-only
- 음성 실측: voice_timing.json의 basis, ends에 문장별 누적 종료 시각을 넣고 prepare.py 실행.
- 대본: master_script.md / tts_script.txt (51개 화면 cue마다 빈 줄)
- 산출물: exports/ns05_act05_249s_timed_1080p30.mp4와 SRT

유체와 신경망이 같은 동역학이라는 주장을 하지 않는다. 유한 행렬에서 최대 절댓값≤Frobenius 노름, RMS≤최대값이다. 8×8 .5/8 행렬은 평균 .6171875, 최대8, L2≈8.9303이다. 양자화는 동일 그룹의 absmax 대칭 INT8[-127,127] 모형이며 모든 양자화 방식에 일반화하지 않는다. LLM.int8과 SmoothQuant는 원 논문에 근거하며 실제 모델 측정이나 구현의 성능 테스트는 아니다. SmoothQuant의 곱 동일성은 정확한 산술/양자화 전 조건이다. sources.md 및 각 spec.md 참조.
