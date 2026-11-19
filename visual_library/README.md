# Visual Library

## 롱폼 격자·대화창 배경

`DialogueBackground`는 검은 바탕, 숫자·좌표축 없는 격자, 하단 흰 테두리
대화창을 제공한다. 메뉴나 중앙 박스 없이 위 공간 전체를 무대로 사용한다.
기본 프레임은 16×9이며 import만으로 렌더 설정을 변경하지 않는다.

```python
from manim import Scene, config
from visual_library.manim import DialogueBackground

config.frame_width, config.frame_height = 16, 9
config.pixel_width, config.pixel_height = 1920, 1080

class MyScene(Scene):
    def construct(self):
        background = DialogueBackground()
        self.add(background)
        background.set_caption("여기에 자막을 표시합니다.")
        # 내용은 y > background.stage_bottom 영역에 배치한다.
```

자막은 `set_caption()`으로 교체하고 빈 문자열로 비운다. 명시적 줄바꿈을
지원하며 글자가 대화창 안에 들어오도록 축소한다. `show_marker=False`로
별표를 숨길 수 있다. 격자 간격·색·투명도와 테두리 굵기도 조절할 수 있다.
`grid_under_dialogue=True`는 격자를 화면 끝까지 이어 대화창이 배경 위에
겹쳐 보이게 한다. 이전 훈련 시안에서 이 옵션을 사용했다.
현재 [3인칭 초기 화면](previews/training/README.md)은 격자를 숨기고 검은 배경·작은 캐릭터 점·큰 빈 대화창만 표시한다. 현재 진입점은 `initial_screen.py`다.
배경은 고정해서 사용하고 내용 객체만 움직인다.

프로젝트 루트에서 배경 정지 화면 확인:

```powershell
python -m manim -s -r 1280,720 --media_dir media/dialogue_background visual_library/manim/dialogue_preview.py DialogueBackgroundPreview
```

반복해서 쓰는 렌더 객체를 에피소드와 분리해 보관하는 저장소다. 새 장면은
에피소드 폴더의 구현을 직접 import하지 않고 이 패키지의 공개 경로를 사용한다.

```python
from visual_library.manim import ACCENT, INK, Pill, WeightMatrix, text
from visual_library.manim.gpu import GPUBlock, data_row
```

## 구조

```text
visual_library/
├─ catalog.yaml          # 사람이 검색하는 객체 인덱스
├─ README.md             # 등록·사용 규칙
└─ manim/
   ├─ theme.py           # 색, 폰트, 화면 설정
   ├─ typography.py      # 텍스트 객체
   ├─ primitives.py      # 범용 UI·데이터 객체
   └─ gpu.py             # GPU 객체의 안정적인 공개 경로
```

다른 렌더러를 시험하게 되면 `motion_canvas/`, `remotion/`처럼 같은 레벨에
추가한다. 동일한 개념은 가능한 한 같은 객체 ID와 태그를 사용한다.

## 객체를 등록하는 기준

다음 조건을 모두 만족할 때 에피소드 코드에서 이곳으로 승격한다.

1. 두 장면 이상에서 다시 쓸 가능성이 있다.
2. 특정 장면의 시간표나 내레이션에 의존하지 않는다.
3. 생성자 인자로 텍스트, 색, 크기, 데이터가 바뀐다.
4. 세로 프레임 밖에서도 배치할 수 있도록 절대 좌표를 내장하지 않는다.
5. 객체를 생성하는 것만으로 전역 렌더 설정을 바꾸지 않는다.

한 장면에서만 쓰는 실험적 객체는 해당 `scene.py`에 둔다. 재사용성이 확인되면
구현을 `visual_library/<renderer>/`로 옮기고 `catalog.yaml`에 등록한다.

## 카탈로그 규칙

각 항목에는 다음 정보를 기록한다.

- `id`: 렌더러와 무관한 안정적인 이름
- `renderer`: 현재 구현체
- `import`: 새 코드에서 사용할 공개 import 경로
- `kind`: typography, container, data, connector, system 중 하나
- `tags`: Codex나 사람이 용도를 찾을 때 사용할 검색어
- `status`: `stable`, `adapter`, `experimental`

`adapter`는 기존 구현을 안정적인 공개 경로로 다시 노출한 객체다. 충분히 정리한
뒤 구현을 이 패키지로 옮기고 `stable`로 바꾼다.

## 호환성

기존 장면이 사용하는 `episodes.prune_series.visuals`는 호환 모듈로 유지한다.
그 모듈은 과거와 동일하게 import 시 세로 영상 설정을 적용한다. 반면
`visual_library.manim` 자체는 import만으로 해상도나 배경색을 바꾸지 않는다.

