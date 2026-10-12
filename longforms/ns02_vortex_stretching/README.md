# 2막 — 왜 3차원에서는 소용돌이가 스스로 강해질 수 있을까?

Navier–Stokes × 신경망의 수학적 패턴. 1막 마지막 질문에서 이어지는 7개 독립 씬이다.

- 화면 길이: 176초(2:56), 사용자 제공 문장별 종료 시각 기준이다. 원래 콘티 길이는 210초이다.
- 해상도: 1920×1080, 30fps. 미리보기 854×480, 15fps.
- 영상은 무음이며 화면과 자막을 사용자 제공 문장별 시각에 맞췄다. 실제 음원 파일이 없어 음성 결합은 미진행이다.
- 사용자 허용에 따라 원래 콘티 내레이션을 다듬고, 단면·축·회전·늘어남을 차례로 보여준다.

## 핵심 구성

1. 엄밀한 2D에서 소용돌이 패치가 변형되어도 회전축 방향 흐름은 없다.
2. 작은 유체 조각의 회전을 통해 보티시티와 속도장 curl을 소개한다.
3. 평면 단면을 3D 관으로 바꾸고 접선 회전과 축을 분리해 보여준다.
4. 같은 물질 조각의 관을 늘려 L×2, A/2, r/√2, ω×2를 비교한다.
5. 보티시티 방정식과 정렬 조건을 통해 증폭이 가능한 이유를 설명한다.
6. 늘어남과 점성 확산을 분리·비교한 뒤 동시에 작용함을 설명한다.
7. 2D/3D 방정식을 비교하고 유한한 전체 에너지와 국소 집중이라는 3막 질문으로 이어간다.

## 실행

Python 3.12, Manim 0.21.0, FFmpeg, Malgun Gothic 사용. 프로젝트 루트에서:

```powershell
python longforms/ns02_vortex_stretching/prepare.py
python longforms/ns02_vortex_stretching/build.py --preview --tag timed
python longforms/ns02_vortex_stretching/build.py --tag timed
python longforms/ns02_vortex_stretching/build.py --scene 4
python longforms/ns02_vortex_stretching/build.py --concat-only --tag timed
```

prepare.py는 DATA에서 대본·spec·자막·씬 파일을 재생성한다. 해당 수동 수정 파일을 덮어쓰므로 원문 수정은 DATA에 먼저 반영한다. 각 씬은 독립적으로 재렌더하고 concat-only로 연결할 수 있다.

영상: exports/ns02_act02_176s_timed_1080p30.mp4. 같은 이름의 SRT를 제공한다. TTS 통합 대본은 tts_script.txt이며 화면 cue마다 빈 줄을 넣었다. 실제 음성 파일 없이 음성을 합성하거나 mux하지 않는다.

## 수학·표현 기준

관은 실제 3D 원통 좌표를 직교 투영해 구현했다. 모양·회전 표지·축 방향 변화는 설명용 모델이다. 전체 Navier–Stokes PDE의 수치 해가 아니다.

물질 관의 비압축성 조건은 λ=L/L₀, r=r₀/√λ, πr²L 일정이다. 보티시티 성장은 부피 보존만으로 도출하지 않는다. 점성을 제외한 국소 affine 예 u=(-ax/2-Ωy, Ωx-ay/2, az), Ω′=aΩ, ωz=2Ω에서 λ=e^(at), ω=ω₀λ를 사용한다. 이 모델은 전역 유한 에너지 해를 주장하지 않는다.

보티시티 방정식은 ν>0, 일정 밀도·점성, 발산 없는 속도장, 외력의 컬이 0인 조건으로 제시한다. 회전 있는 외력이 있으면 curl f가 추가된다. 2D는 z 방향 속도와 의존성이 모두 없는 엄밀한 평면 흐름이다. 2D 전역 매끄러움은 적절한 초기 자료와 공간 조건을 전제로 한다.

3D의 stretching 항은 strain과 보티시티의 정렬에 따라 강화·약화·방향 전환을 일으킬 수 있다. 증폭 경로가 존재한다고 자동으로 자기증폭이 계속되거나 특이점이 발생하는 것은 아니다. 2026년 결과의 증명이나 확정 상태는 다루지 않는다.

점성 확산은 물질 관이 부피를 키우는 것이 아니라 보티시티 분포가 퍼지는 효과로 표현한다. 관의 길이·반지름·회전 강화와 확산 분포를 동일한 기하 변화로 취급하지 않는다.

## 검토 출처

- [Lenya Ryzhik, Stanford Math 256B 강의 노트](https://virtualmath1.stanford.edu/~ryzhik/notes-256B-24.pdf): 보티시티, 2D/3D, stretching, regularity.
- [Clay 문제 기술서](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf): 문제와 자료·공간 조건.

## 대본 수정

첫 정의에서만 와도와 보티시티를 함께 소개하고 이후에는 보티시티로 통일했다. 사용자 수정 대본을 42개 화면 구간에 반영했다. 수식은 벡터 기호를 굵게 표시하고 stretching과 diffusion에 영문 항 이름을 붙였다. 일정 점성·비압축성·curl f=0 조건을 명시했다. 이전 통합 영상은 보존하며 새 영상은 timed로 출력한다. voice_timing.json에 사용자 제공 42개 문장의 누적 종료 시각을 저장하고 적용했다.

## 검증 상태

42개 문장의 화면 cue와 SRT 종료 시각이 사용자 측정값과 모두 일치하며, 마지막 자막은 176초에 끝난다. 최종 영상은 1920×1080, 정확히 30fps·5280프레임·176초인 무음 H.264이다. 대표 화면을 검토했고 전체 디코딩 오류가 없다.
