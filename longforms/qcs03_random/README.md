# EP.03 · 무작위 데이터에서도 양자컴퓨터는 압도적으로 빠를까?

사용자 제공 28문장 종료 시각 기준 155초·20씬. 가로1920×1080 / 세로1080×1920, 60fps, 각각9,300프레임. 전체 내레이션 자막 포함, 음원 미제공으로 무음.

```powershell
py -3.12 scripts/render.py qcs03
py -3.12 longforms/qcs03_random/build.py --layout shorts --preview --scene 06 08 12 15 17
py -3.12 -m longforms.qcs03_random.verify
```

최종 결과: `exports/qcs03_long_v1_155s.mp4`, `exports/qcs03_short_v1_155s.mp4`. 기본 파일 `qcs03_long.mp4`, `qcs03_short.mp4`도 저장한다. `--ending standalone|join` 모두 확정155초와 자막 전체를 유지한다.

공통 테마·자막·타이밍·레이아웃은 1편에서 재사용하며, 2편의 소스 해시 기반 씬별 빌더를 적용했다. 가로·세로는 위치와 크기를 따로 정하고 화면을 늘리거나 자르지 않는다. 대표 씬만 저해상도로 확인한 후 최종 렌더하며 전체 미리보기는 중복 제작하지 않는다. 자동 검사 결과는 render_report_*.json, 시각 검수는 visual_review.json에 기록한다.

대본·명세·타이밍은 prepare.py에서 재생성할 수 있다. scenes/01~20의 scene.py는 각각 독립 렌더·교체 단위다. physics_model.py 및 verify.py는 XOR 조회의 기저128개·중첩·노름 보존과 개념 예시 확률 및 확정 타이밍을 확인한다. 상세 적용 범위와 참고 원논문은 brief.md에 기록했다.
