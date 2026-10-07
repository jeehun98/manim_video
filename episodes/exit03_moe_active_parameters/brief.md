# Dynamic Inference 03 제작 기준

- 핵심 발견은 `Total Parameters와 한 Token에 활성화되는 Active Parameters를 분리할 수 있다`이다.
- MoE가 모델 전체를 Expert로 바꾸는 것처럼 그리지 않고 Transformer block의 FFN sublayer가 Expert들로 대체되는 흐름을 보여준다.
- Router는 Token 단위로 점수를 만들고 예시에서는 8개 중 E2, E7을 고르는 Top-2 routing을 사용한다.
- Expert 수가 4→8→16으로 늘어도 active expert 수가 2일 수 있음을 시각화한다.
- 계산량이 완전히 일정하거나 무료라고 표현하지 않는다. Router, 통신, Token batching 비용을 명시한다.
- Dense와 MoE 비교는 `더 큰 전체 모델`과 `선택된 활성 경로`의 차이에 한정한다.
- Token별 routing과 load imbalance를 보여주되 routing algorithm이나 auxiliary loss 상세는 다루지 않는다.
- Early Exit은 Layer, Token Pruning은 표현, MoE는 Parameter 경로를 선택한다는 Dynamic Inference 흐름을 잇는다.
- 영상은 음성 누적 시점에 맞춘 96초, 1080×1920, 30fps 무음 마스터다.
