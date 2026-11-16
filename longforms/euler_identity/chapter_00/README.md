# 오일러 항등식 — 0장 도입

- 사용자 확정 대본과 18문장 종료 시각 기준, 58초.
- 16:9 1920×1080, 30fps만 제작. 음원 미제공으로 무음, 전체 문장 자막 포함.
- 10개 독립 씬. 색상·상수 객체·단위원·복소평면·지수곡선은 visuals.py에서 공유.
- 소스와 설정의 SHA-256이 같은 씬만 렌더 재사용.
- 마지막 0과 1 배치는 1장 시작의 연결 기준이며, 1장 소스·음원은 아직 없음.

실행: `py -3.12 longforms/euler_identity/chapter_00/build.py`

대표 씬 확인: `py -3.12 longforms/euler_identity/chapter_00/build.py --preview --scene 8`

결과: `exports/euler_identity_ch00_58s_longform_final.mp4`

검증: `verification_final.json`. 문장 경계·씬 프레임 수·합본 길이·해상도·자막 범위를 자동 검사한다.
