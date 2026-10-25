# EVD vs SVD — 가로형 1~8편 합본

입력은사용자가지정한 `exports/evdsvd_long_1.mp4`~`evdsvd_long_8.mp4`이며음성이포함된편집본이다. 이전무음렌더의길이를재사용하지않고각입력의실제영상프레임수로구간을계산한다.

```powershell
python longforms/evdsvd_full_01_08/build.py
```

원본영상프레임은재인코딩없이순서대로연결한다.각입력의음성을48kHz로통일하고영상보다짧은끝부분을무음으로채운뒤연결하여누적싱크밀림을방지한다.원본의편별오프닝·엔딩·여백을유지한다.음성만AAC로재인코딩한다.

MP4내장챕터는프레임단위오프셋,유튜브설명챕터는그시작시각을초단위로내림해표시한다.정확시각은 `chapters.json`에기록한다.

출력: `exports/evdsvd_long_1-8_full.mp4`, `exports/evdsvd_long_1-8_youtube_description.txt`, `exports/evdsvd_long_1-8_chapters.txt`.전체오디오·비디오디코딩검사와챕터·길이·프레임검사는 `verification.json`에기록한다.
