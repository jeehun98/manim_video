# 양자역학 시리즈 작업 방식

다른 로컬 환경의 Codex도 이 문서와 루트 `AGENTS.md`를 읽고 기존 방식으로 이어 작업한다. 최신 구현 예시는 `episodes/ep03_rutherford/`이며, 실제 파일과 사용자 지시를 우선한다.

## 제작 원칙

- 쇼츠 한 편이 롱폼의 한 Chapter가 된다. `현상과 질문 → 기존 설명의 한계 → 새로운 접근 → 결론과 남은 물리적 질문`으로 독립적으로 완결한다.
- 이전 편 복습, 다음 편 예고, 구독 유도, 별도 엔드카드는 넣지 않는다. 같은 도형과 물리적 질문으로 자연스럽게 연결한다.
- **대본 확정 → 해당 대본의 음원 또는 사용자 문장 종료 시각으로 길이 확정 → 씬 spec → 화면 제작 → 미리보기 → 최종 렌더** 순서다. 수정 대본의 시간을 추정하거나 이전 타이밍을 재사용하지 않는다.
- 음원이 없으면 무음·전체 문장 자막으로 제작하고 무음임을 명시한다. TTS 원고는 화면 변화 구간마다 빈 줄로 나누며 제목·타임코드를 넣지 않는다.

## 화면의 느낌

- 차분한 과학 다큐멘터리형 2D 모션그래픽. 짙은 네이비 배경, 흰색 본문, 절제된 이동·Fade·Transform을 사용한다.
- 폰트·색·기본 좌표는 `shared/theme.py`를 재사용한다. 기본 폰트는 **Malgun Gothic**, 배경은 `#0B1020`, 에너지 강조는 금색 `#FFD166`이다. 같은 대상의 색과 의미를 유지한다.
- 화면당 주요 문구 하나를 중심으로, 설명하는 대상 자체를 움직여 보여준다. 문구·범례·자막이 겹치지 않게 한다.
- **9:16 1080×1920 / 16:9 1920×1080, 모두 30fps**. 애니메이션은 공유하되 위치·크기는 layout에서 따로 정한다. 늘리기나 크롭으로 다른 화면비를 만들지 않는다.
- 세로는 중앙·위아래 비교, 가로는 실험과 해석의 좌우 배치를 활용한다. 마지막은 물리적 장면과 질문을 남기고 연결용 프레임도 저장한다.

## 구현과 검수

- 편별 소스는 `episodes/<episode>/`, 공통 도형·물리 계산은 `shared/`, 챕터 조립은 `longform/`에 둔다.
- `script.json`이 확정 대본·문장 시각의 원본이다. `brief.md`, `narration.md`, `tts_script.txt`, 씬별 `spec.md`를 먼저 작성한다. **씬 하나 = 주장 하나 = 독립적으로 렌더·교체 가능한 영상**으로 만든다.
- EP.03의 `direction.py`는 애니메이션, `layouts.py`는 배치, `physics_model.py`와 공통 모듈은 계산, `scenes/*/scene.py`는 독립 진입점이다.
- `to(target)`과 기존 빌더의 프레임 처리를 재사용한다. Manim의 `--disable_caching`과 씬별 프레임 검사를 유지하며, 시간 초과는 해당 구간의 연출을 줄여 해결한다.
- 그래프·경로는 가능한 한 실제 식으로 계산한다. 실측과 이론값, 개념도와 실제 축척, 당시 가설과 현대 해석을 구분한다. 물리 조건·출처·생략한 가정은 편별 README에 기록한다.
- 두 비율의 미리보기에서 주요 장면·자막·마지막 프레임을 확인한 뒤 최종 렌더한다. 길이·해상도·30fps·정확한 프레임 수·전체 디코딩을 검사하고 실제 수행한 검수만 기록한다.

## 다른 환경에서 실행

검증한 조합은 Python 3.12.7 / Manim 0.21.0 / FFmpeg·ffprobe 9.0.1 / Malgun Gothic이다. 사용할 Python에 루트 `requirements.txt`를 설치하고 FFmpeg·ffprobe와 한글 폰트 사용 여부를 확인한다. 폰트를 바꾸면 두 비율의 문구 폭을 다시 검수한다.

저장소 루트에서 아래 명령을 실행한다. `python`은 Manim을 설치한 Python이어야 한다.

```powershell
python scripts/render.py quantum03 --preview
python scripts/render.py quantum03
python scripts/render.py quantum03_shorts
python scripts/render.py quantum03_longform
```

`quantum01`, `quantum02`도 같은 형식이다. 한 씬만 수정할 때는 해당 편 `build.py`의 `--scene`을 사용한다. 나머지 중간 영상이 없으면 먼저 전체를 렌더한다. 기본 종료 모드는 쇼츠 `standalone`, 가로 `join`이며 대본과 길이는 둘 다 유지한다.

완성본은 `exports/quantumNN_shorts.mp4`, `exports/quantumNN_longform.mp4`, 미리보기는 `_preview.mp4`다. EP.03은 각 `_ending.png`도 저장한다. `media/`, `exports/`, `.venv/`는 Git 제외 대상이므로 다른 환경에 없을 수 있다. 미커밋·미추적 소스까지 전달했는지 확인하고 가상환경은 새로 만든다.

현재 EP.01은 86초, EP.02는 101초, EP.03은 105초까지 완성했다. EP.04는 미제작이다. 새 편의 렌더 ID는 `scripts/render.py`에 등록하고, 실제 완성된 가로판만 `longform/chapters.json`에 추가한다. 조립은 `python quantum_series/longform/assemble.py`로 실행한다. 세부 물리 조건과 실행 옵션은 각 편의 README를 참고한다.
