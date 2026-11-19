# 현재 쇼츠 제작 방식과 로컬 재현 가이드

2026-11-19 실제 소스 확인 기준. 최근 수학 쇼츠 `detgeom01`, `detperm01`, `deteff01`에 적용한 방식을 기록한다. 오래된 모든 시리즈가 같은 도구·파일명·fps를 쓰는 것은 아니다. 프로젝트 규칙은 [AGENTS.md](AGENTS.md), 롱폼은 [longforms/README.md](longforms/README.md)를 함께 읽는다.

## 1. 먼저 알아둘 차이

- 최신 기준은 **확정 대본과 실제 문장 종료 시각 → 독립 Scene별 제작 → 대표 Scene 미리보기 → 최종 렌더 → 검증 후 concat**이다. 하나의 긴 Scene만 렌더하는 방식과 다르다.
- 최근 수학 쇼츠는 **9:16, 1080×1920, 30fps**, 대표 미리보기는 **360×640, 30fps**다. 공통 모듈의 원래 기본값은 60fps이므로 그대로 가져오면 결과가 달라진다.
- 화면 자막은 `timing.json`의 `sentences[].text`를 Manim `Text`로 그린다. `captions.srt`를 수정하는 것만으로 영상 속 자막이 바뀌지는 않는다.
- 영상 빌더는 **무음 영상**을 만든다. `tts_script.txt`, SRT 또는 MP3가 같은 폴더에 있어도 자동 합성·결합하지 않는다.
- 에피소드 폴더 하나만 복사하면 부족하다. 아래의 공통 Python 모듈과 **import 시 읽는 JSON**까지 필요하다.
- 2026-11-19 확인 시 최신 세 에피소드 폴더는 Git에서 `??`(미추적) 상태였다. 다른 PC에서 clone/pull만 하면 이 파일들이 오지 않는다. 이동 전 추적 상태를 확인하고 소스·제작 자료를 빠짐없이 전달한다. 이 가이드 작성 과정에서 자동 add/commit은 하지 않았다.

## 2. 검증된 환경과 설치 확인

다음은 이 PC에서 조회한 기준값이다. 모든 OS에서 완전히 동일한 픽셀이나 MP4 바이트를 보장하는 잠금 파일은 아니다.

| 항목 | 확인된 값 |
|---|---|
| OS·셸 | Windows / PowerShell |
| Python | 3.12.7, `C:\Users\as042\AppData\Local\Programs\Python\Python312\python.exe` |
| Manim | 0.21.0, Cairo renderer |
| NumPy / SymPy / Pillow | 2.3.3 / 1.14.0 / 11.3.0 |
| FFmpeg / FFprobe | 9.0.1 full build, 둘 다 PATH에서 실행 가능 |
| LaTeX | MiKTeX-pdfTeX 4.21, MiKTeX 25.4 |
| dvisvgm | 3.4.3 |
| 한국어 폰트 | `Malgun Gothic` 설치 확인 |

`requirements.txt`는 현재 `manim>=0.19,<0.22` 범위만 지정한다. 이것만 설치하면 다른 Manim 버전과 다른 하위 의존성이 선택될 수 있다. 같은 기준을 원하면 0.21.0을 명시하고, 최종적으로 양쪽 PC의 전체 패키지 목록도 비교한다. SymPy는 검산, Pillow는 검수용 이미지 구성에 사용했다.

새 로컬 환경의 예시 명령이다. 프로젝트 루트에서 실행하고 이후에는 같은 Python 실행 파일을 계속 사용한다.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install "manim==0.21.0" "numpy==2.3.3" "sympy==1.14.0" "Pillow==11.3.0"

.\.venv\Scripts\python.exe -c "import sys,manim; print(sys.executable); print(sys.version); print(manim.__version__); print(manim.config.renderer)"
.\.venv\Scripts\python.exe -c "import manimpango; print('Malgun Gothic' in manimpango.list_fonts())"
ffmpeg -version
ffprobe -version
latex --version
dvisvgm --version
```

FFmpeg・LaTeX・dvisvgm・폰트는 pip 명령만으로 위와 같은 시스템 설치 상태가 되지 않는다. 별도로 준비하고 새 터미널에서 PATH를 확인한다. LaTeX 패키지 자동 설치가 필요하면 대표 Scene 렌더 전에 완료한다. 같은 폰트 이름이어도 파일 버전·Pango 등 렌더러 차이로 줄바꿈과 글자 폭이 달라질 수 있다. 다른 OS에서 폰트를 대체하면 해당 환경에서 자막과 본문을 다시 검수한다.

진단 자료가 필요할 때 다음 출력도 함께 비교한다. 이 명령은 조회만 한다.

```powershell
Get-Command python, ffmpeg, ffprobe, latex, dvisvgm
.\.venv\Scripts\python.exe -m pip freeze
Get-ChildItem Env:QCS*
git rev-parse HEAD
git status --short
```

`git rev-parse HEAD`가 같아도 미추적 파일이나 로컬 수정이 다르면 같은 소스가 아니다. 현재 루트에는 `manim.cfg`가 없으므로 다른 PC의 사용자 설정·추가 cfg·OpenGL 설정도 비교한다. 이 문서 때문에 기존 정상 환경을 재설치할 필요는 없다.

## 3. 다른 PC에 필요한 실제 파일

현재 최신 예제는 [episodes/deteff01_gaussian_elimination](episodes/deteff01_gaussian_elimination)이다.

```text
episodes/deteff01_gaussian_elimination/
  narration.md           확정 대본, 실제 기호 표기
  tts_script.txt         발음 원고, 화면 변화 구간별 빈 줄
  brief.md               학습 목표·수학적 조건·제작 기준
  spec.md                Scene별 주장과 화면 구성
  storyboard.md          사용자 제공 콘티 보관본
  timing.json            전체 길이·문장·Scene의 실제 시작/종료 시각
  captions.srt           외부 사용용 자막
  scene.py               Shot01 ... Shot08
  build.py               Scene별 렌더·검증·최종 조립
  prepare.py             위 자료 생성 도구, 렌더 자체에는 실행 불필요
  verification.json      해당 소스 제작 당시 수학 검산 기록
  render_report.json     해당 소스 제작 당시 영상 검수 기록
```

렌더에 필요한 에피소드 간·공통 의존성은 다음과 같다.

```text
episodes/deteff01_gaussian_elimination/scene.py
  → episodes/detperm01_permutation_sign/scene.py
      → episodes/detperm01_permutation_sign/timing.json
  → longforms/qcs01_speed/direction.py
      → longforms/qcs01_speed/script.json
      → longforms/qcs01_speed/layouts.py
      → quantum_series/shared/theme.py
      → quantum_series/shared/components.py
```

`direction.py`와 이전 에피소드의 `scene.py`는 import될 때 자기 JSON을 먼저 읽는다. 새 Scene에서 `data=DATA`로 바꿔도 이 파일들은 필요하다. 위 `qcs01`의 파일명은 양자컴퓨터용이지만, 현재는 `QCSScene`, 자막, 타이밍, 좌표 도우미를 재사용한다. `detperm01`의 `txt`, `eq`, `cards`, `selected`, 색상도 재사용한다. 폴더 이름만 바꾸거나 공통 파일을 최신의 다른 버전으로 대체하지 않는다.

등록 경유 실행에는 `scripts/render.py`도 필요하다. 가장 간단한 이동 방식은 생성물 폴더를 제외한 현재 작업 트리를 보존하는 것이다. `media/`, `exports/`, `.venv/`, `__pycache__/`는 Git 제외 대상이며 소스 전달 필수 항목은 아니다. 이 중 MP4가 없다는 이유로 소스가 없다고 판단하지 않는다. 기존 `render_report.json`도 과거 검수 기록이므로 현재 파일 존재나 새 환경의 렌더 성공을 대신하지 않는다.

`prepare.py`는 문서·JSON·경우에 따라 `build.py`를 다시 쓴다. 기존 결과를 재현할 때 먼저 실행하지 않는다. 생성기 수정 없이 출력만 고쳤다면 재실행으로 그 수정이 덮어써질 수 있다.

## 4. 새 영상의 제작 순서

1. 사용자 콘티에서 질문, 결론, 조건, 장면 순서를 읽고 `narration.md`, `tts_script.txt`, `brief.md`를 작성한다.
2. 사용자 검토로 대본을 확정한다. 구성이나 대본만 요청받은 단계에서는 영상·자막·추정 타이밍을 먼저 만들지 않는다.
3. 해당 확정 대본의 음원 또는 사용자가 제공한 문장 종료 시각으로 길이를 정한다. 이전 버전 시각·글자 수 비례 추정·3분 상한으로 실제 발화시간을 대신하지 않는다.
4. `timing.json`, `captions.srt`, Scene별 `spec.md`, `scene.py`를 맞춘다. 각 Scene의 주장은 하나로 두고 독립 렌더·교체 가능하게 만든다.
5. 새롭거나 변경된 대표 Scene만 360×640으로 확인한다. 수식·자막 겹침과 중요한 전환을 수정한다.
6. 최종 Scene들을 1080×1920으로 렌더하고 검증 후 concat한다.
7. 전체 시간·프레임·자막·수학 검산과 핵심 화면 검수 결과를 기록하고 실제 결과 파일을 전달한다.

일반적인 발음과 화면 표기는 분리한다. 화면·자막은 `2×2`, `R₂ ← R₂ − 2R₁`, `LU`, `det A`를 쓰고 발음은 TTS 원고에 쓴다. TTS 원고에는 읽지 않을 제목·Scene 번호·타임코드를 넣지 않고, 주요 화면 변화 사이에 빈 줄 하나를 둔다.

기본 서사는 해당 질문과 결론으로 완결하고 별도의 이전 편 복습·다음 편 예고·엔드카드를 추가하지 않는다. 사용자가 이미 확정한 문장에 이전 내용 언급이 있으면 임의로 수정하지 않는다. 긴 계산에는 원래 문제·현재 행렬·연산·불변량을 함께 남기고, 같은 수학적 객체의 변화로 설명한다. 쇼츠와 롱폼은 로직을 공유하되 화면비별 배치를 따로 설계한다.

## 5. 타이밍·프레임·자막 구현 계약

`timing.json`의 핵심 구조는 다음과 같다. 예시는 구조 설명용이며 실제 제작 시 확정 시각을 넣는다.

```json
{
  "title": "영상 제목",
  "duration": 10,
  "sentences": [
    {"start": 0, "end": 4, "text": "첫 문장"},
    {"start": 4, "end": 10, "text": "둘째 문장"}
  ],
  "scenes": [
    {"id": "01", "start": 0, "end": 10, "title": "주장 하나", "class": "Shot01"}
  ]
}
```

문장과 Scene은 각각 0부터 전체 길이까지 끊김·역전·중복 없이 이어진다. Scene 경계는 가능한 문장 경계에 둔다. `Shot01.shot=0`은 첫 Scene, `s01()`이 해당 화면을 만든다. `data`를 해당 에피소드 JSON으로 지정한다.

각 Scene의 `self.time`은 0에서 다시 시작한다. `offset=scene.start`이며, 자막은 `offset+self.time`으로 해당 문장을 찾는다. **`self.to(target)`에는 영상 전체 기준 누적 시각을 넣는다.** 앞의 애니메이션 시간을 포함해 그 목표를 넘으면 overrun 오류가 발생한다. 시간을 늘리거나 재생속도를 바꾸지 말고 주어진 발화 구간 안의 전환을 줄이거나 앞당긴다. 30fps에서는 애니메이션과 대기를 `1/30`초의 정수배에 맞추고 전체 프레임 수를 확인한다.

기존 `QCSScene` 재사용 시 다음을 놓치지 않는다.

```python
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene

shared.FPS = 30                 # to()의 프레임 계산
config.frame_rate = 30          # 실제 렌더 fps
config.background_color = '#0B1020'

class MyScene(QCSScene):
    data = DATA                 # 새 에피소드 timing.json
    replace = Scene.replace    # Manim의 replace와 공통 도우미 이름 충돌 방지
```

위 `config`, `Scene`, `DATA`는 `scene.py`에서 별도 import/정의한다. 예전 양자컴퓨터 제목·브랜드를 그대로 남기지 말고 현재 에피소드의 `setup()` 방식처럼 교체한다. 공통 코드를 다른 영상에 영향을 주도록 임의 변경하지 않는다.

| 항목 | 최근 수학 쇼츠 설정 |
|---|---|
| 논리 프레임 | 가로 9 × 세로 16 |
| 제목 / 핵심 규칙 | 보통 y=6.1 / y=5.05 |
| 본문 끝 상태 검사 | x는 −4.38~4.38, y는 −4.9~7.9 안 |
| 자막 중심 | y=−6.15 |
| 자막 패널 | 8.25 × 2.5 |
| 실제 자막 맞춤 한도 | 폭 7.65, 높이 2.15 |
| 자막 글꼴·크기 | Malgun Gothic, 기본 30 후 필요 시 축소 |
| 줄바꿈 | 단어 기준으로 약 26자마다 분리 후 실제 폭·높이 맞춤 |

본문 경계 자동 검사는 Scene **종료 상태**를 대상으로 한다. 전환 중 겹침·화면 이탈까지 전부 검증하는 것은 아니므로 대표 프레임을 눈으로 확인해야 한다. `captions.srt`의 줄바꿈과 영상 안의 자동 줄바꿈이 반드시 같지는 않다.

## 6. 정확한 실행 명령과 출력

아래는 가상환경을 쓰는 PowerShell 예시다. 기존 정상 Python을 사용한다면 실행 파일만 그 경로로 일관되게 바꾼다.

```powershell
# 대표 Scene 하나만 미리보기: 05는 Scene ID, 에피소드 번호가 아님
.\.venv\Scripts\python.exe episodes/deteff01_gaussian_elimination/build.py --preview --scene 05

# 최종 전체 영상: 권장 진입점
.\.venv\Scripts\python.exe scripts/render.py deteff01

# 동일한 최종 빌더를 직접 호출하는 방법
.\.venv\Scripts\python.exe episodes/deteff01_gaussian_elimination/build.py

# 전체 저해상도 영상이 필요할 때만
.\.venv\Scripts\python.exe scripts/render.py deteff01 --preview
```

| 실행 | 실제 출력 |
|---|---|
| 대표 Scene 미리보기 | `media/deteff01/preview/<hash>/Shot05/Shot05.mp4` |
| 최종 전체 | `exports/deteff01_short.mp4` |
| 전체 미리보기 | `exports/deteff01_short_preview.mp4` |
| 렌더 로그 | `media/deteff01/<mode>/<hash>/<ShotXX>/render.log` |
| 자막 기록 | `media/deteff01/<mode>/audit/01.json` 등 |
| 조립 목록 | `media/deteff01/<mode>/concat.txt` |

직접 `manim ... scene.py Shot01`만 실행하면 전체 영상이 아니라 첫 Scene만 만든다. 최신 예제는 `scripts/render.py`가 해당 `build.py`로 위임하므로 일반 에피소드의 단순 복사 방식과 출력 파일명이 다르다. 새 에피소드는 경로·클래스 등록뿐 아니라 필요하면 이 위임도 추가한다. 대본 단계에는 등록하지 않는다.

`exports/`에 사용자가 이름을 바꾼 영상, 음성 결합본 등이 있어도 빌더가 그 이름으로 출력하는 것은 아니다. 출력 경로는 현재 `build.py`를 기준으로 확인한다.

## 7. 캐시와 변경 Scene 재사용

현재 빌더는 `scene.py`, `timing.json`, `build.py`와 나열된 공통 소스의 SHA-256으로 저장 폴더를 정한다. 검증된 Scene MP4가 그 폴더에 있으면 재사용한다. Manim 호출의 `--disable_caching`은 Manim 내부 부분 애니메이션 캐시를 끄는 옵션이며, **빌더의 Scene MP4 재사용까지 끄지는 않는다.**

현재 해시는 환경 전체의 지문이 아니다. Python/Manim/FFmpeg/LaTeX/폰트 버전, 사용자 cfg, import 시 읽는 공통 `script.json`과 이전 편의 `timing.json` 등이 모두 포함되어 있지는 않다. 이 입력이나 환경이 달라졌다면 같은 해시 폴더라도 예전 영상을 그대로 재사용하지 않는다. 다른 PC에서는 기존 `media` 캐시를 옮기지 않고 새로 렌더하는 편이 명확하다.

재렌더를 강제해야 한다면 해당 mode/hash 폴더를 먼저 확인한 뒤 다른 이름으로 보관한다. 삭제나 이름 변경 전에 실행 중인 빌더가 없는지 확인한다. 원본 소스를 바꾸지 않고 결과를 재사용할 때에도 타이밍·레이아웃·렌더 설정까지 동일해야 한다.

에피소드 전체 소스가 해시에 들어가므로 Scene 하나 수정에도 모든 Scene의 해시가 바뀐다. 현재 빌더가 자동으로 변경 Scene만 판별하는 것은 아니다. 이전 클립을 새 해시로 옮길 때는 공통 함수·해당 Scene·타이밍·설정이 동일함을 비교하고 근거를 남긴다. 같은 길이나 같은 프레임 수만으로 재사용하지 않는다.

렌더를 건너뛴 캐시 클립은 자막 audit를 새로 만들지 않는다. audit가 이전 소스의 잔여 파일인지, 현재 클립과 짝인지도 확인한다.

## 8. 최종 검수와 완료 기준

현재 `build.py`가 자동 검사하는 항목:

- 각 Scene 및 합본의 무음 단일 비디오 스트림, 해상도, 30fps.
- 목표 길이 × 30과 정확히 같은 프레임 수, 컨테이너 길이 오차 약 0.017초 미만.
- 같은 순서의 클립을 FFmpeg `concat`·`-c copy`·`+faststart`로 조립한 결과.
- 합본 전체를 FFmpeg로 디코딩했을 때 오류 없음. 검증을 통과한 임시 MP4만 최종 경로로 교체.

`QCSScene`이 실제 렌더 중 검사·기록하는 항목은 자막 상하 경계, 크기·문장 인덱스, 본문 종료 상태의 경계다. 다음은 별도 확인이 필요하며 빌더가 전부 자동 보장한다고 생각하지 않는다.

- `timing.json` 문장·Scene 구간의 연속성과 전체 문장 누락 여부.
- 수학적 등식, 행 연산, 순열의 부호, 도형과 표시 수치의 일치.
- 주요 전환 중 겹침, 긴 자막의 읽기 크기, 행렬 원소의 화면 이탈.
- 최종 파일과 해당 소스의 검증 기록·해시 일치. 이전 보고서를 새 검수 결과처럼 사용하지 않기.

최근 `deteff01`의 기존 검수 기록은 162초, 4,860프레임, 1080×1920, 30fps, 35문장, 8개 Scene, 무음이다. 결과를 재현한 뒤 다음처럼 확인할 수 있다.

```powershell
ffprobe -v error -show_streams -show_format -of json exports/deteff01_short.mp4
ffmpeg -v error -i exports/deteff01_short.mp4 -f null -
```

대표 화면은 FFmpeg로 필요한 시각만 추출해 확인한다. 예를 들어 85초는 소거 결과, 104초는 순열 선택, 148초는 LU 연결이다. 수정된 대표 Scene 검수로 충분하면 전체 미리보기와 전체 프레임 추출을 반복하지 않는다.

## 9. 결과가 다를 때 확인할 순서

| 증상 | 먼저 볼 것 |
|---|---|
| 폴더·모듈·JSON 없음 | 최신 미추적 폴더 전달 여부, 위 import 의존성, 같은 커밋과 로컬 수정 |
| Manim import 실패 | pip에 쓴 Python과 실행 중 Python이 같은지 |
| 길이·fps가 다름 | `shared.FPS=30`과 `config.frame_rate=30` 양쪽, 사용자 cfg, 빌더 경유 여부 |
| 가로 화면 또는 다른 해상도 | import 전에 적용된 `QCS_LAYOUT=shorts`, `QCS_PREVIEW`, 실제 실행 경로 |
| 자막·수식 글꼴과 줄바꿈이 다름 | Malgun Gothic/Pango/LaTeX 버전, 대체 폰트, `timing.json` |
| SRT 수정이 영상에 안 보임 | 자막의 실제 입력은 `timing.json`이며 캐시도 갱신됐는지 |
| `replace` 관련 오류 | 기반 클래스에 `replace = Scene.replace`를 지정했는지 |
| `overrun` 또는 프레임 수 실패 | 전환 시간을 포함한 누적 시각, 1/30초 단위, 다른 fps 사용 |
| 수정했는데 예전 화면 | 외부 Scene 캐시, 해시에서 빠진 import 데이터·환경 변경 |
| LaTeX 렌더 실패 | `render.log`의 실제 종료 오류, 필요한 패키지·dvisvgm·PATH·쓰기 권한 |
| MP4가 안 보임 | 빌더의 실제 출력명과 `media` 경로, 렌더 완료 여부; 과거 보고서만 남았는지 |
| 음성이 없음 | 기본 무음 빌더의 정상 동작. 실제 음원 결합은 별도 단계 |

비교할 때는 사용한 명령, `sys.executable`, 버전 목록, 대상 `scene.py`·`timing.json`·공통 소스, `render.log`, `ffprobe` 결과를 함께 남긴다. 차이의 원인을 확인하기 전에 오래된 다른 시리즈의 기본 설정을 새 쇼츠에 섞지 않는다.
