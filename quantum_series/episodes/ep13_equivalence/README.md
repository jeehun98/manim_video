# EP.13 서로 다른 두 이론은 어떻게 하나가 되었을까?

최종화 · 롱폼 전용 · 221초(3분 41초) · 45문장 · 11개 독립 씬. 1920×1080, 30fps, 무음·전체 문장 자막. 사용자 문장 종료 시각이 콘티의 임시 배분보다 우선한다. 종료 타이틀도 217–221초 안에 포함하며 추가 시간을 붙이지 않는다.

`python scripts/render.py quantum13 --preview` / `python scripts/render.py quantum13`. `quantum13_longform`도 같은 가로판을 만든다. 세로판은 생성하지 않는다. 편별 `build.py --scene <ID>`로 한 씬을 교체한다. standalone/join에서도 확정 본문과 길이를 유지한다.

`script.json`은 확정 대본·시각, `direction.py`는 연출, `layouts.py`는 가로 배치, `shared/representations.py`는 실제 계산과 도형이다. `archive_manifest.json`은 과거 편의 컴포넌트 재사용과 새 요약 도식을 구분한다. EP.04 소스가 존재한다고 표시하지 않는다.

## 실제 계산

- L=1인 무한정사각우물의 정규직교 고유함수 φn(x)=√2 sin(nπx), n=1,2,3. c=(√.5,√.3,√.2)로 정규화된 상태를 만든다. 이 예시 상태는 정확히 세 성분만 포함하지만, 일반적인 기저 전개는 전체 완비 기저(필요하면 연속 스펙트럼의 적분)를 필요로 한다.
- 상태를 표현하는 함수 ψ와 계수벡터 c, 물리량을 표현하는 연산자와 행렬 A를 구분한다. 일반적으로 계수는 복소수이며 영상은 처음에 실수 예를 사용한다.
- 에너지 단위 E1=ħ²π²/(2mL²). 이 에너지 고유상태 부분공간에서 H/E1=diag(1,4,9). 함수에 작용한 Hψ와 행렬곱 Hc가 대응하고 평균 에너지는 3.50 E1이다. 그래프 세로 범위는 함수별로 적합하게 조절하며, Hψ를 정규화된 상태로 소개하지 않는다.
- U는 첫 두 기저를 π/6만큼 섞는 직교행렬(유니터리의 실수 예)이다. φ′=φU, c′=U†c, H′=U†HU를 함께 계산한다. 그림의 함수는 그대로이고 계수와 행렬은 바뀐다. 두 표현의 기대값과 에너지 고유값은 같다.
- 일반 연산자 표는 전체 행렬의 일부를 상징적으로 표시한다. 이를 이용해 유한 3×3 정준 위치·운동량 행렬이 [X,P]=iħI를 정확히 만족한다고 주장하지 않는다. 정준교환관계는 적절한 정의역을 가진 전체 연산자 관계다.
- 수소 준위는 −13.6/n² eV의 비상대론적 값이며 미세구조 등은 생략한다. 1차원 우물의 파형과 수소 파동함수를 혼동하지 않도록 별도 주석을 둔다. 힐베르트 공간 그림은 추상 공간의 개념적 투영이다.
- 1926년의 구조적 연결 발견 이후 변환 이론과 엄밀한 수학적 정식화가 발전했다는 역사적 구분을 유지한다. 첫 시리즈는 1900–1927년에 초점을 두고, 폰 노이만의 후속 작업은 이후 발전으로 다룬다.

## 참고와 재검증

- [MIT Quantum Theory I 강의 2: 기저와 연산자 행렬](https://ocw.mit.edu/courses/8-321-quantum-theory-i-fall-2017/pages/lecture-notes/)
- [MIT Quantum Physics I 강의 11: 무한정사각우물](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/lecture-notes/)
- [Schrödinger, An Undulatory Theory of the Mechanics of Atoms and Molecules (1926)](https://doi.org/10.1103/PhysRev.28.1049)
- [Dirac, On the Theory of Quantum Mechanics (1926), 원문 스캔](https://en.wikisource.org/wiki/Page:On_the_Theory_of_Quantum_Mechanics_by_Paul_Dirac_(1926).pdf/1)

`verify_physics.py`는 기저의 직교정규성, 정규화, 유한차분으로 계산한 에너지 평균과 행렬 평균의 일치, 기저변환 후 재구성·에너지 고유값·기대값을 확인한다. `verify_videos.py`는 최종 221초·6630프레임·1080p30·전체 디코딩·마지막 1초 정지를 확인한다.

검수 완료: 주요 수식·그래프·계수벡터·변환된 행렬·회고·엔딩 배치, 수치 검증, 221.000초·6630프레임·전체 디코딩과 마지막 1초 정지.
