# QR 기하학 4편 — QR은 왜 SVD처럼 대각화하지 않을까?

- 사용자 확정 108초·23문장·27개 독립 교체 가능 컷.
- 새 4편은 QR/SVD 비교다. 이전 최소제곱 4편 107초는 qr04_stable_least_squares에 보존한다.
- 세로 1080×1920 / 가로 1920×1080, 각 30fps. 음원 미제공으로 무음·화면 자막 및 별도 SRT.
- 동일한 A=Rot(30°)[[2,1],[0,1]]를 QR과 SVD 양쪽에 사용한다. Q=Rot(30°), R=[[2,1],[0,1]].
- 특이값 √(3+√5)≈2.288, √(3−√5)≈0.874. U,V는 같은 A에서 실제 계산한다.

## 실행

```powershell
python longforms/qr04_qr_vs_svd/build.py --preview
python longforms/qr04_qr_vs_svd/build.py
```

--layout shorts 또는 longform으로 한 버전만 렌더한다. --scene 18 등으로 수정한 컷만 렌더하고 --concat-only로 재결합한다.

최종 출력: exports/qr04_qr_vs_svd_108s_shorts_final.mp4 및 exports/qr04_qr_vs_svd_108s_longform_final.mp4.

## 제작 기준

- QR은 출력 공간의 첫 열 방향을 유지하고, 둘째 열의 투영 성분이 R의 r₁₂=1로 남는 것을 보여준다.
- SVD는 입력 vᵢ와 출력 uᵢ를 분리 표기한다. 다른 공간의 방향을 같은 좌표계에 겹쳐 비교하지 않는다.
- 단위원의 모든 표본점에 동일한 A를 적용한다. 단순 타원 모양을 임의로 그리지 않는다.
- SVD의 세 단계는 Vᵀ→Σ→U 순서. 입력·출력 양쪽 기준 사이의 작용이 UᵀAV=Σ임을 명시한다.
- 마지막 정지 화면은 107–108초에 포함하며 전체 길이를 늘리지 않는다.
- 자막은 컷 경계와 별도로 문장 종료 시각에 전환한다. 12–18초 컷에서도 14초에 새 문장으로 바뀐다.
- 복습·예고 없음. 컷별 script.txt에 겹친 문장은 timing.json을 기준으로 한 번만 발화한다. 실제 음원 싱크는 미검증.

자료: storyboard.md 원문, narration.md·master_script.md·tts_script.txt 새 확정 원고, timing.json·captions.srt 새 종료 시각, scenes.yaml·manifest.json·scenes/*/spec.md 27컷 인덱스, visuals.py 화면, build.py 렌더·프레임 검증·결합.

math_verification.json은 QR/SVD 복원, Q/U/V 직교성, Avᵢ=σᵢuᵢ와 특이값·비대각 계수·시각 연속성을 검증한다. verify_final.py는 최종 프레임·해상도·길이와 대표 화면을 검증한다.


## 최종 검증 (2026-10-26)

두 최종본 모두 108.000초·30fps·3,240프레임. 세로 1080×1920, 가로 1920×1080. 각 26개 대표 시각 검수 완료. 14초 문장 전환, 입력/출력 기저 표기, QR 비대각 성분과 Σ의 0, 타원/행렬 간격을 확인했다. 쇼츠 두 컷 간격 수정 후 재결합·재검증. QR/SVD 복원과 Q/U/V 직교성, Avᵢ=σᵢuᵢ 및 새 시각 연속성 수치 검증 통과.
