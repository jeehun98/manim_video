# 모든 것이 필요할까? 1–8 통합 롱폼

입력: 사용자가 지정한 exports/minimal_1_long.mp4 ~ minimal_8_long.mp4. 영상·음성을 모두 유지하며, 각 입력의 영상 끝까지 오디오 무음을 보충한 뒤 결합. 영상 재인코딩 없음. 기존 파일 변경 없음.

실행: `python longforms/minimal_full_01_08/build.py`

출력: exports/minimal_1-8_long_full.mp4, exports/minimal_1-8_youtube_description.txt. MP4 내부에 8개 챕터 포함. 정확한 시작 시각·검증은 verification.json 참조. 유튜브 타임스탬프는 초 단위 내림 표시.
