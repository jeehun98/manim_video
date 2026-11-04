# QR 2편 — 왜 R의 아래쪽은 모두 0일까?

현재 사용 버전은 [새 대본 기준 96초 수정본 v2](revisions/v2_96s/README.md)이다. 아래 내용과 이 폴더의 소스·영상은 이전 98초 대본의 보존 자료다. `scripts/render.py qr02_shorts`와 `qr02_longform`은 새 수정본을 제작한다.

- 사용자 확정 대본과 문장 종료 시각: 98초, 22개 문장, 25개 독립 교체 가능 컷.
- 세로 쇼츠 1080×1920 / 가로형 1920×1080, 각 30fps.
- 음원 미제공으로 무음·화면 자막 영상. SRT 별도 제공.
- 3차원 모델을 직교 투영한다. 벡터의 수직 관계를 내적 계수와 R의 해당 칸에 연결한다.
- a₁=(1,1,0), a₂=(0,2,0), a₃=(1,2,2). 양의 대각 규약, 선형독립인 열벡터.

## 실행

```powershell
python longforms/qr02_triangular_structure/build.py --preview
python longforms/qr02_triangular_structure/build.py
python longforms/qr02_triangular_structure/build.py --layout shorts --scene 09
```

기본 실행은 두 버전을 모두 렌더·결합한다. --scene으로 수정한 컷만 렌더하고 --concat-only로 다시 결합한다. --resume은 길이·fps를 검증한 기존 컷을 재사용한다.

출력은 exports/qr02_triangular_structure_98s_shorts_final.mp4 및 exports/qr02_triangular_structure_98s_longform_final.mp4.

## 자료

storyboard.md: 사용자 콘티 원문. narration.md·master_script.md·tts_script.txt: 확정 원고. timing.json·captions.srt: 사용자 종료 시각. scenes.yaml·manifest.json·scenes/*/spec.md: 25개 컷의 주장·길이·소스. base.py: 좌표·레이아웃 공통 기능. visuals.py: 편별 장면. build.py: 렌더·프레임 검증·결합.

컷별 script.txt에 걸쳐 있는 문장은 timing.json에 따라 한 번만 발화하며, 개별 합성으로 중복하지 않는다. 실제 음원 싱크는 음원 미제공으로 미검증이다. prepare.py는 사용자 확정 원고·시각과 컷 인덱스를 재구축한다. 편별 화면은 visuals.py를 수정한다.

## 최종 검증 (2026-10-25)

두 최종본 모두 98.000초·30fps·2,940프레임. 세로 1080×1920, 가로 1920×1080. 각 19개 대표 시각의 최종 프레임을 검수했다. 두 번째 벡터 복원 컷의 시점·성분 라벨 조정 후 재결합하고 재검증했다. A=QR, QᵀQ=I, R=QᵀA, 양의 대각, 앞부분 공간 보존, 22개 문장 타임라인 연속성 검증 통과. verification.json·math_verification.json 및 qa/contact_*.jpg 참조.
