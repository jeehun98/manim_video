# 서로 다른 문제, 같은 수학 01

**가장 가까운 점과 가장 그럴듯한 답은 왜 같을까?** 사용자 제공 30문장·문장 종료 시각 160초에 맞춘 쇼츠(9:16)와 롱폼(16:9) 영상이다. 동일한 대본·색상·애니메이션 로직을 사용하며 화면비별 배치를 따로 한다. TTS 음원이 제공되지 않아 두 영상은 무음이고 자막은 영상에 포함된다.

소스: `script.json`(확정 문장·종료 시각), `brief.md`(수학·제작 기준), `scene.py`(Manim), `build.py`(두 화면비 렌더). `prepare.py`는 `narration.md`, `tts_script.txt`, `timing.json`, `captions.srt`를 확정 대본에서 재생성한다.

```powershell
python episodes/samemath01_least_squares/prepare.py
python episodes/samemath01_least_squares/build.py --preview
python episodes/samemath01_least_squares/build.py
python scripts/render.py samemath01
```

결과: `exports/samemath01_short.mp4`, `exports/samemath01_long.mp4`. 미리보기에는 `_preview`가 붙는다. 화면은 30fps, 최종본은 1080×1920과 1920×1080이다. 원고의 ‘쇼츠’는 콘텐츠 형식명이며 길이는 사용자 지정 160초를 그대로 따른다.
