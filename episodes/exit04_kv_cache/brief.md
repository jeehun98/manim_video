# KV Cache 제작 기준 — 피드백 반영

- 핵심 시각화: 시간 × 위치의 K,V 재계산 삼각형 → 중복 제거 → 새 계산 대각선 + 저장된 Cache.
- 같은 열을 반복 강조하여 새 Token과 과거 재계산을 구별한다. 칸은 K,V projection 생성만 뜻하며 전체 Transformer 계산량이 아니다.
- Causal Attention과 고정 모델·prefix·위치·추론 조건에서 레이어별 과거 표현이 변하지 않는 이유를 설명한다. 양방향 Attention에 일반화하지 않는다.
- Q,K,V 설명은 중복 제거 이후 새 위치를 확대하며 시작한다. 새 위치에서는 Q,K,V 모두 계산한다.
- 과거 Q는 잘못된 값이 되는 것이 아니라 이후 위치 출력을 만들 때 다시 필요하지 않다. Q는 일시적 조명, K,V는 유지되는 정보로 대비한다.
- 새 Q가 과거와 현재 K에 비교되고 softmax 가중치로 V를 가중합하는 계산은 계속 필요하다. 가중치 수치는 예시다.
- 레이어마다 Cache가 있다. full-context 동적 Cache가 커지며 저장 및 읽기 비용이 늘어남을 표현한다. sliding-window 정책은 생략한다.
- 칸 수 및 메모리 도식은 실측 가속·메모리 비율이 아니다.
- 13장면, 100초 추정 발화 시간, 1080×1920 30fps 무음 마스터. 대본·TTS·SRT는 새 장면 순서에 맞춰 갱신한다.
- 박스·화살표 반복 대신 삼각형/대각선, 시간 방향, Query 조명, Cache 축소 확대와 읽기 스윕을 사용한다.

## 내용 검증 출처

- Hugging Face 공식 Cache 설명: https://huggingface.co/docs/transformers/cache_explanation
