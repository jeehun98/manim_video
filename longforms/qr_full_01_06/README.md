# QR 분해의 기하학 — 1~6편 통합본

사용자가 지정한 `exports/qr_long_1.mp4`부터 `qr_long_6.mp4`까지 순서대로 연결한다. 기존 확정 영상과 음성을 유지하며, 새 대본이나 화면을 생성하지 않는다.

실행: `python longforms/qr_full_01_06/combine.py`

출력: `exports/qr_full_01_06_longform.mp4`. 1920×1080, 30fps, 원본 H.264 영상과 AAC 음성 스트림 복사. 구간별 챕터를 포함한다. 정확한 길이와 입력 목록은 `verification.json`에 기록한다.

썸네일은 사용자 첨부 EVD 이미지의 남색 격자·청록·금색 스타일을 참고해 QR 주제로 새로 생성한다. 생성 프롬프트는 `thumbnail_prompt.txt`.
