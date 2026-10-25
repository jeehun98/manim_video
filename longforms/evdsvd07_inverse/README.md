# 행렬 분해 이상형 월드컵 ⑦ — 역변환

확정 원문과 사용자 문장 종료 시각 기준 **142초**,27개독립씬. 세로1080×1920·가로1920×1080,30fps. 자막포함무음(TTS음원미제공).

대본 `master_script.md` → 각씬 `spec.md`·`script.txt` → 확정시각 `timing.json` → 실제좌표Manim → 씬별프레임검증 → concat.

```powershell
python longforms/evdsvd07_inverse/prepare.py
python longforms/evdsvd07_inverse/data.py
python longforms/evdsvd07_inverse/build.py --preview
python longforms/evdsvd07_inverse/build.py --layout both
python longforms/evdsvd07_inverse/verify_final.py
```

한씬수정은 `--scene 22 --layout shorts`,전체재결합은 `--concat-only`.

결과: `exports/evdsvd07_inverse_142s_shorts_final.mp4`, `exports/evdsvd07_inverse_142s_longform_final.mp4`. 동일시각SRT별도제공.

수학예시:전반A₁=diag(2,0.5),후반A₂=diag(2,0). 두입력(0.6,±0.8)→공통출력(1.2,0).의사역행렬선택(0.6,0).평면전체에서는입력선x=0.6전체가가능한해. 의사역행렬은잃은정보를되살리지않고최소제곱해중최소노름해를선택한다.

검산은 `data.py`·`math_verification.json`:역행렬,단위원의정확한변환,무어펜로즈4조건,121개해의노름,별도불일치출력b′=(1.2,0.8)의직교투영·잔차0.8확인.
