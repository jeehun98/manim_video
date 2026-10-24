# 행렬 분해 이상형 월드컵 ⑥ — 복원 정확도

사용자 확정 대본·문장 종료 시각 기준 **133초**, 23개 독립 씬. 세로1080×1920·가로1920×1080,30fps. 자막 포함 무음(TTS 음원 미제공).

전체 대본 `master_script.md` → 씬별 `spec.md`·`script.txt` → 확정 시각 `timing.json` → Manim 씬별 렌더 → 프레임 확인 → concat.

```powershell
python longforms/evdsvd06_reconstruction/prepare.py
python longforms/evdsvd06_reconstruction/data.py
python longforms/evdsvd06_reconstruction/build.py --preview
python longforms/evdsvd06_reconstruction/build.py --layout both
python longforms/evdsvd06_reconstruction/verify_final.py
```

`--scene 08 --layout shorts`로 해당 장면만 교체하고 `--concat-only`로 재결합할 수 있다.

결과: `exports/evdsvd06_reconstruction_133s_shorts_final.mp4`, `exports/evdsvd06_reconstruction_133s_longform_final.mp4`. 동일 시각 SRT도 별도 제공.

실제 수치 실험은 `data.py`, 검산 결과는 `math_verification.json`. B=[[2,3],[0,1]]를5번대각배치. 고윳값2의5성분만남긴EVD오차7.071068, 큰특이값5성분만남긴SVD오차1.207883. 격자의색상은모든패널동일한−6..6범위. 대칭행렬의예외는고윳값절댓값순선택조건을표시한다.

원소별제곱오차를최소화하는절단SVD의성질은Eckart–Young–Mirsky정리다. 후보막대몇개의비교는예시이며증명을대신하지않는다. `data.py`는rank1·재합성·직교성·잔여특이값제곱합·252개성분선택과전체NumPy SVD를검산한다.
