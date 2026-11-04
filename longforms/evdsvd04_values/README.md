# 행렬 분해 이상형 월드컵 ④ — EVD vs SVD: 고윳값과 특이값

- ID: `evdsvd04_values`
- 확정 길이:103초. 마지막 두 문장 종료 시각은 사용자가 대화에서101초·103초로 직접 확인.
- 17개 독립 씬. 쇼츠1080×1920 / 가로형1920×1080,30fps. 최종3090프레임.
- 시작2:1 → 이번 SVD승 → 종료2:2. 음원 미제공,무음·화면자막·별도SRT.

## 학습 목표

하나의 전단행렬에서 고윳값1,1과 특이값sqrt2±1이 서로 어떤 정보를 나타내는지 그래프로 이해한다.

## 핵심 결론

고윳값은 고유방향의 배율이고, 특이값은 특별한 단위 입력 방향에서의 길이 배율이다. 한 번의 변환의 길이 변화를 보는 기준에서는 SVD승.

## 작업 순서

1. 사용자 원문과 확정 시각을 보존한다. 마지막시각은end_times.json.
2.17개spec과타임라인을 확정하고 같은행렬의 수학을 검증한다.
3.두화면비 미리보기와최종렌더를 만들고 전체디코딩·프레임수를 검증한다.

## 실행

프로젝트 루트에서:

```powershell
python longforms/evdsvd04_values/build.py --preview
python longforms/evdsvd04_values/build.py --resume
python scripts/render.py evdsvd04_shorts
python scripts/render.py evdsvd04_longform
python longforms/evdsvd04_values/build.py --layout longform --scene 11
```

Manim0.21.0, FFmpeg,Malgun Gothic.`--jobs`기본2, `--resume`은프레임수검증후기존씬재사용, `--concat-only`는합본만갱신.
출력:`exports/evdsvd04_values_103s_{shorts,longform}_final.mp4`및SRT.

## 수학·시각 기준

- 전체에서 A=[[1,2],[0,1]] 하나만 사용. 점과도형의모든중간프레임은[[1,2t],[0,1]]로계산.
- 고윳값1의중복도2지만고유공간은수평1차원. 두독립고유방향으로표현하지않음.
- 수직입력(0,1)은(2,1)로변환. 방향과길이모두변화.
- 특이값1+sqrt2와sqrt2-1. 입력67.5/-22.5도,출력22.5/-67.5도. 각도는내부데이터만사용.
- 원·타원비교에서도동일척도. 반축길이에숫자연결,전체축길이나비율과장없음.
- 시간역행91/93은추정사용하지않고사용자가확인한101/103으로수정. project.json의ending_confirmed가false면최종합본금지.
