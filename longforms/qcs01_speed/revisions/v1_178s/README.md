# EP.01 · 양자컴퓨터는 왜 빠를까?

현재 작업 원본은 longforms/qcs01_speed/다. 확정 대본·34문장의 사용자 종료 시각을 유지한다. 두 영상 모두 178초·60fps·10,680프레임. 음원 미제공으로 무음이며 전체 내레이션을 하단 자막으로 표시한다.

```powershell
py -3.12 scripts/render.py qcs01 --preview
py -3.12 scripts/render.py qcs01
py -3.12 longforms/qcs01_speed/build.py --layout longform --preview --scene 12 15
py -3.12 longforms/qcs01_speed/build.py --layout shorts
```

- exports/qcs01_long.mp4: 1920×1080, 16:9, 자막 포함.
- exports/qcs01_short.mp4: 1080×1920, 9:16, 자막 포함.
- captions.srt: 사용자 문장 시각을 유지하는 별도 자막.

master_script.md·script.json은 확정 대본, scenes.yaml은 18개 독립 씬의 순서·길이 인덱스다. 각 씬의 spec.md·script.txt·scene.py를 유지한다. _template/ 구조를 사용하며 prepare.py로 대본·인덱스·자막 자료를 재생성한다.

direction.py의 연산과 애니메이션은 공유하며 layouts.py에서 화면비별 좌표·차트 간격·자막 영역을 정한다. 가로 비교는 좌우, 세로 비교는 상하 배치다. 영상을 늘리거나 잘라 다른 비율을 만들지 않는다. 자막은 GPU 개론15의 하단 전용 패널과 문장 경계 갱신 방식을 참고했다.

빌더는 씬 소스·공통 도구·레이아웃·자막 원본·렌더 설정의 해시가 일치하는 클립만 재사용한다. 씬별 프레임, 두 출력의 해상도·길이·프레임 수·전체 디코딩, 34개 자막 전환 시각과 자막 영역을 자동 검사한다. 최종 기록은 render_report_long.json 및 render_report_short.json에 저장한다.

--ending standalone|join 모두 전체 본문과 178초를 보존한다. 다음 편 제목·예고·엔드카드는 없다. 다음 편 소스나 음원은 아직 없다.

이전 episodes/qcs01_speed/의 원본은 이 위치로 이동했다. 이전 출력 exports/qcs01_shorts.mp4는 자막 없는 이전 버전이다. 이전 검증 기록은 revisions/no_captions/에 보관한다.

수학 참고: [IBM Quantum](https://quantum.cloud.ibm.com/learning/modules/computer-science/grovers), [최적성 증명](https://arxiv.org/abs/quant-ph/9711070). O = diag(1,1,1,−1), D = 2|s⟩⟨s|−I로 DO|s⟩ = |11⟩를 구현한다. 진폭 막대는 연산 직후 정규화된 스냅샷이다. py -3.12 -m longforms.qcs01_speed.verify 로 수학·자막 자료를 검사한다.
