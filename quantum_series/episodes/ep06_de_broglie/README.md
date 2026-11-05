# EP.06 드브로이의 물질파
161초·31문장·7개 독립 씬. 음원 미제공으로 무음.

`python scripts/render.py quantum06 --preview` / `python scripts/render.py quantum06`
개별 비율 `quantum06_shorts`, `quantum06_longform`. `build.py --scene` 및 `--ending standalone|join` 지원.

원형 보어 모형에 물질파를 적용한 역사적 해석이다. 파동 그림의 진폭은 전자 궤적의 진폭이 아니다. 정수 위상 조건은 고전적 복사 문제를 독립적으로 해결하지 않는다.
반지름·진폭이 같은3.5와3의 비교에서 복소 위상을 계산한다. 주기 조건은 rp라는 곱을 제한하며 별도의 힘 법칙 없이는 r,p를 각각 확정하지 않는다.

참고: [OpenStax · De Broglie’s Matter Waves](https://openstax.org/books/university-physics-volume-3/pages/6-5-de-broglies-matter-waves).

검증: 운동량2배→파장1/2, 정수 모드의 복소 위상 일치,3.5 모드의 불일치, 시작 위상에 따라 실수부 높이가 같아도 복소 위상이 다를 수 있는 반례, 원형 연결점과 L=nℏ를 계산으로 확인했다. 전개도의 수평 길이는 화면에 맞춰 축척을 조정하되 동일한 호길이 비율과 위상 함수를 사용한다.

사용자 제공 콘티 원문은 `storyboard.md`, 확정 대본·시각은 `script.json`, 구현은 `direction.py`·`layouts.py`, 공통 도형은 `shared/matter_waves.py`에 보존한다. 원문에 언급된 EP.04 소스와 음원은 현재 없으며 이 편이 생성했다고 표시하지 않는다.

최종 검수: 두 비율 미리보기·최종 주요 장면 확인. 최종본 모두161.000초·4830프레임·30fps·H.264·무음. 전체 FFmpeg 디코딩 오류 없음. 마지막1초 정지 및 원본 해상도 엔딩 PNG 확인. `qa_report.json`과 `render_report.json`에 결과 기록.
