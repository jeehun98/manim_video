# 행렬분해 이상형 월드컵 01 — EVD vs SVD: 이름

- ID: `evdsvd01_names`
- 확정 길이: 52초. 사용자 제공 16개 문장 종료 시각 기준.
- 쇼츠: 1080×1920, 30fps. 가로형 롱폼 삽입용: 1920×1080, 30fps.
- 음원 미제공: 무음 영상, 화면 자막 및 별도 SRT. 대본은 사용자 최종 원문 그대로 유지.

## 학습 목표

Eigen과 Singular의 일상 의미를 비교하고, 이름에서 수학적 성질을 얼마나 쉽게 연상할 수 있는지 살펴본다.

## 핵심 결론

이번 이름의 직관성 대결에서는 EVD가 승리한다. 행렬분해 자체의 수학적 우열을 뜻하지 않는다.

## 작업 순서

1. `master_script.md` 확정
2. `scenes.yaml`과 씬별 `spec.md` 작성
3. 씬별 `script.txt`로 TTS 생성 및 길이 기록
4. 씬별 Manim 렌더
5. 씬별 음성 결합
6. 전체 결합과 자막 검수

## 실행

프로젝트 루트에서 실행:

```powershell
python longforms/evdsvd01_names/build.py --preview
python longforms/evdsvd01_names/build.py
python longforms/evdsvd01_names/build.py --layout longform --scene 04
```

`manifest.json`에 등록된 11개 독립 씬을 각각 렌더하고 concat한다. 각 씬은 단독 교체 가능하다.
Manim 0.21.0, FFmpeg, Malgun Gothic 필요. 최종 파일은 `exports/evdsvd01_names_52s_{shorts,longform}_final.mp4`.
모든 구간은 원래 속도로 제작하며 프레임 반올림 오차만 최대 1프레임 보정한다. 결과는 52초, 1560프레임으로 검증한다.

수학 설정: EVD 사례 A=[[2,1],[1,2]], v=(1,1), Av=3v. 양의 고윳값으로 동일 직선 유지 시각화.
SVD 사례 A=diag(2,0.7). 입력 단위원의 상은 반축 2와 0.7인 타원.
회상·다음 편 예고와 추가 연결 내레이션 없음. 오프닝과 점수 화면도 52초 안에 포함한다.
