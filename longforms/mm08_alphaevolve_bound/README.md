# 8막 — AI는 더 좋은 행렬곱 상한을 어떻게 찾았을까?

7막 레이저 방법에서 이어져, 기존 수학적 증명 체계 안에서 더 좋은 선택을 탐색하는 과정을 설명한다. 구조의 활용과 분석, 서로 영향을 주는 조건, 정확한 ω 값과 더 낮은 상한의 차이를 반영했다.

사용자가 제공한 33개 발화 종료 시각을 적용했다. 전체 161초, 7개 독립 씬의 경계는 0·18·38·60·88·113·138·161초다. TTS 대본, narration_timing.json과 captions.srt는 같은 구간을 사용한다. 음성 파일이 제공되지 않아 출력 영상은 무음이다.

본편은 1920×1080, 쇼츠는 1080×1920, 모두 30fps다. 쇼츠는 전체 161초를 유지하며 본편 화면과 33개 구간의 발화 자막을 배치한다.

실행:
- `python longforms/mm08_alphaevolve_bound/build.py`
- `python longforms/mm08_alphaevolve_bound/make_short.py`

출력:
- `exports/mm08_alphaevolve_bound_161s_1080p30.mp4`
- `exports/mm08_alphaevolve_bound_161s_short_1080x1920.mp4`

선택 A·B, 최적화 지형과 경로는 개념도다. 연구의 문제 재구성·현대 최적화·AlphaEvolve 기여를 구분하며, 실제 실행 속도와 이론적 지수 상한 개선을 구별한다. 논문의 수치 인증은 독립 재현하지 않았다.

[전체 대본](master_script.md) · [TTS](tts_script.txt) · [출처와 범위](sources.md)

이전 169초 소스는 revisions/v2_feedback_169s에 보존했다. 기존 AlphaTensor 편은 mm08_alphatensor_game에 이전안으로 보존한다.

검증: 두 영상 모두 4,830프레임·30fps·161초, 오디오 없음.
