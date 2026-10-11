# 2막 — 행렬곱의 계산량은 어디까지 줄어들 수 있을까?

4개 독립 씬으로 성장률·상한·출력 하한·최적 지수를 설명한다.

현재 사용자 문장별 종료 시각을 적용한 137초 무음 영상이다. SRT는 23개 문장 구간과 일치한다. 음성 파일은 미제공으로 결합하지 않았다. 계수체는 복소수로 고정하고 최신 기록의 구체적 수치는 사용하지 않는다. ω=2를 정확한 O(n²) 공식의 존재와 동일시하지 않는다.

미리보기: `python longforms/mm02_growth_bounds/build.py --preview`

1080p: `python longforms/mm02_growth_bounds/build.py`

씬 교체: `--scene 2`로 해당 씬만 렌더한 뒤 `--concat-only`.

[내레이션](master_script.md) · [TTS 발음 대본](tts_script.txt) · [검증 자료](sources.md)

검증 결과: 최종 1920×1080·30fps·4,980프레임·166초, 오디오 없음. 독립 씬 해상도·코덱·프레임 수와 전체 연결 시간을 확인했다. 원문의 내레이션을 다듬었으며 실제 음성에 따른 문장별 길이는 미확정이다.

출력: exports/mm02_growth_bounds_166s_1080p30.mp4

## 137초 타이밍 개정

씬 경계: 0 / 37 / 60 / 86 / 137초. narration_timing.json의 23개 문장별 구간을 적용했다. 166초 출력은 이전 버전이다.

쇼츠 생성: `python longforms/mm02_growth_bounds/make_short.py`. 전체 본편을 보존하고 상단 제목과 하단 문장별 자막을 배치한다.

현재 출력: exports/mm02_growth_bounds_137s_1080p30.mp4, exports/mm02_growth_bounds_137s_short_1080x1920.mp4.

137초 개정 검증: 본편 1920×1080, 쇼츠 1080×1920. 두 파일 모두 30fps·4,110프레임·137초이며 오디오는 없다. 쇼츠의 수식 전체 화면과 문장별 자막 배치를 확인했다.
