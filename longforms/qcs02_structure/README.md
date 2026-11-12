# EP.02 · 양자컴퓨터도 빠르지 못한 문제가 있다

사용자가 제공한 31문장 종료 시각을 적용한 161초·20씬 영상. 가로 1920×1080 / 세로 1080×1920, 60fps, 각각 9,660프레임. 전체 내레이션 자막을 포함하며 음원 미제공으로 무음이다.

```powershell
py -3.12 scripts/render.py qcs02 --preview
py -3.12 scripts/render.py qcs02
py -3.12 longforms/qcs02_structure/build.py --layout longform --preview --scene 13 14 15
py -3.12 -m longforms.qcs02_structure.verify
```

최종 파일은 `exports/qcs02_long.mp4`, `exports/qcs02_short.mp4`이며 `qcs02_long_v1_161s.mp4`, `qcs02_short_v1_161s.mp4`도 저장한다. 미리보기는 `_preview` 접미사를 사용한다. `--ending standalone|join`은 전체 본문과 161초를 보존한다.

`master_script.md`·`script.json`·`timing.json`은 확정 대본과 시각, `scenes.yaml`은 씬 인덱스다. 각 씬의 `scene.py`·`spec.md`·`script.txt`는 독립 렌더와 교체를 지원한다. `physics_model.py`는 나머지 수열·최소 주기·gcd·조건부 입력 상태·QFT와 선택된 측정 사례를 계산한다. `prepare.py`는 대본·자막·명세를 재생성한다.

1편의 도형·타이밍·자막·레이아웃·렌더 검증 방식을 재사용한다. 새 코드는 수열, 인수 추출, QFT 및 비교 장면에 집중한다. 두 비율을 늘리거나 잘라서 만들지 않는다. 빌더는 해당 씬과 공통 의존 파일의 해시가 맞는 클립만 재사용한다. 씬 프레임 수, 출력 해상도·길이·전체 디코딩, 문장 자막 시각·안전 영역을 자동 검사한다. 실제 검수 기록은 render_report_*.json·visual_review.json에 저장한다.

참고 자료: [Grover 최적성 원논문](https://arxiv.org/abs/quant-ph/9711070), [IBM Quantum의 Shor 설명](https://quantum.cloud.ibm.com/learning/en/modules/computer-science/shors-algorithm), [순서 찾기와 고전 후처리](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/shor-algorithm). 수학적 적용 범위와 단순화는 brief.md에 기록한다.
