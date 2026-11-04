# GPU 개론 6~10편 통합 롱폼

원본: exports/gpui_6_long.mp4부터gpui_10_long.mp4까지사용자가지정한음성포함파일을순서대로연결한다. 재제작한무음final영상이나gpui06_long.mp4등다른이름의파일은사용하지않는다.

출력: exports/gpui_6_10_long.mp4. 1920×1080,30fps. 영상은H264스트림복사로재인코딩하지않는다. 음성은각원본의영상길이까지무음패딩한뒤연결해AAC192kbps로기록한다. 원본영상끝부분과편사이간격은유지한다.

실행: `python longforms/gpui_full_06_10/build.py`.

manifest.json에원본별실제길이와시작시각,chapters.ffmetadata에다섯챕터,verification.json에합본검증값을저장한다. youtube_description.txt에는실제합본시작시각을기준으로한챕터목록을둔다.
