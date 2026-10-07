# Dynamic Inference 02 제작 기준

- 핵심 발견은 `Token 하나를 제거하면 그 표현뿐 아니라 attention score 행렬의 행·열도 함께 줄어든다`이다.
- Vision Transformer의 4×4 patch grid를 사용해 이미지 조각과 Token을 연결한다.
- 중요도는 특정 방법 하나로 일반화하지 않고 중간 표현이나 attention 정보, 별도 scorer 등으로 평가할 수 있다고 표현한다.
- 예시는 Top-k 8/16이지만 모든 Token Pruning이 Top-k라고 단정하지 않는다.
- `16×16=256`, `8×8=64`는 QKᵀ attention score 부분의 항목 수다. 전체 Transformer FLOPs가 정확히 1/4이 된다고 표현하지 않는다.
- Weight Pruning은 모델 파라미터, Token Pruning은 입력별 중간 표현을 제거한다.
- 중요한 Token의 조기 제거는 되돌릴 수 없는 정보 손실이 될 수 있음을 보여준다.
- 마지막에 Early Exit은 입력 전체, Token Pruning은 일부 표현을 종료한다는 차이를 회수한다.
- 고양이와 자동차 입력은 내장 생성형 이미지 도구로 만든 PNG이며 Manim은 patch grid와 애니메이션을 담당한다.
- 영상은 93초, 1080×1920, 30fps 무음 마스터다.

## 생성 이미지 프롬프트 요약

- `cat.png`: 선명하고 식별하기 쉬운 줄무늬 고양이, 중립 실내 배경, 텍스트 없음. 01편 생성 에셋 재사용.
- `car.png`: 정면 3/4 구도의 명확한 소형 자동차, 단순한 도심 배경, 4×4 patch 분할에 적합한 정사각형 사진, 로고·텍스트 없음.
