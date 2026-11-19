# 감마함수 2장 — 감마함수는 어떻게 구성되는가

거듭제곱과 감소하는 지수함수의 곱을 부분적분해 팩토리얼의 재귀를 얻는다. 실수 지수에 대응하는 넓이를 그린 뒤 로그 볼록성이 주는 유일성을 설명한다. 43문장, 독립 장면 11개, 214초, 1920×1080, 30fps. 음원 미제공으로 무음이며 화면 자막을 포함한다.

```powershell
python longforms/gamma_chapter_02/build.py --preview --scene 08
python longforms/gamma_chapter_02/build.py
```

최종 영상은 `exports/gamma_chapter_02_long.mp4`에 저장한다. 1장 마지막 화면의 수식 배치를 공유한다. 마지막 장면의 절반 팩토리얼 구도는 `half_factorial_frame()`에 정의한다.

- [확정 대본](master_script.md), [타이밍](timing.json), [별도 자막](captions.srt), [발음 원고](tts_script.txt)
- [장면 인덱스](scenes.yaml), [제공 콘티](storyboard.md)
- 거듭제곱과 지수의 곱은 지수가 −1보다 클 때 적분이 수렴한다. 부분적분의 경계항에는 지수가 양수라는 조건을 표시한다.
- 정수값과 재귀를 유지하는 비교 곡선에는 양의 1주기 인자 `1+a sin(2πx)`를 사용한다. 보어–몰레루프 정리의 초기값은 `Γ(1)=1`이다. [NIST DLMF §5.5(iv)](https://dlmf.nist.gov/5.5.iv)
