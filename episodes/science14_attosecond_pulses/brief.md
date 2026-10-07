# 제작 기준 — 전자의 변화를 어떻게 볼 수 있을까?

- 목표: 아토초 과학을 전자의 사진으로 오해하지 않고, 전자 동역학보다 짧은 빛으로 시간 분해 측정을 가능하게 한 기술로 이해시킨다.
- 15장면, 120초 타이밍 초안, 세로 1080×1920 / 30fps / 무음. 실제 TTS 전에는 대사 문자 수에 비례해 장면 길이를 배분한다.
- 핵심 연쇄는 `터널 이온화 → 레이저 장에서 가속 → 재충돌·재결합 → 고차 고조파 → 위상 정렬 → 아토초 펄스`다.
- 전자 궤적과 원자 그림은 strong-field three-step model의 개념도이며 실제 공간 비율이나 양자 파동함수의 직접 영상이 아니다.
- `1 as = 10^-18 s`, 2001년 Agostini 연구팀의 약 250 as 펄스 열, Krausz 연구팀의 650 as 단일 펄스를 표시한다.
- Anne L’Huillier의 1987년 희가스 고차 고조파 발견이 후속 아토초 펄스 생성의 기반이 되었음을 결론에 연결한다.
- 수상 사유는 물질 속 전자 동역학 연구를 위한 아토초 빛 펄스 생성의 실험 방법이다.

## 근거

- Nobel Prize 2023 press release: https://www.nobelprize.org/prizes/physics/2023/press-release/
- Nobel Prize 2023 popular information: https://www.nobelprize.org/uploads/2023/11/popular-physicsprize2023-1.pdf
- Nobel Prize 2023 scientific background: https://www.nobelprize.org/uploads/2023/10/advanced-physicsprize2023-2.pdf

## 검증

- 미리보기와 접촉시트에서 장면 6–9의 전자 왕복과 빛 방출 인과, 고조파의 위상 정렬, 250 as/650 as 구분, 세로 안전영역을 확인했다.
- 최종본 `exports/science14.mp4`: 1080×1920, 30fps, 3,600프레임, 119.996029초, 비디오 스트림 1개·오디오 스트림 없음.
- 현재 구간 길이는 120초 기준 문자 수 배분 초안이다. 실제 TTS 구간이 확정되면 `scripts/retime_science14.py`에 경계를 반영한다.
