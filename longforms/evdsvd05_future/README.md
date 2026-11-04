# 행렬 분해 이상형 월드컵 ⑤ — 미래 예측

사용자 확정 대본·문장 종료 시각 기준 **130초**. 세로1080×1920 및 가로1920×1080,30fps. 자막 포함 무음.

`master_script.md` → `scenes/*/spec.md`·`script.txt` → 확정 시각 `timing.json` → Manim 독립 씬 → 프레임 검증 → 최종 concat.

```powershell
python longforms/evdsvd05_future/prepare.py
python longforms/evdsvd05_future/build.py --preview
python longforms/evdsvd05_future/build.py --layout both
python longforms/evdsvd05_future/verify_final.py
```

`--scene 14 --layout shorts`로 한 씬만 교체 후 `--concat-only`로 재결합한다.

출력: `exports/evdsvd05_future_130s_shorts_final.mp4`, `exports/evdsvd05_future_130s_longform_final.mp4`. SRT 별도 제공.

수학적 검산은 `math_verification.json`. 원 콘티의 후보 행렬1.25 대신 대본과 일치하는2를 처음부터 사용한다. SVD는 별도 예시임을 명시하며, 실제 반복 변환과 특이값 제곱의 불일치를 보여준다.
