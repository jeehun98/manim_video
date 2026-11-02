# 최소 조건 2부 · 신경망 3편 — IMPACT

**신경망의 차원을 줄여도 성능을 유지할 수 있을까?** 사용자 확정 대본32문장·156초. 공유 콘티의04편을 앞선 신경망1·2편 다음의3편으로 저장했다.

- 롱폼1920×1080, 쇼츠1080×1920, 모두60fps
- 음원 미제공: 무음·전체 문장 자막 및 별도SRT
- 독립 교체 가능한9개 씬의spec.md·script.txt·scene.py
- 사용자 대본의7–16초 연결 구간은 그대로 적용한다. 추가 복습·후속편 번호·예고 문구는 넣지 않는다.
- 기존 사용자 요청대로 도식이나 관측 데이터의 성격을 알리는 별도 안내 자막은 넣지 않는다. 아래에 제작 방식을 기록한다.

## 구현과 정확성

8×8의 W를SVD로8×3·3×8 또는8×2·2×8로 근사한다. 셀 개수와 파라미터 수는64→48→32로 실제 일치한다. 저장량 감소 조건은r(m+n)<mn이다. 두 행렬로 분리하는 것만으로 항상 저장량이 감소한다고 표현하지 않는다.

`demonstration_data.npz`는 고정 난수로 생성한8×8 행렬,96개 입력,실제 계산한활성화Y=XWᵀ,특이값,분해행렬이다. 가중치와 활성화의 막대는 이 수학적 사례의 실제 특이값이며 LLM 실험의 재현이 아니다.

오차 방향 예시는h=(.3,.2),ε1=(0,.75),ε2=(-.75,0)이다. 두 오차의 길이는.75로 같고 x좌표 부호에 따른 분류 결과는A→A와A→B로 다르다. 기울기g=(-1,0)의 내적은0과.75이다. ΔL≈g·ε는 국소1차 근사에 대한 직관 설명으로, IMPACT의 전체 목적함수를 그대로 나타내지 않는다.

기능 보존 비교에는 같은rank2에서 전역Frobenius 오차가 작은SVD 근사와 첫 출력행을 정확히 유지하는 근사를 계산한다. 제작용 분류기f(x)=sign((Wx)₁)에서는 후자가 분류를 보존한다. 이 사례는 IMPACT 전체 알고리즘의 재현이 아니다. IMPACT 자체는 활성화 구조와 기울기 기반 중요도에서 중요도 가중 공분산과 복원 기저를 구성하는 흐름으로 설명한다. 랭크를 줄였다 복구하는 탐색으로 표시하지 않는다.

결과 구간의55.4%만ACL2026 최종 논문에서 보고한 수치다. 비교 방법 대비 최대 더 큰 모델 크기 감소를 뜻하며 원본 전체의55.4% 제거율이나55.4%p가 아니다. 가짜 모델별 정확도·성능 곡선은 넣지 않는다. 끝의 서로 다른 층 폭은 가능성을 묻는 시각화이며 실제 특정 모델의 계층별 압축률이 아니다.

계산 기록: `math_verification.json`. 영상 검사: `verification_final.json`. 최종 두 영상은156초·9,360프레임이어야 한다.

## 실행

프로젝트 루트에서Python3.12·Manim0.21.0·FFmpeg·Malgun Gothic:

```powershell
python longforms/minimal_nn03_impact/build.py --preview
python longforms/minimal_nn03_impact/build.py
```

`--layout longform`/`--layout shorts`, `--scene 2`로 개별 씬 선택. 수정 씬 재렌더 후 `--concat-only`로 결합한다. `--resume`은 기존 영상을 재사용하며 소스 변경을 감지하지 않는다. 프레임 반올림만 최대0.05초 정지 패딩으로 정규화하며 발화 구간은 바꾸지 않는다.

결과: `exports/minimal_nn03_impact_156s_longform_final.mp4`, `exports/minimal_nn03_impact_156s_shorts_final.mp4`.

QA: `python longforms/minimal_nn03_impact/inspect_frames.py --final`.

## 출처

- [공유 콘티](https://chatgpt.com/s/t_6ae8122ed2008191a469909546d5410a)
- [Chowdhury et al., IMPACT, ACL2026 최종본](https://aclanthology.org/2026.acl-long.183/)
- [논문PDF](https://aclanthology.org/2026.acl-long.183.pdf)

2025년초기arXiv초록의48.6%가 아닌 사용자 대본과 일치하는2026년최종판55.4%를 기준으로 한다.
