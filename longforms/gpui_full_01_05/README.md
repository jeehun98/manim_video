# GPU 개론 1~5편 통합 롱폼

입력은 사용자가 지정한 `exports/gpui_1_long.mp4`부터 `gpui_5_long.mp4`까지다. 음성이 포함된 실제 파일을 순서대로 연결한다.

출력: `exports/gpui_1_5_long.mp4`, 1920×1080, 30fps, 751.633초(약 12분 32초), 음성 포함. 비디오는 재인코딩 없이 복사한다. 각 입력의 오디오를 해당 영상 길이까지 무음으로 채우고 이어 붙여 다음 편의 음성이 앞당겨지지 않도록 한다. 기존 편의 끝 여백·대본·화면은 유지한다.

`python longforms/gpui_full_01_05/build.py`

- manifest.json: 실제 소스 길이와 편별 시작 시각
- chapters.ffmetadata: MP4 내부 챕터 5개 (밀리초)
- youtube_description.txt: 유튜브에 붙여 넣을 소개·챕터·주제 설명 (챕터는 가까운 초로 반올림)
- verification.json: 최종 해상도·프레임 수·영상/음성 길이·챕터 검증

새 내레이션·중간 타이틀·예고를 추가하지 않는 단순 합본이다.
