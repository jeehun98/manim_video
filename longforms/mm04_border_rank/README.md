# 4막 — 집합에 없는 점도, 폐포에는 들어갈 수 있을까?

v4 폐포 보강: 7개 독립 씬 · 166초(2분 46초) 무음 콘티 · 1920×1080/30fps. 폐포 이해를 위해 기존 화면보다 시간을 늘렸다. 사용자 제공 문장별 발화 종료 시각으로 화면과 자막을 동기화했다. 음성 파일은 제공되지 않아 출력은 무음이다.

열린 원판의 내부→임의의 작은 주변에도 내부점 존재→빠져 있던 극한점 포함→텐서의 낮은 랭크 집합과 폐포로 연결한다. 이어 행렬에서는 폐포를 취해도 변화 없음, 일부 텐서에서는 새 점 포함이라는 대비를 보여준다.

[대본](master_script.md) · [TTS](tts_script.txt) · [검증 자료](sources.md)

`python longforms/mm04_border_rank/build.py --preview`

`python longforms/mm04_border_rank/build.py`

출력: exports/mm04_border_rank_166s_1080p30.mp4

원판은 폐포 자체의 예시이며 텐서 집합은 포함관계 개념도이다. 일부 경계점이 원래 집합에 포함되어 있을 수도 있다. ‘두 항 이하’ 표현으로 정확히 수정했고, 유한 차수 다항식 형태를 확보한 경우에 한해 계수 복원을 설명한다. 작은 잔여 차이를 남기는 두 성분의 소거를 보여주되 전체 랭크를 평면 그림으로 판정하지 않는다.

이전 소스는 revisions/v1_176s, revisions/v2_154s, revisions/v3_166s에 보존했다.

세로형: `python longforms/mm04_border_rank/make_short.py`
출력: exports/mm04_border_rank_166s_short_1080x1920.mp4
