# 특잇값 0~3장 — AICF에서 잘못 제작된 자료 보관

2026-11-20에 AICF/artifacts에서 복사했습니다. 활성 Manim 제작본이 아닙니다.

- 0장 63초, 1장 100초, 2장 121초, 3장 180초.
- render.py는 Pillow/NumPy로 프레임을 생성하고 FFmpeg로 인코딩합니다. Manim Scene 소스가 아닙니다.
- visual.mp4는 무음 영상, singular-values-chN.mp4는 Windows 한국어 합성 음성 결합본입니다.
- timing.json은 사용자 제공 문장 종료 시각과 대본, narration.srt는 자막입니다.
- 장 사이 상대 import가 있으므로 네 폴더를 함께 유지해야 합니다.
- 이후 제작은 manim_video/AGENTS.md와 longforms/README.md의 씬별 제작 규칙을 따라 진행합니다.
- AICF 원본은 보존했습니다.
