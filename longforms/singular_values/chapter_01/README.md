# 특잇값 1장 — 방향이 아닌 길이의 변화

사용자 확정 18문장·100초. 16:9 1920×1080 30fps.
음원 미제공으로 무음, 화면 자막 및 별도 SRT 포함.
콘티의 다섯 연속 그룹을 독립 렌더하고 하나의 프레임 시계로 결합한다.

- narration.md / tts_script.txt: 사용자 확정 대본과 발음 원고
- storyboard_source.md: 사용자 원문 콘티
- timing.json / captions.srt: 제공된 문장 종료 시각
- scenes/01–05: 독립 소스와 spec.md
- scene_engine.py: 공통 애니메이션, visual_common.py: 0장에서 재사용한 도형

```powershell
python longforms/singular_values/chapter_01/build.py
python longforms/singular_values/chapter_01/build.py --preview --scene 4
python longforms/singular_values/chapter_01/build.py --scenes 4
python longforms/singular_values/chapter_01/verify_video.py
```

결과: exports/singular01_100s_1080p30.mp4 및 .srt.
0장의 전단행렬 B를 이번 장에서는 A로 표시한다. 전 구간 동일 행렬을 각 입력에 한 번씩 적용하며 반복 거듭제곱을 하지 않는다.
65–77초는 하나의 각도 변수에서 입력·출력·길이·그래프를 함께 계산한다. 77–82초에는 지정한 두 방향을 비교하고 82–87초에는 16개 방향을 동시에 변환한다.
출력 궤적 연결선이나 특잇값 숫자를 공개하지 않는다. 마지막 단위 원은 그대로 유지한다.
검수: qa/contact.jpg 및 qa/report.json.
