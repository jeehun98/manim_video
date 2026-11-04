# 자연의 최적화 04 — 최속강하선과 사이클로이드

사용자 확정 대본과 문장 종료 시각을 반영한 165초 영상. 26개 독립 씬, 세로 쇼츠·가로 롱폼 두 레이아웃. 원본 콘티는 `reference/storyboard.txt`에 보존했다. 음원 미제공이므로 자막 포함 무음 출력이다.

```powershell
python longforms/nature04_brachistochrone/prepare.py
python longforms/nature04_brachistochrone/build.py --preview --jobs 2
python longforms/nature04_brachistochrone/verify.py preview
python longforms/nature04_brachistochrone/build.py --jobs 2
python longforms/nature04_brachistochrone/verify.py delivery
python longforms/nature04_brachistochrone/verify.py final
```

일부 씬만 수정한 경우 `--scene 07,15`로 다시 렌더하고, `--concat-only`로 전체를 결합한다. `--resume`은 해상도와 프레임 수만 확인하므로 소스 변경 후 해당 씬에 사용하지 않는다. 사용자 대본과 구간이 바뀌지 않은 상태에서 레이아웃만 수정한다.

출력은 `exports/nature04_brachistochrone_165s_shorts_final.mp4`, `exports/nature04_brachistochrone_165s_longform_final.mp4`와 같은 이름의 SRT다. 미리보기는 15fps, 360×640 / 640×360이다. 최종은 30fps, 1080×1920 / 1920×1080, 각 4950프레임이다.

구현은 `visuals.py`, 수학 계산은 `physics.py`, 확정 시각은 `timing.json`, 제작 기준은 `brief.md`, 각 씬 목적과 대본은 `scenes/*/spec.md`와 `script.txt`에 있다. TTS 발음 원고에는 시간·제목을 넣지 않았다.

같은 두 끝점을 잇는 상대 단위 모형에서 사이클로이드 시간 3.557607, 직선 4.082483, 깊은 곡선 5.393119다. 화면 속 경주는 이 계산으로 얻은 위치를 공통 시간에 평가한다. 실제 초 단위 실험의 측정값으로 제시하지 않는다.

수학 참고: [UCSD 변분법 강의](https://courses.physics.ucsd.edu/2007/Fall/physics110a/LECTURES/110A_VARIATIONAL.pdf), [Illinois 최속강하선 강의](https://liberzon.csl.illinois.edu/teaching/cvoc/node24.html). 외부 이미지·음원은 사용하지 않았다.

## 완료·검증

2026-10-27 두 최종본 렌더 및 전체 디코딩 검증 완료. 두 파일 모두 165.000초, 30fps, 4950프레임, 비디오 스트림만 포함한다. `delivery_verification.json`, `geometry_verification.json`, `qa/contact_shorts_final.png`, `qa/contact_longform_final.png`에 검증 결과를 남겼다. 최종 화면 기준으로 `sync_preview.py`와 `build.py --preview --concat-only`를 실행해 미리보기도 갱신했다.
