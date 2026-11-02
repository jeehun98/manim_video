# 최소 조건 2부 · 신경망 1편 — 내재 차원

사용자 제공 대본 및 29개 문장 종료 시각에 맞춘 **129초** 영상. 첨부 콘티 제목의 02편 대신 현재 사용자 요청의 1편을 적용했다. 이전 영상 복습이나 다음 영상 예고는 없다.

- 롱폼: 1920×1080, 16:9, 60fps
- 쇼츠: 1080×1920, 9:16, 60fps
- 음원 미제공: 두 결과물 모두 무음, 전체 문장 자막 포함
- 9개 교체 가능한 독립 씬. 각 씬의 script.txt·spec.md·scene.py와 공통 엔진 제공.
- 세 가중치 예시는 고정된 선형 투영 좌표계에서 (1,2,3)+t(2,−1,1)를 숫자와 점에 동기화한다.
- 750/199210 비율을 그대로 그린다. 성능 곡선은 개념도이며 원문 실험 데이터를 복원한 그래프가 아니다.
- 750은 MNIST 784→200→200→10 완전연결망에서 기준 모델 성능의 90%에 도달하는 무작위 부분공간 차원 d_int90의 측정값이다.

## 실행

프로젝트 루트에서 Python 3.12·Manim 0.21.0·FFmpeg·Malgun Gothic으로 실행한다.

```powershell
python longforms/minimal_nn01_intrinsic_dimension/build.py --preview
python longforms/minimal_nn01_intrinsic_dimension/build.py
```

`--layout longform` 또는 `--layout shorts`로 화면비 선택, `--scene 3`으로 개별 씬 렌더, `--resume`으로 완료 씬 재사용. 소스 수정 시 해당 씬을 다시 렌더한 후 `--concat-only`로 연결한다. `--resume`은 소스 변경을 자동 감지하지 않는다.

결과: `exports/minimal_nn01_intrinsic_129s_longform_final.mp4`, `exports/minimal_nn01_intrinsic_129s_shorts_final.mp4`. 별도 SRT도 복사한다. `verification_final.json`은 해상도·fps·프레임 수·재생 길이 검사 결과다. 두 결과 모두 7,740프레임이어야 한다. 프레임 단위 반올림만 최대 0.05초 정지 패딩으로 정규화하며 발화 구간은 변경하지 않는다.

QA: `python longforms/minimal_nn01_intrinsic_dimension/inspect_frames.py --final`로 실제 렌더 프레임 확인용 콘택트 시트를 만든다.

출처: [Li et al., ICLR 2018](https://arxiv.org/abs/1804.08838), [논문 PDF](https://yosinski.com/media/papers/Li__2018__Measuring_the_Intrinsic_Dimension_of_Objective_Landscapes__.pdf).
