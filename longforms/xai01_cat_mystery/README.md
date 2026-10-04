# 고양이를 알아본다는 것은 무슨 뜻일까? - Explainable AI

- ID: xai01
- 상태: 최종 5막 대본 반영, 각 막의 무음 화면 프로토타입 제작
- 길이: 13분 50초. 막별 사용자 측정 음성 총길이의 합이며 문장별 음원 정렬은 미확인.
- 화면: 미정. 템플릿의 가로형 1920×1080, 30fps를 후보로 둔다.
- 중심 질문: 정답을 맞힌 모델이 어떤 내부 단서와 상호작용에 의존했는지 어떻게 확인할까?

## 검토와 제작 순서

1. `master_script.md`의 막별 내레이션을 읽고 흐름과 표현을 수정한다.
2. 확정 대본을 독립 씬으로 분할하고 씬별 spec.md와 script.txt를 작성한다.
3. TTS를 생성·측정한 뒤 scenes.yaml에 확정 길이를 기록한다.
4. 확정 길이에 맞춰 화면을 만들고 씬별로 음성을 결합한다.
5. 씬들을 막별로 결합하고, 막별 영상을 전체 영상으로 결합한다.

막은 검토와 편집 단위이고, 실제 렌더 단위는 주장 하나를 담은 씬이다. 이렇게 하면 막 내부의 일부 화면도 독립 교체할 수 있다. 1막의 무음 화면 프로토타입을 작성했다. 사용자 요청에 따라 TTS 길이 확정은 이후 진행한다. 나머지 막의 씬 분할과 화면 제작은 미진행이다.

## 초안의 실험 표현

실제 모델과 데이터는 아직 선정하지 않았다. 본문의 실험은 설명용 시나리오이며 실제 관측을 보고하는 문장이 아니다. 영상에서 사용하려면 실제 실험으로 교체하거나 설명용 예시임을 화면에 명시한다. 점수 하락, 강건성 차이, feature 후보의 의미 등은 검증 전이다.

Hessian 구간은 중간 표현 h에 대한 스칼라 고양이 점수 s(h)의 국소 곡률을 다룬다. 파라미터에 대한 loss Hessian과는 변수와 대상 함수가 다르다. 본문 수식과 수학 조건은 검토용 주석이며 TTS에서 자동으로 읽지 않는다.

## 1막 화면 미리보기

실행: `.\.venv\Scripts\python.exe -m manim -ql --resolution 854,480 --fps 15 --media_dir media/xai01 longforms/xai01_cat_mystery/scenes/01_hook/scene.py Act01Hook`

최종 배포 해상도는 1920×1080, 30fps 후보이며 현재는 854×480, 15fps 검토용 렌더다.

## 사진 스타일 · 30fps 수정본

고양이를 AI 생성 사진 스타일 투명 PNG로 교체했다. 무늬 변화도 동일 고양이를 참조한 별도 생성 이미지다.

실행: `.\.venv\Scripts\python.exe -m manim -qh --resolution 1920,1080 --fps 30 --verbosity ERROR --media_dir media/xai01_photo longforms/xai01_cat_mystery/scenes/01_hook/scene.py Act01Hook`

검토 파일: `exports/xai01_act01_photo_1080p30.mp4`. 길이는 여전히 임시값이다.

## 1막 음성 총길이 반영

사용자가 측정한 음성 총길이 1분 51초에 맞춰 111초, 1920×1080, 30fps로 재렌더한다. 문장별 시각은 음원 없이 대본의 문자 수와 문장부호에 따른 상대 길이로 추정했다. 따라서 실제 음성의 문장 시작점과 정확히 정렬한 것은 아니다. 제목은 첫 문장에 겹쳐 시작하며 별도 무음 시간을 더하지 않는다.

`scenes/01_hook/captions.srt`는 새 화면 배분과 같은 시간으로 갱신한다. CSV는 사용자 요청으로 제거했다. `timing.json`은 렌더와 SRT가 공유하는 내부 설정이다. 배분 재생성: `.\.venv\Scripts\python.exe longforms/xai01_cat_mystery/scenes/01_hook/build_captions.py`.

렌더: `.\.venv\Scripts\python.exe -m manim -qh --resolution 1920,1080 --fps 30 --verbosity ERROR --media_dir media/xai01_111 longforms/xai01_cat_mystery/scenes/01_hook/scene.py Act01Hook`.

결과: `exports/xai01_act01_111s_1080p30.mp4`, 같은 이름의 `.srt`. 이미지 아래의 생성·설명 문구는 제거한 상태를 유지한다.

## 1막 화면 정보 보강본

같은 대본과 111초 시간 배분을 사용하며 24개 대본 구간에 화면 상태·강조·변형을 대응시킨다. 배경 A/B와 점수 변화, 역방향 반응의 예시, 모델별 비교와 조건, 후보 정보와 출력 사이의 경로, 내부 계산을 추가했다. SRT는 유지하고 CSV는 만들지 않는다. 이전 소스는 scenes/01_hook/scene_v1.py에 보존했다.

보강본: `exports/xai01_act01_rich_1080p30.mp4`, 같은 이름의 `.srt`.
렌더: `.\.venv\Scripts\python.exe -m manim -qh --resolution 1920,1080 --fps 30 --verbosity ERROR --media_dir media/xai01_rich_final longforms/xai01_cat_mystery/scenes/01_hook/scene.py Act01Hook`.

문장별 시각은 음원 정렬이 아닌 대본 길이에 따른 추정이다. 점수 막대와 반응 차이는 가정된 상황을 시각화하며 실제 측정 결과가 아니다.

## 2막 영상

사용자 측정 음성 총길이 2:26에 맞춘 146초, 1080p·30fps 무음 영상이다. 대본 전체 45개 문장을 24개 화면 구간에 배분했다. 문장별 시간은 대본 길이 기반 추정이다.

소스: scenes/02_input_changes/scene.py, 대본: script.txt, 자막: captions.srt, 화면 기준: spec.md, 내부 시간 배분: timing.json. CSV는 생성하지 않는다.

렌더: `.\.venv\Scripts\python.exe -m manim -qh --resolution 1920,1080 --fps 30 --verbosity ERROR --media_dir media/xai02 longforms/xai01_cat_mystery/scenes/02_input_changes/scene.py Act02InputChanges`.
결과: `exports/xai01_act02_146s_1080p30.mp4`와 같은 이름의 `.srt`.

## 3막 영상

사용자 측정 음성 총길이 2:34에 맞춘 154초, 1080p·30fps 무음 영상이다. 47개 문장을 22개 화면 구간에 배분했다. 문장별 시각은 대본 길이 기준 추정이다.

소스: scenes/03_internal_clues/scene.py. 같은 폴더의 script.txt, captions.srt, spec.md, timing.json을 사용한다. CSV는 생성하지 않는다.

렌더: `.\.venv\Scripts\python.exe -m manim -qh --resolution 1920,1080 --fps 30 --verbosity ERROR --media_dir media/xai03 longforms/xai01_cat_mystery/scenes/03_internal_clues/scene.py Act03InternalClues`.
결과: `exports/xai01_act03_154s_1080p30.mp4`와 같은 이름의 `.srt`.

## 4막 영상

사용자 측정 음성 길이 3:13에 맞춘 193초, 1080p·30fps 무음 영상이다. 64개 문장을 26개 구간으로 배분했다. 문장별 시각은 대본 길이로 추정했다.

A/B 개입 비교 뒤에 내부 방향에 대한 반응 곡선, gradient의 접선, Hessian의 곡면·단면 비교를 보여준다. 모든 수치와 함수는 설명용이며 실제 모델 측정 결과가 아니다. 수학 조건과 곡면 정의는 scenes/04_intervention/spec.md에 기록했다.

렌더: `.\.venv\Scripts\python.exe -m manim -qh --resolution 1920,1080 --fps 30 --verbosity ERROR --media_dir media/xai04 longforms/xai01_cat_mystery/scenes/04_intervention/scene.py Act04Intervention`.
결과: `exports/xai01_act04_193s_1080p30.mp4`와 같은 이름의 `.srt`. CSV는 생성하지 않는다.

## 마지막 5막과 전체 연결

최종 구성은 5막이다. 앞서 계획한 6·7막의 계산 경로·XAI·결론은 마지막 5막에 통합했다. 이전 7막 대본은 drafts/master_script_7acts.md에 보존했다.

5막은 사용자 측정 총길이 3:46, 226초이다. 77개 문장을 24개 구간에 배분하며 메시지 앞의 ‘연우’는 화자 표기로 간주했다. 고양이·강아지·여우의 공통 특징, 다른 모습·자세·배경, 복합 feature, 기능·의미 구분, 반복 개입과 층별 경로, 처음 CAT와 제목 회귀를 보여준다.

렌더: `.\.venv\Scripts\python.exe -m manim -qh --resolution 1920,1080 --fps 30 --verbosity ERROR --media_dir media/xai05 longforms/xai01_cat_mystery/scenes/05_meaning_and_paths/scene.py Act05MeaningAndPaths`.
5막 결과: `exports/xai01_act05_226s_1080p30.mp4`와 같은 이름의 `.srt`.

전체 연결: `.\.venv\Scripts\python.exe longforms/xai01_cat_mystery/concat_silent.py`.
전체 결과: `exports/xai01_full_silent_1080p30.mp4`, 전체 SRT는 같은 이름의 `.srt`와 프로젝트 captions.srt. 총 830초, 1080p·30fps, 무음이다. 코덱·해상도와 프레임 수를 확인하고 영상 패킷을 재인코딩 없이 연결한다.

문장별 시간은 대본 길이로 추정했고 실제 음원과의 정밀 동기화는 미확인이다. CSV는 생성하지 않는다.
