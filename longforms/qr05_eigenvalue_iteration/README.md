# QR 기하학 5편 — QR을 반복하면 왜 고윳값이 나타날까?

- 사용자 확정 124초·28문장·30개 독립 교체 가능 컷. 현재 기하학 시리즈 최종편.
- 쇼츠 1080×1920 / 가로형 1920×1080, 각 30fps. 음원 미제공으로 무음·화면 자막 및 SRT.
- 동일한 A₀=[[3,1],[1,3]]를 끝까지 사용한다. 실제 QR 분해에서 R의 대각 성분을 양수로 정한다.
- 행렬 원소와 누적 기준 회전은 iterations.json의 실제 계산에 기반한다.

## 실행

```powershell
python longforms/qr05_eigenvalue_iteration/build.py --preview
python longforms/qr05_eigenvalue_iteration/build.py
```

--layout shorts 또는 longform으로 한 버전만 렌더한다. --scene 21 등으로 수정한 컷만 렌더하고 --concat-only로 재결합한다.

출력: exports/qr05_eigenvalue_iteration_124s_shorts_final.mp4 및 exports/qr05_eigenvalue_iteration_124s_longform_final.mp4.

## 수학적·시각적 기준

- Aₖ=QₖRₖ, Aₖ₊₁=RₖQₖ=QₖᵀAₖQₖ. 각 단계는 직교 유사변환이다.
- 원래 공간에 표시하는 기준은 Qₖ 단독이 아닌 누적 Pₖ=Q₀…Qₖ₋₁이다. Aₖ=PₖᵀA₀Pₖ를 만족한다.
- 실제 반복값 사이의 애니메이션은 누적 각도를 보간하며, 중간 행렬도 해당 기준에서 PᵀA₀P로 계산한다. 임의의 네 숫자를 따로 변화시키지 않는다.
- 고유방향은 61초 이전에 표시하지 않는다. 고윳값 4와 2는 사용자 대본의 23초 설명에 맞춰 표시한다.
- 71–77초 단일 벡터는 고정된 A₀의 거듭제곱 후 정규화하는 보조 설명이며, Aₖ를 벡터에 계속 곱하는 QR 알고리즘으로 묘사하지 않는다.
- 유한 반복값은 반올림 근사다. 정확한 diag(4,2)와 45도 정렬은 k→∞로 표시한다.
- 수렴 설명은 현재 실대칭 양의 정부호 예시에 한정한다. 임의 행렬의 일반적인 대각 수렴을 주장하지 않는다.
- 물리적 변환 A₀와 고유방향은 고정하며, 달라지는 것은 이를 기술하는 직교 기준이다.
- 복습·예고·추가 엔딩 발화 없음. 122–124초의 마지막 문구도 확정 124초 안에 포함한다.

## 자료와 검증

storyboard.md 원문, narration.md·master_script.md·tts_script.txt 확정 원고, timing.json·captions.srt 사용자 종료 시각, scenes.yaml·manifest.json·scenes/*/spec.md 30컷 인덱스. 컷 경계를 가로지르는 문장은 상위 timing.json에 따라 한 번만 발화한다. 실제 음원 싱크는 미검증이다.

iterations.json에 k=0…12의 Aₖ,Qₖ,Rₖ,Pₖ,누적 각도와 비대각 성분을 저장한다. math_verification.json은 각 단계 QR 복원·양의 대각·누적 유사변환·직교성·고윳값 불변 및 시간 연속성을 검증한다. verify_final.py는 프레임 수·길이·해상도와 대표 프레임을 검증한다.

일반 실수 비대칭행렬의 실제 QR 고윳값 계산은 대각형 대신 실수 Schur 준위삼각형을 다룰 수 있다. 참고: [LAPACK 비대칭 고윳값 문제](https://www.netlib.org/lapack/lug/node50.html), [SHSEQR의 Schur 형태 설명](https://www.netlib.org/lapack/lapack_routine_v3.8.0/shseqr.f). 이 영상은 그 일반 알고리즘의 수렴을 주장하지 않고 특정 실대칭 양의 정부호 예시를 설명한다.


## 최종 검증 (2026-10-26)

두 최종본 모두 124.000초·30fps·3,720프레임. 세로 1080×1920, 가로 1920×1080. 각 29개 대표 시각의 최종 프레임 검수 완료. 실제 QR 반복값, 누적 기준 Pₖ, 고유방향의 61초 이후 등장, 유한 반복과 극한 구분 및 마지막 122–124초 문구를 확인했다. QR 복원·직교성·누적 유사변환·고윳값 보존·거듭제곱 방향 대응·시간 연속성 수치 검증 통과. 음원 미제공으로 무음·자막 영상.
