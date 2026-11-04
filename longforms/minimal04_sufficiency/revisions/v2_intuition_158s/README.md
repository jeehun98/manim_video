# 04 충분통계량 — 직관 실험 개정본 (158초)

사용자가 확정한 새 대본과 37개 문장 종료 시각을 적용한 현재 버전. 기존 153초 버전은 상위 폴더에 보존한다. 영상은 음원 미제공으로 무음이며 원고와 자막을 별도로 제공한다.

## 서사와 화면

서로 다른 기록 → 같은 평균 → 평균 후보 비교 → 제곱거리 합의 차이 26 → 같은 상대적 지지 → 가정 변경 → 최소충분성. 수식 전개와 확률밀도 계산 장면을 제거하고, 후보 평균을 직접 움직여 관찰한다. 독립적인 15개 씬으로 세로 9:16과 가로 16:9를 각각 렌더한다.

모든 관측값은 고정. n=5와 알려진 동일 분산 σ²=4를 예시로 쓴다. 후보 평균 3일 때 A=10, B=36; 5일 때 A=30, B=56. 제곱거리 합 B−A=26은 후보 평균과 무관하다. 같은 기록 내 후보 3→5의 점수 증가가 20으로 같으므로 상대 지지도 같다. 평균 3을 1로 두면 평균 5의 상대 지지는 두 기록 모두 exp(−20/8)≈0.082085이다. 서로 다른 기록의 원래 우도 절대값이 같다는 뜻이 아니다.

정확한 항등식: S_B−S_A=0, n_B−n_A=0이므로 제곱거리 합 차이는 Q_B−Q_A=81−55=26. 수치 검증은 math_verification.json에 기록한다. 분산이 미지이면 이 차이에 대응하는 우도 비율이 분산에 의존하므로 평균만으로는 평균과 분산을 함께 추론하기에 충분하지 않다.

## 재현

프로젝트 루트에서:

```powershell
python longforms/minimal04_sufficiency/revisions/v2_intuition_158s/build.py --preview
python longforms/minimal04_sufficiency/revisions/v2_intuition_158s/build.py
```

문장 종료 시각은 narration_timing.json, 원문은 narration.md, 발음 원고는 tts_script.txt. 원고에는 타임코드 없이 주요 화면 변화별로 빈 줄을 둔다. 화면은 서술 자막을 포함하지 않고 렌더하며, concat 후 하나의 ASS 트랙으로 자막을 합성한다. 전환 전후 프레임은 verify_caption_boundaries.py로 검사한다.

출력: exports/minimal04_v2_158s_shorts_final.mp4 및 exports/minimal04_v2_158s_longform_final.mp4. 음성은 포함되지 않는다.

## 완료 상태

두 레이아웃 최종본과 미리보기 제작 완료. 158초·30fps 검증, 전체 디코딩, 각 111프레임의 자막 경계 검사 및 주요 화면 검토 통과. 상세 결과는 verification_final.json 및 production_notes.md.
