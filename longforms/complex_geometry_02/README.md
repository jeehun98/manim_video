# 복소평면에 숨겨진 기하학 — 구간 02

사용자 확정 288초·57문장, 16개 독립 씬. 1920×1080·30fps. 음원 미제공: 전체 자막 포함 무음. 구간 01과 동일한 설정의 별도 파트이며 아직 합치지 않음.

- 최종 렌더·조립·검증: `python longforms/complex_geometry_02/build.py`
- 대표 씬: `python longforms/complex_geometry_02/build.py --preview --scene 02 05 06 07 08 14 15 16`
- 결과: `exports/complex_geometry_02.mp4`
- 확정 시각: timing.json, 원고: master_script.md, 자막: captions.srt, 씬별 기준: scenes/*/spec.md.
- 공통 도형·자막·프레임 타이밍은 구간 01과 기존 qcs01 도구를 재사용.
- 금속판의 과도 상태는 T=50+30x+12exp(-β²t)J₀(βr), β는 J₀의 첫 양의 영점. 무차원 열확산계수 1의 열방정식 해. 색상만 임의 보간하지 않음.
- 등각 변환 F=ζ+0.4ζ². 원판의 각 재료점 좌표와 온도가 함께 이동하며 온도는 U(ζ)=50+30Reζ.
- 원본 참고 이미지 27장은 references/에 제공 순서대로 보존. 이후 구간은 아직 생성하지 않음.
