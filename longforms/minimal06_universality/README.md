# 06 재규격화와 보편성 — 다른 구조에서 같은 법칙이 남는 이유

확정 대본 160초·33개 문장 종료 시각. 독립 씬 14개를 세로9:16·가로16:9로 각각 렌더한다. 음원 미제공으로 자막 포함 무음 영상과 TTS 원고를 제공한다.

## 실제 계산과 개념 도식

- 실제 데이터: 16×16 주기 경계 2D 최근접 Ising 모형, h=0, J=kB=1. 고정 시드606의 Wolff 단일 군집 Monte Carlo. 온도별1600회 군집 갱신 후64개 표본, 표본 사이30회 갱신. 저온1.4, 고온4, 임계온도2/log(1+√2). MC 갱신은 평형 표본 생성이며 물리적인 실시간 동역학은 아니다.
- 임계 배열은 독립 난수 배열이 아니다. 혼합된 상관 패턴이 읽히는 평형 표본을 골라 보여준다. 유한 격자 설명용 표본으로 임계 지수를 측정하지 않는다.
- 블록화: 실제 표본에서16→8→4→2. 2×2 합의 부호로 대표 방향을 정하고, 합0은 ±1 각각1/2 확률의 추첨(시드1608). 모든 단계의 재현을 검증한다.
- 유효 상호작용: K, K′, K″는 척도에 따른 이론의 변화를 뜻하는 도식이다. 블록 표본에서 실제 유효 Hamiltonian이나 결합계수를 추정한 결과가 아니다. 일반적으로 먼 이웃·다체 상호작용 등도 생길 수 있다.
- RG 흐름: 고정점 근방의 설명용 선형 좌표(r,g)→(2r,g/2). r=0 임계면 위 두 점은 같은 고정점으로 접근하고, r≠0의 회색 점은 멀어진다. 이 승수들은 Ising 고유값의 측정값이 아니다.
- 초기 유체/자석의 공통 법칙은 같은 보편성 부류라는 조건 아래의 이야기다. 이후2D Ising 격자는 블록화 설명 모형이며 실제3D 유체나 자석의 수치 임계 지수를 대표하지 않는다. 그래프의 거듭제곱 곡선은 설명용이며 측정 데이터가 아니다. β의 수치는 영상에 표시하지 않는다.
- 유체의 임계점은 온도와 압력을 함께 조절하는 조건으로 표시한다. 같은 임계 지수와 물질별 비보편적 진폭·세부 특성은 구분한다. 정적 임계 보편성을 설명하며 동역학 보편성은 다루지 않는다.

## 재현

```powershell
python longforms/minimal06_universality/data_model.py
python longforms/minimal06_universality/build.py --preview
python longforms/minimal06_universality/build.py
python longforms/minimal06_universality/verify_caption_boundaries.py --layout shorts
python longforms/minimal06_universality/verify_caption_boundaries.py --layout longform
```

Python3.12·Manim0.21·FFmpeg/FFprobe·Malgun Gothic. 수식은 LaTeX 없이 Text로 표시한다. simulation_data.npz, simulation_report.json은 계산 데이터와 조건, math_verification.json은 블록화·동률·흐름 검증이다.

최종 파일: exports/minimal06_160s_shorts_final.mp4 (1080×1920), exports/minimal06_160s_longform_final.mp4 (1920×1080). 각각160초·30fps. 미리보기 _preview.mp4. concat 후 단일 ASS 트랙으로 서술 자막을 합성하여 문장 전환 중복을 방지한다.

## 참고

- [David Tong, Cambridge: The Renormalisation Group](https://www.damtp.cam.ac.uk/user/tong/sft/sfthtml/S3.html): 고정점·관련/무관 방향·보편성과 유체/자석의 관계.
- [Cornell, Sethna: Statistical Mechanics](https://sethna.lassp.cornell.edu/StatMech/EntropyOrderParametersComplexity20.pdf): Ising의 임계온도와 Wolff 군집 갱신.
- [Nobel Prize: Wilson의 임계현상 이론](https://www.nobelprize.org/prizes/themes/the-nobel-prize-in-physics-1901-2000/): 재규격화와 임계현상의 맥락.

## 완료 상태

세로·가로 최종본 및 미리보기 완료. 길이·프레임 수·전체 디코딩, 총198프레임 자막 경계, 주요 화면 검토 통과. verification_final.json, math_verification.json, production_notes.md에 결과 기록.
