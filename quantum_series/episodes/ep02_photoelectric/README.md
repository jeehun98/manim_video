# EP.02 · 광전효과와 아인슈타인

사용자 확정 대본 **22문장·101초**. 세로 1080×1920 / 가로 1920×1080, 각각 30fps, 전체 문장 자막. 음원은 제공되지 않아 무음으로 제작한다.

## 제작 구조

`script.json`이 대본과 문장 종료 시각의 원본이다. `narration.md`, `tts_script.txt`와 `scenes/*/spec.md`를 먼저 작성하여 내용을 고정한 뒤 화면을 만든다. 씬 spec은 `longforms/_template/` 규격을 따른다.

각 씬은 독립적인 `scenes/<id>/scene.py`·`spec.md`·`script.txt`와 MP4를 가진다. 5개 씬 길이는 사용자 시각 기준 16+23+23+24+15초다. 공통 애니메이션은 `direction.py`, 화면비별 배치는 `layouts.py`, 실험 조건은 `physics_model.py`, 도형은 `shared/photoelectric.py`에 둔다. 화면비 간 늘리기나 크롭을 사용하지 않는다.

- 0–16초: 같은 금속에서 세기와 색을 바꿔 관찰한다.
- 16–39초: 파동의 진폭과 진동수를 분리한다. 개별 빛 에너지 단위 기호는 등장하지 않는다.
- 39–62초: 아인슈타인의 가설을 소개하고 43초부터 황금색 에너지 단위를 도입한다.
- 62–86초: 단위당 에너지와 일함수를 비교하고, 세기와 진동수의 역할을 분리한다.
- 86–101초: 최초 실험의 차이를 설명한 뒤 플랑크와 아인슈타인의 서로 다른 주장을 연결한다. ‘광자’ 명칭은 97초에 처음 표시한다.

EP.01과 동일한 파동, 진동자, 황금색 에너지 기호를 재사용한다. 영상 순서 언급·별도 복습·다음 편 예고·엔드카드 없이 독립적으로 완결한다. 마지막은 파동과 에너지 기호를 남긴다.

## 실행

```powershell
python scripts/render.py quantum02 --preview
python scripts/render.py quantum02
python scripts/render.py quantum02_shorts
python scripts/render.py quantum02_longform
```

직접 실행: `python quantum_series/episodes/ep02_photoelectric/build.py --layout both`.
씬만 수정할 때: `--scene 04_threshold --layout shorts` (동일 품질·종료 모드의 나머지 MP4가 있어야 한다).
`--ending standalone` / `--ending join` 모두 지원한다. 기본은 쇼츠 standalone, 가로 join이다. 두 모드 모두 101초 대본을 유지한다. standalone은 마지막 빛을 낮추고, join은 밝기를 유지한다. 마지막 1초는 정지한다.

최종 파일: `exports/quantum02_shorts.mp4`, `exports/quantum02_longform.mp4`.
미리보기는 `_preview.mp4`. 로그·중간 씬은 `media/quantum02/` 아래에 저장한다.
빌드 시 각 씬과 최종 3030프레임·101초·30fps·해상도를 검사한다. 대본·자막·타이밍 자료는 음원과 별개다.

## 물리 조건과 표현의 범위

- 하나의 가상 금속을 고정한다. 일함수 Φ=2.2 eV. 낮은 진동수는 700 nm에 해당하며 E≈1.77 eV, 높은 진동수는 450 nm에 해당하며 E≈2.76 eV다. 색은 해당 조건의 예시이며 모든 금속의 문턱값을 뜻하지 않는다.
- `frequency`, `intensity`, `work_function`을 독립 변수로 관리한다. `E=hν`, 임계 진동수 `Φ/h`, 최대 운동에너지 `max(0,E−Φ)`를 계산한다. 빛이 없으면 방출되지 않는다.
- 같은 진동수에서 세기가 4배면 진폭은 2배, 단위 면적·시간당 도달하는 단위 수는 4배다. 진동수를 바꿀 때 세기를 고정하면 단위 수는 `I/(hν)`에 따라 달라지므로, ‘세기=개수’라고 일반화하지 않는다. 79–86초 왼쪽은 진동수 고정, 오른쪽은 단위 수 고정을 명시한다.
- 일반적인 일광자 광전효과의 이상화된 개념도다. 다광자 과정, 표면 상태, 흡수 확률, 실제 방출률을 수치적으로 모사하지 않는다. 낮은 진동수 단위들이 한 전자에 쌓이는 연출을 하지 않는다.
- 금속 내부에 있는 청록색 전자만 방출시킨다. 단위의 황금색 외곽선 크기는 실제 광자의 크기를 뜻하지 않는다. 에너지 비교에는 선형 막대 길이를 쓴다.
- 19–26초의 게이지는 고전적 에너지 전달 직관이다. 전자가 빛 에너지를 시간에 따라 축적하는 실제 광전효과 모형이 아님을 화면에 표시한다.
- 시간에 따른 진동을 보일 때 공간의 조밀한 무늬만으로 설명하지 않고, 고정된 두 지점에서 같은 시간 동안 서로 다른 속도로 움직이는 점을 사용한다.
- 플랑크의 1900년 에너지 분배 계산과 아인슈타인의 1905년 빛 자체에 관한 광양자 가설을 동일시하지 않는다. 97초 전에는 ‘광자’ 명칭을 쓰지 않는다.

출처: [아인슈타인 노벨상 발표 연설](https://www.nobelprize.org/prizes/physics/1921/ceremony-speech/), [OpenStax 광전효과](https://openstax.org/books/university-physics-volume-3/pages/6-2-photoelectric-effect).
