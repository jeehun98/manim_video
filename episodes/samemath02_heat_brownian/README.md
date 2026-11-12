# 서로 다른 문제, 같은 수학 02

**열의 확산과 브라운 운동은 왜 같은 방정식을 따를까?** 사용자 제공 34문장·177초를 그대로 사용한 쇼츠(9:16)와 롱폼(16:9)이다. 두 버전은 장면 로직과 문장 종료 시각을 공유하며 화면비별로 배치한다. 음원 미제공으로 무음이고 전체 자막을 영상에 포함한다.

열은 균질한 1차원 매질의 확산 해로, 입자 위치는 고정 난수 시드의 무편향 보행으로 그렸다. 히스토그램과 이론 확률밀도를 구별한다. 흐름과 보존으로 공통 확산방정식을 유도하며, 온도와 확률밀도의 의미·계수는 구분한다. 상세 조건은 `brief.md`에 기록했다.

```powershell
python episodes/samemath02_heat_brownian/prepare.py
python scripts/render.py samemath02 --preview
python scripts/render.py samemath02
```

결과: `exports/samemath02_short.mp4`, `exports/samemath02_long.mp4`. 미리보기에는 `_preview`가 붙는다. 최종본은 1080×1920·1920×1080, 30fps다. 재생용 쇼츠의 길이는 사용자 지정 177초다.
