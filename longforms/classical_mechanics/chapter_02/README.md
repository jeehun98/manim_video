# 고전역학 2장 — 하나의 원리로 설명되는 운동

사용자 확정 37문장·180초. 16:9 1920×1080·30fps, 전체 원문 자막 포함 **무음** 영상. 음원 미제공.

일반화 좌표에서 출발해 에너지의 합과 차이, 라그랑지안, 운동 이력, 부호 있는 작용, 작용의 정지 조건으로 이어진다. 실제 운동과 세 종류의 끝점 고정 가상 경로를 수치 계산하며, 뉴턴·라그랑주 비교 화면은 같은 진자 상태를 공유한다.

## 실행

```powershell
py -3.12 longforms/classical_mechanics/chapter_02/build.py --preview --scene 5
py -3.12 longforms/classical_mechanics/chapter_02/build.py
```

결과: `exports/classical_ch02_180s_longform_final.mp4`, 같은 이름의 `_captions.srt`.

- `timing.json`: 사용자 제공 문장 종료 시각.
- `manifest.json`, 씬별 `spec.md`: 7개 독립 씬의 주장과 길이.
- `variational.py`: 가상 경로와 도함수·에너지·L·작용의 연결 계산 및 수치 검증.
- `storyboard.md`: 사용자 제공 콘티 원본.
- `../chapter_01/physics.py`, `../chapter_01/visuals.py`: 재사용하는 진자 모델·도형·색·폰트. 의존 소스도 렌더 캐시 해시에 포함한다.

작용 그래프는 선택한 경로 변형에서의 실제 적분값이다. 실제 경로의 작용은 약0.760이며, 정지 조건이 작용 자체가0이라는 뜻은 아니다. 정지와 최소를 구별하는 화면 문구를 포함한다. 연결계는 정적인 좌표 배치 개념도이다.
