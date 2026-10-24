# 행렬 분해 이상형 월드컵 ② — 분해 조건 · 수정본 v2

- 확정 길이: 132초. 사용자 수정 대본의 모든 문장 종료 시각을 그대로 적용.
- 쇼츠: 1080×1920, 가로형: 1920×1080. 최종 30fps, 각각 3960프레임.
- 상태: 132초 수정 대본의 영상 제작본. 상위 폴더의 92초 대본·영상은 이전 버전.
- 음원 미제공: 무음, 화면 자막 및 별도 SRT.

## 학습 목표

EVD의 조건을 이해하고, A의 열벡터가 AᵀA의 원소를 어떻게 결정하는지 발견한다.

## 핵심 결론

입력 좌표축의 출력 길이 제곱과 내적이 Gram 행렬에 담기며, 대칭·양의 준정부호 구조가 SVD의 존재성으로 연결된다. 이번 분해 조건 대결은 SVD 승, 점수 1:1.

## 작업 순서

1. 사용자 수정 원문을 `master_script.md`로 보존한다.
2. 사용자 문장 종료 시각으로 `timing.json`, 씬별 `spec.md`, `scenes.yaml`을 확정한다.
3. Manim 장면과 화면 자막을 해당 시각 안에서 제작한다.
4. 미리보기 화면·수학 검토 후 두 화면비의 최종본을 렌더한다.
5. 씬별 합본과 132초·3960프레임·해상도를 검증한다. 음원 제공 시 별도 mux할 수 있다.

## 실행

프로젝트 루트에서:

```powershell
python longforms/evdsvd02_conditions/revisions/v2_132s/build.py --preview
python longforms/evdsvd02_conditions/revisions/v2_132s/build.py
python longforms/evdsvd02_conditions/revisions/v2_132s/build.py --layout longform --scene 15
python longforms/evdsvd02_conditions/revisions/v2_132s/build.py --layout longform --concat-only
```

23개 씬을 독립 렌더하고 concat한다. 두 레이아웃을 모두 완료한 뒤 결과를 검증한다.
Manim 0.21.0, FFmpeg, Malgun Gothic 필요. 기본 동시 렌더 수 2(`--jobs`).
출력: `exports/evdsvd02_conditions_132s_{shorts,longform}_final.mp4` 및 SRT.
공통 글꼴·레이아웃은 1편, 행렬 렌더링은 2편 이전 소스의 헬퍼를 재사용한다.

## 수학·타이밍 기준

- EVD는 대각화 A=PDP⁻¹. 정사각행렬은 필요조건이며 충분조건이 아니다.
- 76–111초 예시는 A=[[1,2],[2,0],[0,1]], Gram=[[5,2],[2,5]]. 대각 길이 제곱5, 비대각 내적2.
- 실제 직교 고유벡터 (1,1)/√2, (1,-1)/√2. 대응 고윳값7,3.
- 대각 성분은 기준 좌표축의 출력 길이 제곱이다. 임의 입력은 ‖Ax‖²=xᵀAᵀAx로 조합한다.
- 111초 전단행렬 A=[[1,1],[0,1]]로 바꾸고 Gram도 [[1,1],[1,2]]로 교체한다.
- 복소 고유벡터는 수식으로 표시하며 실수 평면의 두 화살표로 표시하지 않는다.
- Gram은 양의 준정부호. 영 특이값·영공간의 기저 보완을 허용하므로 랭크 부족에서도 SVD 존재.
- 기존 92초의 발화시간을 재사용하거나 속도를 변경하지 않는다. 프레임 반올림만 최대1프레임 보정.
- 점수 129초 갱신, 동점131초, 132초 종료. 예고·회상·추가 내레이션 없음.
