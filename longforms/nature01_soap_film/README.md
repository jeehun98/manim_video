# 자연의 최적화 01 — 비눗막은 어떻게 최소 면적을 찾을까?

- 사용자 대본의 문장 종료 시각 기준 **174초**, 24개 독립 Manim 3D 씬.
- 쇼츠: 1080×1920, 롱폼용 가로본: 1920×1080. 모두 30fps.
- 미리보기: 360×640 / 640×360, 15fps.
- 음원 미제공: 원문 자막을 입힌 무음 영상. 음성 속도를 추정하거나 합성하지 않는다.
- 제작 도구: Python 3.12, Manim Community 0.21.0, FFmpeg, Malgun Gothic.

## 실행

프로젝트 루트에서:

```powershell
python longforms/nature01_soap_film/build.py --preview --jobs 2
python longforms/nature01_soap_film/build.py --jobs 2
```

`--layout shorts` / `--layout longform`으로 화면비를 선택한다. `--scene 22`처럼 한 씬만 다시 렌더할 수 있다. `--resume`은 검증된 길이·해상도의 기존 씬을 재사용한다. 소스를 수정한 씬은 `--resume` 없이 다시 렌더한다. `--concat-only`는 기존 씬들을 결합하고 자막을 입힌다.

출력: `exports/nature01_soap_film_174s_{shorts,longform}_{preview,final}.mp4`. 원문 SRT를 함께 복사한다. 화면비별 ASS는 화면 내 줄바꿈과 자막 배치를 담당한다.

## 제작 자료

- `reference/storyboard.txt`: 사용자 원본 콘티 보존.
- `narration.md`, `master_script.md`, `tts_script.txt`: 제공 대본. TTS 파일에는 읽지 않는 제목·시각이 없다.
- `timing.json`: 42개 문장의 사용자 종료 시각. 씬 경계와 문장 경계가 다르면 자막은 원문 시각을 따른다.
- `manifest.json`, `scenes.yaml`, `scenes/*/spec.md`: 24개 독립 교체 단위.
- `geometry.json`: 고리 조건, 안정 가지, 후보 면적 및 변분 면적 곡선의 적분 결과.
- `visuals.py`: 공통 3D 도형·화면비·연출. `build.py`: 렌더·검증·결합·자막.
- `prepare.py`: 사용자 대본·시각에서 위 자료를 재생성한다. 수정 대본의 길이를 추정하는 도구가 아니다.

## 콘티 적용

24개 시퀀스는 개별 수정 가능하도록 각각 렌더한다. 원본의 6개 묶음은 내용상의 대단락으로 유지한다. 사용자가 이번에 지정한 대본과 시각을 영상 제작 기준으로 사용한다.

마지막 165~174초는 비눗막과 국소 법칙·전체 조건의 결론으로 유지한다. 사용자 원문 마지막 문장과 174초는 보존하되, 기존 독립 완결 원칙에 따라 사슬·굴절·다음 편 예고 화면은 넣지 않는다.

## 수학적 조건

`a=1`, `h=1.6`, `R=cosh(0.8)`이고 `R=a cosh(h/(2a))`를 만족한다. `u tanh(u)<1`인 두꺼운 안정 가지를 사용한다. `A=2π∫r√(1+r′²)dz`를 적분한다. 비교 후보는 `r_b(z)=R+b(cosh(z)−R)`로 같은 경계를 유지한다.

변분 그래프는 `r_ε(z)=cosh(z)+ε cos²(πz/h)`의 실제 면적을 적분한다. ε는 시간과 다른 후보 매개변수다. 그래프는 이 축대칭 변형 가족의 예시이며, 모든 가능한 변형에 대한 수치 증명으로 제시하지 않는다.

분자 모형과 LJ 곡선, 형태 보간은 설명용이다. 실제 유체 시간 발전이나 실제 비눗물의 전체 분자 시뮬레이션으로 제시하지 않는다. 표면장력 γ는 한 계면 기준이며 막 전체 자유에너지는 일정 온도·조성에서 `E_film=2γA`로 표시한다. 압력차와 중력 영향을 무시하고 내부의 `H=0`, `δA=0`을 연결한다. 전역 최소를 보장한다고 주장하지 않는다.

## 참고

- [Manim 3D scene API](https://docs.manim.community/en/stable/_modules/manim/scene/three_d_scene.html)
- [Princeton — Minimal Surface: Catenoid](https://vanderbei.princeton.edu/WebGL/catenoid_cosh.html)
- [Geometry of Catenoidal Soap Film Collapse](https://www.damtp.cam.ac.uk/user/gold/pdfs/CatenoidCollapse.pdf)

렌더 성공과 정확한 프레임 수는 생성되는 `preview_report_both.json`, `render_report_both.json`으로 확인한다.

## 완료 확인

2026-10-26 두 최종본 및 미리보기 생성 완료. 최종본은 각각 174.000초, 30fps, **실제 디코딩 프레임 수 5,220**으로 검증했다. 쇼츠 1080×1920, 가로형 1920×1080이며 오디오 스트림은 없다. 검증 기록은 `delivery_verification.json`에 있다.

고정 경계, 안정 가지, 실제 후보 면적, 면적 일차 미분, 패치 경계 장력 적분은 `python longforms/nature01_soap_film/verify.py`로 확인한다. 최종 미디어는 `python longforms/nature01_soap_film/verify.py delivery`, 장면별 검토 이미지는 `python longforms/nature01_soap_film/verify.py final`로 다시 확인할 수 있다.

최종본에서 수정한 분자 장면의 미리보기는 동일 최종 씬을 15fps·낮은 해상도로 변환해 갱신했다. 재생속도와 사용자 시각은 바꾸지 않았다.
