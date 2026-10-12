# Visual Library

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

