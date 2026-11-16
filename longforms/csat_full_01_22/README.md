# 수능 수학 공통 1~22번 — 음성 포함 통합 롱폼

입력: `exports/csat01.mp4`~`csat22.mp4`와 `exports/수능_1.mp3`~`수능_22.mp3`. 번호별로 연결 후 순서대로 합친다.

- 1920×1080,30fps,AAC192k mono48kHz,22개 MP4 챕터.
- 원래 본문·자막 시각 유지. 음성이 더 길면 마지막 프레임을 유지하며, 짧으면 남는 부분은 무음으로 채운다. 음성 속도 변경과 잘라내기 없음.
- 개별 결과: `exports/csat_voiced/csat01_voiced.mp4`~`csat22_voiced.mp4`.
- 통합 결과: `exports/csat_full_01_22_longform.mp4`.
- 실행: `python longforms/csat_full_01_22/build.py`.
- 기존 오일러 롱폼의 mux·concat·챕터·검사 도구를 재사용했다. 확정 대본과 제작된 화면을 그대로 조립한다.


## 결과

길이 4042.900000초, 121287프레임, 22개 챕터. 원본 MP3 대조 22/22 일치, 최대 측정 오프셋 0.0213125초(1프레임 이내). 검사: `python longforms/csat_full_01_22/check_audio.py`.
