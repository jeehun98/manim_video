# 감마함수 1장 — 팩토리얼을 확장한다는 것

세 물체의 배열에서 출발해 팩토리얼을 함수로 보고, 실수로 확장할 때 보존할 재귀 관계를 찾는다. 제공된 20개 문장 종료 시각을 기준으로 독립 장면 7개를 조립한다. 97초, 16:9, 1920×1080, 30fps, 화면 자막 포함. TTS 음원 미제공으로 무음이다.

```powershell
python longforms/gamma_chapter_01/build.py --preview --scene 04
python longforms/gamma_chapter_01/build.py
```

최종 결과는 `exports/gamma_chapter_01_long.mp4`에 저장한다. 수식과 자막에는 각각 Cambria Math와 Malgun Gothic을 사용한다. 수식 렌더는 감마함수 쇼츠의 표현을 재사용한다.

- [확정 대본](master_script.md), [타이밍](timing.json), [자막](captions.srt), [발음 원고](tts_script.txt)
- [장면 인덱스](scenes.yaml)와 [제공 콘티](storyboard.md)
- 정수값 보간 예시는 `sin(πx)`, 실수 재귀도 보존하는 예시는 1주기인 `sin(2πx)`를 사용한다. 확장의 정의역을 0 이상으로 잡아 재귀는 `F(x+1)=(x+1)F(x)`로 표시한다.
- 마지막 2초는 두 규칙의 비교 구도를 유지한다. 후속 장에서 같은 배치를 사용할 수 있도록 `transition_rules()`에 화면 요소를 모았다.
