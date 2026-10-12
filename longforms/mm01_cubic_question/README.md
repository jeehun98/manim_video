# 1막 — 행렬곱은 정말 n³번 계산해야 할까?

새 행렬곱 시리즈 1장. 사용자 콘티의 7개 씬을 구현한다. 동일한 입력 A=[1,2;3,4], B=[5,6;7,8]과 출력 [19,22;43,50]을 유지한다.

M₁의 내레이션 오기를 39에서 65로 수정했다. 입력 조합, 중간 곱, 출력 복원, 항 소거를 이동과 연결선으로 추적한다.

현재 본편과 쇼츠는 사용자 제공 문장별 종료 시각을 적용한 142초 무음 영상이다. 내레이션 시각 34구간과 SRT를 갱신했다. 음성 파일은 제공되지 않아 오디오를 결합하지 않았다.

실행: `python longforms/mm01_cubic_question/build.py --preview`

최종: `python longforms/mm01_cubic_question/build.py`

씬 교체: `python longforms/mm01_cubic_question/build.py --scene 3` 이후 `--concat-only`.

검증: 1920×1080, 30fps, 8,130프레임, 271초, 오디오 없음. 독립 렌더에서 발생한 두 씬의 1프레임 부족분은 마지막 프레임 복제로 정규화했다. 네 출력 복원은 정수 입력 100쌍으로 추가 검산했다.

## 142초 개정

씬 경계: 0 / 19 / 41 / 57 / 76 / 97 / 120 / 142초. narration_timing.json이 기준이다.

쇼츠: `python longforms/mm01_cubic_question/make_short.py`. 1080×1920, 30fps, 전체 가로 화면 보존, 상단 제목·하단 큰 문장 자막.

현재 출력: exports/mm01_cubic_question_142s_1080p30.mp4 및 exports/mm01_cubic_question_142s_short_1080x1920.mp4. 기존 271초 출력은 이전 버전이다.
