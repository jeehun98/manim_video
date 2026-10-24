# 고윳값 간격 — PCA의 주성분 방향이 불안정해지는 이유

고윳값과 고유벡터5편. 사용자 확정 대본, 문장별 종료 시각30개, 총146초, 19개 독립 씬. 음원이 제공되지 않아 무음으로 제작한다.

- 세로 쇼츠1080×1920, 가로 롱폼1920×1080, 각각30fps
- 미리보기360×640 / 854×480, 15fps
- 핵심 자막은 세로60px·두 줄·하단170px 여백 / 가로46px·한 줄. 실제 문장 종료 시각과 일치한다.
- 원문은 narration.md/master_script.md, 읽지 않는 제목·시간을 뺀 발음 원고는 tts_script.txt와 씬별 script.txt. PCA는 피 씨 에이로 표기한다.

## 실행

```powershell
python longforms/eigen05_eigengap/data_model.py
python longforms/eigen05_eigengap/build.py --preview
python longforms/eigen05_eigengap/add_captions.py --preview
python longforms/eigen05_eigengap/build.py
python longforms/eigen05_eigengap/add_captions.py
```

`--layout shorts` / `--layout longform` 지원. `build.py --scene 9`로 독립 씬 수정. 최종 자막 포함 출력은 `exports/eigen05_146s_shorts_final_captioned.mp4`, `exports/eigen05_146s_longform_final_captioned.mp4`.

## 실제 계산되는 데이터

고정 시드20261023, 합성 관측값80개. 모든 장면에서 실제 점의 평균과 표본 공분산(XcᵀXc/79), eigh 고유분해를 계산한다. 고윳값은 큰 순으로 정렬하고, PC 방향은 화살표가 아닌 직선으로 표현한다. 회전량은 부호에 무관한0–90도 직선각이다.

기초 설명의 길쭉한 분포는25도 회전한 diag(3,0.5) 공분산을 사용한다. 본 비교는 C_large=diag(2,1), C_small=diag(1.01,1), 두 공분산에 같은 E=((0,0.01),(0.01,0))가 생기는 실제 점 편집이다.

두 데이터는 각각76개의 중심 대칭·백색화된 점과 공통 제어점(±2,0),(0,±2)로 구성한다. 76개 점의 공분산 기여를 목표 행렬에서8/79 I를 뺀 값에 맞춘다. 네 제어점만 대칭적으로 조금 회전시켜 두 분포에서 정확히 같은 E를 만든다. 따라서 변한 점4개·각 점의 이동 벡터까지 같으며 나머지76개는 고정이다.

- 최대 점 이동0.0989011, RMS 이동0.0221150 (양쪽 동일)
- 공분산 변화 스펙트럴 노름0.01 (양쪽 동일)
- 초기 간격1.00 → PC1 회전0.572881°
- 초기 간격0.01 → PC1 회전31.717474°

비교 장면의 고윳값 막대에는 변경 전 값을 사용한다고 표시한다. 일반 정보 패널은 현재 데이터에서 재계산한 값이며 변경 후 간격은 별도로 달라질 수 있다. 표시 숫자는 소수 셋째 자리로 반올림한다.

## 고윳값이 같은 경우

표본 공분산이 수치 오차 내에서 정확히 I인 유한 점 데이터를 사용한다. 이때 PC1을 임의 선택하지 않고 중립적인 후보 직선들을 표시한다. 어떤 단위 방향의 투영 분산도1이다.

그 상태에서 수평 제어점2개 또는 수직 제어점2개만 이동하면 각각 diag(1.01,1), diag(1,1.01)이 된다. 최대 점 이동은0.096426으로 작지만 선택되는 두 PC1 직선은90도 다르다. 두 결과는 서로 다른 데이터 상태라는 범례를 유지한다.

## 전달과 구조

storyboard.md 원본, timing.json 문장·씬 경계, scenes.yaml/manifest.json 인덱스, scenes/01–19 독립 spec·소스, data_model.py 수학 모델, data_validation.json 검증 수치. Python3.12·Manim0.21.0·FFmpeg/FFprobe·Malgun Gothic. LaTeX 없이 Pango 텍스트 사용. 미세한 Manim 프레임 반올림만 씬 끝에서 보정한다. 복습·예고를 추가하지 않는다.

## 최종 검증 완료

세로1080×1920·가로1920×1080 자막 포함 최종본 모두146.000초,30fps,4,380프레임. FFmpeg 전체 디코딩 통과. 문장 종료 시각30개 및 씬19개 반영. 비교 데이터의202개 중간 상태에서 실제 PCA 고유방향과 동일한 공분산 변화량을 확인했다. 주요 장면의 자막·배치 검토 완료. 음원 미제공으로 무음. 상세 결과는 verification.json에 기록한다.
