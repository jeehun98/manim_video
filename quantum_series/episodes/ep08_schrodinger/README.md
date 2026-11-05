# EP.08 슈뢰딩거의 파동역학
176초·35문장·8개 독립 씬. 음원 미제공으로 무음.
`python scripts/render.py quantum08 --preview` / `python scripts/render.py quantum08`
개별 `quantum08_shorts`, `quantum08_longform`. 편별 `build.py --scene` 및 `--ending standalone|join` 지원.

정상파는 고정단 사인 모드, 수소는 비상대론적 쿨롱 방정식이다. 수치 방사형 고유값과 대표식-13.60/n² eV를 비교한다. 제한된 수치 구간의 상자는 원자에 놓인 실제 벽이 아니다.
원자 파동 그림은1s·2s·2p_z의 공간 부분 단면이며 색은 부호, 밝기는 상대 |ψ|이다. 각 상태별로 밝기를 정규화하므로 서로 다른 상태의 절대 크기 비교용이 아니다. |ψ|²의 확률 해석을 앞당겨 설명하지 않는다.
결합 상태 E<0만 이산적이며 E≥0은 연속 영역이다. 같은 에너지의 여러 상태를 허용한다.
정상상태의 전체 위상은 시간에 따라 변한다. 이 모형의 고립된 들뜬 고유상태와 복사장 결합에 의한 자발방출은 구별한다. 바닥상태 설명은 더 낮은 원자 내부 상태로의 방출 전이 부재에 한정한다.

참고: [OpenStax · Hydrogen Atom](https://openstax.org/books/university-physics-volume-3/pages/8-1-the-hydrogen-atom), [OpenStax · Standing Waves](https://openstax.org/books/university-physics-volume-1/pages/16-6-standing-waves-and-resonance), [슈뢰딩거의 수소 해법 해설](https://arxiv.org/abs/2007.14798).

수치 검증: 원자 단위 방사형 해밀토니안을 삼중대각 행렬로 이산화했다(r_max=120a₀,8000개 내부 점). s상태 고유값은[-13.599235,-3.399952,-1.511102,-0.849997]eV이며 대표식과0.002eV 이내로 일치한다. p의 최저 에너지도-3.40eV 부근이다. 고유벡터 정규화, 정수 줄 모드의 고정단,1.5모드의 끝점 불일치,1s 중심값·2s 마디와 전체 위상의 크기 불변성을 확인했다.

파동함수 단면은 라게르 다항식의 해석적 수소 고유함수에서, 비교 에너지는 방사형 차분 고유값 계산에서 얻는다. 자료 원문은 `storyboard.md`, 확정 대본과 시각은 `script.json`에 보존한다.

최종 검수: 두 비율 미리보기·최종 주요 장면 확인. 최종본 모두176.000초·5280프레임·30fps·H.264·무음. 전체 FFmpeg 디코딩 오류 없음. 마지막1초 정지 및 원본 해상도 엔딩 PNG 확인. `qa_report.json`과 `render_report.json`에 결과 기록.
