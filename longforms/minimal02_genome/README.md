# 모든 것이 필요할까? 02 — 최소 유전체

사용자 확정 대본 33문장과 문장 종료 시각 기준 **164초(2분 44초)**. 독립 씬 17개로 제작하며 세로 쇼츠·가로 롱폼은 같은 데이터에 별도 배치를 사용한다. 음원이 없어 **무음**, 전체 발화 자막 내장 및 SRT 별도 제공.

## 결과물과 실행

- `exports/minimal02_164s_shorts_final.mp4`: 1080×1920, 30fps
- `exports/minimal02_164s_longform_final.mp4`: 1920×1080, 30fps
- 같은 이름 `.srt`: 사용자 문장 종료 시각을 그대로 사용
- `_preview.mp4`: 세로 360×640 / 가로 854×480, 15fps

프로젝트 루트에서 Manim 0.21.0, FFmpeg, Malgun Gothic이 설치된 Python으로 실행:

```powershell
python longforms/minimal02_genome/build.py --preview
python longforms/minimal02_genome/build.py
python longforms/minimal02_genome/build.py --layout shorts --scene 9
python longforms/minimal02_genome/verify_caption_boundaries.py --layout shorts
python longforms/minimal02_genome/verify_caption_boundaries.py --layout longform
```

`--layout shorts|longform|both`, `--scene 1..17`, `--jobs 3`, `--concat-only` 지원. `build.py`는 씬별 렌더 → 프레임 수 확인 → concat → 단일 ASS 자막 합성 → 최종 해상도·프레임 수·길이 확인 순서로 실행한다. `_uncaptioned.mp4`는 자막 합성 이전 중간 산출물이다.

## 제작 자료

- `narration.md`, `master_script.md`, `tts_script.txt`: 원문 대본과 구간별 발음 원고
- `narration_timing.json`, `captions.srt`: 문장 종료 시각 33개
- `manifest.json`, `scenes.yaml`: 17개 독립 씬, 총 164초
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬별 주장·원문·시간·조건
- `storyboard_user.md`: 첨부 콘티 원문
- `scene_engine.py`: 모든 개념도·실험 상태·두 화면비
- `caption_pass.py`: Manim 객체 캐시와 독립적인 최종 단일 자막 트랙
- `inspect_frames.py`: 주요 장면 20개 표본 이미지 추출
- `verify_caption_boundaries.py`: 모든 문장 경계 직전·정각·직후와 마지막 프레임의 자막을 기준 영상과 비교
- `verification_final.json`, `caption_boundary_verification_*.json`: 최종 검증 결과

## 정확성 기준

유전자 블록은 실제 위치가 아닌 추상적 구성 요소다. 세포 전체를 무에서 합성했다고 표현하지 않으며, 기존 유전체의 재설계·합성과 수용 세포로의 도입을 구분한다.

A/B는 실제 유전자명을 사용하지 않는 **개념 모델**이다. 같은 원본의 독립 복제본에서 A만/B만/둘 다 제거한다. 하나의 기능을 대체·보완하는 모델은 합성 치사의 한 가지 설명이며, 모든 합성 치사의 원인이 유전자 기능 중복이라는 주장은 하지 않는다.

환경 비교는 같은 내부 합성 경로 결손에서 외부 공급만 바꾸는 가상 조건이다. 실제 성장 환경·대체 경로에 따라 필수성이 달라질 수 있다. 분열 장면은 현미경 영상의 정량적 재현이 아닌 형태 차이를 보여주는 개념도다.

473과 149는 **2016년 최초 발표** 기준이다. 유전자 배열은 실제 473칸 중 149칸을 강조하며 비율은 약 31.5%다. 현재까지 149개 모두 기능이 알려지지 않았다고 주장하지 않는다. 473개를 보편적인 생명 최소 유전자 수나 증명된 하한으로 제시하지 않는다.

## 확인한 1차 출처

- [Hutchison et al., Design and synthesis of a minimal bacterial genome, Science (2016)](https://www.jcvi.org/publications/design-and-synthesis-minimal-bacterial-genome)
- [JCVI의 2016년 발표: 473개 유전자와 149개 기능 미해명](https://www.jcvi.org/media-center/first-minimal-synthetic-bacterial-cell-designed-and-constructed-scientists-venter)
- [Pelletier et al., Genetic requirements for cell division in a genomically minimal cell, Cell (2021)](https://www.jcvi.org/publications/genetic-requirements-cell-division-genomically-minimal-cell)

실제 음원과의 청각적 동기 검토는 음원 수령 후 가능하다. 현재는 제공 시각과 화면·자막의 일치를 기준으로 제작한다.
