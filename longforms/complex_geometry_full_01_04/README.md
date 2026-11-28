# 복소평면에 숨겨진 기하학 — 음성 포함 통합 롱폼

`complex_geometry_01~04.mp4`와 사용자 제공 `복소_1~4.mp3`를 번호별로 먼저 결합한 뒤 하나의 영상으로 연결한다. 원본은 보존하며 음성의 속도를 바꾸거나 끝을 자르지 않는다. 음원이 더 긴 구간은 마지막 화면을 필요한 프레임만큼 유지한다.

실행: `py -3.12 longforms/complex_geometry_full_01_04/build.py`

- 구간별 음성 포함 영상: `exports/complex_geometry_01_voiced.mp4` ~ `complex_geometry_04_voiced.mp4`
- 통합 영상: `exports/complex_geometry_full_01_04_longform.mp4`
- 유튜브 설명란: `exports/complex_geometry_youtube_description.txt`
- 통합 자막: `exports/complex_geometry_full_01_04_longform_captions.srt`
- 검증 결과: `verification.json`

1920×1080 30fps. 개별 영상은 AAC 192kbps 모노 48kHz 음성을 포함한다. 통합 영상의 화면은 결합된 네 영상에서 복사하고, 음성은 각 구간과 같은 길이로 정렬한 원본 MP3를 한 번 인코딩해 AAC 경계의 패딩 오차와 불필요한 재인코딩 손실을 피한다. 실제 구간 길이로 MP4 챕터·유튜브 타임스탬프·통합 SRT를 생성하고, 프레임 수·음성 길이·전체 디코딩을 검사한다.
