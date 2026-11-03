# GPU 개론 03 — 스위치의 연결이 어떻게 논리 연산이 될까?

사용자 확정 원문 34문장·164초·14개 독립 씬. 가로 1920×1080 / 세로 1080×1920, 30fps. 음원 미제공으로 무음·전체 문장 자막 영상.

직렬·병렬 스위치에서 연결 조건을 발견하고 CMOS NAND의 실제 레일 연결을 추적한다. NAND로 만든 NOT·AND·OR와 XOR의 배선을 비교한 뒤, 고정 회로·면적·지연·에너지라는 물리적 제약까지 연결한다.

## 자료

- `storyboard_reference.md`: 사용자 상세 콘티 원문.
- `narration.md`, `master_script.md`, `tts_script.txt`: 원문·확정 시각·발음 원고.
- `timing.json`, `captions.srt`: 사용자 문장별 종료 시각.
- `scenes.yaml`, `manifest.json`: 14개 씬 인덱스와 확정 길이.
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬별 명세·TTS 대본·독립 Manim 클래스.
- `logic_model.py`: 화면에 그리는 트랜지스터 연결·NAND netlist.
- `check_logic.py`: 네 입력 조합과 NOT·AND·OR·XOR의 진리표, 레일 간 단락 없음, 34개 시간 경계 검증.
- `scene_engine.py`: 공통 벡터 도형·회로·애니메이션·단일 자막 객체.
- `brief.md`: 조건·생략 범위·기술 참고 자료.

## 실행

프로젝트 루트에서 Manim 0.21.0·FFmpeg·Malgun Gothic 사용.

```powershell
python longforms/gpui03_logic_connections/prepare.py
python longforms/gpui03_logic_connections/check_logic.py
python longforms/gpui03_logic_connections/build.py --preview
python longforms/gpui03_logic_connections/build.py
```

`--layout longform` / `--layout shorts`로 레이아웃 선택, `--scene 8`로 한 씬 렌더. `--resume`은 프레임 수가 맞는 기존 씬을 재사용하므로 소스를 수정한 씬은 명시적으로 재렌더해야 한다.

결과:

- `exports/gpui03_logic_164s_longform_final.mp4`
- `exports/gpui03_logic_164s_shorts_final.mp4`

둘 다 30fps·4920프레임·164초. 씬별 무음 영상 정규화 후 concat한다. 추후 음원 제공 시 확정 시간 안에서 씬별 mux 후 concat한다. 영상에 자막을 포함하고 별도 SRT는 자동 이중 표시를 피하도록 `_captions.srt`로 저장한다.

검수: `python longforms/gpui03_logic_connections/inspect_frames.py [--preview]`, `python longforms/gpui03_logic_connections/inspect_caption_boundaries.py [--preview]`. 실제 인코딩 영상의 주요 장면과 모든 자막 경계 전·해당·후 프레임을 추출한다. 최종 포맷과 프레임 확인은 `verification_final.json`, 논리 검증은 `qa/logic_verification.json`에 기록한다.
