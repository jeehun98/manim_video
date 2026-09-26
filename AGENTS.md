# 프로젝트 작업 안내 (2026-09-26 현재 체크아웃 기준)

이 저장소는 주어진 콘티를 Manim으로 구현해 세로형 교육 영상을 만드는 프로젝트다. 작업을 시작할 때 README의 전체 목록을 현재 존재하는 에피소드로 간주하지 말고 실제 파일을 먼저 확인한다.

## 현재 실제 구조

- `episodes/prune01_zero_weights/`부터 `prune04_hardware_aware/`까지: 현재 구현된 Pruning & Sparsity 4편. 각 폴더에 `scene.py`(영상), `narration.md`(구간별 대본), `brief.md`(제작·내용 기준), `captions.srt`(자막), `tts_script.txt`(음성 합성용 발음 표기)가 있다.
- `episodes/prune_series/visuals.py`: Pruning 시리즈의 색상, 한글 폰트, 해상도, 공통 시각 요소. 새 편을 같은 시리즈로 만들면 우선 참고한다.
- `scripts/render.py`: 에피소드 ID를 Manim scene에 연결하고 `media/<ID>/`에 렌더한 뒤 `exports/<ID>.mp4`로 복사한다. `--preview`는 `exports/<ID>_preview.mp4`를 만든다.
- `requirements.txt`: Python 의존성 범위 `manim>=0.19,<0.22`.
- `archive/`: 이전 버전과 프로토타입 보존 자료. 새 영상의 활성 소스가 아니다.
- `gpu_series/`: 이전 GPU 시리즈의 공통 컴포넌트만 남아 있다.
- `media/`, `exports/`, `.venv/`, `__pycache__/`는 Git 제외 대상이며 현재 체크아웃에 없을 수 있다. MP4가 보이지 않아도 소스 누락을 뜻하지는 않는다.

README와 `scripts/render.py`에는 ReLU, GPU, LA, SVD, EML, FlashAttention, Quantization 등 과거 시리즈의 항목이 많이 남아 있지만, 현재 Git 추적 파일에는 그 에피소드 폴더가 없다. `scripts/prepare_svd.py`도 현재 없는 `episodes/svd_series/data.py`를 참조한다. 해당 항목을 렌더하거나 이전 시리즈를 이어갈 때는 소스 복구 여부를 먼저 확인한다.

## 콘티에서 새 영상까지

1. 사용자에게 받은 콘티의 학습 목표, 주장, 수학적 조건, 장면 순서, 전체 길이와 구간별 시간을 먼저 읽고 기존 편의 `brief.md` 형식으로 제작 기준을 정리한다. 불명확한 내용은 기존 시리즈의 표현과 구별해 확인한다.
2. `episodes/<ID>_<slug>/`에 `narration.md`, `brief.md`, `scene.py`, 필요 시 `captions.srt`, `tts_script.txt`를 둔다. 화면·자막·대본은 원래 숫자와 영문 표기를 쓰고, 한국어 발음 표기는 `tts_script.txt`에 둔다.
3. 기존 Pruning 편처럼 장면에서 구간 목표 시각으로 진행한다. `Scene.time`과 각 구간의 누적 시간을 맞추고, `to(target)`의 초과 오류를 해결한다. 화면 요소가 세로 프레임을 벗어나거나 한글 자막을 가리지 않는지 미리보기로 확인한다.
4. `scripts/render.py`의 `EPISODES`에 새 ID, 상대 `scene.py` 경로, Scene 클래스 이름을 등록한다. README에도 새 에피소드의 실제 파일과 실행 명령을 기록한다.
5. `python scripts/render.py <ID> --preview`로 360×640 미리보기를 만들고 화면·타이밍을 검토한 뒤 `python scripts/render.py <ID>`로 1080×1920, 30fps 최종본을 만든다. 영상은 기본적으로 무음이며 TTS와 SRT는 별도 자료다.

## 노트북 환경 확인

Windows에서 프로젝트 루트를 작업 위치로 열고, 사용할 Python에 Manim을 설치한다. 예: `py -m venv .venv`, `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, `.\.venv\Scripts\python.exe scripts/render.py prune01 --preview`. 렌더 전 `python -m manim --version`, FFmpeg 사용 가능 여부, `Malgun Gothic` 한글 폰트를 확인한다. 렌더가 실패하면 설치한 Python과 실행에 사용한 Python이 같은지 확인한다.

2026-09-26 확인 시 이 환경의 기본 `python`은 `C:\msys64\mingw64\bin\python.exe`(3.11.9)이며 Manim이 설치되지 않았고, `ffmpeg` 명령도 PATH에서 찾을 수 없었다. 따라서 이 체크아웃에서 렌더 성공 여부는 아직 검증되지 않았다. 이는 저장소 구조에 대한 설명이며 다른 컴퓨터의 설치 상태를 뜻하지 않는다.
