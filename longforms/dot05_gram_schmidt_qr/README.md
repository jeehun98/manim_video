# 내적 LEVEL 05 — 그람–슈미트 직교화와 QR 분해

사용자 확정 원고와 41개 문장 종료 시각을 적용한 153초 영상.
9:16 쇼츠 1080×1920와 16:9 롱폼 1920×1080, 각각 30fps.
음원 미제공으로 자막이 포함된 무음 영상이다.

## 핵심 설명

원래 열벡터는 `a₁=(1,1)`, `a₂=(2,0)`이다.
첫 벡터를 정규화해 `q₁=(1,1)/√2`를 만든다.
둘째 벡터의 정사영 `(1,1)`을 빼면 `v₂=(1,−1)`이 남는다.
이를 정규화해 `q₂=(1,−1)/√2`를 얻는다.

`Q=[q₁ q₂]`, `R=[[√2,√2],[0,√2]]`로 두 원래 열을 복원한다.
`QᵀQ=I`, `QR=[[1,2],[1,0]]=A`다.
첫 방향은 원래 a₁과 같고, 둘째 방향을 직교화한다.
원래 두 벡터가 선형독립이므로 직교화 전후 모두 같은 R²를 생성한다.

## 제작·실행

대본 → 사용자 제공 종료 시각 → 템플릿 기반 11개 씬 명세 → 화면 → 미리보기 → 최종 렌더.

```powershell
python longforms/dot05_gram_schmidt_qr/build.py --preview
python longforms/dot05_gram_schmidt_qr/build.py
```

사용 환경: Python 3.12, Manim 0.21.0, FFmpeg·FFprobe, Malgun Gothic.
`--layout shorts` 또는 `--layout longform`은 해당 규격만 제작한다.
`--scene 04`는 정사영 제거 씬만 교체한다. 그 뒤 `--concat-only`로 조립한다.
`--resume`은 완성된 동일 규격의 씬을 재사용한다.

## 자료

- `storyboard.md`: 사용자 첨부 콘티 원문
- `master_script.md`, `narration.md`: 확정 원고와 문장 종료 시각
- `tts_script.txt`: 화면 변화 구간별 발음 원고, 시간·제목 없음
- `timing.json`, `captions.srt`: 41개 자막의 0–153초 타이밍
- `manifest.json`, `scenes.yaml`: 11개 독립 씬과 영상 규격
- `scenes/*/spec.md`, `script.txt`, `scene.py`: 씬 계약·TTS·Manim 진입점
- `visuals.py`: 정규화·정사영 제거·직교 검사·공간 보존·Q/R 구성
- `build.py`: 렌더·자막 합성·concat·프레임 수와 길이 검증

정규화는 같은 방향에서 길이만 바꾼다. 잔차는 정사영 끝점에서 원래 끝점으로
먼저 그린 뒤 방향과 길이를 보존해 원점으로 평행이동한다.
Q의 단위벡터는 길이 1로 유지하고 복제 화살표에 R의 계수를 곱한다.
공간 비교에서는 두 평면에 같은 색을 사용한다.
행렬 원소는 열별로 색을 맞춰 R열과 원래 A열의 대응을 표시한다.
영상에는 이전 편 복습·다음 편 예고를 추가하지 않는다.

## 결과

- `exports/dot05_gram_schmidt_qr_153s_shorts_final.mp4`
- `exports/dot05_gram_schmidt_qr_153s_longform_final.mp4`
- 동일 이름의 `.srt`

미리보기는 `_preview` 접미사다. 최종 검증 메타데이터는 `render_report_both.json`이다.
