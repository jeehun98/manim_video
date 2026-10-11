# 5막 — 여러 행렬곱을 하나로 묶으면 무엇이 달라질까?

v2: 6씬 · 151초(2분31초) · 무음 콘티 · 사용자 제공 발화 시각 적용, 실제 음성 파일 미제공 · 1920×1080/30fps.

3개의 2×2 → 9개의 4×4 → 27개의 8×8. 비용 상한 r/r²/r³를 나란히 비교한 뒤 정리에 실제 기준 r=21을 대입해 Strassen 지수를 재현한다. r<21 분해의 존재는 주장하지 않는다.

`python longforms/mm05_direct_sum/build.py --preview`

`python longforms/mm05_direct_sum/build.py`

출력: exports/mm05_direct_sum_151s_1080p30.mp4

[발화 대본](tts_script.txt) · [전체 대본](master_script.md) · [수학 출처](sources.md)

이전165초 소스: revisions/v1_165s. 기존 영상도 보존. 자막은 사용자 제공 문장별 종료 시각 적용.

세로형: python longforms/mm05_direct_sum/make_short.py
출력: exports/mm05_direct_sum_151s_short_1080x1920.mp4
