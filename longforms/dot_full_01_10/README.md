# 내적 LEVEL 01–10 통합 롱폼

사용자가 지정한 음성 포함 파일 `exports/dot_long1.mp4`부터 `dot_long10.mp4`까지 숫자 순서로 연결한다. 기존 무음 렌더나 비슷한 이름의 다른 출력본을 사용하지 않는다. 각 파일 끝의 여유 구간도 보존한다.

출력: `exports/dot_full_01_10_longform.mp4`.
1920×1080,30fps,H.264/AAC. 영상·음성을 재인코딩하지 않는 stream copy 방식으로 품질을 보존한다. 총42,406프레임, 영상 길이1,413.533초(23분33.533초). MP4에10개 챕터도 포함한다.

```powershell
python longforms/dot_full_01_10/combine.py
python longforms/dot_full_01_10/combine.py --verify-only
```

기존 출력은 덮어쓰지 않는다. 검증은 원본과 출력의 프레임 합·해상도·fps·음성 존재·전체 길이·10개 챕터 위치·전체 디코딩을 확인한다. 기록은 `verification.json`, `concat.log`, `decode.log`에 있다.

유튜브 설명은 `youtube_description.txt`와 `exports/dot_full_01_10_youtube_description.txt`에 저장한다. 원본의 정확한 영상 프레임 수를 누적해 챕터를 계산하며, MP4 챕터는1/30초 정밀도, 설명의 mm:ss는 해당 경계보다 늦지 않도록 초 단위로 내림한다. 편별 길이를 대본에서 추정하지 않는다.
