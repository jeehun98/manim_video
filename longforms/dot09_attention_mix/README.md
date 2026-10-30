# 내적 LEVEL 09 — Attention: 정보의 점수와 결합

사용자 확정 원고36문장과 문장 종료 시각을 적용한154초 영상. Query–Key 내적으로 점수3,2를 계산하고 √2 스케일링과 Softmax를 거쳐 약67%,33% 가중치를 얻는다. 별도의 Value(4,0),(0,2)를 결합해 약(2.68,0.66)을 만든다.

세로1080×1920 및 가로1920×1080,30fps. 음원 미제공으로 무음이며 한국어 자막을 포함한다. SRT와 화면 전환별 발음 원고를 별도로 제공한다.

```powershell
python longforms/dot09_attention_mix/build.py --preview
python longforms/dot09_attention_mix/build.py
python longforms/dot09_attention_mix/check_math.py
python longforms/dot09_attention_mix/check_delivery.py
```

Manim0.21.0, Python3.12, FFmpeg/FFprobe, Malgun Gothic. 수식은 Text로 그려 LaTeX를 요구하지 않는다. `--scene 08 --layout shorts`로 한 씬을 다시 렌더하고 `--concat-only`로 결합할 수 있다. `--resume`는 완료된 동일 해상도·프레임 수의 씬을 재사용한다.

`manifest.json`의11개 독립 씬과 각 `spec.md`에 주장·대본·실제 길이·화면 순서를 정의했다. `timing.json`은36개 원본 발화 구간이다. `visuals.py`가 화면을 만들고 `build.py`가 렌더·결합·자막 처리를 한다. 기존 에피소드용 `scripts/render.py`와 별도로 실행한다.

문장 예시의 고양이·소파는 개념도이며 실제 토큰 경계나 측정값이 아니다. 숫자 예제는 별도로 구별해67%·33%를 해당 단어에 붙이지 않는다. 원점수·스케일링 점수·가중치의 막대는 단계 이름을 명시한다. 모든 가중치·벡터는 같은 정확한 Softmax 수치로 계산하고 표시만 반올림한다. Key와 Value를 서로 다른 역할과 벡터로 표현한다. 정사영의 단위벡터·잔차 직교 조건을 Attention에 적용하지 않는다. 같은 각도에서 Key 길이만2배로 바꿔 점수가3에서6으로 변하는 장면을 포함한다. 행렬식 Softmax는 각Query행에 적용한다.

결과: `exports/dot09_attention_mix_154s_shorts_final.mp4`, `exports/dot09_attention_mix_154s_longform_final.mp4`. 검증 자료: `qa_math.json`, `preview_report_both.json`, `render_report_both.json`, `qa_delivery.json`.
