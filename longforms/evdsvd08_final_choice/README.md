# 행렬 분해 이상형 월드컵 ⑧ — 최종 선택

사용자 확정 대본·문장 종료 시각 기준 **149초**,30개독립씬.세로1080×1920·가로1920×1080,30fps.자막포함무음(TTS음원미제공).

대본 `master_script.md` → 씬별 `spec.md`·`script.txt` → 확정시각 `timing.json` → 실제좌표Manim → 씬별프레임검증 → concat.

```powershell
python longforms/evdsvd08_final_choice/prepare.py
python longforms/evdsvd08_final_choice/data.py
python longforms/evdsvd08_final_choice/build.py --preview
python longforms/evdsvd08_final_choice/build.py --layout both
python longforms/evdsvd08_final_choice/verify_final.py
```

한씬수정: `--scene 16 --layout shorts`,전체재결합: `--concat-only`.

출력: `exports/evdsvd08_final_choice_149s_shorts_final.mp4`, `exports/evdsvd08_final_choice_149s_longform_final.mp4`.동일시각SRT별도제공.

13–86초대표행렬A=diag(-2,1). EVD P=I,D=A. SVD U=diag(-1,1),Σ=diag(2,1),V=I.같은출력(-2,0)을부호있는고윳값또는비음수특이값과출력방향으로설명한다.고유방향과특이방향의일반적인일치를주장하지않는다.

89초에는별도7라운드B=diag(2,0),93초에는별도6라운드10×10근사예시로전환명시.최종누적스코어3:4는새로운8라운드승점을더하지않는다.사용자가명시적으로요청한최종편종합·회상구조를유지했다.마지막1초정지.

수학검산: `data.py`, `math_verification.json`.음수고윳값·정확한두분해·직교기저·특이값비음수·거듭제곱·별도정보소실·rank5오차·7라운드점수확인.
