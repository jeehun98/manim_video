# 자연의 최적화 03 — 빛은 목적지를 모르는데 어떻게 최단시간 경로가 나타날까?

- 사용자 원문·문장 종료 시각 기준 **149초**, 22개 독립 Manim 2D/3D 씬.
- 쇼츠 1080×1920 / 롱폼용 가로형 1920×1080, 30fps.
- 미리보기 360×640 / 640×360, 15fps.
- 음원 미제공: 사용자 시각에 맞춘 원문 자막이 있는 무음 영상.
- 제작 환경: Python 3.12, Manim Community 0.21.0, FFmpeg, Malgun Gothic.

## 실행

프로젝트 루트에서 실행한다.

```powershell
python longforms/nature03_refraction/build.py --preview --jobs 2
python longforms/nature03_refraction/build.py --jobs 2
```

`--layout shorts` / `--layout longform`으로 한 화면비를 선택한다. `--scene 16` 또는 `--scene 10,11`은 해당 씬만 다시 만든다. 이후 `--concat-only`로 결합·자막을 갱신한다. `--resume`은 기존 길이·해상도가 맞는 씬을 재사용하므로 수정한 씬에는 사용하지 않는다.

출력: `exports/nature03_refraction_149s_{shorts,longform}_{preview,final}.mp4`. 원문 SRT도 복사한다.

## 자료

- `reference/storyboard.txt`: 사용자 첨부 원본.
- `narration.md`, `master_script.md`, `tts_script.txt`: 제공된 확정 대본. 발화용 파일에는 제목·시각이 없다.
- `timing.json`, SRT, 화면비별 ASS: 원문 및 사용자 종료 시각.
- `manifest.json`, `scenes.yaml`, `scenes/*/spec.md`: 22개 독립 교체 단위와 확정 길이.
- `physics.py`, `geometry.json`: 광선·시간·파면·페이저의 공통 계산 자료.
- `visuals.py`, `build.py`: 화면 구현 및 렌더·검증·자막·결합.
- `verify.py`, `geometry_verification.json`, `delivery_verification.json`: 물리·수학 및 출력 검증.

## 공통 광학 모형

경계는 y=0, 공기 위쪽, 물 아래쪽이다. `A=(-2.4,1.4)`, `B=(2.4,-1.1)`, `v₁=1`, `v₂=.75`, `n₁=1`, `n₂=4/3`의 상대 단위를 쓴다. 정지·균일·등방성·비분산 매질의 이상화로 위상속력을 표현한다. 반사와 진폭 전달 계수는 생략한다.

`T(x)=|A−C|/v₁+|C−B|/v₂`, `C=(x,0)`에서 T′=0을 풀어 실제 통과점 x≈1.3161853을 구한다. 직선 통과점은 x=.288이다. 실제 경로의 거리는 5.5154로 직선 5.4120보다 길지만 시간은 6.0301로 직선 6.2058보다 짧다. 모든 표시 수치는 이 동일 좌표에서 계산한다.

두 매질의 파면은 `φⱼ=ω(sⱼ·r−t)`의 등위면이다. `sⱼ=kⱼ/ω`의 크기는 1/vⱼ이고 경계 평행 성분이 이어진다. 파면은 임의로 꺾는 고무판이 아니라 각 매질의 위상장으로 계산한 평면 패치다. 광선 방향은 그 법선과 일치한다. 시각화에서는 같은 위상의 면을 12주기마다 발췌한다. 점광원의 전체 구면파와 구별되는 국소 평면파 모형이다.

페이저는 동일한 ω=120, 표본 9개, 통과점 범위 ±.16에서 비교한다. 공통 위상 ωT_min을 제거한 `exp(iω(Tⱼ−T_min))`를 표시하며 벡터 합의 크기는 바뀌지 않는다. 비정지 영역의 정규화 합은 약 .017, 정지시간 근처는 약 .965다. 이는 동일 진폭의 개념적 기여 합이며, 실제 장의 진폭·기하·경계 계수 전체를 계산한 결과가 아니다. 짧은 파장·기하광학 근사의 정지위상 직관으로 사용하고 다른 기여가 정확히 0이라고 하지 않는다.

이 평면 경계의 시간 함수는 엄격히 볼록해 최소가 된다. 일반 페르마 원리는 정지 조건이며 모든 광학계의 전역 최소를 뜻하지 않는다.

## 서사와 화면

빛을 먼저 전파하고, 이미 전파된 빛에서 B를 선택한다. 첫 0~10초와 재전파 장면에는 B를 미리 표시하지 않는다. 파면 설명에서도 B 없이 전파한 다음 다시 관찰점을 고른다. 실제 시간에 따른 전파와 경로 후보를 바꾸는 수학적 비교를 구분한다.

마지막의 비눗막·사슬·굴절 비교는 이번 사용자 콘티에 명시된 결론이다. 별도 복습 대사나 다음 편 예고는 추가하지 않는다. 이전 편의 카테노이드·현수선은 같은 매개변수의 직접 제작 도형을 사용한다.

## 재현과 검증

```powershell
python longforms/nature03_refraction/prepare.py
python longforms/nature03_refraction/physics.py
python longforms/nature03_refraction/verify.py
python longforms/nature03_refraction/verify.py delivery
python longforms/nature03_refraction/verify.py final
```

첫 두 명령은 사용자 대본 인덱스와 광학 자료를 재생성한다. 발화시간을 추정하지 않는다. `verify.py final`은 자막이 포함된 장면별 검토 이미지를 `qa/`에 만든다.

## 참고

- [The Feynman Lectures I, Chapter 26 — Principle of Least Time](https://www.feynmanlectures.caltech.edu/I_26.html)
- [University of Virginia — Plane Electromagnetic Waves](https://galileoandeinstein.phys.virginia.edu/Elec_Mag/2022_Lectures/EM_46_Plane_Electromagnetic_Waves.html)
- [MIT OpenCourseWare — The Physics of Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/ef731c1b91d77a6db003f6c27e300d25_MIT8_03SCF16_Textbook.pdf)

## 제작 완료

2026-10-27 두 최종본과 미리보기 생성 완료. 사용자 원문 36문장의 종료 시각을 반영했다. 두 최종본의 실제 디코딩 프레임 수는 각각 **4,470**, 길이는 **149.000초**, 프레임률은 **30fps**다. 쇼츠 1080×1920, 가로형 1920×1080이며 자막이 포함된 무음 영상이다.

`qa/contact_{shorts,longform}_final.png`에 자막 포함 장면별 검토 이미지를 저장했다. 수정된 씬의 미리보기는 동일 최종 씬을 낮은 해상도와 15fps로 변환해 갱신했다. 재생속도나 제공된 문장 시각은 바꾸지 않았다.
