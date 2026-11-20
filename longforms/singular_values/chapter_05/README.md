# 특잇값 5장 — 행렬식과 공간의 부피

사용자 확정 29문장·151초. 16:9 1920×1080 30fps.
음원 미제공으로 무음, 화면 자막과 별도 SRT 포함. 일곱 연속 그룹 독립 렌더.

- narration.md / tts_script.txt: 확정 원고·발음 원고
- storyboard_source.md: 사용자 콘티
- timing.json / captions.srt: 문장 종료 시각
- scenes/01–07: 독립 소스·spec.md
- scene_engine.py / visual_common.py: 애니메이션과 기존 도형 재사용

```powershell
python longforms/singular_values/chapter_05/build.py
python longforms/singular_values/chapter_05/build.py --preview --scene 5
python longforms/singular_values/chapter_05/build.py --preview --scene 7
python longforms/singular_values/chapter_05/build.py --scenes 7
python longforms/singular_values/chapter_05/verify_video.py
```

결과: exports/singular05_151s_1080p30.mp4 및 .srt.
넓이·부피는 원판과 내부 영역, 실제 구면의 반투명 표면으로 표현한다. 3D 변환은 diag(2,1,0.75)이며 부피 배율은1.5다.
특잇값은 내림차순 표기. 행렬식의 절댓값을 제곱근 단계에서도 유지한다. 반사 비교는 동일한 비대칭 표본점과 순서로 표현한다.
세 타원의 비교는 동일 척도. 극단적 배율은 s=100^p, 1/s를 하나의 변수로 제어한다. 전체 화면의 점선 폭은100으로 고정하고, 실제 두께는 ×1000 중앙 단면으로 표시한다. 주황색 중심선은 위치 표시이며 실제 두께가 아니다.
마지막 출력 오차는 개념도로 명시하며 역변환·조건수 계산은 진행하지 않는다.
검수: qa/report.json 및 qa/contact_1.jpg–contact_3.jpg.
