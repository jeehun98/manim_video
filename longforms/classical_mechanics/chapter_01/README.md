# 고전역학 1장 — 예측이 가능해진 물체의 운동

사용자 확정 29문장·156초. 16:9 1920×1080·30fps, 전체 원문 자막 포함 **무음** 영상. 음원 미제공.

물체의 위치만으로 미래를 정할 수 없다는 질문에서 출발해, 뉴턴 법칙·진자의 힘 분해·비선형 운동방정식·미래 위치 예측으로 이어진다. 7개 독립 씬. 대본은 사용자 원문을 보존하고 모델의 조건과 수학적 구별은 화면에서 표시한다.

## 실행

```powershell
py -3.12 longforms/classical_mechanics/chapter_01/build.py --preview --scene 5
py -3.12 longforms/classical_mechanics/chapter_01/build.py
```

결과: `exports/classical_ch01_156s_longform_final.mp4`, 같은 이름의 `_captions.srt`.

`timing.json`에 문장 종료 시각, `manifest.json`에 독립 씬 길이, 씬별 `spec.md`에 주장을 기록한다. `physics.py`는 비선형 진자 RK4 적분을 미리 수행하며, 진자와 힘·모델·예측 위치가 같은 상태를 참조한다. 렌더 소스와 설정의 해시가 같을 때만 캐시를 재사용한다.

마지막 연결계는 힘과 제약의 정적 개념도이다. 연결계의 동역학을 시뮬레이션한 화면이 아니다. 이후 챕터 영상은 포함하지 않는다.
