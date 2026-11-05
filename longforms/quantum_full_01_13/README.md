# 양자역학의 발견 Part I · 1–13편 합본

사용자가 지정한 `exports/quantum_long_1.mp4`부터 `quantum_long_13.mp4`까지 숫자 순서로 결합한다. 각 파일의 기존 화면·음성·끝 여백을 보존한다. 개별 쇼츠나 이전 무음 렌더로 대체하지 않는다.

실행: `python longforms/quantum_full_01_13/build.py`

4편만 1280×720·24fps이므로 1920×1080·30fps로 변환한다. 끝 프레임 보존을 위해 30fps의 다음 프레임 시각으로 올림하며 늘어나는 길이는 1/60초다. 나머지 12편의 영상은 스트림 복사한다. 각 편의 음성을 해당 영상 길이까지 무음으로 채워 이어 붙여 챕터 경계의 동기화를 유지한다. 음성은 AAC로 한 번 인코딩한다.

`manifest.json`에 실제 입력·길이·시작 시각, `chapters.ffmetadata`에 정확한 MP4 챕터, `youtube_description.txt`에 설명문과 초 단위 챕터를 기록한다. 생성물은 `exports/quantum_long_1_13_full.mp4`, 설명문 사본은 `exports/quantum_long_1_13_youtube_description.txt`다.

검증은 해상도·fps·전체 프레임·음성 길이·13개 챕터·전체 디코딩 및 연결부 확인으로 수행한다. 원본 파일은 수정하지 않는다.

완성: 33분 27.100초, 60213프레임. 13개 챕터의 시작·종료 시각, 원본과 합본의 챕터 시작 후 화면 일치, 각 편 음성의 표본 상관, 전체 디코딩을 확인했다. `python longforms/quantum_full_01_13/verify.py`로 메타데이터·연결부 검사를 재실행할 수 있다. 전체 디코딩은 별도 FFmpeg 검사다.
