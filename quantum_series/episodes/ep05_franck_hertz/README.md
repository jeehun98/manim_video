# EP.05 프랑크–헤르츠 실험
122초 · 24문장 · 무음 · 6개 독립 씬.

실행: `python quantum_series/episodes/ep05_franck_hertz/build.py --layout both --preview`
최종: 위 명령에서 `--preview` 제외. `--ending standalone|join` 지원.

`experiment_model.py`는 고정 난수 수송 모형이며 실측 데이터를 재현한 자료가 아니다. 최소점 간격과 수집 조건을 설명한다.
에너지 보존, 내부 들뜸, 격자 이후 감속을 분리한다. 파장 253.7 nm는 자외선이다.

참고: [Utah 실험 안내](https://web.physics.utah.edu/~detar/phys6720/handouts/fh/franck_hertz.html), [IWU 실험 안내](https://sun.iwu.edu/~gspaldin/10_Franck-Hz_v3.pdf), [역사 해설](https://employees.csbsju.edu/cgearhart/pubs/FH_APS_April%202013.pdf).

모형의 제한: 1차원 가속, 고정된 들뜸 에너지, 간략화한 충돌 확률과 검출 효율을 사용한다. 온도·공간전하·실제 충돌 단면적을 맞춘 정량 실험 곡선이 아니다. 접촉 전위 1.3 V, 감속 전위 0.8 V는 설명용 설정이다.

물리 계산 검증: 문턱 아래/위 충돌의 에너지 보존, 단일 충돌 뒤 감속 구간의 반환점, 격자 이전 두 번의 충돌, 0이 아닌 전류 최소점과 약4.9 V 간격을 확인했다. 253.7 nm의 광자 에너지는 약4.887 eV이며 영상의4.9 eV는 근삿값이다.

소스: `direction.py`(연출), `layouts.py`(배치), `experiment_model.py`(설명용 계산), `../../shared/franck_hertz.py`(공통 도형), `scenes/*/spec.md`(씬별 기준). 사용자 발화 시각은 `script.json`에 보존한다.

최종 검수: 두 화면비 미리보기 및 최종 주요 프레임 확인. 최종본 모두122.000초·3660프레임·30fps·H.264·무음. 전체 FFmpeg 디코딩 오류 없음. 마지막1초 정지 및 원본 해상도 엔딩 PNG 확인.
