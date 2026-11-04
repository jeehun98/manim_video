# 자연의 최적화 02 — 매달린 사슬이 포물선이 아닌 이유

- 사용자 대본·문장 종료 시각 기준 **150초**, 22개 독립 Manim 3D 씬.
- 쇼츠 1080×1920 / 가로형 1920×1080, 30fps.
- 미리보기 360×640 / 640×360, 15fps.
- 음원 미제공: 제공 원문과 시각에 맞춘 자막 무음 영상.
- 환경: Python 3.12, Manim Community 0.21.0, FFmpeg 9.0.1, Malgun Gothic.

## 실행

프로젝트 루트에서 실행한다.

```powershell
python longforms/nature02_catenary/build.py --preview --jobs 2
python longforms/nature02_catenary/build.py --jobs 2
```

`--layout shorts` 또는 `--layout longform`으로 한 화면비만 선택한다. `--scene 13` 또는 `--scene 06,07`로 해당 씬만 교체한다. `--concat-only`는 기존 씬을 결합하고 원문 자막을 입힌다. `--resume`은 길이와 해상도가 맞는 기존 씬을 재사용하므로 소스를 바꾼 씬에는 사용하지 않는다.

출력: `exports/nature02_catenary_150s_{shorts,longform}_{preview,final}.mp4`. 원문 SRT도 복사한다.

## 자료

- `reference/storyboard.txt`: 첨부 원본 콘티.
- `narration.md`, `master_script.md`, `tts_script.txt`: 사용자 확정 대본. 발화용 파일에는 읽지 않는 제목·시각이 없다.
- `timing.json`, `captions.srt`, 화면비별 ASS: 35문장 원문과 사용자 종료 시각.
- `manifest.json`, `scenes.yaml`, `scenes/*/spec.md`: 22개 교체 가능한 시퀀스와 확정 길이.
- `physics.py`, `geometry.json`: 정확한 길이 제약을 만족하는 연속체 후보와 실제 에너지 적분.
- `dynamics.npz`: 별도 계산한 거리 제약·중력·감쇠 질점 사슬의 궤적과 U·K.
- `visuals.py`, `build.py`: 두 화면비의 Manim 장면과 렌더·자막·결합.

## 수학과 물리

균일하고 유연하며 늘어나지 않는 이상적인 사슬, 동일 높이의 고정점, 균일 중력이다. `a=1`, `b=0.8`, 끝점은 `x=±b, y=cosh(b)`이고 `L=2a sinh(b/a)`다. 기준면 y=0, 질량밀도 λ=1, g=1의 무차원 수치를 사용한다.

후보는 `y=cosh(x)+αsin(πx/b)+βcos(πx/(2b))`다. 끝점은 그대로이고, β를 수치적으로 풀어 모든 후보의 실제 호길이를 L로 맞춘다. 에너지는 `U=∫λgy sqrt(1+y′²)dx`를 적분한다. 단순히 처짐을 달리한 서로 다른 길이의 후보를 비교하지 않는다.

실제 움직임은 33개 질점·고정 끝점·동일한 32개 구간의 거리 제약을 가진 PBD 근사다. 시간간격 1/240초, 감쇠 및 반복 투영을 사용한다. 금속 고리의 강체 접촉 모형과 구별한다. 투영에 따른 수치 소산도 포함한다. 검증한 거리 오차를 `geometry.json`에 기록하며 이상적인 연속체 후보와 이산 질점 근사를 혼동하지 않는다.

장력의 정확한 연속체 성분은 `Tₓ=λga`, `Tᵧ=λga sinh(x/a)`다. 유한 구간에 작용하는 두 장력과 그 구간의 중력을 합해 평형을 검증한다. 포물선 비교는 같은 꼭짓점과 중심 곡률을 가진 `1+x²/2`이며, 동일 길이 후보의 에너지 비교와 별개다.

회전에서는 최저점보다 a 아래에 있는 축을 선택해 반지름 `r(x)=a cosh(x/a)`를 사용한다. 1편과 같은 `a=1,h=1.6,R=cosh(.8)`의 안정한 카테노이드다. 서로 다른 에너지 문제를 같은 물리적 기작이라고 주장하지 않는다. 마지막의 비눗막 비교는 이번 사용자 콘티와 원문에 명시되어 있으며 다음 편 예고는 없다.

## 재현과 검증

```powershell
python longforms/nature02_catenary/prepare.py
python longforms/nature02_catenary/physics.py
python longforms/nature02_catenary/verify.py
python longforms/nature02_catenary/verify.py delivery
```

첫 두 명령은 대본 인덱스와 물리 계산 자료를 재생성한다. 실제 음성 길이를 추정하는 명령이 아니다. 최종 파일은 `render_report_both.json`, 실제 디코딩 프레임 수는 `delivery_verification.json`으로 확인한다.

## 참고

- [University of Cambridge — Catenary worked example](https://www.damtp.cam.ac.uk/user/reh10/lectures/nst-mmii-handout3.pdf)
- [University of Cambridge — Variational problems](https://www.damtp.cam.ac.uk/user/examples/B6b.pdf)
- [Manim 3D scene API](https://docs.manim.community/en/stable/_modules/manim/scene/three_d_scene.html)


본 계산에서 질점 모형의 고정점 오차는 0, 구간 길이 최대 오차는 약 9.7×10⁻⁶, 총길이 상대 오차는 0.0072% 미만이다. 연속체 후보들의 길이 오차는 10⁻¹⁴ 미만이다. 두 모형의 정확도 범위는 geometry_verification.json에 구분해 기록한다.

## 제작 완료

2026-10-27 두 최종본과 미리보기 생성 완료. 두 최종본의 실제 디코딩 프레임 수는 각각 **4,500**, 길이는 **150.000초**, 프레임률은 **30fps**로 검증했다. 쇼츠는 1080×1920, 가로형은 1920×1080이며 자막이 포함된 무음 영상이다.

`qa/contact_{shorts,longform}_final.png`는 각 시퀀스의 자막 포함 검토 이미지다. 수정된 씬의 미리보기는 동일한 최종 씬을 낮은 해상도와 15fps로 변환해 갱신했으며 재생속도나 발화 시각은 바꾸지 않았다.

