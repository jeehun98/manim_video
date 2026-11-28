# 인트로 포함 음성 롱폼

`python longforms/complex_geometry_full_00_04/build.py`

인트로 영상과 `exports/복소_0.mp3`를 결합하고 기존 1–4부 통합 영상 앞에 붙인다. 음원 전체를 보존하도록 인트로 마지막 화면을 0.867초 유지한다. 본편 영상은 재인코딩 없이 복사하고, 음성은 원본 MP3 0–4를 각 파트의 정확한 길이에 맞춰 한 번 인코딩한다.

출력: `exports/complex_geometry_00_voiced.mp4`, `exports/complex_geometry_full_00_04_longform.mp4`, 통합 SRT, 갱신한 유튜브 설명. 기존 1–4부 결과는 유지한다.

검증: 1920×1080·30fps, 전체 프레임 수와 음성 길이, MP4 챕터 5개, 자막 201개 연속성, 전체 디코딩, 원본 음원과 각 챕터의 오디오 정렬. 결과는 `verification.json`, `audio_alignment.json`에 기록한다.
