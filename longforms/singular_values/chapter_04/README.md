# 특잇값 4장 — 정보의 보존과 소실

사용자 확정 25문장·137초. 16:9 1920×1080 30fps.
음원 미제공으로 무음, 화면 자막과 별도 SRT 포함. 여섯 연속 그룹을 독립 렌더한다.

- narration.md / tts_script.txt: 확정 대본·발음 원고
- storyboard_source.md: 사용자 콘티 원문
- timing.json / captions.srt: 사용자 문장 종료 시각
- scenes/01–06: 독립 소스와 spec.md
- scene_engine.py / visual_common.py: 애니메이션 및 기존 도형 재사용

```powershell
python longforms/singular_values/chapter_04/build.py
python longforms/singular_values/chapter_04/build.py --preview --scene 2
python longforms/singular_values/chapter_04/build.py --preview --scene 4
python longforms/singular_values/chapter_04/build.py --scenes 4
python longforms/singular_values/chapter_04/verify_video.py
```

결과: exports/singular04_137s_1080p30.mp4 및 .srt.
Aₜ=diag(2,t); 작은 양수와 정확한0을 구분하며, 랭크는 정확한0에서만 감소한다. 차원은 출력 이미지 공간의 차원을 말한다.
3D B=diag(2,s,t)의 타원체가 평면 영역과 선분으로 붕괴한다. 경계만이 아니라 영역·표본 격자를 사용한다.
저랭크 근사 A₁=diag(2,0)의 단위입력 최대 절대 오차는0.1이다. 설명용 분포는 랭크7→4, 제거한 가장 큰 값0.08이다.
주요 검수: 작은 양수와 정확한0, 영공간과 동일출력, 3D차원붕괴, 근사오차, 자막25구간, 전체길이·프레임.
검수 기록: qa/report.json / qa/contact_1.jpg–contact_3.jpg.
