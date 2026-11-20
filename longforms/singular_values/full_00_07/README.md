# 특잇값 0–7장 음성 결합 롱폼

각 장 1080p30 원본에 exports/sig_0.mp3~sig_7.mp3를 번호별 결합한 뒤 순서대로 연결한다. 음성 속도 유지, 음성 전체 보존, 부족한 화면은 마지막 프레임 유지. 원본은 보존한다.

`python longforms/singular_values/full_00_07/build.py`

결과: exports/singular_ch00_voiced.mp4~singular_ch07_voiced.mp4, singular_full_00_07_longform.mp4, 통합 SRT, youtube_description.txt.
