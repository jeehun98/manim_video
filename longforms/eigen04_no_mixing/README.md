# 행렬의 성분이 서로 섞이지 않는 좌표계가 있을까?

고윳값과 고유벡터4편. 사용자 확정 대본과 문장별 종료 시각27개, 총115초, 15개 독립 씬. 실제 음원은 제공되지 않아 무음 제작한다.

- 세로 쇼츠1080×1920, 가로 롱폼1920×1080, 각30fps
- 미리보기360×640 / 854×480, 15fps
- 핵심 자막: 세로60px·두 줄·하단170px 여백 / 가로46px·한 줄. 제공 문장 경계와 정확히 일치.
- TTS 원고에는 읽지 않는 제목·시간을 넣지 않고 화면 전환에 따라 문단을 나눈다. 원문은 narration.md, 발음은 tts_script.txt 및 씬별 script.txt.

## 실행

```powershell
python longforms/eigen04_no_mixing/build.py --preview
python longforms/eigen04_no_mixing/add_captions.py --preview
python longforms/eigen04_no_mixing/build.py
python longforms/eigen04_no_mixing/add_captions.py
```

`--layout shorts` / `--layout longform` 지원. `build.py --scene 8`로 씬 단독 수정. 최종 출력은 `exports/eigen04_115s_shorts_final_captioned.mp4`, `exports/eigen04_115s_longform_final_captioned.mp4`.

## 수학과 연출

A=((2,1),(1,2)), 최종 P=((1,1),(1,−1)), D=diag(3,1).

도입 입력은 콘티에서 허용한 (1,0)을 사용해 방향이 변하는 모습을 명확히 한다. 임의 기저 S=((1,1),(0,1))에서는 Ab1=(2,1)=b1+b2이고 M=((1,0),(1,3)). 원본 콘티 앞부분의 2b1+b2는 뒤의 정정 지시에 따라 사용하지 않는다. 두 번째 축의 섞임은 별도의 임의 기저 T=((1,0),(1,1))에서 보여준다.

첫 고유축 탐색은 R=((1,0),(0.2,−1)) → H=((1,0),(1,−1)) 경로를 사용한다. H에서 표현은 ((3,−1),(0,1))이므로 M21만0이고 M12는 남는다. 두 번째 축을 H → P로 바꾸면 M12도0이 된다. 두 연속 경로 모두 행렬식이0을 지나지 않으며, 서로 다른 방향성의 초기 임의 기저와 탐색 기저는 독립 장면으로 제시한다.

기저와 표현 행렬은 매 프레임 M=B⁻¹AB로 동시 계산한다. 선택한 축 b_j에 실제 A를 곱한 출력도 함께 갱신한다. 비대각 원소는 소수 둘째 자리까지 표시하되 미세한 비영 값은 ≈0, 정확한0은 청록색0으로 구분한다. 각 기저벡터 끝점에 단위 눈금1을 둔다.

세 단계는 실제 벡터(2,1)를 고유좌표(1.5,0.5)로 읽는 P⁻¹, (4.5,0.5)로 바꾸는 D, 원래 좌표(5,4)로 복원하는 P 순서다. A=PDP⁻¹은 오른쪽부터 적용함을 세 단계 화살표와 강조로 표시한다. 첫 단계와 복원 단계에서는 실제 벡터를 움직이지 않는다.

자료: storyboard.md 원본, timing.json 문장·씬 경계, scenes.yaml/manifest.json 인덱스, scenes/01–15 독립 spec·소스·발음 원고. Python3.12·Manim0.21.0·FFmpeg·FFprobe·Malgun Gothic. LaTeX 없이 Pango 수식을 사용한다. 미세한 Manim 프레임 반올림은 씬 끝 수 프레임만 보정한다.

## 완료 검증

두 자막 포함 최종본 각각115.000초·3,450프레임·30fps와 요청 해상도를 확인했다. FFmpeg 전체 디코딩 오류 없음. 문장·핵심 자막27개 경계 일치, Ab1=b1+b2, 첫 고유축 단계에서 M21만0, 최종 두 고유축에서 두 비대각 원소0, 세 단계의 최종 출력(5,4)을 검증했다. 기저 변경202개 표본에서 가역성을 확인했다. 두 화면비 미리보기18개 시점 및 수정된 자막 포함 최종 화면을 점검했다. 상세 결과는 `verification.json`.
