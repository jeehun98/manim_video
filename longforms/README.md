# 롱폼 제작 규격

- [양자역학의 발견 1–13편 통합 롱폼](quantum_full_01_13/README.md): 사용자 지정 음성 포함 `quantum_long_1~13.mp4` 합본. 33분 27.100초, 1080p30, MP4 챕터와 유튜브 설명 포함. `python longforms/quantum_full_01_13/build.py`.

- [GPU 개론 07 — 회로는 언제 값을 갱신할까?](gpui07_clock_timing/README.md): 확정135초·31문장·14씬, 가로/세로1080p30, 무음·전체 자막. `python longforms/gpui07_clock_timing/build.py --preview` / `python longforms/gpui07_clock_timing/build.py`.

- [GPU 개론 06 — 논리 게이트는 어떻게 값을 기억할까?](gpui06_sr_latch/README.md): 확정140초·29문장·14씬, 가로/세로1080p30, 무음·전체 자막. `python longforms/gpui06_sr_latch/build.py --preview` / `python longforms/gpui06_sr_latch/build.py`.

- [GPU 개론 1~5편 통합 롱폼](gpui_full_01_05/README.md): 사용자 지정 음성 포함 gpui_1~5_long.mp4 합본. 12분 31.633초, 1080p30, MP4 챕터와 유튜브 설명 포함. `python longforms/gpui_full_01_05/build.py`.

- [GPU 개론 05 — 하나의 회로로 여러 연산을 수행하는 방법](gpui05_alu_reuse/README.md): 확정 175초·35문장·16씬, 가로/세로 1080p30, 무음·전체 자막. `python longforms/gpui05_alu_reuse/build.py --preview` / `python longforms/gpui05_alu_reuse/build.py`.

- [GPU 개론 04 — 논리 게이트는 어떻게 숫자를 더할까?](gpui04_binary_adder/README.md): 확정 143초·35문장·15씬, 가로/세로 1080p30, 무음·전체 자막. `python longforms/gpui04_binary_adder/build.py --preview` / `python longforms/gpui04_binary_adder/build.py`.

## GPU 개론

- [03 — 스위치의 연결이 어떻게 논리 연산이 될까?](gpui03_logic_connections/README.md): 사용자 제공 34문장·164초, 독립 씬 14개. CMOS NAND 네 입력과 NAND-only NOT·AND·OR·XOR netlist 검증. 직렬·병렬·출력 전압·기능적 완전성·물리 비용을 구별한다. 가로·세로 1080p30fps·무음·전체 자막. `python longforms/gpui03_logic_connections/build.py --preview` / `python longforms/gpui03_logic_connections/build.py`.

- [02 — 트랜지스터는 어떻게 전기 신호를 제어할까?](gpui02_transistor/README.md): 사용자 제공 28문장·142초, 독립 씬 10개. 입력 제어와 전류 경로를 분리하고 n채널 MOSFET의 전기장·전도 채널, 상보적 CMOS 인버터와 출력 전압을 설명한다. 가로·세로 1080p30fps·무음·전체 자막. `python longforms/gpui02_transistor/build.py --preview` / `python longforms/gpui02_transistor/build.py`.

- [01 — 컴퓨터는 왜 0과 1을 사용할까?](gpui01_binary_signals/README.md): 사용자 제공 26문장 종료 시각 기준 113초, 독립 씬 8개, 가로·세로 두 버전. 전압을 이용한 정보 표현에서 잡음·판정 경계·두 상태·조합 확장·Bit까지 이어지는 실험. 가로 1920×1080 / 세로 1080×1920, 30fps. 무음·전체 문장 자막. `python longforms/gpui01_binary_signals/build.py --preview` / `python longforms/gpui01_binary_signals/build.py`.

이 문서는 다른 컴퓨터나 새 Codex 세션에서도 같은 방식으로 롱폼을 이어 만들기 위한 최소 규격이다. 새 프로젝트는 `_template/`을 복사해 `longforms/<ID>_<slug>/`로 만든다.

## 핵심 원칙

- **씬 하나 = 주장 하나 = 독립적으로 교체 가능한 완성 영상**으로 만든다.
- 12~18분 영상은 보통 20~40초짜리 씬 30~40개로 나눈다. 실제 TTS 길이를 우선한다.
- 제작 순서는 `전체 대본 → Scene Specification → 씬별 TTS → TTS 길이 확정 → Manim 화면 → 씬별 mux → 최종 concat`이다.
- 롱폼 화면은 잦은 교체보다 한 대상을 `등장 → 관찰 → 변화 → 해석`하는 흐름을 우선한다.
- 한 씬을 수정할 때 다른 씬을 다시 렌더하지 않아도 되어야 한다.

## 최소 구조

```text
longforms/<ID>_<slug>/
├─ README.md                 # 제목, 목표, 실행법, 현재 상태
├─ master_script.md          # 전체 내레이션과 논리 흐름
├─ scenes.yaml               # 씬 순서와 파일·클래스·길이 인덱스
├─ scenes/
│  ├─ 01_hook/
│  │  ├─ spec.md             # 목적, 주장, 화면, 타임라인, 연결
│  │  ├─ script.txt          # TTS에 직접 넣는 문장
│  │  ├─ scene.py            # Manim 장면
│  │  ├─ narration.mp3       # 생성물, Git 제외
│  │  ├─ visual.mp4          # 무음 렌더, Git 제외
│  │  └─ final.mp4           # 음성 결합본, Git 제외
│  └─ 02_.../
├─ concat.txt                # 최종 결합 순서
├─ captions.srt
└─ longform_final.mp4        # 생성물, Git 제외
```

아직 음성과 영상이 없는 초기 단계에서는 `README.md`, `master_script.md`, `scenes.yaml`, 각 씬의 `spec.md`와 `script.txt`만 있어도 된다.

## 작업 계약

1. `master_script.md`에서 전체 주장과 순서를 먼저 확정한다.
2. 각 씬에 주장 하나만 배정하고 `spec.md`를 작성한다.
3. `script.txt`로 TTS를 생성한 뒤 실제 음성 길이를 잰다.
4. 측정한 길이를 `scenes.yaml`의 `duration_seconds`에 기록한다.
5. `scene.py`의 애니메이션을 그 길이에 맞춘다. 임의 정지 프레임이나 사후 속도 변경은 예외로 둔다.
6. 씬별 무음 영상과 음성을 mux하여 `final.mp4`를 만든다.
7. 모든 씬의 해상도, fps, 코덱, 오디오 형식을 통일한 뒤 순서대로 concat한다.
8. 수정 시 해당 씬만 다시 TTS·렌더·mux하고 최종 concat만 갱신한다.

## Scene Specification 필수 항목

각 `spec.md`에는 다음을 반드시 적는다.

- 목적과 핵심 주장
- 앞 장면에서 받은 내용
- TTS 원문과 확정 길이
- 화면 구성과 시간대별 애니메이션
- 화면 텍스트
- 시작 상태와 종료 상태
- 다음 장면으로 넘길 질문 또는 시각적 연결
- 수학적 조건, 과장 방지 문구, 출처가 필요한 주장

씬 템플릿은 [`_template/scenes/01_example/spec.md`](_template/scenes/01_example/spec.md), 전체 인덱스 예시는 [`_template/scenes.yaml`](_template/scenes.yaml)을 사용한다.

## 구현 시 주의

- 해상도와 화면비는 프로젝트마다 `scenes.yaml`에 명시한다. 기존 세로형 숏폼 설정을 롱폼에 무조건 재사용하지 않는다.
- 화면의 숫자·수식·영문 표기는 원문 그대로 두고, 한국어 발음용 변형은 `script.txt` 또는 별도 TTS 파일에서만 관리한다.
- TTS 대본은 화면 전환 구간마다 문단을 나눈다. 각 구간 사이에 빈 줄을 넣고, 읽지 않을 제목이나 타임코드는 통합 `tts_script.txt`에 넣지 않는다. 사용자 제공 문장별 종료 시각이 있으면 추정 배분 대신 해당 시각을 적용한다.
- `narration.mp3`, 씬별 MP4, 최종 MP4는 생성물이며 Git에 커밋하지 않는다.
- 렌더·mux·concat 자동화 스크립트가 추가되면 프로젝트 `README.md`에 정확한 실행 명령과 필요한 도구 버전을 기록한다.
- 현재 저장소의 `scripts/render.py`는 기존 에피소드용이다. 롱폼 지원이 구현되기 전에는 롱폼을 자동으로 처리한다고 가정하지 않는다.

## SVD 관측 실험

- [1막 — 서로 다른 입력을 행렬은 구별할 수 있을까?](svd01_distinguish_inputs/README.md): 사용자 문장 종료 시각 기준 133초. 16개 독립 씬을 결합하는 가로형 영상. 실행: `python longforms/svd01_distinguish_inputs/build.py --preview` 또는 `python longforms/svd01_distinguish_inputs/build.py`.
- [이전 전체 초안](svd_information_map/README.md): 관점 전환 전 5막·15씬 자료. 현재 1막 제작본과 구분한다.
- [2막 — 행렬이 가장 잘 구별하는 방향은 어디일까?](svd02_direction_map/README.md): 사용자 문장 종료 시각 기준154초, 독립 씬20개. 실행: `python longforms/svd02_direction_map/build.py --preview` 또는 `python longforms/svd02_direction_map/build.py`.
- [3막 — 행렬은 하나의 입력을 어떻게 읽어낼까?](svd03_read_and_reassemble/README.md): 사용자 문장 종료 시각 기준152초, 독립 씬23개. 실행: `python longforms/svd03_read_and_reassemble/build.py --preview` 또는 `python longforms/svd03_read_and_reassemble/build.py`.
- [4편 — 출력에 남은 정보를 되돌리면 왜 오차가 커질까?](svd04_inverse_sensitivity/README.md): 사용자 문장 종료 시각 기준176초, 독립 씬20개. 실행: `python longforms/svd04_inverse_sensitivity/build.py --preview` 또는 `python longforms/svd04_inverse_sensitivity/build.py`.
- [5편 — 사라진 정보는 복원할 수 있을까?](svd05_lost_information/README.md): 사용자 문장 종료 시각 기준251초, 독립 씬28개. 실제3D 차원 소실과 계산된 이미지 SVD. 실행: `python longforms/svd05_lost_information/build.py --preview` 또는 `python longforms/svd05_lost_information/build.py`. 1–5편 무음 통합본은 `python longforms/svd05_lost_information/combine_series.py`로 결합한다(866초).

## 고윳값과 고유벡터

- [1막 — 행렬을 계속 곱하면 왜 특정 방향만 남을까?](eigen01_dominant_direction/README.md): 사용자 콘티 기준 119초, 14개 독립 씬. 세로 쇼츠·가로 롱폼 두 버전. `python longforms/eigen01_dominant_direction/build.py --preview` 또는 `python longforms/eigen01_dominant_direction/build.py`. TTS 음원 미제공으로 무음 제작.

- [2막 — 숫자가 다른 두 행렬이 같은 변환일 수 있을까?](eigen02_same_map/README.md): 사용자 문장별 종료 시각27개 기준120초, 13개 독립 씬. 세로 쇼츠·가로 롱폼 및 핵심 자막. `python longforms/eigen02_same_map/build.py --preview` / `python longforms/eigen02_same_map/build.py`, 자막은 `python longforms/eigen02_same_map/add_captions.py`. 음원 미제공으로 무음 제작.

- [3막 — 행렬의 숫자가 바뀌어도 변하지 않는 것은?](eigen03_invariants/README.md): 사용자 문장 종료 시각27개 기준121초, 14개 독립 씬. 연속 기저 변경·불변량·항등/전단 반례. `python longforms/eigen03_invariants/build.py --preview` / `python longforms/eigen03_invariants/build.py`, 핵심 자막은 `python longforms/eigen03_invariants/add_captions.py`. 세로 쇼츠·가로 롱폼 무음 제작.

- [4막 — 행렬의 성분이 서로 섞이지 않는 좌표계가 있을까?](eigen04_no_mixing/README.md): 사용자 문장 종료 시각27개 기준115초, 15개 독립 씬. 첫 고유축과 두 고유축의 차이, 비대각 원소 제거, P⁻¹→D→P. `python longforms/eigen04_no_mixing/build.py --preview` / `python longforms/eigen04_no_mixing/build.py`, 자막은 `python longforms/eigen04_no_mixing/add_captions.py`. 세로·가로 무음 영상.

- [5막 — 고윳값 간격: PCA의 주성분 방향이 불안정해지는 이유](eigen05_eigengap/README.md): 사용자 문장 종료 시각30개 기준146초, 19개 독립 씬. 같은 제어점4개·같은 공분산 교란에서 PC1 회전0.57°/31.72°를 실제 계산. `python longforms/eigen05_eigengap/build.py --preview` / `python longforms/eigen05_eigengap/build.py`, 핵심 자막은 `python longforms/eigen05_eigengap/add_captions.py`. 세로·가로 무음 영상.

## 행렬분해 이상형 월드컵

- [01 — EVD vs SVD: 이름](evdsvd01_names/README.md): 사용자 확정 52초, 11개 독립 씬. 9:16 쇼츠와 16:9 가로형. 실행: python longforms/evdsvd01_names/build.py (--preview 미리보기). 음원 미제공, 무음·자막 영상.


- [월드컵 02 — EVD vs SVD: 분해 조건](evdsvd02_conditions/README.md): 사용자 콘티 기준 92초, 18개 독립 씬, 세로·가로. 실행: python longforms/evdsvd02_conditions/build.py (--preview 미리보기). 마지막 종료 시각은 첨부 콘티 명시에 따라 91/92초 적용.


- [월드컵 02 — 분해 조건, 132초 수정본 v2](evdsvd02_conditions/revisions/v2_132s/README.md): 23개 독립 씬. 열벡터의 길이·내적으로 Gram 행렬을 구성하는 새 대본. 상위92초 자료와 구분. 실행: python longforms/evdsvd02_conditions/revisions/v2_132s/build.py.


- [월드컵 03 — EVD vs SVD: 분해 구조](evdsvd03_structure/README.md): 사용자 종료 시각149초,24개 독립 씬,쇼츠·가로형. 실행: python longforms/evdsvd03_structure/build.py (--preview 미리보기).


- [월드컵03 — 분해 구조,153초 그래프 수정본](evdsvd03_structure/revisions/v2_153s/README.md):18개 독립 씬. 숫자 계산 제거,좌표·투영·회전된 원/타원 애니메이션. 실행: python longforms/evdsvd03_structure/revisions/v2_153s/build.py.


- [월드컵04 — 고윳값과 특이값](evdsvd04_values/README.md):103초,17개독립씬. 마지막종료시각101/103사용자확정. 실행: python longforms/evdsvd04_values/build.py.

## EVD vs SVD ⑤ — 미래 예측

최종8편: [최종 선택·149초·30개독립씬](evdsvd08_final_choice/README.md). 같은행렬의음수고윳값과SVD반전표현,최종3:4,질문에서시작하는분해선택.

7편: [역변환·142초·27개독립씬](evdsvd07_inverse/README.md). 원→타원→원,선분으로의붕괴,의사역행렬의최소노름선택.사용자발화시각기준.

6편: [복원 정확도·133초·23개독립씬](evdsvd06_reconstruction/README.md). 같은10×10 행렬을5개성분으로근사. 고정색상격자와실제Frobenius오차.

[130초·세로/가로 프로젝트](evdsvd05_future/README.md). 고유성분의 반복 변화와 특이값 거듭제곱의 불일치. 실제 사용자 발화 시각 기준.

## QR 분해

- [1편 — 벡터는 어떻게 새로운 공간을 만드는가?](qr01_new_directions/README.md): 사용자 문장 종료 시각 기준 95초, 24개 교체 가능 컷. 세로 쇼츠·가로형. `python longforms/qr01_new_directions/build.py --preview` / `python longforms/qr01_new_directions/build.py`. 음원 미제공으로 무음·자막 제작.

- [2편 — 왜 R의 아래쪽은 모두 0일까?](qr02_triangular_structure/README.md): 사용자 종료 시각 기준 98초, 25개 독립 컷, 세로·가로 무음 자막 영상. `python longforms/qr02_triangular_structure/build.py --preview` / `python longforms/qr02_triangular_structure/build.py`.

- [QR 2편 현재 수정본 v2 — 공간의 차원이 만드는 위삼각 구조](qr02_triangular_structure/revisions/v2_96s/README.md): 새 대본·96초 종료 시각·24컷. `python longforms/qr02_triangular_structure/revisions/v2_96s/build.py`. 이전 98초 버전과 구분.

- [QR 3편 — 대각선과 부피](qr03_diagonal_volume/README.md): 사용자 108초·27개 독립 컷·쇼츠/가로형 무음 자막 영상. `python longforms/qr03_diagonal_volume/build.py --preview` / `python longforms/qr03_diagonal_volume/build.py`.

- [QR 4편 — 컴퓨터는 왜 정규방정식보다 QR을 선호할까?](qr04_stable_least_squares/README.md): 사용자 107초·28컷. `python longforms/qr04_stable_least_squares/build.py --preview` / `python longforms/qr04_stable_least_squares/build.py`. 열공간 고정·계수 상쇄·조건수 제곱·후진대입, 무음 자막 영상.

- [현재 기하학 4편 — QR과 SVD의 방향 선택](qr04_qr_vs_svd/README.md): 새 확정 원고·108초·27컷, 같은 회전된 행렬을 사용하는 QR/SVD. `python longforms/qr04_qr_vs_svd/build.py`. 이전 최소제곱 4편과 구분.

- [기하학 5편 최종편 — QR 반복과 고윳값](qr05_eigenvalue_iteration/README.md): 124초·30개 독립 컷·쇼츠/가로형 무음 자막. `python longforms/qr05_eigenvalue_iteration/build.py --preview` / `python longforms/qr05_eigenvalue_iteration/build.py`.

- [QR 기하학 — 직교성으로 연결하는 마무리](qr_series_closing/README.md): 요청된 시리즈 회고, 89초·25컷·가로형만. `python longforms/qr_series_closing/build.py --preview` / `python longforms/qr_series_closing/build.py`.

- [QR 1~6편 음성 포함 통합본](qr_full_01_06/README.md): exports/qr_long_1.mp4~qr_long_6.mp4 순서 연결. 10분 37.96초, 1920×1080·30fps, 원본 영상·음성 유지 및 챕터 포함. 실행: python longforms/qr_full_01_06/combine.py. 썸네일: exports/qr_full_01_06_thumbnail.png.

## 자연의 최적화

- [01 — 비눗막은 어떻게 최소 면적을 찾을까?](nature01_soap_film/README.md): 사용자 문장 종료 시각 기준 174초, 24개 독립 Manim 3D 씬. 쇼츠·가로형 자막 무음 영상. 실행: python longforms/nature01_soap_film/build.py --preview 또는 python longforms/nature01_soap_film/build.py.


- [02 — 매달린 사슬이 포물선이 아닌 이유](nature02_catenary/README.md): 사용자 문장 종료 시각 기준 150초, 22개 독립 Manim 3D 씬. 같은 길이 후보의 에너지 적분·거리 제약 사슬·현수선 회전. 세로/가로 자막 무음 영상. python longforms/nature02_catenary/build.py --preview / python longforms/nature02_catenary/build.py.


- [03 — 빛은 목적지를 모르는데 어떻게 최단시간 경로가 나타날까?](nature03_refraction/README.md): 사용자 종료 시각 기준 149초, 22개 독립 Manim 2D/3D 씬. 위상장 기반 파면 굴절·실제 이동 시간·페이저 비교. 세로/가로 자막 무음 영상. python longforms/nature03_refraction/build.py --preview / python longforms/nature03_refraction/build.py.


- [04 — 최속강하선과 사이클로이드](nature04_brachistochrone/README.md): 165초·26개 독립 씬. 물리 시간 경주·에너지·회전 원·층별 Snell 경로와 연속 극한. 세로/가로 자막 무음 영상. `python longforms/nature04_brachistochrone/build.py --preview` / `python longforms/nature04_brachistochrone/build.py`.

- [05 — 최소작용 원리와 뉴턴의 운동법칙](nature05_stationary_action/README.md): 162초·27개 독립 씬. 시간 이력·부호 있는 작용·정지 조건·뉴턴 법칙 유도와 두 해법의 일치. 세로/가로 자막 무음 영상. `python longforms/nature05_stationary_action/build.py --preview` / `python longforms/nature05_stationary_action/build.py`.

- [자연의 최적화 1~5편 통합 롱폼](nature_full_01_05/README.md): 음성 포함 가로형 `nature_1.mp4`~`nature_5.mp4` 순서 결합. 13분 35초, 1920×1080·30fps, 재인코딩 없음, 편별 챕터. `python longforms/nature_full_01_05/combine.py`.

## 내적
- [LEVEL 01 — 방향을 측정하는 연산](dot01_direction_measure/README.md): 102초, 8개 독립 씬, 9:16 쇼츠·16:9 롱폼. 사용자 제공 27개 문장 종료 시각. python longforms/dot01_direction_measure/build.py (--preview). 음원 미제공으로 무음·자막 제작.


- [내적 LEVEL 02 — Projection / 정사영](dot02_projection/README.md): 101초, 9개 독립 씬, 세로 쇼츠·가로 롱폼. x=(4,2), 45도 단위벡터, 내적값3√2로 정사영(3,3) 생성. python longforms/dot02_projection/build.py (--preview). 음원 미제공으로 무음·자막 제작.


- [내적 LEVEL 03 — 방향 성분 제거와 직교 잔차](dot03_orthogonal_residual/README.md): 사용자 종료 시각 기준101초, 8개 독립 씬, 쇼츠·가로형. (4,2)−(3,3)=(1,−1), 잔차의 내적0과 성분 재구성. python longforms/dot03_orthogonal_residual/build.py (--preview). 음원 미제공으로 무음·자막 제작.


- [내적 LEVEL 04 — 직교정규기저와 좌표](dot04_orthonormal_coordinates/README.md): 사용자 종료 시각137초, 9개 독립 씬, 쇼츠·가로형. 고정 x=(5,1), 새 좌표(3√2,−2√2), 두 정사영(3,3)+(2,−2)로 복원. python longforms/dot04_orthonormal_coordinates/build.py (--preview). 음원 미제공으로 무음·자막 제작.


## GPU 계층 구조

- [LEVEL 01 — Thread](gpuh01_thread/README.md): 사용자 문장 종료 시각 기준 152초, 16개 독립 씬, 세로·가로 무음 자막 영상. 실행: python longforms/gpuh01_thread/build.py --preview / python longforms/gpuh01_thread/build.py. CUDA 배열 덧셈 실행 검증 완료.

- [LEVEL 02 — Warp](gpuh02_warp/README.md): 사용자 문장 종료 시각 기준 167초, 20개 독립 씬, 세로·가로 무음 자막 영상. 같은 GPU·SM·Block 지도에서 고정 32 Lane의 SIMT·분기 경로·마스크를 시각화. 실행: `python longforms/gpuh02_warp/build.py --preview` / `python longforms/gpuh02_warp/build.py`. CUDA 결과와 참여 mask 검증, 실제 명령 trace와 소스 경로 개념도 구분.

- [LEVEL 03 — Block](gpuh03_block/README.md): 사용자 종료 시각178초, 20개 독립 씬, 세로·가로 무음 자막 영상. 같은 지도·네 Warp·한 Shared 배열·Block 장벽으로128개 입력을8256으로 합산. 실행: `python longforms/gpuh03_block/build.py --preview` / `python longforms/gpuh03_block/build.py`. 원본 CUDA 결과와8단계×128개 슬롯 검증.

- [LEVEL 04 — SM](gpuh04_sm/README.md): 사용자 종료 시각178초, 16개 독립 씬, 세로·가로 무음 자막 영상. 상주 Warp의 위치를 유지하며 데이터 대기·준비·명령 발행을 구분한다. 실행: `python longforms/gpuh04_sm/build.py --preview` / `python longforms/gpuh04_sm/build.py`. CUDA 1,003개 결과 검증, 스케줄링 개념도와 실제 측정값 구분.

- [LEVEL 05 — Grid](gpuh05_grid/README.md): 사용자 종료 시각178초, 18개 독립 씬, 세로·가로 무음 자막 영상. 12Block×128Thread의 논리 공간과4SM의 설명용 배치, 인덱스5·133, 별도5×4Grid의 이미지 타일. 실행: `python longforms/gpuh05_grid/build.py --preview` / `python longforms/gpuh05_grid/build.py`. CUDA1536개 배열 출력과2D 이미지 결과 검증.

- [LEVEL 06 — Register](gpuh06_register/README.md): 사용자종료시각175초,18개독립씬,세로·가로무음자막영상. Thread2의계산과SM RegisterFile,가상4096/8192개요구량,Pressure와Spilling의구분. 실행: `python longforms/gpuh06_register/build.py --preview` / `python longforms/gpuh06_register/build.py`. 실제CUDA1536개결과·12Register/Thread·Spill0bytes검증.

- [내적 LEVEL 05 — 그람–슈미트 직교화와 QR 분해](dot05_gram_schmidt_qr/README.md): 사용자 문장 종료 시각153초, 11개 독립 씬, 쇼츠·가로형. a₁=(1,1), a₂=(2,0)에서 기저를 만들고 Q열·R계수로 A를 복원. python longforms/dot05_gram_schmidt_qr/build.py (--preview). 음원 미제공으로 무음·자막 제작.


- [내적 LEVEL 06 — 최소제곱과 직교 잔차](dot06_least_squares/README.md): 사용자 문장 종료 시각170초, 11개 독립 씬, 쇼츠·가로형. b=(2,3,4), xy평면의 최적 결과(2,3,0), 수직 잔차(0,0,4), 정규방정식과 Q=A·R=I₂인 축약QR. python longforms/dot06_least_squares/build.py (--preview). 음원 미제공으로 무음·자막 제작.

- [내적 LEVEL 07 — PCA와 최적 방향](dot07_pca_direction/README.md): 사용자 문장 종료 시각149초, 12개 독립 씬, 쇼츠·가로형. 같은16개 데이터에서 오차 최소와 분산 최대의 동치, 공분산행렬과 첫 번째 주성분을 시각화. 실행: `python longforms/dot07_pca_direction/build.py --preview` / `python longforms/dot07_pca_direction/build.py`. 음원 미제공으로 무음·자막 제작.

- [내적 LEVEL 08 — SVD와 방향별 행렬 작용](dot08_svd_direction/README.md): 사용자 문장 종료 시각147초, 11개 독립 씬, 쇼츠·가로형. A=[[0,−1],[3,0]]의 Vᵀ→Σ→U 계산과 벡터 합, 직접 행렬곱 검증. 실행: `python longforms/dot08_svd_direction/build.py --preview` / `python longforms/dot08_svd_direction/build.py`. 음원 미제공으로 무음·자막 제작.

- [내적 LEVEL 09 — Attention과 정보 결합](dot09_attention_mix/README.md): 사용자 문장 종료 시각154초, 11개 독립 씬, 쇼츠·가로형. Query–Key내적→√dₖ스케일링→Softmax→Value가중합을 같은 수치로 연결하고 정사영과 구별. 실행: `python longforms/dot09_attention_mix/build.py --preview` / `python longforms/dot09_attention_mix/build.py`. 음원 미제공으로 무음·자막 제작.

- [내적 LEVEL 10 — 기울기와 경사하강법](dot10_gradient_descent/README.md): 사용자 문장 종료 시각169초, 13개 독립 씬, 쇼츠·가로형. L=θ₁²+4θ₂², 방향미분·국소 최급강하·실제 갱신·큰 학습률의 손실증가. 사용자 요청 LEVEL01–10 결론 포함. 실행: `python longforms/dot10_gradient_descent/build.py --preview` / `python longforms/dot10_gradient_descent/build.py`. 무음·자막 제작.

- [내적 LEVEL 01–10 통합 롱폼](dot_full_01_10/README.md): 사용자 지정 `exports/dot_long1.mp4`~`dot_long10.mp4` 음성 포함 파일을 순서대로 무손실 결합. 약23분33.5초, 내장10챕터와 유튜브 설명용 타임라인. 실행: `python longforms/dot_full_01_10/combine.py`.


- [GPU LEVEL 07 — Shared Memory](gpuh07_shared_memory/README.md): 160초, 17씬, 가로·세로. Block 내부 공유·동기화, 2×2 타일 재사용, 용량과 Bank Conflict. 실제 CUDA 결과 검증. `python longforms/gpuh07_shared_memory/build.py`.

- [GPU LEVEL 08 — Global Memory & Coalescing](gpuh08_global_memory/README.md): 165초, 14개 독립 씬, 가로·세로. 32Lane의 정렬된 float32 접근을 고정 격자에서 비교하며 4→32 Sector로 변화. 실제 CUDA 출력 및 주소 모델 검증. `python longforms/gpuh08_global_memory/build.py`.

- [GPU LEVEL 09 — L1 & L2 Cache](gpuh09_cache/README.md): 169초, 독립 씬14개, 가로·세로. 메모리 공간과 캐시 계층, L1/L2 Hit·Miss·L1 Bypass의 가정 경로, Unified L1/Shared 물리 자원의 개념 분할. `python longforms/gpuh09_cache/build.py`.

- [GPU LEVEL 10 — Memory Controller & DRAM](gpuh10_dram/README.md): 164초, 독립 씬14개, 가로·세로. 논리 주소와 물리 저장 장치, Controller 요청·데이터 반환, DRAM Row 상태와 명령, GDDR/HBM 구조. `python longforms/gpuh10_dram/build.py`.

- [GPU LEVEL 11 — 최종 통합편](gpuh11_integrated/README.md): 191초, 독립 씬16개, 가로형만. N512/Block128/Grid4의 vectorAdd에서 Block1 Thread5(i133)의 4+7=11을 끝까지 추적하며 논리 조직·SM 실행·데이터 공급을 연결. `python longforms/gpuh11_integrated/build.py`.

- [GPU LEVEL 01–11 통합 롱폼](gpuh_full_01_11/README.md): 사용자 지정 `gpuh_1.mp4`~`gpuh_11.mp4` 음성 포함 파일을 순서대로 스트림 복사. 약31분46초, MP4 내장11챕터와 유튜브 구간 설명. `python longforms/gpuh_full_01_11/combine.py`.

## 모든 것이 필요할까?

- [01 — 최소 표현의 조건](minimal01_preserve/README.md): 사용자 문장 종료 시각 기준154초, 독립 씬15개. 세로·가로 두 버전, 무음·전체 발화 자막. 반복 기록의 복원, 도로의 연결성/최단거리, 동전 횟수/최대 연속, 작은 후보와 최소성의 구분. 실행: python longforms/minimal01_preserve/build.py (--preview 미리보기).

- [모든 것이 필요할까? 02 — 최소 유전체](minimal02_genome/README.md): 사용자 문장 종료 시각 기준164초, 독립 씬17개. 세로·가로 무음·전체 발화 자막. 합성 치사의 독립 A/B 실험, 환경 의존성, 분열 특성, 2016년 149/473개 기능 미해명을 구분한다. 실행: python longforms/minimal02_genome/build.py (--preview 미리보기).

- [모든 것이 필요할까? 03 — 그래프 희소화](minimal03_sparsification/README.md): 사용자 종료 시각163초, 독립 씬15개, 세로·가로 무음·전체 발화 자막. 신장 트리·에너지·유효 저항, 28→8간선 가중 사례의 모든 값 배치에서 ε=0.15 보장 검증. 실행: python longforms/minimal03_sparsification/build.py (--preview 미리보기).

- [모든 것이 필요할까? 04 — 충분통계량](minimal04_sufficiency/README.md): 사용자 종료 시각153초, 독립 씬15개, 세로·가로 무음·전체 발화 자막. 알려진 분산 정규모형의 평균 충분성, 최대값1로 정규화한 상대 우도, 미지 분산의 합계·제곱합, 최소충분의 의미를 구분한다. 실행: python longforms/minimal04_sufficiency/build.py (--preview 미리보기).


충분통계량 4편 현재 개정본: [158초 직관 실험 버전](minimal04_sufficiency/revisions/v2_intuition_158s/README.md). 기존 153초 원본 보존.


- [모든 것이 필요할까? 05 — 최소 실현](minimal05_realization/README.md): 사용자 발화 시각 기준 154초·16개 독립 씬·세로/가로. 실행: `python longforms/minimal05_realization/build.py --preview` 또는 `python longforms/minimal05_realization/build.py`.


- [모든 것이 필요할까? 06 — 재규격화와 보편성](minimal06_universality/README.md):160초·14개 독립 씬·세로/가로. 실행: `python longforms/minimal06_universality/build.py --preview` 또는 `python longforms/minimal06_universality/build.py`.


- [모든 것이 필요할까? 07 — 복권 가설](minimal07_lottery/README.md):170초·16개 독립 씬·세로/가로. 실행: `python longforms/minimal07_lottery/build.py --preview` 또는 `python longforms/minimal07_lottery/build.py`.


- [01–07 통합 마무리 · 모든 것이 필요할까?](../longforms/minimal01_07_finale/README.md): 사용자 확정163초, 14개 독립 씬, 16:9 롱폼만. 실행: `python longforms/minimal01_07_finale/build.py --preview` / `python longforms/minimal01_07_finale/build.py`. 음원 미제공, 무음·단일 트랙 자막.


- [모든 것이 필요할까? 1–8 통합 롱폼](minimal_full_01_08/README.md): 사용자 지정 음성 포함 `minimal_1_long.mp4`–`minimal_8_long.mp4` 순차 결합. 21분49초,1080p30fps,8개 챕터와 유튜브 설명문. 실행: `python longforms/minimal_full_01_08/build.py`.


## 최소 조건 2부 · 신경망

- [1편 — 내재 차원](minimal_nn01_intrinsic_dimension/README.md): 사용자 문장 종료 시각 기준 129초, 9개 독립 씬. 롱폼 1920×1080·쇼츠 1080×1920, 60fps, 무음·전체 대본 자막. 실행: python longforms/minimal_nn01_intrinsic_dimension/build.py (--preview 미리보기).

- [2편 — 신경망의 진짜 차원은 몇 개일까?](minimal_nn02_representation_dimension/README.md): 사용자 문장 종료 시각 기준 153초, 12개 독립 씬. 뉴런 수·실제 차원·추정 차원을 구분한다. 롱폼·쇼츠 1080p·60fps·무음·전체 문장 자막. 실행: `python longforms/minimal_nn02_representation_dimension/build.py` (`--preview` 미리보기).

- [3편 — IMPACT: 신경망의 차원을 줄여도 성능을 유지할 수 있을까?](minimal_nn03_impact/README.md): 사용자 문장 종료 시각156초·9개 독립 씬. 실제 계산한 행렬분해와 오차 방향 비교, ACL2026 보고 수치. 롱폼·쇼츠1080p·60fps·무음·자막. 실행: `python longforms/minimal_nn03_impact/build.py` (`--preview` 미리보기).

- `gpui08_register_datapath/`: GPU 개론 08, 레지스터·MUX·데이터 경로. 확정 153초, 14개 독립 씬. `python longforms/gpui08_register_datapath/build.py`.

- [GPU 개론 09 — 명령어는 어떻게 회로를 제어할까?](gpui09_instruction_control/README.md): 확정141초·27문장·14씬,가로/세로1080p30,무음·전체자막. `python longforms/gpui09_instruction_control/build.py`.

- [GPU 개론 10 — 컴퓨터는 어떻게 프로그램을 실행할까?](gpui10_program_execution/README.md): 확정165초·35문장·15씬, 가로/세로1080p30, 무음·전체자막. `python longforms/gpui10_program_execution/build.py`.

- [GPU 개론 6~10편 통합 롱폼](gpui_full_06_10/README.md): 사용자 지정 음성 포함 `gpui_6_long.mp4`~`gpui_10_long.mp4` 합본. `python longforms/gpui_full_06_10/build.py`.
