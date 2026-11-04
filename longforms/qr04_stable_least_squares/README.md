# QR 4편 — 컴퓨터는 왜 정규방정식보다 QR 분해를 선호할까?

이 폴더는 이전 107초 최소제곱 4편의 보존 자료다. 현재 기하학 4편은 [108초 QR/SVD 비교](../qr04_qr_vs_svd/README.md)다. 기본 qr04_shorts·qr04_longform은 새 영상으로 연결되며, 이 영상은 qr04_least_squares_shorts·qr04_least_squares_longform 또는 아래 직접 실행 명령으로 재현한다.

- 사용자 확정 107초·27개 문장·28개 독립 교체 가능 컷.
- 쇼츠 1080×1920 / 가로형 1920×1080, 각 30fps.
- 음원 미제공으로 무음·화면 자막 영상 및 별도 SRT. 실제 음원 싱크는 미검증.
- Aε=[[1,1],[0,ε],[0,0]], ε>0. b=(0,1,1.2), 투영점 p=(0,1,0).
- ε가 작아져도 열공간인 xy평면은 고정한다. 작은 독립 성분과 큰 계수의 상쇄를 보여준다.
- 축약 Q는 3×2 정규직교 열 행렬이며 R=[[1,1],[0,ε]].

## 실행

```powershell
python longforms/qr04_stable_least_squares/build.py --preview
python longforms/qr04_stable_least_squares/build.py
```

--layout shorts 또는 longform으로 한 버전만 제작한다. --scene 12 등으로 컷별 재렌더 후 --concat-only로 결합한다.

출력: exports/qr04_stable_least_squares_107s_shorts_final.mp4 및 exports/qr04_stable_least_squares_107s_longform_final.mp4.

## 정확성 기준

- κ₂(AᵀA)=κ₂(A)²는 열 전체 계수 행렬에 대한 정확한 조건수 관계다. 실제 오차의 제곱이나 고정 배율을 뜻하지 않는다.
- κ₂(R)=κ₂(A)이며 QR도 원래 문제의 민감성을 제거하지 않는다.
- 안정성은 Householder QR 같은 안정적인 구현을 기준으로 설명한다. 정규방정식도 조건수가 작고 정밀도가 충분한 경우 유효하다.
- 후반 유한 정밀도 결과점 그림은 개념도다. 두 알고리즘의 측정 오차나 보편적 오차 순위를 주장하지 않는다.
- 조건수 1,000→1,000,000 화면은 관계를 설명하는 예시이며, 모든 앞 장면의 ε와 같은 수치를 뜻하지 않는다.

## 자료

storyboard.md 원문, narration.md·master_script.md·tts_script.txt 확정 원고, timing.json·captions.srt 사용자 종료 시각, scenes.yaml·manifest.json·scenes/*/spec.md 컷 인덱스. 컷 경계를 가로지르는 문장은 전체 timing.json에 따라 한 번만 발화한다.

math_verification.json은 여러 양의 ε에서 QR·수직 잔차·최소제곱 해·조건수 관계를 검증한다. verify_final.py는 프레임·해상도·길이와 대표 프레임을 검증한다.

참고: [LAPACK QR 최소제곱](https://netlib.org/lapack/lug/node40.html), [SIAM: Numerical Methods for Least Squares Problems, Chapter 2](https://epubs.siam.org/doi/abs/10.1137/1.9781611977950.ch2).

## 최종 검증 (2026-10-26)

두 최종본 모두 107.000초·30fps·3,210프레임. 세로 1080×1920, 가로 1920×1080. 각 24개 대표 시각의 최종 프레임 검수 완료. 비교 경로 박스의 흐림 처리 수정 후 재결합·재검증했다. 27문장 종료 시각 연속성, A=QR·QᵀQ=I, 수직 잔차, 투영점, 조건수 제곱 및 R의 조건수 유지 수치 검증 통과. verification.json, math_verification.json, qa/contact_*.jpg 참조. 음원 미제공으로 무음·자막 영상.
