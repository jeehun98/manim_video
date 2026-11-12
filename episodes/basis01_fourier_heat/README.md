# 사인과 코사인 · 푸리에 급수

175초·1080×1920·60fps·무음·전체 자막. 확정 대본과 문장 경계: narration.md, script.json.

최종 렌더: `py -3.12 scripts/render.py basis01`

대표 씬: `py -3.12 episodes/basis01_fourier_heat/build.py --preview --scene 05 08 09 10`

열 모델은 L=π, α=.18, 양끝 기준 온도 고정. u=T−Tref, u(0,t)=u(π,t)=0. 사인 모드 진폭의 지수 감쇠를 정확히 계산. 일반 푸리에 급수와 세 성분 예시 구별. 기저의 비유일성 표기.
