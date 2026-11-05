# EP.10 데이비슨–거머 실험

171초 · 30fps · 쇼츠 1080×1920 / 롱폼 1920×1080. 음원 미제공으로 무음이며 자막을 포함한다.

실행: `python quantum_series/episodes/ep10_davisson_germer/build.py` (미리보기 `--preview`). `--layout`, `--scene`, `--ending standalone|join` 지원. 두 종료 모드의 확정 내레이션 길이는 동일하다.

`script.json`은 확정 대본과 문장 시각, `scenes/*/spec.md`는 독립 씬의 주장, `direction.py`는 공통 애니메이션, `layouts.py`는 화면비별 배치, `shared/diffraction.py`는 간섭 계산을 관리한다. 장치는 2D 개념도로서 원형 도식을 그대로 실물 크기로 해석하지 않는다.

## 해석과 출처

- [Davisson–Germer 원논문, Physical Review 30, 705 (1927)](https://elton.freeshell.org/Mse311/Literature/PhysRev30-Davisson-Germer1927_electron-diff-Ni.pdf): 1925 사고, 재결정화, 방향별 산란 및 파동 해석.
- 정량 화면의 D≈0.215 nm는 표면 원자열 간격의 입문용 근사이며 벌크 결정면 간격 d와 구분한다. 검출각 φ는 표면 바깥 법선에서 측정한다. λ≈D sinφ는 정상 입사의 표면 격자 모형으로, 내부 전위·다중 산란을 포함한 정밀 분석은 아니다.
- 54 V에서 비상대론적 드브로이 파장은 약 0.1669 nm. 서술에 맞춰 0.167 nm와 회절 추정 약 0.165 nm를 비교한다. 표시된 50°와 간격은 반올림값으로, 곱을 계산하면 약 0.1647 nm다.
- 각도 그래프는 정성적 재구성이다. 간섭 화면의 보강·상쇄 진폭은 exp(2πinD sinφ/λ)의 8개 항을 합산한다. 전자를 여러 조각으로 복제해 산란시키는 뜻이 아니다.
- 마지막 파동묶음은 위치와 운동량에 관한 질문을 위한 개념도이며 불확정성 원리의 정량 실험은 아니다.
- [G. P. Thomson, Diffraction of Cathode Rays by a Thin Film (1927)](https://www.nature.com/articles/119890a0): 독립적인 박막 투과 전자 회절 연구.
