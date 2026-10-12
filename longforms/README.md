# 롱폼 제작 규격

이 문서는 다른 컴퓨터나 새 Codex 세션에서도 같은 방식으로 롱폼을 이어 만들기 위한 최소 규격이다. 새 프로젝트는 `_template/`을 복사해 `longforms/<ID>_<slug>/`로 만든다.

## 핵심 원칙

- **씬 하나 = 주장 하나 = 독립적으로 교체 가능한 완성 영상**으로 만든다.
- 12~18분 영상은 보통 20~40초짜리 씬 30~40개로 나눈다. 실제 TTS 길이를 우선한다.
- 제작 순서는 `전체 대본 → Scene Specification → 씬별 TTS → TTS 길이 확정 → Manim 화면 → 씬별 mux → 최종 concat`이다.
- 롱폼 화면은 잦은 교체보다 한 대상을 `등장 → 관찰 → 변화 → 해석`하는 흐름을 우선한다.
- 한 씬을 수정할 때 다른 씬을 다시 렌더하지 않아도 되어야 한다.

## 최소 구조

```text
longforms/<ID>_<slug>/
├─ README.md                 # 제목, 목표, 실행법, 현재 상태
├─ master_script.md          # 전체 내레이션과 논리 흐름
├─ scenes.yaml               # 씬 순서와 파일·클래스·길이 인덱스
├─ scenes/
│  ├─ 01_hook/
│  │  ├─ spec.md             # 목적, 주장, 화면, 타임라인, 연결
│  │  ├─ script.txt          # TTS에 직접 넣는 문장
│  │  ├─ scene.py            # Manim 장면
│  │  ├─ narration.mp3       # 생성물, Git 제외
│  │  ├─ visual.mp4          # 무음 렌더, Git 제외
│  │  └─ final.mp4           # 음성 결합본, Git 제외
│  └─ 02_.../
├─ concat.txt                # 최종 결합 순서
├─ captions.srt
└─ longform_final.mp4        # 생성물, Git 제외
```

아직 음성과 영상이 없는 초기 단계에서는 `README.md`, `master_script.md`, `scenes.yaml`, 각 씬의 `spec.md`와 `script.txt`만 있어도 된다.

## 작업 계약

1. `master_script.md`에서 전체 주장과 순서를 먼저 확정한다.
2. 각 씬에 주장 하나만 배정하고 `spec.md`를 작성한다.
3. `script.txt`로 TTS를 생성한 뒤 실제 음성 길이를 잰다.
4. 측정한 길이를 `scenes.yaml`의 `duration_seconds`에 기록한다.
5. `scene.py`의 애니메이션을 그 길이에 맞춘다. 임의 정지 프레임이나 사후 속도 변경은 예외로 둔다.
6. 씬별 무음 영상과 음성을 mux하여 `final.mp4`를 만든다.
7. 모든 씬의 해상도, fps, 코덱, 오디오 형식을 통일한 뒤 순서대로 concat한다.
8. 수정 시 해당 씬만 다시 TTS·렌더·mux하고 최종 concat만 갱신한다.

## Scene Specification 필수 항목

각 `spec.md`에는 다음을 반드시 적는다.

- 목적과 핵심 주장
- 앞 장면에서 받은 내용
- TTS 원문과 확정 길이
- 화면 구성과 시간대별 애니메이션
- 화면 텍스트
- 시작 상태와 종료 상태
- 다음 장면으로 넘길 질문 또는 시각적 연결
- 수학적 조건, 과장 방지 문구, 출처가 필요한 주장

씬 템플릿은 [`_template/scenes/01_example/spec.md`](_template/scenes/01_example/spec.md), 전체 인덱스 예시는 [`_template/scenes.yaml`](_template/scenes.yaml)을 사용한다.

## 구현 시 주의

- 해상도와 화면비는 프로젝트마다 `scenes.yaml`에 명시한다. 기존 세로형 숏폼 설정을 롱폼에 무조건 재사용하지 않는다.
- 화면의 숫자·수식·영문 표기는 원문 그대로 두고, 한국어 발음용 변형은 `script.txt` 또는 별도 TTS 파일에서만 관리한다.
- TTS 대본은 화면 전환 구간마다 문단을 나눈다. 각 구간 사이에 빈 줄을 넣고, 읽지 않을 제목이나 타임코드는 통합 `tts_script.txt`에 넣지 않는다. 사용자 제공 문장별 종료 시각이 있으면 추정 배분 대신 해당 시각을 적용한다.
- `narration.mp3`, 씬별 MP4, 최종 MP4는 생성물이며 Git에 커밋하지 않는다.
- 렌더·mux·concat 자동화 스크립트가 추가되면 프로젝트 `README.md`에 정확한 실행 명령과 필요한 도구 버전을 기록한다.
- 현재 저장소의 `scripts/render.py`는 기존 에피소드용이다. 롱폼 지원이 구현되기 전에는 롱폼을 자동으로 처리한다고 가정하지 않는다.
