# SVD 5편 — 사라진 정보는 복원할 수 있을까?

사용자 확정 대본의 52개 문장 종료 시각을 그대로 사용한 251초(4분 11초) 가로 영상. 28개 독립 씬이며 씬 하나만 교체해 다시 결합할 수 있다. 제공 콘티는 storyboard_source.md, 대본은 narration.md와 master_script.md, 발음 원고는 tts_script.txt에 있다.

## 내용과 정확성

- Null Space는 원점을 지나는 ker(A), 같은 출력을 만드는 해 집합은 x₀+ker(A)로 구분한다. 예시는 A=diag(1,0), 출력(1,0), 입력(1,t).
- 58–85초는 실제 ThreeDScene의 타원체·채워진 원판·선분이다. 세계 좌표에서 세 축을 변화시키며 정확히 0인 상태에서만 Rank가 줄어든다.
- 의사역행렬은 최소 노름 최소제곱해를 선택한다. 117초부터 별도 관측(1,0.3)을 사용해 최소 잔차0.3과 최소 노름(1,0)을 구분한다.
- 6개 랭크1 성분의 특잇값은(8,4,2,1,0.5,0.2). 3개를 남긴 제곱오차는1.29.
- 동일한 회색조 이미지(192×160)에 실제 NumPy SVD를 계산해 Rank1→2→5→10을 보여준다. 재사용한 소재는 xai01_cat_mystery/assets/cat_photo.png로, 사진 스타일 생성 이미지다. 촬영 사진으로 소개하지 않는다. 해당 폴더 generation.md에 제작 기록이 있다.
- 이미지 표시만 밝기를[0,1]로 제한한다. 랭크와 오차는 표시 전 실수 행렬에서 계산한다. 블러를 사용하지 않는다.
- 동일 Rank2 비교는 별도 σ=(8,4,2) 예시다. 8·4 유지의 제곱오차4와8·2 유지의16을 비교한다. 최적성은 Frobenius norm 기준이며 모든 의미적 목적의 최적성을 뜻하지 않는다.
- 작은 표식은 별도 설계한16×16 테스트 영상이다. 일정한 배경에 행·열 합이0인2×2 표식을 더해 두 성분을 직교시킨다. 특잇값은8과0.3. 최적 Rank1에서 표식 점수0.15→0, 제곱오차0.09, 상대 Frobenius 오차약3.75%를 실제 계산으로 검증한다. 사진 속 임의 특징이 사라진다고 주장하지 않는다.
- 마지막2초에는 SVD의 전체 질문을 유지한다. 사용자 제공 최종 통합 대본을 그대로 사용한다.

## 재현

```powershell
python longforms/svd05_lost_information/prepare.py
python longforms/svd05_lost_information/prepare_assets.py
python longforms/svd05_lost_information/build.py --preview
python longforms/svd05_lost_information/build.py
```

씬만 교체: `python longforms/svd05_lost_information/build.py --scene 14` 후 `--concat-only`. 여러 씬은 `--scenes 14 15`로 지정한다. 최종에서 미리보기 동기화는 sync_preview.py.

최종 출력은 exports/svd05_lost_information_251s_1080p30.mp4와 SRT. 1920×1080,30fps,7530프레임. 미리보기854×480,15fps,3765프레임. 음원이 제공되지 않아 영상은 무음이며 화면 자막이 포함된다. 임의 발화시간 추정이나 사후 속도 변경 없이 사용자 시간을 적용한다.

수치 검증: assets/numerical_checks.json. 화면 검수: qa/. Manim0.21.0, FFmpeg9.0.1, PyAV, NumPy, Malgun Gothic을 사용한다.

## 최종 검증

2026-10-22: 최종본 전체7530프레임을 디코딩해 251초·1080p·30fps와 시각의 단조 증가를 확인했다. 52개 문장 구간과28개 씬이 연속하며, 최종 영상32개 시점의 화면·수식·자막을 검수했다. 미리보기는 최종 씬에서 동기화했으며251초·854×480·15fps·3765프레임이다.

수치 검사는 이미지 SVD의 꼬리 제곱합, Rank3 오차1.29, 같은Rank2 비교의4와16, 치역 밖 관측의 최소제곱해, 검증 표식의 실제 소실을 확인한다. 기록은 [qa/report.json](qa/report.json), 화면은 [1](qa/final_part_1.jpg) · [2](qa/final_part_2.jpg) · [3](qa/final_part_3.jpg) · [4](qa/final_part_4.jpg)에 있다.

## 1–5편 통합

`python longforms/svd05_lost_information/combine_series.py`로 각 편의 확정 길이133·154·152·176·251초를 유지해 결합한다. 출력은 exports/svd_longform_866s_1080p30.mp4와 통합SRT. 14분26초,25980프레임의 무음 시각화 마스터이며 기존 음성 결합본을 덮어쓰지 않는다. 각 편의 시작은0:00,2:13,4:47,7:19,10:15다. 검증 결과는 qa/combined_report.json에 기록한다.
