# 7막 — 레이저 방법

목적: 이미 낮은 분해 비용을 가진 구조에서 독립적인 행렬곱을 추출하고, 개수·크기·비용 상한을 비교해 더 좋은 성장 지수 상한을 증명한다.

사용자 제공 30개 누적 발화 종료 시각을 적용한 147초 무음 영상. 실제 음성 파일은 미제공이다. 6개 씬의 경계는 0 / 23 / 39 / 62 / 82 / 102 / 147초다.

- tts_script.txt: 사용자 입력 발음 대본과 누적 종료 시각.
- narration_timing.json: 화면 표기용 문장 30개와 정확한 시작·종료 시각.
- captions.srt: 같은 30개 구간의 자막.
- 씬별 script.txt/spec.md: 발화 원문과 목적, 적용한 구간.
- revisions/v1_procedure_170s/: 절차 중심 이전 소스.
- revisions/v2_purpose_170s/: 목적 중심 개정의 타이밍 적용 전 소스.

본편 렌더: `python longforms/mm07_laser_method/build.py`
미리보기: `python longforms/mm07_laser_method/build.py --preview`
쇼츠: `python longforms/mm07_laser_method/make_short.py`

출력:
- exports/mm07_laser_method_147s_1080p30.mp4 (1920×1080, 30fps)
- exports/mm07_laser_method_147s_short_1080x1920.mp4 (1080×1920, 30fps)

쇼츠는 본편 화면을 자르지 않고 전부 보존하고, 상단 제목과 하단 발화 구간별 자막을 배치한다. 이전 170초 출력은 과거 버전이다.

작은 세 항 모형은 실제 행렬곱이 아닌 변수 제거와 독립성의 예시다. 보더 랭크 상한은 실제 실행 시간과 구분한다. 제거 자체가 개선을 보장하지 않으며, 잔여 구조가 행렬곱 직합인지 확인한 뒤 규모와 비용 상한을 비교한다.

147초 출력 검증: 본편 1920×1080, 쇼츠 1080×1920. 두 파일 모두 30fps·4,410프레임·147초·오디오 없음. 쇼츠의 전체 화면 보존과 긴 문장 자막, 마지막 발화 자막 배치를 확인했다.
