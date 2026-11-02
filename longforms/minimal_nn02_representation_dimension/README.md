# 최소 조건 2부 · 신경망 2편 — 신경망의 진짜 차원은 몇 개일까?

사용자 제공 대본과 33개 문장 종료 시각을 그대로 적용한 **153초** 영상. 첨부 콘티 원본 제목의 03편은 보존하고, 앞서 제작한 신경망 1편 다음의 2편으로 저장했다.

- 롱폼: 1920×1080, 16:9, 60fps
- 쇼츠: 1080×1920, 9:16, 60fps
- 음원 미제공: 무음·전체 문장 자막
- 12개 독립 씬. script.txt·spec.md·timing.json·scene.py 제공
- 과거 영상 복습·다음 영상 예고 없음
- 사용자의 최신 요청에 따라 영상 내부에는 ‘개념도’, ‘원문 데이터가 아님’, ‘실제 데이터가 아닌 관측 데이터’ 같은 안내성 문구를 넣지 않는다. 대본 자막과 개념 구분용 제목·라벨은 유지한다.

## 시각화의 의미와 출처

3차원 곡선은 `ThreeDAxes.c2p(t,t²,t³)`와 `ParametricFunction`으로 계산한다. 매개변수의 미분 `(1,2t,3t²)`은 항상 영벡터가 아니므로 이 예시의 곡선은 내재 차원1이다. 출력은 학습 가중치가 아닌 뉴런 활성화값 h로 표기한다.

층별 곡선은 2019년 논문에서 보고한 증가 후 감소 경향을 정성적으로 설명하며 원문 측정 데이터의 정량 재현은 아니다. 수치 눈금·가짜 모델별 결과·임의 추정값을 넣지 않는다. 4,096은 도입 질문의 예시이며 특정 논문 결과값에 대응시키지 않는다.

직선에서 점들이 흩어지는 장면은 관측·표본 특성에 대한 설명이다. 2026년 논문의 직접 반례를 재현한 실험이 아니며, 잡음을 더한 데이터의 엄밀한 차원이1이라고 표시하지 않는다. 2026년 연구가 실제 차원의 특정 경로를 규명했거나 저차원 구조의 존재를 부정했다고 그리지 않는다. 수학적 예시와 연구 결과의 제작상 구분은 이 문서에 기록하고 화면의 안내성 자막은 생략한다.

- [Ansuini et al., NeurIPS 2019](https://papers.nips.cc/paper_files/paper/2019/hash/cfcce0621b49c983991ead4c3d4d3b6b-Abstract.html)
- [Schulte & Rügamer, AISTATS 2026](https://proceedings.mlr.press/v300/schulte26a.html)

## 실행

프로젝트 루트, Python 3.12·Manim 0.21.0·FFmpeg·Malgun Gothic:

```powershell
python longforms/minimal_nn02_representation_dimension/build.py --preview
python longforms/minimal_nn02_representation_dimension/build.py
```

`--layout longform` 또는 `--layout shorts`, `--scene 4`로 개별 씬 선택. 소스 수정 후 해당 씬을 렌더하고 `--concat-only`로 재결합한다. `--resume`은 기존 완성 씬을 재사용하며 소스 변경을 감지하지 않는다.

결과는 `exports/minimal_nn02_representation_153s_longform_final.mp4`, `exports/minimal_nn02_representation_153s_shorts_final.mp4`. 별도 SRT도 제공한다. `verification_final.json`에서 해상도·fps·재생 길이·프레임 수를 확인한다. 두 최종 파일 모두153초·9,180프레임이어야 한다. 프레임 경계의 미세 반올림만 최대0.05초 정지 패딩으로 정규화한다.

QA: `python longforms/minimal_nn02_representation_dimension/inspect_frames.py --final`.
