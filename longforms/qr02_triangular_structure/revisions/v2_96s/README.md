# QR 2편 — 공간의 차원이 만드는 위삼각 구조 (96초 수정본 v2)

- 사용자 제공 새 대본·문장 종료 시각: 96초, 23개 문장, 24개 독립 교체 가능 컷.
- 이전 98초 원본은 상위 폴더에 보존한다. 이번 버전은 새 원고·새 시각만 사용한다.
- 쇼츠 1080×1920 / 가로형 1920×1080, 각 30fps. 음원 미제공으로 무음·화면 자막 및 별도 SRT.
- 질문 이후 행렬을 숨기고 원점→직선→평면→3차원 공간을 구축한다. 51초부터 계수를 R의 열로 정리한다.
- a₁=(1,1,0), a₂=(0,2,0), a₃=(1,2,2), 선형독립·양의 대각 규약.

## 실행

```powershell
python longforms/qr02_triangular_structure/revisions/v2_96s/build.py --preview
python longforms/qr02_triangular_structure/revisions/v2_96s/build.py
```

출력: exports/qr02_triangular_structure_v2_96s_shorts_final.mp4 및 exports/qr02_triangular_structure_v2_96s_longform_final.mp4.

--scene 09 등으로 컷별 렌더 후 --concat-only로 결합한다. --layout shorts 또는 longform으로 한 버전만 제작한다.

## 제작 기준

- 직선과 평면은 다음 차원이 추가되어도 남아 있다.
- 원래 벡터는 흰색, q₁ 파랑·q₂ 초록·q₃ 주황. 투영·부분공간 보라.
- q₂는 a₂의 기존 방향 성분을 제거한 잔여 벡터를 정규화해 얻는다. q₃도 평면 투영 제거·평행이동·정규화를 구별한다.
- 마지막 비교는 같은 좌표 모델의 직선·평면·공간을 두 화면에 동일하게 그린다. 공통 회전으로 aᵢ를 qᵢ로 바꾸지 않는다.
- 0의 원인은 뒤 직교 방향과 앞 벡터가 수직이라는 사실로 명시한다.
- 복습·예고 없음. 길이는 새 사용자 종료 시각 96초에 고정한다.
- 각 script.txt가 공유하는 문장은 timing.json을 기준으로 한 번만 발화한다. 실제 음원 싱크는 미검증.

자료: storyboard.md 원문, narration.md·master_script.md·tts_script.txt 새 확정 원고, timing.json·captions.srt 새 시각, scenes.yaml·manifest.json·scenes/*/spec.md 컷 인덱스. base.py·helpers.py·visuals.py는 이 폴더 안에서 완결되는 구현이다.


## 최종 검증

두 영상 모두 96.000초·30fps·2,880프레임. 새 원고 23문장·24컷. 각 22개 대표 시각을 검수했다. 쇼츠 평면/행렬 간격과 가로형 도입 행렬 중앙 배치를 최종 수정한 뒤 재결합·재검증했다. verification.json, math_verification.json, qa/contact_*.jpg 참조.
