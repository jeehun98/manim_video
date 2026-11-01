# GPU LEVEL 01–11 통합 롱폼

사용자가 지정한 `exports/gpuh_1.mp4`~`gpuh_11.mp4`의 영상과 음성을 숫자 순서대로 스트림 복사한다. 원본별 길이와 끝부분을 그대로 보존한다.

```powershell
python longforms/gpuh_full_01_11/combine.py
python longforms/gpuh_full_01_11/combine.py --verify-only
```

기본 출력은 `exports/gpuh_full_01_11_longform.mp4`. 기존 출력을 덮어쓰지 않는다. 영상 1920×1080 / 30fps / H.264, 음성 AAC / 44.1kHz / mono. 입력의 실제 프레임 수로 챕터 시작 시각을 계산하고 MP4에 11개 챕터를 넣는다. 유튜브용 표시는 직전 정수 초로 내린다.

`youtube_description.txt`에는 도입 설명, 11개 타임라인, 구간별 학습 내용이 있다. 같은 내용을 `exports/gpuh_full_01_11_youtube_description.txt`로도 저장한다. 원본보다 음성이 먼저 끝나는 꼬리 구간도 그대로 유지한다.

`verification.json`에 최종 길이·프레임 수·음성 정보·전체 디코딩 검사·챕터 검증 결과를 기록한다. `chapters.json`에는 원본별 길이와 정확한 누적 시작 시각이 있다.
