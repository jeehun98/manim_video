# 행렬 분해 이상형 월드컵 ③ — EVD vs SVD: 분해 구조

현재 제작본은 [153초 그래프 중심 수정본 v2](revisions/v2_153s/README.md)이다. 아래149초 자료는 이전 대본 기준으로 보존하며 새 대본의 타이밍으로 사용하지 않는다. 기본 렌더 ID는153초 수정본을 실행한다.

- ID: `evdsvd03_structure`
- 확정 길이: 149초. 사용자 문장 종료 시각 그대로 적용.
- 쇼츠 1080×1920 / 가로형 1920×1080, 30fps. 최종 각4470프레임.
- 음원 미제공: 무음·화면 자막·별도 SRT.
- 시작 점수1:1, 이번 판정 EVD, 종료 점수2:1.

## 학습 목표

EVD의 같은 고유기저와 SVD의 입력·출력 정규직교기저를 구분하고, 내적을 통해 좌표를 얻는 조건을 이해한다.

## 핵심 결론

EVD는 같은 고유기저에서, SVD는 서로 다른 두 정규직교기저 사이에서 성분별 변환을 표현한다.

## 작업 순서

1. 사용자 확정 대본과 발화 종료 시각을 보존한다.
2. `spec.md`, `scenes.yaml`, `timing.json`으로24개 독립 씬을 확정한다.
3. 두 화면비의 화면·자막을 제작하고 미리보기로 검토한다.
4. 최종 렌더·concat·프레임 수·전체 디코딩을 검증한다.

## 실행

프로젝트 루트에서:

```powershell
python longforms/evdsvd03_structure/build.py --preview
python longforms/evdsvd03_structure/build.py
python scripts/render.py evdsvd03_shorts
python scripts/render.py evdsvd03_longform
python longforms/evdsvd03_structure/build.py --layout longform --scene 11
```

Manim0.21.0, FFmpeg, Malgun Gothic. 공통 타이포그래피·행렬 헬퍼는 이전 월드컵 소스를 재사용한다.
`--jobs` 기본2. `--concat-only`는 기존 씬으로 합본만 갱신한다.
결과는 `exports/evdsvd03_structure_149s_{shorts,longform}_final.mp4` 및 SRT.

## 정확성

- EVD 예시 A_E=[[2,1],[0,1]], P=[[1,1],[0,-1]], D=diag(2,1). 이 예시에서는 P⁻¹=P지만 일반적인 성질은 아니다.
- x=(2,-1), P⁻¹x=(1,1), D좌표=(2,1), Ax=(3,-1). Pᵀx=(2,3)은 고유기저 좌표와 다르다.
- 좌표 변경 구간에서는 실제 벡터를 움직이지 않는다. D단계는 실제 변환이므로 벡터가 변한다.
- 음의 고윳값의 방향 반전은 별도 일반 예시로만 언급. 본 예시의 고윳값은2,1로 양수.
- SVD 예시 A_S=[[0,-1],[3,0]], V=I, Σ=diag(3,1), U=90도 회전. 실제 입력·출력 좌표를 같은 길이 척도로 표시.
- v1=(1,0)→Av1=(0,3), u1=(0,1)는 단위벡터, σ1=3. v2=(0,1)→u2=(-1,0).
- 임의 단위벡터의 Ax 크기·방향 분해는 이 가역 예시에서 Ax≠0이므로 유효.
- x=(2,1)에 대해 Vᵀx=(2,1), Σ좌표=(6,1), 출력(-1,6). 좌표 추출과 최종 출력을 구분한다.
- EVD의 일반 벡터를 읽는 V는 화면 pᵢ로 표시해 SVD의 vᵢ와 혼동을 줄인다.
- 취향 판정의 기준은 하나의 기저라는 구조적 간결성. 계산 효율·일반적 수학 우열을 주장하지 않는다.
