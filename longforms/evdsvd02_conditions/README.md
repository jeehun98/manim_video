# 행렬 분해 이상형 월드컵 ② — EVD vs SVD: 분해 조건

현재 제작본은 [132초 수정본 v2](revisions/v2_132s/README.md)이다. 아래 92초 자료는 이전 대본 기준으로 보존하며, 수정 대본의 타이밍으로 사용하지 않는다. 기본 렌더 ID `evdsvd02_shorts`, `evdsvd02_longform`은 132초 수정본을 실행한다.

- ID: `evdsvd02_conditions`
- 확정 길이: 92초, 사용자 27개 문장 종료 시각 및 첨부 콘티 기준.
- 마지막 시각 81/82는 첨부 콘티에서 명시한 91/92로 적용. `timing_source.md` 참고.
- 쇼츠: 1080×1920, 30fps. 가로형 롱폼 삽입용: 1920×1080, 30fps.
- 음원 미제공: 무음 영상과 화면 자막, 별도 SRT.

## 학습 목표

EVD의 정사각행렬·독립 고유벡터·수 체계 조건을 구분하고 SVD의 보편적 존재성을 이해한다.

## 핵심 결론

분해 가능한 실수 행렬의 범위에서는 SVD가 우위다. 이번 라운드 승자 SVD, 누적 점수 1:1.

## 작업 순서

1. `master_script.md` 확정
2. `scenes.yaml`과 씬별 `spec.md` 작성
3. 씬별 `script.txt`로 TTS 생성 및 길이 기록
4. 씬별 Manim 렌더
5. 씬별 음성 결합
6. 전체 결합과 자막 검수

## 실행

프로젝트 루트에서:

```powershell
python longforms/evdsvd02_conditions/build.py --preview
python longforms/evdsvd02_conditions/build.py
python longforms/evdsvd02_conditions/build.py --layout shorts --scene 07
python longforms/evdsvd02_conditions/build.py --concat-only
```

18개 독립 씬을 각각 렌더하고 concat한다. `--jobs`는 동시 렌더 프로세스 수이며 기본값 2.
Manim 0.21.0, FFmpeg, Malgun Gothic. 1편의 공통 레이아웃·타이포그래피를 재사용한다.
결과는 `exports/evdsvd02_conditions_92s_{shorts,longform}_final.mp4`와 같은 이름의 SRT.
30fps 최종본은 92초, 2760프레임으로 검증한다. 속도 변경 없이 각 씬의 프레임 반올림 오차만 최대 1프레임 보정.

## 수학적 정확성

- 이 영상에서 EVD는 `A=PDP⁻¹` 대각화. 영벡터는 고유벡터가 아니다.
- 전단 A=[[1,1],[0,1]]은 고윳값 1의 중복도가 2, 고유공간 차원은 1.
- 90도 회전 R=[[0,-1],[1,0]]은 실수 고유벡터 없음. 복소수에서 ±i로 대각화.
- B=[[1,0,0],[0,2,0]]은 특이값 2,1. 세 번째 입력축은 영공간이며 특이값 개수를 3개로 세지 않는다.
- AᵀA=[[1,1],[1,2]]의 실제 고유벡터를 `numpy.linalg.eigh`로 구해 렌더한다.
- 대칭·양의 준정부호 성질은 SVD 존재성을 이해하는 원리이며, 실제 알고리즘이 항상 AᵀA를 직접 형성한다는 의미가 아니다.
- 0 특이값에 해당하는 좌우 영공간 기저는 별도로 보완할 수 있다. 화면은 전체 존재 증명보다 핵심 단서에 집중한다.
