# 열방정식 1–5장 음성 포함 롱폼

exports의 확정 장별 MP4와 열방정식_1~5.mp3를 번호별 결합한 후 이어 붙인다. 원본은 보존하고 heat_ch01~05_voiced.mp4를 먼저 생성한다. 음성을 자르거나 속도를 바꾸지 않으며, 더 긴 음성의 끝까지 마지막 화면을 유지하고 30fps 프레임 경계로 맞춘다.

실행: `py -3.12 longforms/fourier_heat/full_01_05/build.py`

최종: exports/heat_full_01_05_longform.mp4. 1080p30, 48kHz AAC 음성, MP4 챕터 포함. 통합 SRT와 heat_youtube_description.txt를 함께 생성한다. 유튜브 구간 시각은 실제 장별 결합 길이를 누적한다. 모든 스트림의 전체 디코딩과 최종 프레임·해상도·음성 길이를 확인한다.
