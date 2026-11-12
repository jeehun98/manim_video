# EP.09 보른의 확률 해석
178초·40문장·9개 독립 씬. 음원 미제공으로 무음.
`python scripts/render.py quantum09 --preview` / `python scripts/render.py quantum09`
개별 `quantum09_shorts`, `quantum09_longform`. 편별 `build.py --scene` 및 `--ending standalone|join` 지원.

보른의1926산란 연구와 현대적 반복 검출 개념 실험을 구별한다. 방향별7채널은 같은 수집 효율을 가정한 설명용 이산 모형이다. 실제 산란 단면적이 아니다.
반복 검출은 정규화한 복소 가우스 상태의 |ψ|²와 독립 Gaussian 보조 좌표에서 표본을 추출한다. 모든 누적 점과 가로 주변 밀도 히스토그램은 같은 seed1926 표본을 사용한다. 실측이나 수소 분포가 아니다.
진폭은 복소수, |ψ|²는 확률밀도다. 영역의 확률은 밀도를 적분해 구한다. 화면에 한 점이 나타나는 것을 확정된 물리적 붕괴 과정으로 그리지 않는다.
간섭은 두 경로가 구별되지 않고 위상 관계가 유지될 때의 예다. 두 출력의 진폭을(1±exp(iφ))/2로 두어 전체 확률을1로 유지한다. 한 출력이0이 되어도 다른 출력은1이다. 경로 정보가 기록된 경우의 간섭 소실은 적용 조건에 명시한다.
동전의 예는 고전적 결정론적 이상화이며 모든 숨은변수 이론의 부정을 주장하지 않는다.

참고: [Born Nobel Lecture](https://www.nobelprize.org/uploads/2018/06/born-lecture.pdf), [Born1926 원논문](https://doi.org/10.1007/BF01397477), [OpenStax Wave Functions](https://openstax.org/books/university-physics-volume-3/pages/7-1-wave-functions).

계산 검증: ∫|ψ|²dx=1, |ψ|²=ρ,7채널 확률 합1, 각 N의 히스토그램 총도수=N 및 면적1, 모든 위상에서 두 출력 확률 합1을 확인했다. 3000표본의 x 평균은-0.001996, 표준편차0.890268(이론0.9), Gaussian CDF에 대한 최대 차이는0.012152이다. 3000점 모두 표시 창 안에 있으며 영역 밖의 점을 제거하지 않았다.

최종 검수: 두 비율 미리보기·최종 주요 장면 확인. 최종본 모두178.000초·5340프레임·30fps·H.264·무음. 전체 FFmpeg 디코딩 오류 없음. 마지막1초 정지 및 원본 해상도 엔딩 PNG 확인. `qa_report.json`과 `render_report.json`에 결과 기록.
