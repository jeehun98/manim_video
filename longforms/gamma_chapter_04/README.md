# 감마함수 4장 — 확률분포에서 감마함수가 등장하는 이유

가우스 함수의 정규화에서 출발해 대기 시간의 감마분포와 실수 형태 매개변수로 이어진다. 제공된 40문장, 독립 장면 11개, 225초, 1920×1080, 30fps. 음원이 없어 무음이고 화면 자막을 포함한다.

```powershell
python longforms/gamma_chapter_04/build.py --preview --scene 08
python longforms/gamma_chapter_04/build.py
```

최종 영상은 `exports/gamma_chapter_04_long.mp4`에 저장한다. 손님의 도착은 발생률 1인 포아송 과정으로 모델링하며, 정수가 아닌 양의 형태 매개변수는 분포의 모양을 나타낸다. 화면의 곡선은 유한 범위를 그리고, 표시한 전체 넓이는 정의역 전체의 적분을 뜻한다. 마지막 구도는 `probability_transition()`에 정의한다.

[대본](master_script.md) · [타이밍](timing.json) · [자막](captions.srt) · [발음 원고](tts_script.txt) · [장면 인덱스](scenes.yaml) · [콘티](storyboard.md)

감마분포의 밀도 식과 형태 매개변수 범위는 NIST의 표준형을 따른다. [NIST 감마분포](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366b.htm)
