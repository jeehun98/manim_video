> 이 폴더는 이전 153초 대본 기준 제작물입니다. 현재 개정본: [158초 직관 실험](revisions/v2_intuition_158s/README.md).

# 모든 것이 필요할까? 04 — 충분통계량

사용자 확정 대본 **33문장·153초(2분33초)**. 독립 씬15개, 세로 쇼츠와 가로 롱폼 별도 배치. 음원 미제공으로 **무음**, 전체 발화 자막 내장 및 SRT 제공.

## 결과물과 실행

- `exports/minimal04_153s_shorts_final.mp4`: 1080×1920,30fps
- `exports/minimal04_153s_longform_final.mp4`: 1920×1080,30fps
- 같은 이름 `.srt`: 사용자 문장 종료 시각 적용
- `_preview.mp4`: 세로360×640 / 가로854×480,15fps
- `_uncaptioned.mp4`: 자막 합성 전 중간 산출물

프로젝트 루트에서 Manim0.21.0·FFmpeg·Malgun Gothic이 설치된 Python:

```powershell
python longforms/minimal04_sufficiency/data_model.py
python longforms/minimal04_sufficiency/build.py --preview
python longforms/minimal04_sufficiency/build.py
python longforms/minimal04_sufficiency/build.py --layout shorts --scene 10
python longforms/minimal04_sufficiency/verify_caption_boundaries.py --layout shorts
python longforms/minimal04_sufficiency/verify_caption_boundaries.py --layout longform
```

`--layout shorts|longform|both`, `--scene 1..15`, `--jobs 3`, `--concat-only` 지원. 씬별 프레임 수 확인 → concat → 단일 ASS 자막 합성 → 최종 해상도·153초·4,590프레임 확인 순서다.

## 제작 자료

- `narration.md`, `master_script.md`, `tts_script.txt`: 확정 원문·구간별 발음 원고
- `narration_timing.json`, `captions.srt`: 문장 종료 시각33개
- `manifest.json`, `scenes.yaml`, `scenes/*/{spec.md,script.txt,scene.py}`: 독립 씬15개
- `storyboard_user.md`: 사용자 첨부 콘티 원문
- `scene_engine.py`: 두 화면비와 수식·관측값·계산된 곡선
- `data_model.py`, `math_verification.json`: 제곱합 전개·우도·데이터 요약 검증
- `caption_pass.py`: concat 후 단일 자막 트랙. 이전 문장 캐시 잔상 방지
- `inspect_frames.py`: 주요 장면20개 표본 추출
- `verify_caption_boundaries.py`: 모든 문장 경계 직전·정각·직후와 마지막 프레임의 자막을 기준 영상과 비교
- `verification_final.json`, `caption_boundary_verification_*.json`: 최종 영상·자막 검사 결과

## 모형과 실제 계산

평균 추론 부분은 **독립·동일 정규분포, 알려진 분산, 고정 n**이다. 모집단 평균 μ는 미지 모수이고 표본평균 x̄와 구별한다. 도입의 백만 개는 전체 관측 수이며 화면 숫자120개는 일부를 대표하는 가상 측정값이다. 도입에서 그 대표값의 평균을 전체 백만 개의 실제 평균이라고 제시하지 않는다.

곡선 비교에는 공통으로 알려진 `σ²=4`, `n=5`를 사용한다.

| 데이터 | 합 S | 평균 | 제곱합 Q | 평균에서의 제곱거리 합 |
| --- | --- | --- | --- | --- |
| A:1,2,3,4,5 | 15 | 3 | 55 | 10 |
| B:0,0,3,6,6 | 15 | 3 | 81 | 36 |

중복 관측0과6은 세로 적층해 B의 점5개를 모두 보여준다. 점 그래프는 관측값이며 모집단 분포의 추정 곡선으로 표현하지 않는다. 움직이는 정규 밀도에서는 관측값을 고정하고 후보 μ만 이동한다.

정규화한 상대 우도는 다음과 같다.

`L(μ|x)/L(x̄|x)=exp[-n(μ−x̄)²/(2σ²)]`.

두 데이터의 정규화 곡선을 각각 계산하여 최대 오차약1.22×10⁻¹⁵로 일치함을 확인했다. 원래 우도는 같지 않다. 예컨대 μ=3일 때 A의 높이는약9.0476×10⁻⁵, B는약3.5081×10⁻⁶이다. 두 곡선은 각자의 최대 우도값으로 나눠서만 겹친다. 최대값1 정규화는 면적1의 모수 확률분포를 만든다는 뜻이 아니다.

## 수학적 근거

`Σ(x_i−μ)² = Q−2μS+nμ²`를 사용한다. 알려진 σ²에서

`L(μ|x)=h(x) exp[μS/σ²−nμ²/(2σ²)]`,

`h(x)=(2πσ²)^(-n/2) exp[-Q/(2σ²)]`.

따라서 μ와 데이터가 함께 등장하는 부분에는 S만 남는다. 인수분해 정리에 의해 S가 충분하며, 고정 n에서 x̄=S/n는 같은 정보를 담는다. 표본 곡선의 수치 일치만으로 모든 데이터의 충분성을 증명했다고 하지 않는다.

알려진 분산·고정 n에서 두 자료 x,y의 우도비가 μ에 무관할 필요충분조건은 합계가 같은 것이다. 정상적인 공통 지지집합의 정규모형에서 이 우도비 기준으로 x̄의 최소충분성을 설명할 수 있다. 화살표는 **임의의 다른 충분통계량 S → T=g(S)**이다. T에서 원자료를 복원하는 역화살표를 만들지 않는다.

분산까지 미지로 바뀌면 `(S,Q)`가 `(μ,σ²)`에 충분하다. 두 자료의 우도비는 분산1,4,9에서 서로 달라져, 같은 평균만으로 두 모수에 대한 우도 정보를 동일하게 취급할 수 없음을 확인했다. 화면의 제곱거리 합10과36을 모집단 분산의 참값이라고 표시하지 않는다.

최소충분은 통계적 구분의 의미다. 저장 비트·실수 좌표 개수·계산량의 최솟값이나 유한 정밀도에서 무손실 저장을 보장하는 주장이 아니다.

## 참고한 강의 자료

- [MIT14.381 Lecture4 — Sufficient Statistics, Introduction to Estimation](https://ocw.mit.edu/courses/14-381-statistical-method-in-economics-fall-2018/1c6d8a7fe4fbdd22c659af374a830e6a_MIT14_381F18_lec4.pdf)
- [MIT18.655 — Sufficiency](https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/bbbca14a2009e47add8c7ea2a49daa41_MIT18_655S16_LecNote6.pdf)

실제 음원과의 청각적 동기는 음원 수령 후 확인한다. 현재는 제공된 문장 종료 시각과 화면·자막의 일치를 기준으로 제작한다.
