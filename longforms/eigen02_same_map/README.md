# 숫자가 다른 두 행렬이 같은 변환일 수 있을까?

고윳값과 고유벡터 시리즈 2편. 사용자 확정 대본, 문장별 종료 시각 27개, 총120초, 13개 독립 씬.

- 세로 쇼츠: 1080×1920, 30fps / 미리보기 360×640, 15fps
- 가로 롱폼: 1920×1080, 30fps / 미리보기 854×480, 15fps
- 세로 비교는 위아래, 가로 비교는 좌우 배치.
- 내레이션 음원 미제공. 무음 영상이며 TTS 합성은 수행하지 않는다.
- 문장별 종료 시각은 timing.json, 전체 SRT, 영상 구간, 핵심 자막에 반영한다. 발음 원고 본문에는 시간·제목을 넣지 않는다.
- 1편에서 수정한 핵심 자막 크기와 위치 사용. 세로 60px·하단170px 여백·두 줄, 가로46px·한 줄. 외곽선 없음. 수식은 별도 보조 영역.

## 제작과 실행

```powershell
python longforms/eigen02_same_map/build.py --preview
python longforms/eigen02_same_map/add_captions.py --preview
python longforms/eigen02_same_map/build.py
python longforms/eigen02_same_map/add_captions.py
```

`--layout shorts` 또는 `--layout longform`으로 화면비를 지정한다. `build.py --scene 8`로 독립 씬을 수정할 수 있다. 최종 자막 포함 출력은 `exports/eigen02_120s_shorts_final_captioned.mp4`, `exports/eigen02_120s_longform_final_captioned.mp4`다.

## 수학과 연출

A=((2,1),(1,2)), D=diag(3,1), P=((1,1),(1,−1)). x_world=P x_eigen, A P=P D. 표준 입력(2,1)은 고유좌표(1.5,0.5), 표준 출력(5,4)은 고유좌표(4.5,0.5).

0–31초에는 두 행렬을 모두 표준 좌표에서 비교한다. 31–64초에는 실제 입력 화살표를 고정하고 축·단위·좌표만 바꾼다. 64–79초에는 좌표 숫자 평면임을 명시한다. 79–85초에는 P를 통해 고유좌표 출력을 실제 공간으로 대응시킨 뒤 같은 원점·척도로 두 출력을 겹친다. 89–99초에는 추가 입력3개로 대응을 확인하며 AP=PD로 일반성을 요약한다.

검증 환경: Python3.12, Manim0.21.0, FFmpeg/FFprobe, Malgun Gothic. LaTeX 없이 Pango 수식을 사용한다. Manim의 프레임 반올림 차이는 씬 마지막 수 프레임에서만 보정해 120초를 유지한다.

TTS 원고와 씬별 `script.txt`는 숫자의 한국어 발음(예: 일 점 오)을 사용하며 원문 숫자는 `narration.md`와 자막에 보존한다. 실제 음성 파일은 아직 없다.

## 완료 검증

두 자막 포함 최종본 각각120.000초·3,600프레임·30fps, 세로1080×1920·가로1920×1080을 ffprobe로 확인했다. FFmpeg 전체 디코딩 오류 없음. AP=PD 및 콘티 입력4개의 실제 출력 대응을 검증했다. 양쪽 화면비 미리보기16개 시점을 점검하고, 최종 자막 포함본에서 좌표 분해·계산·겹침 장면을 확인했다. 상세 결과는 `verification.json`.
