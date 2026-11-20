# 특잇값 6장 — 작은 오차가 커지는 이유

사용자 확정 29문장·156초. 16:9 1920×1080 30fps.
음원 미제공으로 무음, 화면 자막과 별도 SRT 포함. 일곱 연속 그룹 독립 렌더.

- narration.md / tts_script.txt: 확정 대본과 발음 원고
- storyboard_source.md: 사용자 콘티 원문
- timing.json / captions.srt: 사용자 문장 종료 시각
- scenes/01–07: 독립 소스와 spec.md
- scene_engine.py / visual_common.py: 애니메이션 및 기존 도형 재사용

```powershell
python longforms/singular_values/chapter_06/build.py
python longforms/singular_values/chapter_06/build.py --preview --scene 3
python longforms/singular_values/chapter_06/build.py --preview --scene 5
python longforms/singular_values/chapter_06/build.py --scenes 6
python longforms/singular_values/chapter_06/verify_video.py
```

결과: exports/singular06_156s_1080p30.mp4 및 .srt.
A=I, B=diag(1,0.01), C=0.01I를 사용한다. 절대 오차 실험은 x=(1,1), Δy=(0,0.002)로 정확한 데이터와 오차가 동일한 역변환을 받는다.
상대 오차 비교는 새 입력x=(1,0)을 명시하며 B는0.2%→20%, C는20%→20%다. 두 경우 모두 절대 복원 오차는0.2다.
1/σmin은 최대 절대 오차 증폭률, κ₂는 상대 오차 증폭의 최악 상한이다. 행렬은 고정되어 있고 우변에만 오차가 발생하는 선형방정식의 민감도를 다룬다.
확대창은 출력 끝점 세로차이×200, C의 원은 균일 확대×50으로 명시한다. 정확히0일 때만 역행렬 없음·κ=∞를 표시한다.
검수 자료: qa/report.json 및 qa/contact_1.jpg–contact_3.jpg.
