# QR 3편 — QR 분해의 대각선에 부피가 숨어 있는 이유

- 사용자 확정 대본·문장 종료 시각: 108초, 25문장, 27개 독립 교체 가능 컷.
- 첨부 콘티의 약 110초 임시 배분 대신 사용자 종료 시각을 적용한다.
- 쇼츠 1080×1920 / 가로형 1920×1080, 각 30fps.
- 음원 미제공으로 무음·화면 자막 영상 및 별도 SRT.
- 단위 정육면체의 모든 꼭짓점에 동일한 선형변환을 적용한다. R을 먼저, Q를 나중에 적용한다.
- 실제 예시 A=[[1,0,1],[1,2,2],[0,0,2]]. |det A|=4, 양의 대각 QR에서 √2×√2×2=4.

## 실행

```powershell
python longforms/qr03_diagonal_volume/build.py --preview
python longforms/qr03_diagonal_volume/build.py
```

기본 실행은 두 화면비를 모두 렌더·결합한다. --scene 17 등으로 해당 컷만 렌더하고 --concat-only로 재결합한다. --layout shorts 또는 longform으로 한 버전만 제작한다.

출력은 exports/qr03_diagonal_volume_108s_shorts_final.mp4 및 exports/qr03_diagonal_volume_108s_longform_final.mp4.

## 자료와 검증

storyboard.md는 사용자 원문, narration.md·master_script.md·tts_script.txt는 확정 대본, timing.json·captions.srt는 사용자 종료 시각이다. scenes.yaml·manifest.json·scenes/*/spec.md는 27개 컷의 목적·시각·소스다. base.py·visuals.py는 독립적인 이 프로젝트 구현이다.

원고의 영문·숫자 표기는 화면·자막에 유지하고 TTS 원고만 발음 표기로 작성했다. 컷 경계를 가로지르는 문장은 timing.json에 따라 한 번만 발화한다. 실제 음원 싱크는 음원 미제공으로 미검증이다.

math_verification.json은 A=QR, 직교성, 행렬식과 대각 곱, 전단의 넓이·부피 보존, 새 시각 연속성의 수치 검증 결과다. verify_final.py는 최종 영상 프레임 수와 해상도·길이를 검증하고 대표 프레임을 qa/에 추출한다.


## 최종 검증

두 최종본 모두 108.000초·30fps·3,240프레임. 세로 1080×1920, 가로 1920×1080. 각 23개 대표 시각의 프레임 검수 완료. 25문장 새 종료 시각 연속성, A=QR, Q 직교성·부피 보존, 대각 곱4, 평면 전단 넓이2 및 공간 전단 부피4의 수치 검증 통과. 음원 미제공으로 무음·자막 영상.
