# 자연의 최적화 1~5편 통합 롱폼

`exports/nature_1.mp4`부터 `nature_5.mp4`까지 순서대로 결합했다. 사용자가 지정한 음성 포함 가로형 파일을 사용하며, 영상과 음성은 재인코딩 없이 보존한다. 편별 챕터를 포함한다.

출력: `exports/nature_full_01_05_longform.mp4`.
해상도 1920×1080, 30fps, H.264/AAC. 원본 영상 길이의 합은 815.3초(13분 35.3초), 최종 컨테이너 길이는 AAC 타임스탬프를 포함해 815.323초다. 총 24,459프레임.

재실행: `python longforms/nature_full_01_05/combine.py`.
기존 출력은 덮어쓰지 않으며 `--verify-only`로 재검증할 수 있다. 원본별 길이와 챕터 위치는 `verification.json`, 결합 명령 로그는 `concat.log`, 전체 디코딩 결과는 `decode.log`·`decode_progress.txt`, 장면 확인은 `qa/chapters.png`에 있다.

## 통합 썸네일

내장 image_gen 도구로 제작했다. 확정 프롬프트는 `thumbnail_prompt.txt`. `exports/nature_full_01_05_thumbnail.png`는 생성 원본 1672×941, `exports/nature_full_01_05_thumbnail_4k.png`는 Lanczos 업스케일한 3840×2160 출력본이다. 문구는 「자연의 최적화」와 「서로 다른 법칙, 하나의 수학」, 중앙 수식은 δJ=0이다.
