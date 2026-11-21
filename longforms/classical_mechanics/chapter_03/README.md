# 고전역학 3장 — 새로운 공간에 기록된 운동

사용자 확정56문장·299초. 16:9 1920×1080·30fps, 전체 원문 자막 포함 **무음** 영상. 음원 미제공.

실제 진자 → 각도·각속도 상태 공간 → 라그랑지안의 기울기와 정준운동량 → 르장드르 변환 → 위상 공간으로 이어진다. 8개 독립 씬, 동일한 비선형 진자 상태 데이터를 여러 표현에 연결한다.

## 실행

```powershell
py -3.12 longforms/classical_mechanics/chapter_03/build.py --preview --scene 5
py -3.12 longforms/classical_mechanics/chapter_03/build.py
```

결과: `exports/classical_ch03_299s_longform_final.mp4`, 같은 이름의 `_captions.srt`.

`timing.json`은 사용자 제공 종료시각, `manifest.json`과 씬별 `spec.md`는 독립 구간과 주장, `storyboard.md`는 사용자 콘티이다. `mechanics.py`는 정준운동량·르장드르 변환·정확한 비선형 위상 궤적과 수치 검증을 담당한다. `../chapter_01/physics.py`, `../chapter_01/visuals.py`의 재사용 의존성도 캐시 해시에 포함한다.

르장드르 변환은 각도를 고정한 진자의 L(ω) 그래프에서 보여준다. 기울기 pθ와 접선 절편 −H가 새 함수 H의 점과 연결된다. 단순한 축 이름 교체로 표현하지 않는다. 이 모델에서는 속도에 대한 헤시안 I=4>0이므로 역변환이 가능하다.

위상 공간은 국소 각도 차트로 표시하며 선택한 왕복 진폭 범위의 정확한 에너지 등고선을 사용한다. 마지막은 다음 장 별도 타이틀 없이 H(q,p)로 마무리한다.
