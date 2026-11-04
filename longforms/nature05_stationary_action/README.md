# 자연의 최적화 05 — 최소작용 원리와 뉴턴의 운동법칙

사용자 확정 162초·38문장, 첨부 콘티의 27개 독립 씬. 세로 쇼츠와 가로 롱폼 두 레이아웃으로 제작한다. 음원 미제공으로 자막 포함 무음 영상이다. 원본 콘티는 `reference/storyboard.txt`에 보존했다.

## 실행

```powershell
python longforms/nature05_stationary_action/prepare.py
python longforms/nature05_stationary_action/verify.py
python longforms/nature05_stationary_action/build.py --preview --jobs 2
python longforms/nature05_stationary_action/verify.py preview
python longforms/nature05_stationary_action/build.py --jobs 2
python longforms/nature05_stationary_action/verify.py delivery
python longforms/nature05_stationary_action/verify.py final
```

일부 씬은 `--scene 07,16`으로 교체한 뒤 `--concat-only`로 합친다. `--layout shorts` 또는 `--layout longform`으로 한 버전만 만든다. `--resume`은 해상도·프레임 수만 검사하므로 소스를 수정한 씬에는 사용하지 않는다. `prepare.py`는 확정 원고와 spec을 재생성하므로 spec을 바꾸려면 생성기의 VISUALS도 함께 수정한다.

출력: `exports/nature05_stationary_action_162s_shorts_final.mp4` (1080×1920), `exports/nature05_stationary_action_162s_longform_final.mp4` (1920×1080), 각 30fps·4860프레임. 같은 이름의 SRT도 출력한다. 미리보기는 360×640 / 640×360·15fps. 최종 수정 후 `sync_preview.py`, `build.py --preview --concat-only`로 같은 재생시간의 미리보기를 갱신할 수 있다.

## 데이터와 검증

`physics.py`: m=g=1, x(t)=t, y(t)=.5+2t−t²/2, t=0..4. 공간 운동·시간 그래프·에너지·작용·두 운동 해법에서 동일한 데이터다. 수치는 상대 단위의 이상화이며 실제 실험 측정값이 아니다.

S(0)=−8/3, 수직 성분의 Sᵧ(0)=−14/3. 고정한 수평 운동의 작용은 후보 공통 상수 2다. εsin(πt/4) 변형의 작용 차이는 π²ε²/16이며, 위치·속도를 함께 바꿔 계산한 적분값과 일치한다. 이 예제는 작용의 최소다. 일반적인 최소·최대·안장점 도식은 별도 수학 예시이며 이 공의 작용 그래프로 제시하지 않는다.

뉴턴 방식은 초기값 문제의 수치 적분, 변분 방식은 고정 끝점 이산 작용의 정상 조건에서 얻은 삼중 대각 선형계다. 후자는 y[i−1]−2y[i]+y[i+1]=−gΔt²를 풀고 보간한다. 동일 초기 위치·속도를 얻고 해석적 포물선과 일치하는지 검증한다. 후보 비교는 자연이 미래를 탐색하는 물리적 과정으로 표현하지 않는다.

검증 자료는 `geometry_verification.json`, 최종 디코딩 결과는 `delivery_verification.json`, 장면 검수 이미지는 `qa/contact_*_final.png`다. 전체 원고·자막·시각은 `narration.md`, `tts_script.txt`, `captions.srt`, `timing.json`. 소스는 `visuals.py`와 `scenes/*/scene.py`이며 씬별 목적과 조건은 `spec.md`에 있다.

## 참고·환경

[Cambridge Classical Dynamics](https://www.damtp.cam.ac.uk/user/tong/dynamics/dynhtml/S2.html), [MIT Structure and Interpretation of Classical Mechanics](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/9579/sicm_edition_2.zip/chapter001.html). 원본 이미지 링크는 콘티의 참고로만 보존했으며 외부 미디어는 사용하지 않았다.

Python 3.12, Manim Community 0.21.0 Cairo, SciPy/NumPy, FFmpeg 9.0.1, Malgun Gothic. LaTeX 설치를 요구하지 않는 Text 기반 수식이다.

## 완료 상태

2026-10-27 세로·가로 최종본 제작과 시각 검수 완료. 두 파일 모두 실제 디코딩 기준 162.000초·30fps·4860프레임, 비디오 스트림만 포함한다. 작용 적분과 해석식의 최대 차이는 8.9×10⁻¹⁶, 뉴턴 해와 해석적 포물선은 4.5×10⁻¹⁵ 이내, 변분 해는 2.7×10⁻¹⁴ 이내였다. 최종 화면 기준으로 미리보기를 갱신했다.
