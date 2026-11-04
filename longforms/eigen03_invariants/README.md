# 행렬의 숫자가 바뀌어도 변하지 않는 것은?

고윳값과 고유벡터 3편. 사용자 제공 확정 원문과 문장별 종료 시각27개, 총121초, 14개 독립 씬. 실제 음원 미제공으로 무음 제작한다. 사용자 제공 도입을 그대로 사용하며 내레이션을 추가하거나 수정하지 않는다.

- 세로 쇼츠: 1080×1920, 30fps / 미리보기360×640, 15fps
- 가로 롱폼: 1920×1080, 30fps / 미리보기854×480, 15fps
- 비교는 세로 위아래·가로 좌우. 핵심 자막은 세로60px·하단170px 여백·두 줄, 가로46px·한 줄.
- 실제 문장 종료 시각은 timing.json, 원문SRT, 핵심 자막, 씬에 반영. TTS 발음 원고에는 읽지 않는 제목·시간을 넣지 않는다.

## 실행

```powershell
python longforms/eigen03_invariants/build.py --preview
python longforms/eigen03_invariants/add_captions.py --preview
python longforms/eigen03_invariants/build.py
python longforms/eigen03_invariants/add_captions.py
```

두 도구 모두 `--layout shorts` / `--layout longform`을 지원한다. `build.py --scene 5`로 독립 씬을 렌더할 수 있다. 자막 포함 출력: `exports/eigen03_121s_shorts_final_captioned.mp4`, `exports/eigen03_121s_longform_final_captioned.mp4`.

## 수학과 시각 구현

A=((2,1),(1,2)). 현재 기저 P에 대한 M=P⁻¹AP를 실제 계산하며 격자와 원소를 동시에 갱신한다. 표시 원소·좌표는 소수 첫째 자리로 반올림한다. 고윳값3,1·대각합4·행렬식3은 정확한 값이다.

연속 변경 경로는 I → Q=((1,−1),(1,1)) → S=((1,1),(0,1)). Q는 고유기저의 두 번째 벡터 부호만 바꾼 동등한 선택이다. 방향성을 유지하는 가역 기저 사이를 연속 보간하며, 음의 행렬식 기저로 보간하다 특이행렬을 통과하는 문제를 피한다. Q⁻¹AQ=diag(3,1), S⁻¹AS=((1,0),(1,3)). 고유벡터(1,1)의 실제 방향은 고정하고 그 좌표는 기저에 따라 계산한다.

행렬식 장면의 단위 정사각형 꼭짓점은 A를 곱해 정확히 (0,0),(2,1),(3,3),(1,2)로 변환한다. 면적1→3을 같은 척도로 보여준다. 일반적인 합·곱 관계에는 정사각행렬·복소 고윳값 포함·대수적 중복도 조건을 화면에 명시한다.

반례는 I와 B=((1,1),(0,1)). 고윳값1,1·대각합2·행렬식1은 같지만 P⁻¹IP=I이므로 닮음이 아니다. 조르당 형식 등으로 확장하지 않는다.

## 자료와 환경

`storyboard.md` 원본 콘티, `master_script.md`·`narration.md` 원문, `tts_script.txt` 및 씬별 `script.txt` 발음 원고, `timing.json` 문장 및 씬 경계, `scenes.yaml`·`manifest.json` 인덱스, `scenes/01`–`scenes/14` 독립 소스와 spec. Python3.12·Manim0.21.0·FFmpeg/FFprobe·Malgun Gothic. LaTeX 없이 Pango 수식 사용. Manim의 미세 프레임 반올림은 씬 마지막 수 프레임만 보정한다.

## 최종 검증

두 자막 포함 최종본 각각121.000초·3,630프레임·30fps 및 요청 해상도를 ffprobe로 확인했다. FFmpeg 전체 디코딩 오류 없음. 문장별 종료 시각27개와 자막 경계가 일치한다. 기저 경로202개 표본에서 가역성·고윳값3,1·대각합4·행렬식3을 확인했고 단위 정사각형의 변환 면적3과 전단 면적1을 검사했다. 두 화면비의 미리보기18개 시점과 최종 자막 포함 화면을 확인했다. 상세 메타데이터는 `verification.json`.
