# EP.03 · 러더퍼드의 금박 실험과 원자핵의 발견

사용자 확정 **20문장·105초**, 전체 문장 자막. 세로 1080×1920 / 가로 1920×1080을 별도 배치하여 30fps로 제작한다. 음원 미제공으로 무음이다.

## 소스와 제작 순서

`script.json`이 대본·문장 시각의 원본이다. `narration.md`, `tts_script.txt`, `brief.md`와 6개 씬의 `spec.md`를 먼저 작성하고 화면을 제작한다. `longforms/_template/`의 씬 규격을 따르며, 사용자가 정한 타이밍으로 길이를 확정했다. 씬은 각각 `scene.py`, `spec.md`, `script.txt`와 독립 MP4를 갖는다.

- 0–16초: 실험 결과와 질문. 원자 내부는 숨긴다.
- 16–40초: 중성, 전자 발견, 톰슨 모형, 작은 산란 예상.
- 40–51초: 가이거·마즈든 실험과 큰 산란.
- 51–77초: 양전하 집중, 쿨롱 반발력, 접근 거리에 따른 서로 다른 궤적.
- 77–91초: 1911년 원자핵 모형과 핵의 작은 크기.
- 91–105초: 핵과 전자의 인력, 고전적 모형의 안정성 문제와 질문.

`direction.py`는 애니메이션, `layouts.py`는 화면비별 위치·크기, `shared/rutherford.py`는 시각 요소, `shared/coulomb.py`는 물리 계산이다. 9:16을 늘리거나 가로 영상을 잘라서 다른 비율을 만들지 않는다.

## 실행

```powershell
python scripts/render.py quantum03 --preview
python scripts/render.py quantum03
python scripts/render.py quantum03_shorts
python scripts/render.py quantum03_longform
```

직접 실행: `python quantum_series/episodes/ep03_rutherford/build.py --layout both`.
한 씬만 다시 렌더: `--scene 04_coulomb --layout shorts` (같은 품질·종료 모드의 나머지 씬이 있어야 한다).

기본 종료 모드는 쇼츠 standalone, 가로 join이다. `--ending standalone` / `--ending join`으로 바꿀 수 있으며 두 모드 모두 105초 대본을 그대로 유지한다. 마지막 104–105초는 정지한다. standalone은 궤적을 약간 낮추고, join은 밝기를 유지한다. 예고·별도 엔드카드는 없다.

최종 출력: `exports/quantum03_shorts.mp4`, `exports/quantum03_longform.mp4`.
미리보기는 `_preview.mp4`. 최종 엔딩 프레임은 `exports/quantum03_shorts_ending.png`, `exports/quantum03_longform_ending.png`에 따로 저장한다. EP.04를 제작한 상태로 표시하지 않는다.

각 씬의 프레임 수와 최종 **3150프레임·105초·30fps·해상도**를 빌드에서 검사한다. 중간 영상·로그는 `media/quantum03/` 아래에 있다.

## 물리 모형과 한계

입자 질량을 1로 정규화하고, 양전하의 전체 세기를 κ=0.12, 초기 총에너지를 E=0.5로 고정한다. 양전하가 반지름 R=1.8의 균일한 구에 퍼진 경우와 중심의 점 전하인 경우를 비교한다. 좌표와 시간은 설명용 무차원 값이다.

- 점 전하의 가속도: `a = κ r / |r|³`, 퍼진 구 내부: `a = κ r / R³`. 구 외부의 식과 전체 양전하량은 같다.
- 퍼진 구 내부의 퍼텐셜: `V = κ[3 − (r/R)²]/(2R)`, 구 외부와 점 전하: `V = κ/r`. 같은 총에너지를 갖도록 초기 속도를 정한다.
- 4차 Runge–Kutta, dt=0.008로 궤적을 미리 계산한다. Manim에서는 같은 시간 간격의 위치를 보간하여 재생한다. 가까운 통과에서 속도가 변하고 방향이 부드럽게 바뀌며 표면에 부딪혀 반사되지 않는다.
- 에너지·각운동량 보존, 해석적 러더퍼드 산란각과의 비교, 양·음 충돌 매개변수의 대칭, 가까운 경로와 먼 경로의 산란각 관계를 검사한다.
- 핵은 고정하며 반동, 전자의 차폐, 원자 전체의 중성장, 다중 산란, 물질 내 에너지 손실은 생략한다. 톰슨 모형에서는 양전하 분포만 비교한 것이며, 완전한 산란 이론을 재현한 그림이 아니다.
- 경로는 대표 사례를 선택한 개념도다. 화면의 입자 개수로 실제 산란 빈도를 주장하지 않는다. 원자·핵·알파 입자의 크기는 서로 실제 축척이 아니다.
- 금색 이동 점은 알파 입자, 붉은 점은 핵, 청록색 점은 전자다. 예상은 회색 점선, 대표 관측·설명 경로는 청록색 실선으로 고정한다. 금색 화살표는 힘의 방향을 나타내는 기호이며 힘의 크기를 정량적으로 표현하지 않는다.
- 러더퍼드 모형의 전자는 정지한 기호로 두고 안정된 원형 궤도·에너지 준위·오비탈을 그리지 않는다.
- 100–105초의 나선은 **고전적인 복사하는 궤도 모형을 가정했을 때 생기는 문제의 상징**이다. 실제 전자의 궤도가 아니며 복사 손실 방정식을 적분한 결과도 아니다. 핵과 충돌하기 전에 정지한다. 화면에도 이 범위를 표시한다.

역사·물리 출처: [러더퍼드의 1911년 원문](https://personal.math.ubc.ca/~cass/rutherford/rutherford.html), [AIP 원자핵 발견 자료](https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html), [Rutgers 러더퍼드 산란 강의](https://www.physics.rutgers.edu/~shapiro/507/book4_2.pdf).
