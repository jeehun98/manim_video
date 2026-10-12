# 3막 — 행렬곱을 하나의 수학적 구조로 바꾼다면?

현재 3막: 6개 독립 씬, 164초(2분 44초) 보강 무음 콘티. 사용자 제공 기존 TTS 길이는 152초이며 세 부분을 보강한 원고는 아직 재측정 전이다. 자막의 수정 구간은 임시 배정이다.

[대본](master_script.md) · [TTS](tts_script.txt) · [원 초안](source_storyboard.md) · [검증 자료](sources.md) · [수정 기록](revision_notes.md)

미리보기: `python longforms/mm03_tensor_rank/build.py --preview`

본편: `python longforms/mm03_tensor_rank/build.py`

세 축은 A 입력 위치·B 입력 위치·C 출력 위치다. C 축은 추가 입력이 아니다. 단순항 명칭을 소개한 뒤 두 입력 조합→곱셈 한 번→출력 분배를 직접 보여준다. 여섯 항 가능성 질문을 거쳐 최소 개수 문제를 랭크로 명명한다.

M₁은 최종 출력이 아닌 기여분, w는 고정 분배 규칙이다. 64개 계수의 정확한 검산은 랭크 상한 확인이며 별도의 랭크 하한 증명을 대신하지 않는다.

출력: exports/mm03_tensor_rank_164s_1080p30.mp4. 1920×1080·30fps·4,920프레임을 목표로 렌더하며 최종 결과는 렌더 로그에서 확인한다. 음성 파일이 제공되지 않아 오디오 없음.

원 사용자 발화 시각은 narration_timing_152s_user.json에 보존했다. 보강 구간은 narration_timing.json의 timing_basis로 구분한다.

쇼츠용: `python longforms/mm03_tensor_rank/make_short.py`. 현재 `exports/mm03.mp4`(164초)를 자르지 않고 세로 프레임에 배치하며 하단에 동기화 자막을 추가한다. 출력 `exports/mm03_tensor_rank_164s_short_1080x1920.mp4`.
