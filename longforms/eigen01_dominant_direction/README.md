# 행렬을 계속 곱하면 왜 특정 방향만 남을까?

고윳값과 고유벡터 1막. 사용자 제공 확정 내레이션과 119초 콘티 기준.

- 쇼츠용: 1080×1920, 30fps, 119초
- 롱폼용: 1920×1080, 30fps, 119초
- 미리보기: 각각 360×640 / 854×480, 15fps
- 14개 독립 씬. 세로 비교 화면은 위아래, 가로 비교 화면은 좌우 배치.
- 화자 표기: 연우. 실제 음원은 제공되지 않아 영상은 무음이다. 음성 합성은 수행하지 않았다.
- 자막은 사용자 제공 씬 경계 단위의 별도 SRT다. 문장별 발화시간을 추정하지 않았으며 영상에 자막을 굽지 않았다. 음원 도착 후 문장별 자막과 mux를 수행한다.
- 수학 모델: A=((2,1),(1,2)), x₀=(1,0), v₁=(1,1), v₂=(1,−1). 초기 벡터는 콘티의 좌표를 유지한다(표준 x축 위이며 고유방향에 비스듬함).
- 초반 실제 벡터 성장 장면은 구간별 고정 척도를 사용한다. 정규화 비교에는 표시 목적이라는 문구를 명시한다. 성분 성장 막대는 27배까지 동일 척도다.
- 미세한 Manim 프레임 반올림은 씬 끝에서 1~수 프레임 정지 보정 후 정확한 프레임 수로 결합한다. 음성 속도 조정은 없다.

## 실행

```powershell
python longforms/eigen01_dominant_direction/build.py --preview
python longforms/eigen01_dominant_direction/build.py
python longforms/eigen01_dominant_direction/build.py --layout shorts --scene 8
```

출력: `exports/eigen01_119s_shorts_final.mp4`, `exports/eigen01_119s_longform_final.mp4` 및 같은 이름의 SRT. 미리보기는 `_preview.mp4`.

필요 도구: Python 3.12, Manim 0.21.0, FFmpeg/FFprobe, Malgun Gothic. LaTeX 설치 없이 Pango 텍스트로 수식을 표시한다.

## 자료

- `storyboard.md`: 원본 콘티
- `master_script.md`, `narration.md`, `tts_script.txt`: 확정 대본
- `brief.md`: 제작 기준
- `manifest.json`, `scenes.yaml`, `timing.json`: 14개 구간과 길이
- `scenes/01`–`scenes/14`: 씬별 spec, TTS 원문, Manim 클래스, 렌더
- `scene_engine.py`: 공통 수학 모델과 화면비별 레이아웃

## 검증 결과

두 최종본 각각 119.000초, 3,570프레임, 30fps 및 요청 해상도를 ffprobe로 확인했다. FFmpeg 전체 디코딩 오류 없음. 미리보기 주요 화면(세로 17개·가로 15개)을 시각 점검했다. 상세 메타데이터는 `verification.json`.

## 내레이션 핵심 자막 포함본

`python longforms/eigen01_dominant_direction/add_captions.py`로 기존 최종 영상에 19개 핵심 발췌 자막을 굽는다. 두 화면비에 맞춰 세로는 두 줄, 가로는 한 줄로 배치하고, 기존 수식 아래에 별도 자막 영역을 사용한다. 시간은 사용자 콘티의 구간 경계와 정의·성장률 세부 타이밍을 사용한다. 음원 기반 문장 종료 시각으로 간주하지 않는다.

출력: `exports/eigen01_119s_shorts_final_captioned.mp4`, `exports/eigen01_119s_longform_final_captioned.mp4`. 자막이 영상에 포함되므로 별도 SRT를 불러올 필요가 없다. 편집 원본은 `caption_cues.json`, `captions_excerpt_*.ass`, `captions_excerpt_*.srt`다. 기존 무음 최종본과 전체 내레이션 구간 SRT는 유지한다.

## 자막 배치 수정

`episodes/prune01_zero_weights/scene.py`, `episodes/calc01_transpose/scene.py`, `episodes/dist03_what_is_variance/scene.py`, `episodes/learn01_after_accuracy/scene.py`의 구성 참고. 기존 쇼츠는 9×16 좌표에서 자막 중심 y=−5.8~−6.25, 글자 25~27을 사용하고 수식·보조 설명을 그 위에 둔다.

이번 세로판은 자막을 하단 약 12% 지점에 두고 60px ASS 글자(이전 대비 25% 확대), 두 줄, 외곽선 없이 표시한다. 보조 설명은 y=−4.25(14.22 높이 기준), Manim 21 크기·보조색으로 낮춰 위계를 분리한다. 가로판은 46px 한 줄로 확대한다. 시간과 화면 속 수학은 그대로 유지한다.
