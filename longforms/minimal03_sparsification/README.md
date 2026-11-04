# 모든 것이 필요할까? 03 — 그래프 희소화

사용자 확정 대본 36문장·종료 시각 기준 **163초(2분 43초)**. 독립 씬 15개, 세로 쇼츠와 가로 롱폼 두 배치. 음원 미제공으로 **무음**, 전체 발화 자막 내장 및 SRT 제공.

## 결과물

- `exports/minimal03_163s_shorts_final.mp4`: 1080×1920, 30fps
- `exports/minimal03_163s_longform_final.mp4`: 1920×1080, 30fps
- 같은 이름 `.srt`: 사용자 종료 시각을 그대로 적용
- `_preview.mp4`: 세로 360×640 / 가로 854×480, 15fps
- `_uncaptioned.mp4`: concat 후 자막 합성 전 중간 산출물

## 실행

프로젝트 루트, Manim 0.21.0·FFmpeg·Malgun Gothic이 설치된 Python:

```powershell
python longforms/minimal03_sparsification/data_model.py
python longforms/minimal03_sparsification/build.py --preview
python longforms/minimal03_sparsification/build.py
python longforms/minimal03_sparsification/build.py --layout shorts --scene 13
python longforms/minimal03_sparsification/verify_caption_boundaries.py --layout shorts
python longforms/minimal03_sparsification/verify_caption_boundaries.py --layout longform
```

`--layout shorts|longform|both`, `--scene 1..15`, `--jobs 3`, `--concat-only` 지원. 씬별 프레임 수 확인 → concat → 단일 ASS 자막 합성 → 최종 해상도·163초·4,890프레임 확인 순서다. 기존 에피소드용 `scripts/render.py`에 존재하지 않는 ID를 등록하지 않는다.

## 제작 자료

- `narration.md`, `master_script.md`, `tts_script.txt`: 확정 원문·구간별 발음 원고
- `narration_timing.json`, `captions.srt`: 문장 종료 시각 36개
- `manifest.json`, `scenes.yaml`, `scenes/*/{spec.md,script.txt,scene.py}`: 독립 씬 15개
- `storyboard_user.md`: 사용자 첨부 원문
- `scene_engine.py`: 두 화면비와 실제 계산값 시각화
- `data_model.py`, `math_verification.json`: 그래프·에너지·유효 저항·전칭 오차 검증
- `caption_pass.py`: concat 후 단일 자막 트랙. Manim 자막 캐시 겹침 방지
- `inspect_frames.py`: 주요 장면 20개 표본 추출
- `verify_caption_boundaries.py`: 문장 경계 직전·정각·직후와 마지막 프레임의 자막을 기준 영상과 비교
- `verification_final.json`, `caption_boundary_verification_*.json`: 최종 영상·자막 검사 결과

## 실제 사용한 그래프

1. 도입: 고정 원형 배치 32노드·96간선. 보존 가능성을 묻는 개념 화면.
2. 연결성: K8에서 경로형 신장 트리 선택. 노드 8개·간선 7개, 연결·비순환.
3. 최단거리: 단위 길이 정사각형의 상단 간선 삭제. A–B 거리 1→3.
4. 한 간선 에너지: 값1,3·가중치2에서 2×(1−3)²=8. 두 값이 같아지면 0.
5. 삼각형: 모든 원본 가중치1, 값0,1,2이면 에너지6. 차이1인 밑변을 지우고 나머지 두 가중치를1.5로 바꾸면7.5. 모든 벡터의 에너지 비율은 [0.5,1.5]. **최악 상대 오차50%의 원리 예시**로 표시한다.
6. 집단 비교: K4 두 개와 다리 하나, 총13간선. 모든 가중치1. 내부 간선의 유효 저항0.5, 다리1.0. 저항은 가중치의 역수인 전기 회로 관점이며, 중요도 점수의 예는 wR이다.
7. 후반 검증 예시: 같은8노드에서 원본28간선 → 축소8간선. **가중 완전그래프**이며 단위 가중치 K8의 예시가 아니다. 원본의 순환8간선 가중치4, 나머지20간선0.1. 축소 그래프는 순환만 남겨 각 가중치4.6. 모든 x에서 에너지 비율 [0.87358048,1.12195122], 따라서 ε=0.15를 보장한다.

## 모든 x에 대한 검증

후반 사례는 표본 대입만으로 보장했다고 하지 않는다. 순환 라플라시안을 L_C, 완전그래프 라플라시안을 L_K라 하면:

`L_G = 3.9 L_C + 0.1 L_K`, `L_H = 4.6 L_C`.

상수 벡터에는 두 에너지가 모두0이다. 상수에 직교하는 공간에서 L_K의 고윳값은8, L_C의 고윳값은 `λ_k = 2−2cos(2πk/8)`이다. 에너지 비율의 극값은 `4.6λ_k/(3.9λ_k+0.8)`의 최솟값·최댓값이며, 라플라시안 일반화 고윳값 계산과도 대조했다. 고윳값 범위가 [0.85,1.15] 안이므로 모든 실수 벡터에 대한 이차형식 부등식이 성립한다.

이것은 특정 소형 가중 그래프의 구성·검증 예시다. 모든 그래프가 같은 간선 감소율과 오차를 갖는다는 주장이 아니며, 유효 저항 표본추출 알고리즘을 직접 실행한 결과라고 하지 않는다.

## 보존 조건과 출처

스펙트럴 근사는 모든 값 배치에서의 에너지 상대 오차를 제한한다. 모든 최단거리나 모든 성질을 정확히 보존하는 것은 아니다. 에너지 계산의 가중치는 전도도이며 거리 예시의 길이와 구별한다. 무방향 간선을 한 번씩 합산하고 비음수 가중치를 사용한다.

- [Spielman–Srivastava, Graph Sparsification by Effective Resistances](https://arxiv.org/abs/0803.0929)
- [저자들의 스펙트럴 희소화 개요](https://cs-www.cs.yale.edu/homes/spielman/PAPERS/CACMsparse.pdf)

모든 발화 자막은 제공 시각에 맞췄으며 실제 음원과의 청각적 동기는 음원 수령 후 확인한다.
