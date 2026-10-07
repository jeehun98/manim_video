# 제작 기준 — 기억을 저장하는 신경망은 왜 에너지를 최소화할까?

- 목표: Hopfield network의 연상기억을 분류가 아니라 `상태 갱신 → 에너지 감소 → 안정점 수렴 → 패턴 복원`으로 이해시킨다.
- 17장면, 151초, 세로 1080×1920 / 30fps / 무음. 사용자가 제공한 TTS 누적 시각을 장면 경계로 사용한다.
- 이진 노드는 `s_i ∈ {-1,+1}`로 단순화한다. 원 논문의 0/1 표현과 등가인 ±1 표현을 사용한다.
- 비동기식 단일 노드 업데이트와 대칭 가중치, 자기연결 없음이라는 이상적 조건에서 에너지가 증가하지 않는 구조를 표현한다.
- “가장 가까운 패턴”을 항상 찾는다고 단정하지 않는다. 초기 상태가 속한 attraction basin의 안정점으로 수렴한다고 설명한다.
- 에너지 지형은 고차원 상태공간을 2차원 단면으로 그린 개념도다. 일반적인 현대 신경망의 loss landscape와 동일시하지 않는다.
- Hinton과 Boltzmann machine은 다음 편을 예고하는 연결만 제공한다.

## 근거

- Nobel Prize 2024 press release: https://www.nobelprize.org/prizes/physics/2024/press-release/
- Nobel Prize 2024 popular information: https://www.nobelprize.org/prizes/physics/2024/popular-information/
- Popular science PDF: https://www.nobelprize.org/uploads/2024/10/popular-physicsprize2024-2.pdf

## 검증

- 미리보기와 접촉시트에서 손상·복원 픽셀 패턴, 픽셀 갱신과 공의 하강 동기화, basin 표현, 수식과 세로 안전영역을 확인했다.
- 장면 경계: 0, 8, 15, 23, 33, 41, 51, 60, 68, 75, 83, 93, 102, 110, 120, 129, 139, 151초.
- 최종본 `exports/science15.mp4`: 1080×1920, 30fps, 4,530프레임, 150.994987초, 비디오 스트림 1개·오디오 스트림 없음.
