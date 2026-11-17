# 교환법칙이 당연하다고 생각하시나요?

167초 · 9:16 쇼츠 · 1080×1920 · 60fps · 전체 내레이션 자막 · 무음

사용자 제공 대본과 문장 종료 시각을 확정 입력으로 사용한다. 가로 콘티는 쇼츠 요청에 맞춰 세로 재배치한다. 음원 미제공. 이전 편 복습·다음 편 예고·별도 엔드카드 없이 독립적으로 완결한다.

실제 3차원 책 정점에 오른손 능동 회전 행렬을 적용하고 고정된 사선 카메라로 직교 투영한다. 원본 정점은 불변이며 매 프레임 orientation @ vertices로 계산한다. 금색 앞표지/FRONT·TOP 표식, 적갈색 책등, 아이보리 페이지, 표지 법선 화살표로 방향을 구분한다. 월드 X(코랄), Y(파랑), Z(초록)축은 책과 함께 회전시키지 않는다.

A=Rx(+90°), B=Ry(+90°). X→Y의 자세는 BA, 앞표지 법선은 −Y. Y→X는 AB, 앞표지 법선은 +X. 열벡터에 오른쪽 행렬부터 작용한다. 비교 실험은 동일 초기 자세에서 시작하고 회전 명령을 순차 실행한다. 2차원 원점 회전은 기저·행렬 도입용이며 가환임을 작은 문구로 명시한다. 비가환성은 다시 3차원에서 보인다. 행렬의 표현 대상은 여기서 선형인 원점 회전이다.

참고: Modern Robotics §3.2.1, https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-2-1-rotation-matrices-part-2-of-2/ ; MIT 16.1 Matrices and Linear Transformations, https://math.mit.edu/~djk/18_022/chapter16/section01.html .

렌더: `python scripts/render.py commute01`. 대표 검수: `python episodes/commute01_rotation/build.py --preview --scene 02`.
