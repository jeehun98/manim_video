# 오일러 항등식 — 음성 결합 및 7편 통합

입력은 `exports/euler_identity_1.mp4`–`euler_identity_7.mp4`와 정확히 같은 번호의 `euler_1.mp3`–`euler_7.mp3`이다. `euler_1(1).mp3`, 기존 `euler_1.mp4`와 `euler_2.mp4`는 이 작업의 입력이나 덮어쓰기 대상이 아니다.

실행: `py -3.12 longforms/euler_identity/full_01_07/build.py`

개별 결과는 `exports/euler_identity_1_voiced.mp4`–`euler_identity_7_voiced.mp4`, 합본은 `exports/euler_identity_full_01_07_longform.mp4`다.

모든 음성을 보존하며 음원이 더 길면 마지막 프레임을 유지한다. 영상 속도와 내레이션 속도는 바꾸지 않는다. 1920×1080 60fps로 통일하며 원본 30fps 구간은 프레임을 반복한다. 각 장을 H.264 CRF 18 / AAC 192kbps 48kHz mono로 결합한 뒤, 합본 영상 스트림은 복사하고 오디오는 연속 타임라인으로 인코딩한다. 원본 파일은 보존한다.

`verification.json`에 각 원본·음원 길이, 마지막 화면 유지 시간, 합본의 챕터 시작 시각과 검증 결과를 기록한다. 자동 검수는 개별 프레임 수와 A/V 길이, 합본 프레임 수·길이 및 전체 오디오·비디오 디코딩을 확인한다.
