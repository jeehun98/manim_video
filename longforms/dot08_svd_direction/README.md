# 내적 LEVEL 08 — SVD: 행렬의 방향별 작용

사용자 확정 원고33문장과 문장 종료 시각을 적용한147초 영상. 예제 A=[[0,−1],[3,0]], x=(2,1)을 Vᵀ→Σ→U 순서로 계산한다. 성분(2,1)을(6,1)로 조절한 뒤 위쪽6·왼쪽1을 더해 출력(−1,6)을 만든다.

세로1080×1920 및 가로1920×1080,30fps. 음원 미제공으로 무음이며 한국어 자막을 포함한다. SRT와 화면 전환별 발음 원고를 별도로 제공한다.

```powershell
python longforms/dot08_svd_direction/build.py --preview
python longforms/dot08_svd_direction/build.py
python longforms/dot08_svd_direction/check_math.py
```

Manim0.21.0, Python3.12, FFmpeg/FFprobe, Malgun Gothic. 수식과 행렬은 Text로 그려 LaTeX를 요구하지 않는다. `--scene 07 --layout shorts`로 한 씬을 다시 렌더하고 `--concat-only`로 결합할 수 있다. `--resume`는 완료된 동일 해상도·프레임 수의 씬을 재사용한다.

`manifest.json`의11개 독립 씬과 각 `spec.md`가 주장·대본·실제 길이·화면 순서를 정의한다. `timing.json`은33개 원본 발화 구간이다. 소스는 `visuals.py`, 제작과 결합은 `build.py`에 있다. 기존 에피소드용 `scripts/render.py`와 별도 실행한다.

입력과 출력의 고정 좌표평면을 분리하고 같은 단위배율로 표시한다. Σ 단계는 출력 방향을 적용하지 않은 숫자 막대다. 특이값3,1은 양수이며 왼쪽 방향은 U의 두 번째 열에서 나온다. V=I₂는 이 예제의 성질이다. 일반화 장면에서는 회전된 V′를 쓰는 다른 행렬 A′를 명시해 구별한다. PCA 관계는 행이 샘플인 중심화 데이터 행렬 X를 기준으로 설명한다. 요청 대본의 비교 이외 추가 복습·예고는 넣지 않는다.

결과: `exports/dot08_svd_direction_147s_shorts_final.mp4`, `exports/dot08_svd_direction_147s_longform_final.mp4`. 검증 자료: `qa_math.json`, `preview_report_both.json`, `render_report_both.json`.

`check_math.py`는 직교정규성·분해 복원·두 단위입력의 반응·성분과 벡터 합을 검사하고361개 입력 방향에서 직접 계산과 분해 계산을 비교한다. 회전 기저를 쓰는 별도 예제와 직사각형·계수부족 행렬의 일반식도 확인한다. `check_delivery.py`는33개 연속 구간과 SRT 종료 시각, 발음 원고, 두 최종본의147초·4,410프레임·해상도·전체 디코딩을 검사해 `qa_delivery.json`에 기록한다.
