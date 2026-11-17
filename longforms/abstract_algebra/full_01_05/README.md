# 추상대수학 — 군·환·체 1~5장 음성 포함 롱폼

실행: `py -3.12 longforms/abstract_algebra/full_01_05/build.py`

exports의 각 장 무음 최종본과 군체환_1.mp3~군체환_5.mp3를 번호대로 결합한다. 모든 원본은 보존한다. 실제 발화가 기존 영상 끝을 넘어가므로 음성 길이를 자르거나 속도를 바꾸지 않고, 마지막 화면을 다음 프레임 경계까지 짧게 유지한다.

기존 오일러 롱폼 조립 도구 재사용. 1080p60 H.264 CRF18, AAC 192kbps 48kHz mono. 장별 음성 포함 MP4 다섯 개를 먼저 만든 뒤 합본과 MP4 챕터를 생성한다. 자막은 장별 원래 시각을 유지하며 마지막 자막만 장 종료까지 연장하고 연결 오프셋을 더한다.

결과: exports/abstract_algebra_full_01_05_longform.mp4
유튜브 설명: youtube_description.txt 및 exports/abstract_algebra_youtube_description.txt
검증: verification.json, 최종 영상·음성 전체 디코드 검사.

## 완성본 검증

9분 19.183초, 33,551프레임. MP4 챕터 5개와 자막 121개. 전체 영상·음성 디코드 통과. 장별 마지막 프레임 유지: 0.517 / 0.267 / 0.467 / 0.517 / 0.417초.
