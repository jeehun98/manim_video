# QR 분해의 기하학 — 마무리 영상

- 사용자 확정 89초·17문장·25개 독립 교체 가능 컷.
- 요청한 가로 롱폼만 제작: 1920×1080, 30fps. 세로 영상은 생성하지 않는다.
- 첨부 콘티의 9:16 배치는 가로형으로 재설계했다.
- 음원 미제공으로 무음·화면 자막 및 별도 SRT. 실제 음원 싱크는 미검증.
- 사용자가 명시적으로 요청한 시리즈 회고 영상이다. 기존의 편별 독립 완결 원칙과 구분해 이번 마무리 영상에만 회고를 포함한다.

## 실행

```powershell
python longforms/qr_series_closing/build.py --preview
python longforms/qr_series_closing/build.py
```

기본값과 허용 레이아웃은 longform만이다. --scene 23 등으로 컷별 수정 후 --concat-only로 다시 결합한다.

출력: exports/qr_series_closing_89s_longform_final.mp4.

## 제작·수학 기준

- 공간과 부피 예시는 사용자 제공 A₃=[[2,1,1],[0,2,1],[0,0,2]]. 양의 대각 QR은 Q₃=I, R₃=A₃. 수직 높이는 2·2·2이며 부피 배율은 8이다.
- SVD에서는 xy평면에 제한한 같은 변환 C=[[2,1],[0,2]]를 사용한다고 화면에 표시한다. 입력 V와 출력 U를 구분한다. 이 C의 두 특이값은 모두 1보다 크므로 실제 축소를 꾸며내지 않고 최대·최소 확대를 보여준다.
- QR 반복은 별도로 명시한 A₀=[[3,1],[1,3]]의 실대칭 양의 정부호 예시다. 원래 삼각행렬 A₃가 같은 방식으로 대각화된다고 암시하지 않는다.
- 누적 Pₖ와 Aₖ=PₖᵀA₀Pₖ를 실제 계산한다. 정확한 diag(4,2)에는 k→∞ 극한을 표시한다.
- 마지막 네 패널은 QR 기저, 입력 특이기저 V, 출력 특이기저 U, 대칭행렬 고유기저를 각각 표시한다. 서로 같은 벡터라는 뜻이 아닌 공통 성질인 직교성을 묶는다.
- 새 내레이션·예고·음성 엔딩은 추가하지 않는다. 마지막 문구도 89초 안에 포함한다.

## 자료

storyboard.md 사용자 원문, narration.md·master_script.md·tts_script.txt 확정 원고, timing.json·captions.srt 사용자 종료 시각, scenes.yaml·manifest.json·scenes/*/spec.md 25컷 인덱스. 컷 경계를 가로지르는 문장은 timing.json에 따라 한 번만 발화한다.

visuals.py는 독립적인 이 프로젝트 소스다. iterations.json은 누적 QR 기준과 행렬, math_verification.json은 부피·평면 제한·SVD·누적 유사변환·고윳값 보존·시각 연속성의 수치 검증 자료다. verify_final.py는 최종 프레임·길이·해상도와 대표 프레임을 검증한다.


## 최종 검증 (2026-10-26)

가로형 최종본 1920×1080·89.000초·30fps·2,670프레임 검증 완료. 25개 대표 시각의 최종 프레임을 검수했다. 부피8, 평면 제한 C와 입력/출력 특이방향, 별도 대칭행렬 QR 반복 및 극한, 서로 다른 네 직교 기준의 구분과 마지막 문구를 확인했다. 세로형 출력은 생성하지 않았다. verification.json·math_verification.json·qa/contact_longform.jpg 참조.
